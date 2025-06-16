import pytest


async def test_get_bookings(ac):
    response = await ac.get("/bookings", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-06-09", "2025-06-10", 200),
        (1, "2025-06-09", "2025-06-10", 200),
        (1, "2025-06-09", "2025-06-10", 200),
        (1, "2025-06-09", "2025-06-10", 200),
        (1, "2025-06-09", "2025-06-10", 200),
        (1, "2025-06-09", "2025-06-10", 400),
    ],
)
async def test_add_bookings(room_id, date_from, date_to, status_code, db, ac):
    response = await ac.post(
        "/bookings",
        follow_redirects=True,
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)


@pytest.fixture(scope="session")
async def delete_all_bookings(db):
    await db.bookings.delete()
    await db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, counter",
    [
        (1, "2025-06-09", "2025-06-10", 1),
        (1, "2025-06-09", "2025-06-10", 2),
        (1, "2025-06-09", "2025-06-10", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id, date_from, date_to, counter, delete_all_bookings, db, ac
):
    await ac.post(
        "/bookings",
        follow_redirects=True,
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    response = await ac.get("/bookings/me", follow_redirects=True)

    assert len(response.json()) == counter
