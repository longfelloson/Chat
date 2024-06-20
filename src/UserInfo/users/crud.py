from sqlalchemy import select, and_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Optional

from src.UserInfo.users.models import User


async def get_user_by_credentials(email: str, session: AsyncSession, hashed_password: str = None) -> Optional[User]:
    """
    Gets a user by its credentials.
    """
    stmt = select(User).where(User.email == email)
    if hashed_password:
        stmt = stmt.where(and_(User.hashed_password == hashed_password, User.email == email))

    user = await session.execute(stmt)
    return user.scalar_one_or_none()


async def create_user(email: str, hashed_password: str, session: AsyncSession) -> None:
    """
    Creates a new user.
    """
    await session.execute(insert(User).values(email=email, hashed_password=hashed_password))
    await session.commit()
