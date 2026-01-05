from app.core.user import AuthService


def test_create_access_token():
    jwt_token = AuthService().create_access_token({"user_id": 1})

    assert jwt_token is not None
    assert isinstance(jwt_token, str)
