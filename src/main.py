import uvicorn
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src import database
from src.Chat.chats.router import router as chats_router
from src.Chat.messages.router import router as messages_router
from src.UserInfo.auth.router import router as auth_router
from src.UserInfo.auth.utils import get_current_user, auth_guard
from src.UserInfo.posts.router import router as posts_router
from src.UserInfo.users.models import User

app = FastAPI()
templates = Jinja2Templates(directory="../templates")


@app.on_event("startup")
async def startup():
    """
    Startup function
    """
    await database.create_tables()


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized(_request, _exception):
    """
    Show login page
    """
    return RedirectResponse(url='/login')


@app.get("/", dependencies=[Depends(auth_guard)])
async def root(request: Request, user: User = Depends(get_current_user)):
    """
    Root endpoint
    """
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


if __name__ == '__main__':
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(chats_router)
    app.include_router(auth_router)
    app.include_router(messages_router)
    app.include_router(posts_router)

    uvicorn.run(app)
