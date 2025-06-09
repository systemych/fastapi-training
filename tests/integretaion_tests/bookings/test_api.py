async def test_get_bookings(ac):
    response = await ac.get("/bookings", follow_redirects=True)
    assert response.status_code == 200


async def test_add_bookings(db, ac):
    room = (await db.rooms.get_all())[0]

    for i in range(0, room.quantity):
        response = await ac.post(
            "/bookings",
            follow_redirects=True,
            json={"room_id": room.id, "date_from": "2025-06-09", "date_to": "2025-06-10"},
        )
        assert response.status_code == 200
        res = response.json()
        assert isinstance(res, dict)

    response = await ac.post(
        "/bookings",
        follow_redirects=True,
        json={"room_id": room.id, "date_from": "2025-06-09", "date_to": "2025-06-10"},
    )
    assert response.status_code == 400