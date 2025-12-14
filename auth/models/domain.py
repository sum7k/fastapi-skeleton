import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from auth.models.enums import UserRole

@dataclass
class UserDTO:
    id: uuid.UUID | None = None
    email: str | None = None
    password: str | None = None
    hashed_password: str | None = None
    role: Optional[UserRole] = None
    is_active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class TokenDTO:
    id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None
    expires_at: datetime | None = None
    is_active: bool | None = None
    ip_address: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
