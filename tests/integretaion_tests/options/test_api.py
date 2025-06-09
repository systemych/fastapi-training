async def test_get_options(ac):
    response = await ac.get("/options", follow_redirects=True)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_create_option(ac):
    option = "Холодильник"
    response = await ac.post("/options", follow_redirects=True, json={"title": option})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["title"] == option