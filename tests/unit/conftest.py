from typing import Any, List, Optional
from unittest.mock import AsyncMock, Mock

import pytest


class AsyncCtxMgr:
    """Simple async context manager used for `async with session.begin():`"""

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class ExecuteResult:
    """
    Lightweight mimic of SQLAlchemy result for tests.
    - .scalars().all() -> list
    - .scalar_one() -> item or raise NoResultFound
    """

    def __init__(
        self, scalars_list: Optional[List[Any]] = None, scalar_single: Any = None
    ):
        self._scalars_list = list(scalars_list or [])
        self._scalar_single = scalar_single

        # scalars() returns object with .all() (sync) in SQLAlchemy; we mimic that
        class _Scalars:
            def __init__(self, lst):
                self._lst = lst

            def all(self):
                return self._lst

        self._scalars = _Scalars(self._scalars_list)

    def scalars(self):
        return self._scalars

    def scalar_one(self):
        # prefer explicit scalar_one override, else use first element, else raise
        if self._scalar_single is not None:
            return self._scalar_single
        if self._scalars_list:
            return self._scalars_list[0]
        # raise same exception SQLAlchemy raises for no result
        from sqlalchemy.exc import NoResultFound  # type: ignore

        raise NoResultFound("No row found for query")


def make_session_mock() -> Mock:
    """
    Return a Mock that behaves like sqlalchemy.ext.asyncio.AsyncSession for tests.
    - session.execute is AsyncMock returning ExecuteResult
    - session.begin() returns an async context manager object
    - commit/refresh/delete are AsyncMock (awaitable)
    - add is regular Mock (add is sync in SQLAlchemy)
    """
    session = Mock(name="AsyncSessionMock")

    # Async methods
    session.execute = AsyncMock(name="execute")
    session.flush = AsyncMock(name="flush")
    session.refresh = AsyncMock(name="refresh")
    session.delete = AsyncMock(name="delete")

    # add is sync in SQLAlchemy; keep as Mock
    session.add = Mock(name="add")

    # store a default execute result that tests can replace
    session._last_execute_result = ExecuteResult([])

    async def _execute_side_effect(*args, **kwargs):
        # always return the stored ExecuteResult (synchronous object)
        return session._last_execute_result

    session.execute.side_effect = _execute_side_effect

    # begin() should return an async context manager
    session.begin = Mock(name="begin", return_value=AsyncCtxMgr())

    return session


@pytest.fixture
def session_mock():
    return make_session_mock()
