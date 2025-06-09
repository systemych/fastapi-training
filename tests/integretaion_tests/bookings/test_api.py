async def test_get_bookings(ac):
    response = await ac.get("/bookings", follow_redirects=True)
    assert response.status_code == 200


async def test_add_booking(db, ac):
    room_id = room_id = (await db.rooms.get_all())[0].id
    response = await ac.post(
        "/bookings",
        follow_redirects=True,
        json={"room_id": room_id, "date_from": "2025-06-09", "date_to": "2025-06-09"},
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
