"""FastAPI application factory."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.lifespan import lifespan
from backend.app.routers import include_routers
from backend.app.middleware import setup_rate_limiting
from backend.config import settings
from backend.api.v1.schemas import ErrorResponse, ErrorDetail


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="OSRS Tool Hub API",
        description="API for OSRS tools including flipping and gear calculators",
        lifespan=lifespan,
        version="1.0.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting middleware (if enabled)
    if settings.rate_limit_enabled:
        app = setup_rate_limiting(app)

    # Include routers
    include_routers(app)

    # Global exception handler for consistent error responses
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """
        Convert HTTPExceptions to consistent ErrorResponse format.

        Args:
            request: FastAPI request object
            exc: HTTPException instance

        Returns:
            JSONResponse with ErrorResponse schema
        """
        # Extract error code from status code
        error_code = f"HTTP_{exc.status_code}"

        # Handle different detail formats
        if isinstance(exc.detail, dict):
            # Already structured, extract message and details
            message = exc.detail.get("message", exc.detail.get("detail", "An error occurred"))
            details = {k: v for k, v in exc.detail.items() if k not in ("message", "detail")}
        elif isinstance(exc.detail, str):
            message = exc.detail
            details = None
        else:
            message = str(exc.detail) if exc.detail else "An error occurred"
            details = None

        error_response = ErrorResponse(
            error=ErrorDetail(
                code=error_code,
                message=message,
                details=details,
            )
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )

    return app
