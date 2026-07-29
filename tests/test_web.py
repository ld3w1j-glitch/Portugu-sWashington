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

    def test_progress_api(self):
        response = self.client.post(
            "/api/progresso",
            json={"lesson_id": "fundamentos", "completed": True, "score": 100},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["ok"])

    def test_health(self):
        response = self.client.get("/saude")
        self.assertEqual(response.get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
