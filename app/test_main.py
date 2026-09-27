import main


def client():
    return main.app.test_client()


def test_healthz():
    resp = client().get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_index_ok(monkeypatch):
    monkeypatch.setattr(main, "FAIL_RATE", 0)
    resp = client().get("/")
    assert resp.status_code == 200
    assert "version" in resp.get_json()


def test_index_fails_when_fail_rate_is_one(monkeypatch):
    monkeypatch.setattr(main, "FAIL_RATE", 1)
    assert client().get("/").status_code == 500
