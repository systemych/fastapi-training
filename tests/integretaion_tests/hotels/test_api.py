async def test_api(ac):
    response = await ac.get("/hotels", follow_redirects=True)
    print(f"{response=}")

    assert response.status_code == 200