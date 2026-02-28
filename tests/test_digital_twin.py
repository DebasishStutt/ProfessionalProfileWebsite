import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = (ROOT / "index.html").read_text(encoding="utf-8")
EMAIL_HTML = (ROOT / "email.html").read_text(encoding="utf-8")
TWIN_JS = (ROOT / "twin.js").read_text(encoding="utf-8")
STYLES = (ROOT / "styles.css").read_text(encoding="utf-8")


class TestDigitalTwin(unittest.TestCase):
    def test_widget_present(self):
        self.assertIn("data-twin-widget", INDEX_HTML)
        self.assertIn("data-twin-widget", EMAIL_HTML)
        self.assertIn("data-twin-messages", INDEX_HTML)

    def test_widget_styles_present(self):
        self.assertIn(".twin-widget", STYLES)
        self.assertIn(".twin-panel", STYLES)

    def test_frontend_uses_local_api(self):
        self.assertIn("/api/chat", TWIN_JS)

    def test_no_api_key_exposed(self):
        for content in (INDEX_HTML, EMAIL_HTML, TWIN_JS, STYLES):
            self.assertNotIn("OPENROUTER_API_KEY", content)
            self.assertNotIn("sk-or-", content)
            self.assertNotIn("openrouter.ai", content)


if __name__ == "__main__":
    unittest.main()
