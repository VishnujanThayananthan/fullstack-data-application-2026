from collections.abc import Iterator
from dataclasses import dataclass, fields
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items, reservations


@dataclass
class Storage:

    items: dict[int, dict[str, Any]]
    reservations: dict[int, dict[str, Any]]

    def reset_all(self) -> None:
        for field in fields(self):
            getattr(self, field.name).clear()


@pytest.fixture
def storage() -> Iterator[Storage]:
    storage = Storage(items=items.FAKE_DB, reservations=reservations.FAKE_DB)
    storage.reset_all()
    yield storage
    storage.reset_all()


@pytest.fixture
def client(storage: Storage) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def existing_item(client: TestClient) -> dict[str, Any]:
    response = client.post(
        "/items",
        json={
            "titre": "Vélo électrique",
            "description": "Parfait pour la ville",
            "tarif_jour": 30.5,
            "disponible": True,
        },
    )
    assert response.status_code == 201
    return response.json()
