import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
EMAIL_HTML = (ROOT / "email.html").read_text(encoding="utf-8")


class TestSiteContent(unittest.TestCase):
    def test_name_present(self):
        self.assertIn("Debasish Mukherjee", HTML)

    def test_contact_channels(self):
        self.assertIn("email.html", HTML)
        self.assertIn("linkedin.com/in/erdebasish", HTML)
        self.assertIn("mailto:debasishformasters@gmail.com", EMAIL_HTML)
        self.assertIn("mail.google.com/mail", EMAIL_HTML)
        self.assertIn("outlook.office.com/mail/deeplink/compose", EMAIL_HTML)

    def test_no_phone_labels(self):
        for content in (HTML, EMAIL_HTML):
            self.assertNotRegex(content, r"(?i)phone")
            self.assertNotRegex(content, r"(?i)mobile")

    def test_known_phone_numbers_absent(self):
        for number in ["+4915510495848", "015168656484"]:
            self.assertNotIn(number, HTML)
            self.assertNotIn(number, EMAIL_HTML)


if __name__ == "__main__":
    unittest.main()
