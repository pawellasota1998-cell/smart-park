from fastapi.testclient import TestClient

from app.main import app


# Test ochrony endpointu
def test_get_me_requires_authentication() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
