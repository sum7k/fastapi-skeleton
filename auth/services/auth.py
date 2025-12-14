import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.domain import TokenDTO, UserDTO
from auth.models.enums import UserRole
from auth.models.mappers import UserMapper
from auth.models.schemas import AuthCreds, TokenBase, TokenOut, UserCreate, UserOut
from auth.repositories.auth import TokenRepository, UserRepository
from core.database import get_db_session
from core.exceptions import AlreadyRegisteredException, UnauthorizedException
from core.settings import get_settings

security = HTTPBearer()
AuthHeaderDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


class PasswordService:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"])

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        result: bool = self.pwd_context.verify(password, hashed_password)
        return result

    async def get_password_hash(self, password: str) -> str:
        hashed: str = self.pwd_context.hash(password)
        return hashed


class TokenService(TokenRepository):
    secret_key = get_settings().jwt_secret_key
    algorithm = "HS256"
    default_timedelta = timedelta(minutes=60)

    async def create_access_token(
        self, data: UserDTO, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta is None:
            expires_delta = self.default_timedelta
        expiry = datetime.now(timezone.utc) + expires_delta

        # Create TokenDTO with required fields
        token_dto = TokenDTO(
            user_id=data.id,
            expires_at=expiry,
            is_active=True,
        )

        created_token = await self.create(token_dto)
        token_id = created_token.id

        # Create JWT payload with all claims
        serialized_data = {
            "id": str(data.id),
            "email": data.email,
            "exp": int(expiry.timestamp()),
            "iss": "fa-skeleton",
            "sub": str(token_id),
        }
        encoded_jwt: str = jwt.encode(serialized_data, self.secret_key, self.algorithm)
        return encoded_jwt

    async def deactivate(self, token_id_str: str) -> None:
        token_id = uuid.UUID(token_id_str)
        await self.update(token_id, {"is_active": False})

    def decode(self, encoded_token: str) -> dict[str, Any]:
        try:
            decoded: dict[str, Any] = jwt.decode(
                encoded_token, self.secret_key, algorithms=[self.algorithm]
            )
            return decoded
        except JWTError:
            raise UnauthorizedException

    async def validate(self, token_id_str: str) -> bool:
        token_id = uuid.UUID(token_id_str)
        token = await self.get(token_id)
        return token is not None and token.is_active is True


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.password_service = PasswordService()
        self.token_service = TokenService(session)
        self.user_repo = UserRepository(session)
        self.user_mapper = UserMapper()

    async def register_user(self, user: UserCreate) -> UserOut:
        if await self.user_repo.get_by_email(user.email):
            raise AlreadyRegisteredException
        hashed_password = await self.password_service.get_password_hash(user.password)
        user_dto = UserDTO(email=user.email, hashed_password=hashed_password)
        user_dto = await self.user_repo.create(user_dto)
        return UserOut(
            email=user_dto.email,  # type: ignore
            id=user_dto.id,  # type: ignore
            created_at=user_dto.created_at,  # type: ignore
            updated_at=user_dto.updated_at,  # type: ignore
        )

    async def authenticate_user(self, login_user: AuthCreds) -> TokenOut:
        if not (user := await self.user_repo.get_by_email(login_user.email)):
            raise UnauthorizedException
        if not await self.password_service.verify_password(
            login_user.password,
            user.hashed_password,  # type: ignore
        ):
            raise UnauthorizedException
        jwt = await self.token_service.create_access_token(user)
        return TokenOut(access_token=jwt)

    async def get_current_user(self, token: TokenBase) -> UserOut:
        payload = self.token_service.decode(token.access_token)
        if not await self.token_service.validate(str(payload.get("sub"))):
            raise UnauthorizedException
        if not (email := payload.get("email")):
            raise UnauthorizedException
        if not (user_dto := await self.user_repo.get_by_email(email)):
            raise UnauthorizedException
        return UserOut(
            email=user_dto.email or "",
            id=user_dto.id or uuid.UUID("00000000-0000-0000-0000-000000000000"),
            role=user_dto.role or UserRole.VIEWER,
            created_at=user_dto.created_at or datetime.now(timezone.utc),
            updated_at=user_dto.updated_at or datetime.now(timezone.utc),
        )

    async def logout(self, credentials: HTTPAuthorizationCredentials) -> None:
        payload = self.token_service.decode(credentials.credentials)
        await self.token_service.deactivate(str(payload.get("sub")))


def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    return AuthService(session)


async def get_current_user_service(
    credentials: AuthHeaderDep,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserOut:
    token = TokenBase(access_token=credentials.credentials)
    return await auth_service.get_current_user(token)


AuthServiceDep = Depends(get_auth_service)
CurUserDep = Annotated[UserOut, Depends(get_current_user_service)]
