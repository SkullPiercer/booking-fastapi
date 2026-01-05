import pytest
from fastapi import status


@pytest.mark.parametrize(
    "email, password, confirm_password, status_code",
    [
        ("k0t@pes.com", "1234", "1234", status.HTTP_200_OK),
        ("k0t@pes.com", "1234", "1234", status.HTTP_400_BAD_REQUEST),
        ("k0t1@pes.com", "1235", "1235", status.HTTP_200_OK),
        ("abcde", "1235", "1235", status.HTTP_422_UNPROCESSABLE_CONTENT),
        ("abcde@abc", "1235", "1235", status.HTTP_422_UNPROCESSABLE_CONTENT),
    ],
)
async def test_auth_flow(
    email: str,
    password: str,
    confirm_password: str,
    status_code: int,
    async_client,
):
    # /register
    resp_register = await async_client.post(
        "/users/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
        },
    )
    assert resp_register.status_code == status_code
    if status_code != status.HTTP_200_OK:
        return

    # /login
    resp_login = await async_client.post(
        "/users/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert resp_login.status_code == status.HTTP_200_OK
    assert async_client.cookies["access_token"]
    assert "access_token" in resp_login.json()

    # /me
    resp_me = await async_client.get("/users/me")
    assert resp_me.status_code == status.HTTP_200_OK
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    resp_logout = await async_client.post("/users/logout")
    assert resp_logout.status_code == status.HTTP_200_OK
    assert "access_token" not in async_client.cookies
