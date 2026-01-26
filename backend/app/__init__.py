"""
Application package.

This module provides the FastAPI application factory and lifecycle management.
"""

from backend.app.factory import create_app

__all__ = ["create_app"]
