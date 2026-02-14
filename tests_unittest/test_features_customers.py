import unittest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCustomersFeatures(unittest.TestCase):
    def test_list_customers(self):
        r = client.get("/api/customers?page=1&limit=5")
        self.assertEqual(r.status_code, 200)
        self.assertIn("customers", r.json())

    def test_top_customers(self):
        r = client.get("/api/customers/top?n=5")
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_customer_profile(self):
        r = client.get("/api/customers?page=1&limit=1")
        cid = r.json()["customers"][0]
        r2 = client.get(f"/api/customers/{cid}")
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json()["id"], str(cid))
