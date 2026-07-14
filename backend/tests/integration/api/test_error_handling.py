from fastapi.testclient import TestClient

from app.main import app


def test_validation_error_has_standard_shape() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/barrier/check-access",
            json={
                "registration_number": "@@@",
            },
        )

    assert response.status_code == 422

    response_body = response.json()

    assert response_body["detail"]["code"] == "VALIDATION_ERROR"
    assert response_body["detail"]["message"] == "Request validation failed."
    assert "errors" in response_body["detail"]
    assert "request_id" in response_body["detail"]
