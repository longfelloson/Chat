from typing import Optional, List

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.UserInfo.posts.models import Post


async def get_posts(user_id: int, session: AsyncSession) -> Optional[List[Post]]:
    """
    Return a list of all posts.
    """
    posts = await session.execute(select(Post).where(Post.user_id == user_id))
    return posts.scalars().all()


async def create_post(user_id: int, text: str, session: AsyncSession, img_path: str = None) -> None:
    """
    Create a new post.
    """
    await session.execute(insert(Post).values(img_path=img_path, user_id=user_id, text=text))
    await session.commit()
