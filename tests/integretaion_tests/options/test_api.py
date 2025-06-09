async def test_api(ac):
    response = await ac.get("/options", follow_redirects=True)
    assert response.status_code == 200

    response = await ac.post("/options", follow_redirects=True, json={"title": "Холодильник"})
    assert response.status_code == 200