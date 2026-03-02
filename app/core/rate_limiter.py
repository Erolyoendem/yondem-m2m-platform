import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, FastAPI

# Disable rate limiting during automated tests to prevent quota exhaustion
_enabled = os.getenv("TESTING") != "true"
limiter = Limiter(key_func=get_remote_address, enabled=_enabled)

def setup_rate_limiting(app: FastAPI):
    """Configure rate limiting for the application"""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
