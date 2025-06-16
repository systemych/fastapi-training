import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.services.auth import AuthService


@pytest.mark.parametrize(
    "email, password, register_status_code, login_status_code, get_info_status_code, logout_status_code",
    [
        ("person@mail.ru", "Strong_Passw0rd", 200, 200, 200, 200),
        ("person@mail.ru", "Strong_Passw0rd", 409, 200, 200, 200),
    ],
)
async def test_auth_controller(
    email,
    password,
    register_status_code,
    login_status_code,
    get_info_status_code,
    logout_status_code,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/auth/register", json={"email": email, "password": password}
        )
        payload = response.json()
        assert response.status_code == register_status_code

        if response.status_code == 200:
            assert payload["email"] == email
            assert AuthService().verify_password(
                password, AuthService().hash_password(password)
            )

        response = await ac.post(
            "/auth/login", json={"email": email, "password": password}
        )
        payload = response.json()

        assert response.status_code == login_status_code
        assert ac.cookies["access_token"]
        assert payload["access_token"]

        response = await ac.get("/auth/me")
        payload = response.json()
        assert response.status_code == get_info_status_code

        response = await ac.post("auth/logout")
        assert response.status_code == logout_status_code
