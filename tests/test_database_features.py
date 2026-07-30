import tempfile
import unittest
from pathlib import Path

from database import Database
from grammar_engine import analyze_sentence


class DatabaseFeatureTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp_dir.name) / "test.db")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_search_delete_and_export(self):
        first_id = self.database.save_analysis(
            "O aluno estudou.",
            analyze_sentence("O aluno estudou."),
        )
        self.database.save_analysis(
            "A professora explicou a matéria.",
            analyze_sentence("A professora explicou a matéria."),
        )
        self.assertEqual(len(self.database.search_analyses("professora")), 1)
        self.assertTrue(self.database.delete_analysis(first_id))
        exported = self.database.export_data()
        self.assertEqual(len(exported["analyses"]), 1)
        self.assertIn("lesson_progress", exported)
        self.assertIn("attempts", exported)

    def test_lesson_can_be_reopened(self):
        self.database.save_progress("fundamentos", True, 100)
        self.database.save_progress("fundamentos", False, 0)
        progress = self.database.progress()["fundamentos"]
        self.assertFalse(progress["completed"])
        self.assertEqual(progress["score"], 100)

    def test_review_uses_latest_attempt(self):
        self.database.save_attempt(7, "Pergunta", "errada", "certa", False)
        self.assertEqual(self.database.incorrect_exercise_ids(), {7})
        self.database.save_attempt(7, "Pergunta", "certa", "certa", True)
        self.assertEqual(self.database.incorrect_exercise_ids(), set())


if __name__ == "__main__":
    unittest.main()
