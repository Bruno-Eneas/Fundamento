import os, tempfile, unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from src.core import CASES, explain


class AppTests(unittest.TestCase):
    def test_cases_themes_navigation_and_feedback(self):
        with tempfile.TemporaryDirectory() as t:
            old_db = os.environ.pop("DATABASE_URL", None)
            os.environ["FUNDAMENTO_DB"] = t + "/ui.sqlite"
            try:
                a = AppTest.from_file(
                    str(Path(__file__).parents[1] / "app.py"), default_timeout=50
                ).run()
                self.assertEqual(len(a.exception), 0)
                self.assertEqual(a.session_state["result"]["case"], "Caso B — fictício")
                score = a.session_state["result"]["score"]
                a.button(key="theme_dark").click().run()
                self.assertEqual(len(a.exception), 0)
                self.assertEqual(a.session_state["result"]["score"], score)
                a.button(key="nav_Evidências").click().run()
                self.assertEqual(len(a.exception), 0)
                a.button(key="nav_Método").click().run()
                self.assertEqual(len(a.exception), 0)
                a.button(key="nav_Análise").click().run()
                self.assertEqual(a.session_state["result"]["score"], score)
                next(b for b in a.button if b.label == "Salvar avaliação").click().run()
                self.assertFalse(any("registrada" in x.value for x in a.success))
                a.radio[0].set_value("Concordo")
                a.text_area[0].set_value("Comentário sobre B")
                next(b for b in a.button if b.label == "Salvar avaliação").click().run()
                self.assertTrue(any("registrada" in x.value for x in a.success))
                a.selectbox[0].select("Caso A — fictício").run()
                self.assertAlmostEqual(
                    a.session_state["result"]["score"],
                    explain(CASES["Caso A — fictício"])["score"],
                )
                self.assertIsNone(a.radio[0].value)
                self.assertEqual(a.text_area[0].value, "")
                self.assertNotIn("generated", a.session_state)
                a.button(key="theme_light").click().run()
                self.assertEqual(len(a.exception), 0)
            finally:
                os.environ.pop("FUNDAMENTO_DB", None)
                if old_db:
                    os.environ["DATABASE_URL"] = old_db


if __name__ == "__main__":
    unittest.main()
