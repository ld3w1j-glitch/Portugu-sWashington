import unittest

from grammar_engine import analyze_sentence


class AdvancedGrammarEngineTests(unittest.TestCase):
    def analyze(self, sentence):
        return analyze_sentence(sentence)["sintaxe"]

    def term_types(self, sentence):
        return {
            item["tipo"]
            for item in self.analyze(sentence)["termos"]
        }

    def test_compound_postposed_subject(self):
        syntax = self.analyze("Chegaram João e Maria.")
        self.assertEqual(syntax["sujeito"], "João e Maria")
        self.assertEqual(syntax["tipo_sujeito"], "composto posposto")

    def test_crasis_and_regency(self):
        self.assertIn(
            "objeto indireto",
            self.term_types("Obedeci às regras."),
        )

    def test_enclisis_and_two_objects(self):
        terms = self.term_types("Entreguei-lhe o documento.")
        self.assertIn("objeto indireto pronominal", terms)
        self.assertIn("objeto direto", terms)

    def test_analytic_passive_with_auxiliary_chain(self):
        syntax = self.analyze("Ela havia sido avisada.")
        self.assertEqual(syntax["voz_verbal"], "voz passiva analítica")
        self.assertEqual(syntax["locucao_verbal"], "havia sido avisada")
        self.assertEqual(syntax["sujeito"], "Ela")

    def test_reduced_infinitive_clauses(self):
        temporal = self.analyze("Ao terminar a prova, saiu.")
        causal = self.analyze("Por estudar muito, passou.")
        self.assertIn("temporal reduzida de infinitivo", temporal["oracoes_detalhadas"][0]["tipo"])
        self.assertIn("causal reduzida de infinitivo", causal["oracoes_detalhadas"][0]["tipo"])

    def test_free_relative_as_subject_clause(self):
        syntax = self.analyze("Quem estuda aprende.")
        self.assertIn("oracional", syntax["tipo_sujeito"])
        self.assertIn("Quem estuda", syntax["sujeito"])

    def test_predicative_clause(self):
        syntax = self.analyze("A verdade é que ele mentiu.")
        self.assertEqual(syntax["tipo_predicado"], "nominal")
        self.assertIn(
            "oração com função de predicativo do sujeito",
            {item["tipo"] for item in syntax["termos"]},
        )

    def test_subjective_clause(self):
        syntax = self.analyze("Convém que você estude.")
        self.assertIn("oracional", syntax["tipo_sujeito"])
        self.assertIn(
            "subordinada substantiva subjetiva",
            syntax["oracoes_detalhadas"][1]["tipo"],
        )

    def test_completive_nominal_clause(self):
        syntax = self.analyze("Tenho certeza de que ele virá.")
        self.assertIn(
            "oração com função de complemento nominal",
            {item["tipo"] for item in syntax["termos"]},
        )

    def test_action_verb_with_subject_predicative(self):
        syntax = self.analyze("As crianças brincavam felizes.")
        self.assertTrue(syntax["tipo_predicado"].startswith("verbo-nominal"))
        self.assertIn("predicativo do sujeito", self.term_types("As crianças brincavam felizes."))

    def test_modal_locution(self):
        syntax = self.analyze("Ele precisa estudar.")
        self.assertEqual(syntax["locucao_verbal"], "precisa estudar")
        self.assertEqual(syntax["oracoes"], 1)

    def test_punctuation_does_not_inflate_confidence(self):
        without_punctuation = analyze_sentence("Eu estudo")
        with_punctuation = analyze_sentence("Eu estudo.")
        self.assertEqual(
            without_punctuation["qualidade"]["confianca_media"],
            with_punctuation["qualidade"]["confianca_media"],
        )


if __name__ == "__main__":
    unittest.main()
