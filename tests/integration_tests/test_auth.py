from app.core.user import AuthService


def test_encode_and_decode_access_token():
    service = AuthService()
    data = {'user_id': 1}
    jwt_token = service.create_access_token(data)

    payload = service.decode_access_token(jwt_token)
    assert payload is not None
    assert payload['user_id'] == data['user_id']