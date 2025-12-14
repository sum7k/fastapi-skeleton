from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.db import Token, User
from auth.models.domain import TokenDTO, UserDTO
from auth.models.mappers import TokenMapper, UserMapper
from auth.repositories.repository import Repository


class TokenRepository(Repository[TokenDTO, Token]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Token, TokenMapper())


class UserRepository(Repository[UserDTO, User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User, UserMapper())

    async def get_by_email(self, email: str) -> UserDTO | None:
        query = await self.session.execute(select(User).where(User.email == email))
        user = query.scalar_one_or_none()
        if user:
            return self.mapper.from_db(user)
        return None
