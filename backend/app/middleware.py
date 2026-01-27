"""Rate limiting middleware for FastAPI."""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)


def setup_rate_limiting(app):
    """
    Set up rate limiting middleware for the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    # Add rate limit error handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    return app
