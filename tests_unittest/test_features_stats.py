import unittest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestStatsFeatures(unittest.TestCase):
    def test_overview(self):
        r = client.get("/api/stats/overview")
        self.assertEqual(r.status_code, 200)
        self.assertIn("total_transactions", r.json())

    def test_amount_distribution(self):
        r = client.get("/api/stats/amount-distribution")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("bins", data)
        self.assertIn("counts", data)

    def test_by_type(self):
        r = client.get("/api/stats/by-type")
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_daily(self):
        r = client.get("/api/stats/daily")
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
