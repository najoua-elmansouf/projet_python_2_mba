def test_list_transactions(client):
    r = client.get("/api/transactions?page=1&limit=5")
    assert r.status_code == 200
    data = r.json()
    assert "transactions" in data
    assert isinstance(data["transactions"], list)


def test_get_transaction_by_id(client):
    r = client.get("/api/transactions?page=1&limit=1")
    tid = r.json()["transactions"][0]["id"]

    r2 = client.get(f"/api/transactions/{tid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == tid


def test_types(client):
    r = client.get("/api/transactions/types")
    assert r.status_code == 200
    assert "types" in r.json()


def test_recent(client):
    r = client.get("/api/transactions/recent?n=3")
    assert r.status_code == 200
    assert "transactions" in r.json()


def test_search(client):
    r = client.post(
        "/api/transactions/search",
        json={"type": "Online Transaction", "amount_min": 1, "amount_max": 300},
    )
    assert r.status_code == 200
    assert "transactions" in r.json()


def test_by_customer(client):
    r = client.get("/api/transactions?page=1&limit=1")
    cid = r.json()["transactions"][0]["client_id"]

    r2 = client.get(f"/api/transactions/by-customer/{cid}")
    assert r2.status_code == 200
    assert "transactions" in r2.json()


def test_to_customer(client):
    r = client.get("/api/transactions/to-customer/123")
    assert r.status_code == 200
    assert "transactions" in r.json()


def test_delete_fake(client):
    r = client.get("/api/transactions?page=1&limit=1")
    tid = r.json()["transactions"][0]["id"]

    r2 = client.delete(f"/api/transactions/{tid}")
    assert r2.status_code == 200
    assert r2.json()["deleted"] is True
