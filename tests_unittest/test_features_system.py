import unittest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSystemFeatures(unittest.TestCase):
    def test_health(self):
        r = client.get("/api/system/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get("status"), "ok")

    def test_metadata(self):
        r = client.get("/api/system/metadata")
        self.assertEqual(r.status_code, 200)
        self.assertIn("version", r.json())
