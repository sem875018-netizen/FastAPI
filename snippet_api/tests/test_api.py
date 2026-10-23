from fastapi.testclient import TestClient
from main import app


def test_healthcheck():
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
