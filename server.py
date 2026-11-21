
"""MuscleMethod local educational demo server."""

import json

from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer
)

from pathlib import Path
from compensation_layer import predict


HERE = Path(__file__).resolve().parent
PORT = 8001


class Handler(BaseHTTPRequestHandler):

    def send_json(self, obj, status=200):

        data = json.dumps(obj).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))

        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):

        if self.path == "/health":
            return self.send_json({
                "status": "ok",
                "mode": "synthetic demo"
            })

        if self.path not in ("/", "/index.html"):
            return self.send_error(404)

        data = (HERE / "index.html").read_bytes()

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))

        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):

        if self.path != "/predict":
            return self.send_error(404)

        try:
            size = int(
                self.headers.get("Content-Length", "0")
            )

            if not 0 < size <= 16384:
                raise ValueError(
                    "Body size must be 1..16384 bytes"
                )

            payload = json.loads(
                self.rfile.read(size).decode("utf-8")
            )

            self.send_json(predict(payload))

        except (
            ValueError,
            TypeError,
            KeyError,
            UnicodeDecodeError
        ) as error:

            self.send_json(
                {"error": str(error)},
                400
            )


if __name__ == "__main__":

    print("Open http://127.0.0.1:8001")
    print("Simulation only; Ctrl+C to stop")

    ThreadingHTTPServer(
        ("127.0.0.1", PORT),
        Handler
    ).serve_forever()
