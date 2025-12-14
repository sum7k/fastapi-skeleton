from auth.models.db import Token, User
from auth.models.domain import TokenDTO, UserDTO


class UserMapper:
    def from_db(self, user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def to_db(self, user_dto: UserDTO) -> User:
        return User(
            id=user_dto.id,
            email=user_dto.email,
            hashed_password=user_dto.hashed_password,
            is_active=user_dto.is_active,
            role=user_dto.role,
            created_at=user_dto.created_at,
            updated_at=user_dto.updated_at,
        )


class TokenMapper:
    def from_db(self, token: Token) -> TokenDTO:
        return TokenDTO(
            id=token.id,
            user_id=token.user_id,
            expires_at=token.expires_at,
            is_active=token.is_active,
            ip_address=token.ip_address,
        )

    def to_db(self, token_dto: TokenDTO) -> Token:
        return Token(
            id=token_dto.id,
            user_id=token_dto.user_id,
            expires_at=token_dto.expires_at,
            is_active=token_dto.is_active,
            ip_address=token_dto.ip_address,
        )
