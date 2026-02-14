import unittest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestTransactionsFeatures(unittest.TestCase):
    def test_list_transactions(self):
        r = client.get("/api/transactions?page=1&limit=5")
        self.assertEqual(r.status_code, 200)
        self.assertIn("transactions", r.json())

    def test_get_transaction_by_id(self):
        r = client.get("/api/transactions?page=1&limit=1")
        tid = r.json()["transactions"][0]["id"]
        r2 = client.get(f"/api/transactions/{tid}")
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json()["id"], tid)

    def test_search_transactions(self):
        r = client.post(
            "/api/transactions/search",
            json={"type": "Online Transaction", "amount_min": 1, "amount_max": 300},
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("transactions", r.json())

    def test_types(self):
        r = client.get("/api/transactions/types")
        self.assertEqual(r.status_code, 200)
        self.assertIn("types", r.json())

    def test_to_customer(self):
        r = client.get("/api/transactions/to-customer/123")
        self.assertEqual(r.status_code, 200)
        self.assertIn("transactions", r.json())
