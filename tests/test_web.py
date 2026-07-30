import unittest

from app import app


class WebAppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_public_pages(self):
        for path in ("/", "/analisador", "/curso", "/curso/substantivo", "/exercicios", "/historico"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_analysis_post(self):
        response = self.client.post(
            "/analisador",
            data={"sentence": "O menino comprou um livro ontem."},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Resultado da análise".encode(), response.data)
        self.assertIn("objeto direto".encode(), response.data)

    def test_advanced_analysis_is_visible(self):
        response = self.client.post(
            "/analisador",
            data={"sentence": "Ela havia sido avisada."},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Voz verbal".encode(), response.data)
        self.assertIn("voz passiva analítica".encode(), response.data)
        self.assertIn("Análise de cada oração".encode(), response.data)

    def test_progress_api(self):
        response = self.client.post(
            "/api/progresso",
            json={"lesson_id": "fundamentos", "completed": True, "score": 100},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["ok"])

    def test_progress_api_rejects_invalid_types(self):
        invalid_score = self.client.post(
            "/api/progresso",
            json={"lesson_id": "fundamentos", "completed": False, "score": "abc"},
        )
        invalid_boolean = self.client.post(
            "/api/progresso",
            json={"lesson_id": "fundamentos", "completed": "false", "score": 0},
        )
        self.assertEqual(invalid_score.status_code, 400)
        self.assertEqual(invalid_boolean.status_code, 400)

    def test_exercise_filters_and_export(self):
        filtered = self.client.get("/exercicios?tipo=oração&nivel=avancado")
        exported = self.client.get("/exportar-dados")
        self.assertEqual(filtered.status_code, 200)
        self.assertIn("Assunto".encode(), filtered.data)
        self.assertEqual(exported.status_code, 200)
        self.assertIn("attachment", exported.headers["Content-Disposition"])

    def test_health(self):
        response = self.client.get("/saude")
        self.assertEqual(response.get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
