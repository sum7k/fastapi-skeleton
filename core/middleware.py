import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars
import structlog

logger = structlog.get_logger()

CORRELATION_HEADER = "X-Correlation-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        correlation_id = request.headers.get(CORRELATION_HEADER) or str(uuid.uuid4())

        # Bind context for this request
        bind_contextvars(
            correlation_id=correlation_id,
            path=request.url.path,
            method=request.method,
        )

        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

            response.headers[CORRELATION_HEADER] = correlation_id
            return response

        finally:
            clear_contextvars()


import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    ERROR_COUNT,
)


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        method = request.method
        path = request.url.path

        status_code = "500"

        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            return response

        finally:
            duration = time.perf_counter() - start_time

            REQUEST_COUNT.labels(
                method=method,
                path=path,
                status_code=status_code,
            ).inc()

            REQUEST_LATENCY.labels(
                method=method,
                path=path,
                status_code=status_code,
            ).observe(duration)

            if status_code.startswith("5"):
                ERROR_COUNT.labels(
                    method=method,
                    path=path,
                    status_code=status_code,
                ).inc()
