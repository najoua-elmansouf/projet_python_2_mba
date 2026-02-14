import unittest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestFraudFeatures(unittest.TestCase):
    def test_summary(self):
        r = client.get("/api/fraud/summary")
        self.assertEqual(r.status_code, 200)
        self.assertIn("total_frauds", r.json())

    def test_by_type(self):
        r = client.get("/api/fraud/by-type")
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_predict(self):
        r = client.post("/api/fraud/predict", json={"type": "Online Transaction", "amount": 6000})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("isFraud", data)
        self.assertIn("probability", data)
