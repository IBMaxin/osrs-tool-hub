"""
Wiki service package.

This module provides OSRS Wiki API client, database sync functionality,
and wiki page scraping for gear progression guides.
"""

from backend.services.wiki.client import WikiAPIClient
from backend.services.wiki.scraper import (
    BaseWikiGuideScraper,
    RangedGuideScraper,
    MeleeGuideScraper,
    MagicGuideScraper,
    GearGuide,
    GuideSection,
    TierLoadout,
    ContentSpecificItem,
    BonusTableRow,
    SlotItem,
    scrape_ranged_guide,
    scrape_all_guides,
    guide_to_json,
)

# Backward compatibility alias
WikiClient = WikiAPIClient

__all__ = [
    "WikiAPIClient",
    "WikiClient",
    "BaseWikiGuideScraper",
    "RangedGuideScraper",
    "MeleeGuideScraper",
    "MagicGuideScraper",
    "GearGuide",
    "GuideSection",
    "TierLoadout",
    "ContentSpecificItem",
    "BonusTableRow",
    "SlotItem",
    "scrape_ranged_guide",
    "scrape_all_guides",
    "guide_to_json",
]
