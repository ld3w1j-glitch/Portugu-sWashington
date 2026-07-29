import tempfile
import unittest
from pathlib import Path

from database import Database
from grammar_engine import analyze_sentence


class GrammarEngineTests(unittest.TestCase):
    def test_basic_sentence(self):
        result = analyze_sentence("O menino comprou um livro ontem.")
        classes = {item["token"]: item["classe"] for item in result["palavras"]}
        self.assertEqual(classes["O"], "artigo")
        self.assertEqual(classes["menino"], "substantivo")
        self.assertEqual(classes["comprou"], "verbo")
        self.assertEqual(classes["ontem"], "advérbio")
        self.assertEqual(result["sintaxe"]["sujeito"], "O menino")
        self.assertEqual(result["sintaxe"]["tipo_predicado"], "verbal")

    def test_accent_distinguishes_verb(self):
        result = analyze_sentence("A aluna está atenta.")
        words = {item["token"]: item for item in result["palavras"]}
        self.assertEqual(words["está"]["classe"], "verbo")
        self.assertEqual(result["sintaxe"]["tipo_predicado"], "nominal")

    def test_nominal_sentence(self):
        result = analyze_sentence("Que dia bonito!")
        self.assertEqual(result["sintaxe"]["oracoes"], 0)

    def test_postposed_subject(self):
        result = analyze_sentence("Chegaram os alunos.")
        self.assertEqual(result["sintaxe"]["sujeito"], "os alunos")
        self.assertEqual(result["sintaxe"]["tipo_sujeito"], "simples posposto")

    def test_verbal_nominal_predicate(self):
        result = analyze_sentence("O aluno chegou atento.")
        self.assertEqual(result["sintaxe"]["tipo_predicado"], "verbo-nominal (hipótese)")

    def test_ambiguous_canto_context(self):
        noun_result = analyze_sentence("O canto ecoou.")
        verb_result = analyze_sentence("Eu canto.")
        noun = next(item for item in noun_result["palavras"] if item["token"] == "canto")
        verb = next(item for item in verb_result["palavras"] if item["token"] == "canto")
        self.assertEqual(noun["classe"], "substantivo")
        self.assertEqual(verb["classe"], "verbo")

    def test_database_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database = Database(Path(temp_dir) / "test.db")
            result = analyze_sentence("O aluno estudou.")
            analysis_id = database.save_analysis(result["frase"], result)
            saved = database.get_analysis(analysis_id)
            self.assertEqual(saved["sentence"], result["frase"])
            self.assertEqual(database.stats()["analyses"], 1)


if __name__ == "__main__":
    unittest.main()
