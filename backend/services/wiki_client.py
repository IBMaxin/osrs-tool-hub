"""
Wiki client module (backward compatibility shim).

This module re-exports from backend.services.wiki for backward compatibility.
New code should import directly from backend.services.wiki.
"""

from backend.services.wiki import WikiAPIClient as _WikiAPIClient
from backend.services.wiki.sync import sync_items_to_db as _sync_items_to_db, sync_prices_to_db as _sync_prices_to_db


class WikiAPIClient(_WikiAPIClient):
    """WikiAPIClient with backward-compatible sync methods."""
    
    async def sync_items_to_db(self, session):
        """Sync items to database (backward compatibility method)."""
        return await _sync_items_to_db(self, session)
    
    async def sync_prices_to_db(self, session):
        """Sync prices to database (backward compatibility method)."""
        return await _sync_prices_to_db(self, session)


# Backward compatibility alias
WikiClient = WikiAPIClient

__all__ = ["WikiAPIClient", "WikiClient"]
