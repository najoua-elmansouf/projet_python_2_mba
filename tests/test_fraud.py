def test_summary(client):
    r = client.get("/api/fraud/summary")
    assert r.status_code == 200
    assert "total_frauds" in r.json()


def test_fraud_by_type(client):
    r = client.get("/api/fraud/by-type")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_predict(client):
    r = client.post(
        "/api/fraud/predict",
        json={"type": "Online Transaction", "amount": 6000},
    )
    assert r.status_code == 200
    data = r.json()
    assert "isFraud" in data
    assert "probability" in data
