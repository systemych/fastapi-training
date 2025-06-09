async def test_get_bookings(ac):
    response = await ac.get("/bookings", follow_redirects=True)
    assert response.status_code == 200