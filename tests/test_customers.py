def test_list_customers(client):
    r = client.get("/api/customers?page=1&limit=5")
    assert r.status_code == 200
    assert "customers" in r.json()


def test_customer_profile(client):
    r = client.get("/api/customers?page=1&limit=1")
    cid = r.json()["customers"][0]

    r2 = client.get(f"/api/customers/{cid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == str(cid)


def test_top_customers(client):
    r = client.get("/api/customers/top?n=5")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
