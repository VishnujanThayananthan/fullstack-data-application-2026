import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {"titre": "ab", "description": "court", "tarif_jour": 12.5, "disponible": True},
        {"titre": "Vélo", "description": "court", "tarif_jour": 0, "disponible": True},
        {
            "titre": "Vélo",
            "description": "court",
            "tarif_jour": 12.5,
            "disponible": True,
            "couleur": "rouge",
        },
    ],
)
def test_create_item_rejects_invalid_payload(client, payload):
    response = client.post("/items", json=payload)
    assert response.status_code == 422


def test_create_item_returns_201_and_persists(client):
    payload = {
        "titre": "Vélo électrique",
        "description": "Parfait pour la ville",
        "tarif_jour": 30.5,
        "disponible": True,
    }

    response = client.post("/items", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["titre"] == payload["titre"]
    assert data["description"] == payload["description"]
    assert data["tarif_jour"] == payload["tarif_jour"]
    assert data["disponible"] is True
    assert client.get("/items/1").json() == data


def test_list_items_supports_filters_and_pagination(client):
    client.post("/items", json={"titre": "Vélo", "description": "A", "tarif_jour": 15, "disponible": True})
    client.post("/items", json={"titre": "Skate", "description": "B", "tarif_jour": 25, "disponible": False})
    client.post("/items", json={"titre": "Vélo électrique", "description": "C", "tarif_jour": 40, "disponible": True})

    response = client.get("/items?q=velo&disponible=true&skip=1&limit=1")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 3,
            "titre": "Vélo électrique",
            "description": "C",
            "tarif_jour": 40.0,
            "disponible": True,
        }
    ]


def test_get_missing_item_returns_404(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item 999 introuvable"}


def test_patch_item_updates_only_sent_fields(client):
    created = client.post(
        "/items",
        json={
            "titre": "Vélo",
            "description": "Pour la ville",
            "tarif_jour": 20,
            "disponible": True,
        },
    ).json()

    response = client.patch(
        f"/items/{created['id']}",
        json={"titre": "Vélo de route", "disponible": False},
    )

    assert response.status_code == 200
    patched = response.json()
    assert patched["id"] == created["id"]
    assert patched["titre"] == "Vélo de route"
    assert patched["description"] == "Pour la ville"
    assert patched["tarif_jour"] == 20.0
    assert patched["disponible"] is False


def test_delete_item_removes_it(client):
    created = client.post(
        "/items",
        json={
            "titre": "Trottinette",
            "description": "Compacte",
            "tarif_jour": 18,
            "disponible": True,
        },
    ).json()

    delete_response = client.delete(f"/items/{created['id']}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert client.get(f"/items/{created['id']}").status_code == 404
