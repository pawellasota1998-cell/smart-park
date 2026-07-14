from fastapi.testclient import TestClient

from app.main import app


def test_response_contains_request_id_header() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/health",
        )

    assert response.status_code == 200
    assert response.headers["x-request-id"]


def test_request_id_header_is_preserved() -> None:
    request_id = "test-request-id"

    with TestClient(app) as client:
        response = client.get(
            "/api/v1/health",
            headers={
                "X-Request-ID": request_id,
            },
        )

    assert response.status_code == 200
    assert response.headers["x-request-id"] == request_id
