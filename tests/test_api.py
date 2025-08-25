"""Tests for the FastAPI card information endpoint."""

from fastapi.testclient import TestClient

from dealdex.api import app

client = TestClient(app)


def test_api_get_card_info() -> None:
    response = client.get("/cards/Black%20Lotus")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Black Lotus"
    assert data["set"]
    assert data["collector_number"]


def test_api_unknown_card() -> None:
    response = client.get("/cards/This%20Card%20Does%20Not%20Exist")
    assert response.status_code == 404
