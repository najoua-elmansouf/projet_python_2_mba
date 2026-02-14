def test_overview(client):
    r = client.get("/api/stats/overview")
    assert r.status_code == 200
    assert "total_transactions" in r.json()


def test_amount_distribution(client):
    r = client.get("/api/stats/amount-distribution")
    assert r.status_code == 200
    data = r.json()
    assert "bins" in data
    assert "counts" in data


def test_by_type(client):
    r = client.get("/api/stats/by-type")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_daily(client):
    r = client.get("/api/stats/daily")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
