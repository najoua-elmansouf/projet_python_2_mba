def test_health(client):
    r = client.get("/api/system/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_metadata(client):
    r = client.get("/api/system/metadata")
    assert r.status_code == 200
    assert "version" in r.json()
