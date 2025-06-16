async def test_api(ac):
    response = await ac.get("/hotels", follow_redirects=True)
    assert response.status_code == 200
