import threading
import time
import unittest
from urllib import parse, request

from app import run_server


class WebAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8765
        cls.thread = threading.Thread(target=run_server, kwargs={"host": "127.0.0.1", "port": cls.port}, daemon=True)
        cls.thread.start()
        time.sleep(0.2)

    def test_health(self):
        with request.urlopen(f"http://127.0.0.1:{self.port}/health") as resp:
            body = resp.read().decode("utf-8")
        self.assertIn('"status":"ok"', body)

    def test_home_get(self):
        with request.urlopen(f"http://127.0.0.1:{self.port}/") as resp:
            body = resp.read().decode("utf-8")
        self.assertIn("Maharishi Mission Agents", body)

    def test_preview_path_get(self):
        with request.urlopen(f"http://127.0.0.1:{self.port}/preview") as resp:
            body = resp.read().decode("utf-8")
        self.assertIn("Maharishi Mission Agents", body)

    def test_preview_path_post(self):
        payload = parse.urlencode(
            {
                "agent": "operations",
                "request_id": "T3",
                "date": "2026-02-15",
                "requested_by": "QA",
                "priority": "High",
                "goal": "Test preview post",
                "context": "Ctx",
                "constraints": "None",
                "structured_data": "Owner: A; Due: Tomorrow",
                "unstructured_notes": "Notes",
                "output_format": "markdown",
            }
        ).encode("utf-8")
        req = request.Request(f"http://127.0.0.1:{self.port}/preview", data=payload, method="POST")
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
        self.assertIn("Operations Agent Response", body)

    def test_home_post_all(self):
        payload = parse.urlencode(
            {
                "agent": "all",
                "request_id": "T2",
                "date": "2026-02-15",
                "requested_by": "QA",
                "priority": "High",
                "goal": "Test all",
                "context": "Ctx",
                "constraints": "None",
                "structured_data": "Owner: A; Due: Tomorrow",
                "unstructured_notes": "Notes",
                "output_format": "markdown",
            }
        ).encode("utf-8")
        req = request.Request(f"http://127.0.0.1:{self.port}/", data=payload, method="POST")
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
        self.assertIn("Education Agent Response", body)
        self.assertIn("Healthcare Outreach Agent Response", body)


if __name__ == "__main__":
    unittest.main()
