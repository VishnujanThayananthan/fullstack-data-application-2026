import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {"item_id": 0, "date_debut": "2026-01-10", "date_fin": "2026-01-12"},
        {"item_id": 1, "date_debut": "2026-01-12", "date_fin": "2026-01-12"},
        {"item_id": 1, "date_debut": "2026-01-12", "date_fin": "2026-01-10"},
    ],
)
def test_create_reservation_rejects_invalid_payload(client, payload):
    response = client.post("/reservations", json=payload)
    assert response.status_code == 422


def test_create_and_get_reservation(client):
    payload = {"item_id": 1, "date_debut": "2026-01-10", "date_fin": "2026-01-12"}

    response = client.post("/reservations", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data == {
        "id": 1,
        "item_id": 1,
        "date_debut": "2026-01-10",
        "date_fin": "2026-01-12",
        "statut": "active",
    }
    assert client.get("/reservations/1").json() == data


def test_list_reservations_can_filter_by_item_id(client):
    client.post("/reservations", json={"item_id": 1, "date_debut": "2026-01-10", "date_fin": "2026-01-12"})
    client.post("/reservations", json={"item_id": 2, "date_debut": "2026-02-10", "date_fin": "2026-02-12"})

    response = client.get("/reservations?item_id=1&limit=10")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "item_id": 1,
            "date_debut": "2026-01-10",
            "date_fin": "2026-01-12",
            "statut": "active",
        }
    ]


def test_cancel_reservation_updates_status_twice_raises_conflict(client):
    reservation = client.post(
        "/reservations",
        json={"item_id": 3, "date_debut": "2026-03-01", "date_fin": "2026-03-05"},
    ).json()

    cancel_response = client.post(f"/reservations/{reservation['id']}/annuler")
    assert cancel_response.status_code == 200
    assert cancel_response.json()["statut"] == "annulee"

    repeat_cancel = client.post(f"/reservations/{reservation['id']}/annuler")
    assert repeat_cancel.status_code == 409
    assert repeat_cancel.json() == {"detail": "Reservation déjà annulée"}


def test_get_missing_reservation_returns_404(client):
    response = client.get("/reservations/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Reservation 999 introuvable"}
