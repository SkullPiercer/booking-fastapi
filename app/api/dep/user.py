from typing import Annotated

from fastapi import Depends, Request, HTTPException, status

from app.core.user import AuthService


def get_token_from_cookie(request: Request):
    access_token = request.cookies.get("access_token", None)
    if access_token is not None:
        return access_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пожалуйста войдите в систему!",
    )


def get_user_id(access_token: str = Depends(get_token_from_cookie)):
    user_data = AuthService().decode_access_token(access_token)
    user_id = user_data.get("user_id", None)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пожалуйста войдите в систему!",
        )
    return user_id


UserIdDep = Annotated[int, Depends(get_user_id)]
