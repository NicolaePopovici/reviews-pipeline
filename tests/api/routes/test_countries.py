from fastapi.testclient import TestClient
from sqlmodel import Session

from app import settings
from tests.utils.country import create_random_country


def test_read_item(client: TestClient, db: Session) -> None:
    country = create_random_country(db)
    response = client.get(f"{settings.API_V1_STR}/countries/{country.id}")

    assert response.status_code == 200
    content = response.json()

    assert content["name"] == country.name

# TODO: Add test for all endpoints with different usecases