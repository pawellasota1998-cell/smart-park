import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class BarrierRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        enabled: bool,
        path: str,
        limit: int,
        window_seconds: int,
    ) -> None:
        super().__init__(app)
        self.enabled = enabled
        self.path = path
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        if not self.enabled or request.url.path != self.path:
            return await call_next(request)

        client_host = request.client.host if request.client is not None else "unknown"

        now = time.monotonic()
        window_start = now - self.window_seconds

        request_times = [
            request_time
            for request_time in self._requests.get(
                client_host,
                [],
            )
            if request_time > window_start
        ]

        if len(request_times) >= self.limit:
            retry_after = int(self.window_seconds - (now - request_times[0]))

            return JSONResponse(
                status_code=429,
                content={
                    "detail": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": ("Too many requests. " "Please try again later."),
                    }
                },
                headers={
                    "Retry-After": str(max(retry_after, 1)),
                },
            )

        request_times.append(now)
        self._requests[client_host] = request_times

        return await call_next(request)
