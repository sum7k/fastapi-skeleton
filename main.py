from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import Depends, FastAPI

from auth.routers.auth import router as auth_router
from core.security import RequireMember
from core.settings import Settings, get_settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


@app.get("/health")
def health() -> dict[str, str]:
    # TODO: add health checks as and when added
    return {"status": "healthy", "message": "Service is running"}


@app.get("/v1/ping")
def ping() -> str:
    return "PONG"


@app.get("/info")
def info(user: RequireMember, settings: Settings = Depends(get_settings)):
    return {
        "db": settings.db_url,
    }
