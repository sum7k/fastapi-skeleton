import uuid
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models.enums import UserRole
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.VIEWER)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    # Relationships
    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="user")


# class File(Base):
#     __tablename__ = "file"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     description: Mapped[str] = mapped_column()
#     created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
#     updated_at: Mapped[datetime] = mapped_column(
#         default=datetime.now(UTC), onupdate=datetime.now(UTC)
#     )
#     expenses: Mapped[list["Expense"]] = relationship(
#         "Expense", back_populates="source", cascade="all, delete-orphan"
#     )


# class Expense(Base):
#     __tablename__ = "expense"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     date: Mapped[datetime] = mapped_column()
#     amount: Mapped[float] = mapped_column()
#     currency: Mapped[str] = mapped_column()
#     vendor: Mapped[str] = mapped_column()
#     category: Mapped[str] = mapped_column()
#     description: Mapped[str] = mapped_column()
#     created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
#     updated_at: Mapped[datetime] = mapped_column(
#         default=datetime.now(UTC), onupdate=datetime.now(UTC)
#     )
#     source_id: Mapped[int | None] = mapped_column(ForeignKey("file.id"), nullable=True)
#     source: Mapped["File | None"] = relationship("File", back_populates="expenses")


class Token(Base):
    __tablename__ = "tokens"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    ip_address: Mapped[str | None] = mapped_column(String(length=255))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tokens")

    __table_args__ = (  # type: ignore[assignment]
        Index("ix_tokens_user_id", "user_id"),
        Index("ix_tokens_ip_address", "ip_address"),
    )
