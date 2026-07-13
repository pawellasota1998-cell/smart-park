from fastapi.testclient import TestClient

from app.main import app


def test_create_application_requires_authentication() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/applications",
            json={
                "registration_number": "WA12345",
                "preferred_floor": 2,
            },
        )

    assert response.status_code == 401
