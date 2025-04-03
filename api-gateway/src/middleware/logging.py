import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from config import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request: {request.method} {request.url.path} - {process_time:.2f}s")
        return response
