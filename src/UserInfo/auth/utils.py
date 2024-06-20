import jwt
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from src.UserInfo.auth.token import create_access_token, decode_token
from src.UserInfo.users import crud as users_crud
from src.UserInfo.users.models import User
from src.database import get_async_session


class AuthGuard:
    async def __call__(self, request: Request):
        if not (token := request.cookies.get("token")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            if decode_token(token):
                return True
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_current_user(request: Request, session: AsyncSession = Depends(get_async_session)) -> User:
    """
    Gets current user and returns it
    """
    payload = decode_token(request.cookies.get("token"))
    return await users_crud.get_user_by_credentials(payload['email'], session)


def get_response_with_token(url='/', status_code: int = 303, token_data: dict = None) -> RedirectResponse:
    """
    Gets redirect response with token
    """
    response = RedirectResponse(url, status_code)
    response.set_cookie(key='token', value=create_access_token(token_data))
    return response


auth_guard = AuthGuard()
