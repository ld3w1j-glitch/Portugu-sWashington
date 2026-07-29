"""Persistência SQLite simples para estudo individual e offline."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


BRAZIL_TIME = timezone(timedelta(hours=-3), name="UTC-03")


def now_text() -> str:
    # Não depende do pacote tzdata/ZoneInfo, evitando falhas em instalações Windows.
    return datetime.now(BRAZIL_TIME).strftime("%d/%m/%Y %H:%M")


class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentence TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS lesson_progress (
                    lesson_id TEXT PRIMARY KEY,
                    completed INTEGER NOT NULL DEFAULT 0,
                    score INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise_id INTEGER,
                    question TEXT NOT NULL,
                    user_answer TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    is_correct INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def save_analysis(self, sentence: str, result: dict) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO analyses(sentence, result_json, created_at) VALUES (?, ?, ?)",
                (sentence, json.dumps(result, ensure_ascii=False), now_text()),
            )
            return int(cursor.lastrowid)

    def recent_analyses(self, limit: int = 20) -> list[dict]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT id, sentence, result_json, created_at FROM analyses ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            {
                "id": row["id"],
                "sentence": row["sentence"],
                "result": json.loads(row["result_json"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def get_analysis(self, analysis_id: int) -> dict | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT id, sentence, result_json, created_at FROM analyses WHERE id = ?",
                (analysis_id,),
            ).fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "sentence": row["sentence"],
            "result": json.loads(row["result_json"]),
            "created_at": row["created_at"],
        }

    def save_progress(self, lesson_id: str, completed: bool, score: int):
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO lesson_progress(lesson_id, completed, score, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    completed = MAX(lesson_progress.completed, excluded.completed),
                    score = MAX(lesson_progress.score, excluded.score),
                    updated_at = excluded.updated_at
                """,
                (lesson_id, int(completed), max(0, min(100, score)), now_text()),
            )

    def progress(self) -> dict[str, dict]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT lesson_id, completed, score, updated_at FROM lesson_progress"
            ).fetchall()
        return {
            row["lesson_id"]: {
                "completed": bool(row["completed"]),
                "score": row["score"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        }

    def save_attempt(
        self,
        exercise_id: int | None,
        question: str,
        user_answer: str,
        correct_answer: str,
        is_correct: bool,
    ):
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO attempts(
                    exercise_id, question, user_answer, correct_answer, is_correct, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    exercise_id,
                    question,
                    user_answer,
                    correct_answer,
                    int(is_correct),
                    now_text(),
                ),
            )

    def stats(self) -> dict:
        with self.connect() as connection:
            analyses = connection.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
            attempts = connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]
            correct = connection.execute(
                "SELECT COUNT(*) FROM attempts WHERE is_correct = 1"
            ).fetchone()[0]
            completed = connection.execute(
                "SELECT COUNT(*) FROM lesson_progress WHERE completed = 1"
            ).fetchone()[0]
        return {
            "analyses": analyses,
            "attempts": attempts,
            "correct": correct,
            "accuracy": round(correct / attempts * 100) if attempts else 0,
            "completed_lessons": completed,
        }
