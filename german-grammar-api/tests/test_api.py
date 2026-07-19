from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/api/v1/health").json() == {"status": "ok"}


def test_dative_correction():
    response = client.post("/api/v1/analyze", json={"text": "Ich gehe mit den Mann."})
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["corrected_sentence"] == "Ich gehe mit dem Mann."
