"""Local ingest sink for browser-side scraping payloads.

Accepts POSTs on 127.0.0.1:8765/ingest and appends each body as one JSONL line
to _ingest.jsonl next to this script. CORS is wide-open so the Instagram page
can post cross-origin from https://www.instagram.com.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SINK = os.path.join(HERE, "_ingest.jsonl")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        body = b"ping-ok"
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        with open(SINK, "ab") as fh:
            fh.write(raw.rstrip(b"\n") + b"\n")
        try:
            kind = json.loads(raw.decode("utf-8", "replace")).get("kind", "?")
            tail = json.loads(raw.decode("utf-8", "replace")).get("sc", "?")
        except Exception:
            kind, tail = "raw", "?"
        print(f"[ingest] +{len(raw)}b kind={kind} sc={tail}", flush=True)
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        body = b"ok"
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print(f"[ingest] listening on http://127.0.0.1:8765 -> {SINK}", flush=True)
    srv.serve_forever()
