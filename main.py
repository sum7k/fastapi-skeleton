import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import Depends, FastAPI, Response, status
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
import structlog

from auth.routers.auth import router as auth_router
from core.exceptions import ReadinessError
from core.logging import setup_logging
from core.middleware import CorrelationIdMiddleware, PrometheusMetricsMiddleware
from core.readiness import check_db_readiness
from core.security import RequireMember
from core.settings import Settings, get_settings

READINESS_TIMEOUT = 1.0  # seconds

setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(PrometheusMetricsMiddleware)
app.include_router(auth_router)


@app.get("/health", tags=["infra"])
async def health():
    return {"status": "ok"}


@app.get("/ready", tags=["infra"])
async def ready():
    try:
        await asyncio.wait_for(
            asyncio.gather(
                check_db_readiness(),  # REQUIRED
                # check_redis(redis),        # OPTIONAL
            ),
            timeout=READINESS_TIMEOUT,
        )
        return {"status": "ready"}

    except (asyncio.TimeoutError, ReadinessError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready"},
        )


@app.get("/info")
def info(user: RequireMember, settings: Settings = Depends(get_settings)):
    logger.info("handling info request", user_id=user.id)
    return {
        "db": settings.db_url,
    }


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )