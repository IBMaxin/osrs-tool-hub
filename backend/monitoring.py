"""Monitoring and observability configuration.

Provides error tracking, performance monitoring, and application metrics.
"""

import logging
import time
from typing import Callable

import sentry_sdk
from fastapi import Request, Response
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

DB_QUERY_DURATION = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation']
)

EXTERNAL_API_DURATION = Histogram(
    'external_api_duration_seconds',
    'External API call duration in seconds',
    ['service', 'endpoint']
)

ERROR_COUNT = Counter(
    'errors_total',
    'Total number of errors',
    ['type', 'endpoint']
)


def init_sentry() -> None:
    """Initialize Sentry error tracking.
    
    Only initializes if SENTRY_DSN is configured in environment.
    """
    if not settings.SENTRY_DSN:
        logger.info("Sentry DSN not configured, skipping initialization")
        return
    
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=settings.SENTRY_PROFILES_SAMPLE_RATE,
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
            HttpxIntegration(),
        ],
        before_send=before_send_sentry,
        release=settings.APP_VERSION,
    )
    logger.info(f"Sentry initialized for environment: {settings.ENVIRONMENT}")


def before_send_sentry(event, hint):
    """Filter and modify events before sending to Sentry."""
    # Don't send 404 errors
    if event.get('exception'):
        exc_values = event['exception'].get('values', [])
        if exc_values:
            exc_type = exc_values[0].get('type', '')
            if exc_type == 'HTTPException' and hint.get('exc_info', [None, None, None])[1]:
                status_code = getattr(hint['exc_info'][1], 'status_code', None)
                if status_code == 404:
                    return None
    
    # Add custom context
    if 'request' in hint:
        request = hint['request']
        event.setdefault('contexts', {})['request_info'] = {
            'client_ip': request.client.host if hasattr(request, 'client') else None,
            'user_agent': request.headers.get('user-agent'),
        }
    
    return event


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics for all requests."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip metrics endpoint itself
        if request.url.path == '/metrics':
            return await call_next(request)
        
        method = request.method
        endpoint = request.url.path
        
        # Start timing
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status = response.status_code
            
            # Record metrics
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(
                time.time() - start_time
            )
            
            return response
        
        except Exception as e:
            # Record error
            ERROR_COUNT.labels(type=type(e).__name__, endpoint=endpoint).inc()
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=500).inc()
            raise


async def metrics_endpoint(request: Request) -> Response:
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class PerformanceLogger:
    """Context manager for logging operation performance."""
    
    def __init__(self, operation: str, metric: Histogram = None):
        self.operation = operation
        self.metric = metric
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        
        # Log performance
        if duration > 1.0:  # Log slow operations (>1s)
            logger.warning(
                f"Slow operation detected: {self.operation} took {duration:.2f}s"
            )
        else:
            logger.debug(f"{self.operation} completed in {duration:.2f}s")
        
        # Record metric if provided
        if self.metric:
            self.metric.labels(operation=self.operation).observe(duration)
        
        return False  # Don't suppress exceptions


def log_external_api_call(service: str, endpoint: str, duration: float, success: bool):
    """Log external API call metrics."""
    EXTERNAL_API_DURATION.labels(service=service, endpoint=endpoint).observe(duration)
    
    if not success:
        ERROR_COUNT.labels(type='ExternalAPIError', endpoint=f"{service}/{endpoint}").inc()
    
    if duration > 5.0:
        logger.warning(
            f"Slow external API call: {service}/{endpoint} took {duration:.2f}s"
        )
