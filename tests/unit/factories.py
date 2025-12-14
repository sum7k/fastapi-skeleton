# tests/factories/expense_dto_factory.py

import uuid

import factory
from faker import Faker

from auth.models.db import Token, User
from auth.models.domain import TokenDTO, UserDTO

fake = Faker()


class UserDTOFactory(factory.Factory):
    class Meta:
        model = UserDTO

    id = factory.LazyFunction(lambda: uuid.uuid4())
    email = factory.Faker("email")
    is_active = True
    role = "USER"


class UserDBFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(lambda: uuid.uuid4())
    email = factory.Faker("email")
    hashed_password = factory.LazyFunction(
        lambda: fake.password(length=60)
    )  # bcrypt length
    is_active = True
    role = "USER"


class TokenDTOFactory(factory.Factory):
    class Meta:
        model = TokenDTO

    id = factory.Sequence(lambda n: n + 1)
    user_id = factory.LazyFunction(lambda: uuid.uuid4())
    expires_at = factory.LazyFunction(lambda: fake.future_datetime(end_date="+30d"))
    is_active = True
    ip_address = factory.Faker("ipv4")


class TokenDBFactory(factory.Factory):
    class Meta:
        model = Token

    id = factory.Sequence(lambda n: n + 1)
    user_id = factory.LazyFunction(lambda: uuid.uuid4())
    expires_at = factory.LazyFunction(lambda: fake.future_datetime(end_date="+30d"))
    is_active = True
    ip_address = factory.Faker("ipv4")
