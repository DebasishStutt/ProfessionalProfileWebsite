import json
import os
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MODEL = "openai/gpt-5.2"
MAX_BODY_BYTES = 16000
MAX_MESSAGE_CHARS = 1000
MAX_HISTORY = 8
RATE_LIMIT_WINDOW = 600
RATE_LIMIT_MAX = 20

SYSTEM_PROMPT = """You are the digital twin of Debasish Mukherjee.
Speak in a professional, concise tone. Use only the profile information provided.
If a question goes beyond the profile, say you do not have that information.
Never provide phone numbers. If asked for contact, provide only email and LinkedIn.

Profile summary:
- Team Lead and Embedded Software Engineer at Bosch eBike Systems (BikeOS platform).
- 10+ years building embedded software, middleware, and system-level services.
- Strengths: platform architecture, roadmap planning, cross-functional leadership.
- Embedded domains: eBike systems, IoT firmware, embedded cybersecurity, automotive.
- Tech: C/C++, Python, FreeRTOS, CMSIS, ARM Cortex-M3/M4/M33, SPI/I2C/USART/CAN.
- Tooling: GoogleTest/GoogleMock, JLink/ST-Link/Segger, VS Code, Keil, MCUXpresso.
- Education: MSc INFOTECH Embedded Systems (University of Stuttgart), BTech EEE.
- Location: Stuttgart, Germany.
"""


def load_env_key():
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return ""
    with open(env_path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() == "OPENROUTER_API_KEY":
                return value.strip().strip("\"'")
    return ""


class RateLimiter:
    def __init__(self):
        self.storage = {}

    def allow(self, key):
        now = time.time()
        window_start = now - RATE_LIMIT_WINDOW
        events = [ts for ts in self.storage.get(key, []) if ts > window_start]
        if len(events) >= RATE_LIMIT_MAX:
            self.storage[key] = events
            return False
        events.append(now)
        self.storage[key] = events
        return True


rate_limiter = RateLimiter()


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), interest-cohort=()",
        )
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404, "Not Found")
        return None

    def is_forbidden_path(self, path):
        lowered = path.lower()
        if "/.git" in lowered or lowered.startswith("/."):
            return True
        if lowered.endswith(".env"):
            return True
        return False

    def do_GET(self):
        if self.is_forbidden_path(self.path):
            self.send_error(404, "Not Found")
            return
        if self.path.startswith("/api/"):
            self.send_error(405, "Method Not Allowed")
            return
        super().do_GET()

    def do_HEAD(self):
        if self.is_forbidden_path(self.path):
            self.send_error(404, "Not Found")
            return
        if self.path.startswith("/api/"):
            self.send_error(405, "Method Not Allowed")
            return
        super().do_HEAD()

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404, "Not Found")
            return

        if not rate_limiter.allow(self.client_address[0]):
            self.send_response(429)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"Rate limit exceeded"}')
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            self.send_response(413)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"Payload too large"}')
            return

        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"Invalid JSON"}')
            return

        messages = payload.get("messages", [])
        cleaned = []
        if isinstance(messages, list):
            for msg in messages:
                if not isinstance(msg, dict):
                    continue
                role = msg.get("role")
                content = msg.get("content")
                if role not in ("user", "assistant"):
                    continue
                if not isinstance(content, str):
                    continue
                content = content.strip()
                if not content:
                    continue
                if len(content) > MAX_MESSAGE_CHARS:
                    content = content[:MAX_MESSAGE_CHARS]
                cleaned.append({"role": role, "content": content})

        cleaned = cleaned[-MAX_HISTORY:]

        api_key = load_env_key()
        if not api_key:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"Server not configured"}')
            return

        request_body = json.dumps(
            {
                "model": MODEL,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + cleaned,
                "temperature": 0.3,
                "max_tokens": 500,
            }
        ).encode("utf-8")

        request = Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=request_body,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Debasish Mukherjee Digital Twin",
            },
        )

        try:
            with urlopen(request, timeout=30) as response:
                response_body = response.read().decode("utf-8")
        except (HTTPError, URLError):
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"Upstream unavailable"}')
            return

        try:
            data = json.loads(response_body)
            reply = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )
        except (ValueError, AttributeError):
            reply = ""

        if not reply:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"Empty response"}')
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"reply": reply}).encode("utf-8"))


def run():
    server_address = ("", 8000)
    httpd = ThreadingHTTPServer(server_address, Handler)
    print("Serving on http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
