from typing import Optional

from fastapi import APIRouter, UploadFile, Form, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from src.UserInfo.auth.utils import get_current_user
from src.UserInfo.posts import crud
from src.UserInfo.users.models import User
from src.database import get_async_session

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get('/posts')
async def get_posts_page(request: Request):
    """
    Return posts page
    """
    return templates.TemplateResponse('/posts/posts.html', {'request': request})


@router.get('/posts/create-post')
async def create_post_page_endpoint(request: Request):
    """
    Create post page
    """
    return templates.TemplateResponse('/posts/create-post.html', {'request': request})


@router.get('/posts/get-posts')
async def get_user_posts_endpoint(
        session: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_user)
):
    """
    Return all user's posts'
    """
    return await crud.get_posts(user.id, session)


@router.post('/posts/create-post', response_class=Optional[JSONResponse])
async def create_user_post(
        text: str = Form(...),
        img: UploadFile = Form(...),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user)
):
    """
    Create new user's post in database
    """
    img_path = f'../src/UserInfo/posts/photos/{img.filename}'
    with open(img_path, "wb") as f:
        f.write(img.file.read())

    await crud.create_post(user.id, text, session, img_path)

    return RedirectResponse(url='/posts', status_code=status.HTTP_303_SEE_OTHER)
