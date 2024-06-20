from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from src.UserInfo.auth.password import get_hashed_password
from src.UserInfo.auth.utils import get_response_with_token
from src.UserInfo.users import crud as users_crud
from src.database import get_async_session

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get('/reg')
async def register_page_endpoint(request: Request):
    """
    Returns registration page
    """
    return templates.TemplateResponse("reg.html", {"request": request})


@router.post('/register-user')
async def create_new_user(
        email: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Creates new user and redirects to root page
    """
    await users_crud.create_user(email, get_hashed_password(password), session)

    return get_response_with_token(status_code=status.HTTP_303_SEE_OTHER, token_data={"email": email})


@router.get('/login')
async def login(request: Request):
    """
    Returns login page
    """
    return templates.TemplateResponse("auth.html", {"request": request})


@router.post('/auth')
async def create_access_token_endpoint(
        email: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_async_session)
):
    if not await users_crud.get_user_by_credentials(email, session, hashed_password=get_hashed_password(password)):
        return {"message": "User not found"}

    return get_response_with_token(status_code=status.HTTP_303_SEE_OTHER, token_data={"email": email})
