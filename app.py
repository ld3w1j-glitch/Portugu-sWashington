from __future__ import annotations

import json
import os
import random
from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from course_data import EXERCISES, LESSONS, LESSONS_BY_ID, module_groups
from database import Database
from grammar_engine import CLASS_DESCRIPTIONS, analyze_sentence


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "gramatica-offline-local"),
    JSON_AS_ASCII=False,
    MAX_CONTENT_LENGTH=1 * 1024 * 1024,
)
db = Database(Path(os.environ.get("DATABASE_PATH", BASE_DIR / "data" / "gramatica.db")))


@app.context_processor
def inject_global_data():
    progress = db.progress()
    return {
        "total_lessons": len(LESSONS),
        "completed_lessons": sum(1 for item in progress.values() if item["completed"]),
        "class_descriptions": CLASS_DESCRIPTIONS,
    }


@app.get("/")
def index():
    stats = db.stats()
    recent = db.recent_analyses(3)
    progress = db.progress()
    percentage = round(stats["completed_lessons"] / len(LESSONS) * 100)
    return render_template(
        "index.html",
        title="Início",
        stats=stats,
        recent=recent,
        progress_percentage=percentage,
        first_pending=next(
            (lesson for lesson in LESSONS if not progress.get(lesson["id"], {}).get("completed")),
            LESSONS[-1],
        ),
    )


@app.route("/analisador", methods=["GET", "POST"])
def analyzer():
    result = None
    error = None
    sentence = ""
    if request.method == "POST":
        sentence = request.form.get("sentence", "").strip()
        try:
            result = analyze_sentence(sentence)
            analysis_id = db.save_analysis(sentence, result)
            result["analysis_id"] = analysis_id
        except ValueError as exc:
            error = str(exc)
    return render_template(
        "analyzer.html",
        title="Analisador",
        result=result,
        sentence=sentence,
        error=error,
    )


@app.get("/analise/<int:analysis_id>")
def saved_analysis(analysis_id: int):
    item = db.get_analysis(analysis_id)
    if not item:
        abort(404)
    result = item["result"]
    result["analysis_id"] = item["id"]
    return render_template(
        "analyzer.html",
        title="Análise salva",
        result=result,
        sentence=item["sentence"],
        error=None,
        saved_at=item["created_at"],
    )


@app.get("/curso")
def course():
    progress = db.progress()
    return render_template(
        "course.html",
        title="Curso",
        modules=module_groups(),
        progress=progress,
    )


@app.get("/curso/<lesson_id>")
def lesson(lesson_id: str):
    lesson_data = LESSONS_BY_ID.get(lesson_id)
    if not lesson_data:
        abort(404)
    index = next(i for i, item in enumerate(LESSONS) if item["id"] == lesson_id)
    return render_template(
        "lesson.html",
        title=lesson_data["title"],
        lesson=lesson_data,
        lesson_number=index + 1,
        progress=db.progress().get(lesson_id, {}),
        previous_lesson=LESSONS[index - 1] if index > 0 else None,
        next_lesson=LESSONS[index + 1] if index + 1 < len(LESSONS) else None,
    )


@app.get("/exercicios")
def exercises():
    level = request.args.get("nivel", "todos")
    exercise_type = request.args.get("tipo", "todos")
    review_errors = request.args.get("revisar") == "erros"
    quantity = max(5, min(20, request.args.get("quantidade", 10, type=int)))
    incorrect_ids = db.incorrect_exercise_ids()
    available = [
        exercise
        for exercise in EXERCISES
        if (level == "todos" or exercise["level"] == level)
        and (exercise_type == "todos" or exercise["type"] == exercise_type)
        and (not review_errors or exercise["id"] in incorrect_ids)
    ]
    chosen = random.sample(available, min(quantity, len(available)))
    return render_template(
        "exercises.html",
        title="Exercícios",
        exercises=chosen,
        level=level,
        exercise_type=exercise_type,
        review_errors=review_errors,
        review_count=len(incorrect_ids),
        quantity=quantity,
    )


@app.get("/historico")
def history():
    query = request.args.get("q", "").strip()
    return render_template(
        "history.html",
        title="Histórico",
        analyses=db.search_analyses(query, 100),
        stats=db.stats(),
        query=query,
    )


@app.post("/historico/<int:analysis_id>/excluir")
def delete_history_item(analysis_id: int):
    db.delete_analysis(analysis_id)
    return redirect(url_for("history"))


@app.post("/historico/limpar")
def clear_history():
    db.clear_analyses()
    return redirect(url_for("history"))


@app.get("/exportar-dados")
def export_data():
    content = json.dumps(db.export_data(), ensure_ascii=False, indent=2)
    filename = f"gramatica-backup-{datetime.now().strftime('%Y-%m-%d')}.json"
    return app.response_class(
        content,
        mimetype="application/json; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/progresso")
def api_progress():
    payload = request.get_json(silent=True) or {}
    lesson_id = payload.get("lesson_id", "")
    if lesson_id not in LESSONS_BY_ID:
        return jsonify({"ok": False, "error": "Aula inválida."}), 400
    completed = payload.get("completed", False)
    score = payload.get("score", 0)
    if not isinstance(completed, bool):
        return jsonify({"ok": False, "error": "O estado da aula deve ser verdadeiro ou falso."}), 400
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 100:
        return jsonify({"ok": False, "error": "A pontuação deve estar entre 0 e 100."}), 400
    db.save_progress(lesson_id, completed, score)
    return jsonify({"ok": True, "completed": completed, "score": score})


@app.post("/api/tentativa")
def api_attempt():
    payload = request.get_json(silent=True) or {}
    exercise = next(
        (item for item in EXERCISES if item["id"] == payload.get("exercise_id")),
        None,
    )
    if not exercise:
        return jsonify({"ok": False, "error": "Exercício inválido."}), 400
    answer = str(payload.get("answer", "")).strip()
    is_correct = answer.casefold() == exercise["answer"].casefold()
    db.save_attempt(
        exercise["id"],
        exercise["prompt"],
        answer,
        exercise["answer"],
        is_correct,
    )
    return jsonify(
        {
            "ok": True,
            "correct": is_correct,
            "answer": exercise["answer"],
            "explanation": exercise["explanation"],
        }
    )


@app.get("/saude")
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html", title="Página não encontrada"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
