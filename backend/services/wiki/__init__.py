"""
Wiki service package.

This module provides OSRS Wiki API client and database sync functionality.
"""

from backend.services.wiki.client import WikiAPIClient

# Backward compatibility alias
WikiClient = WikiAPIClient

__all__ = ["WikiAPIClient", "WikiClient"]
