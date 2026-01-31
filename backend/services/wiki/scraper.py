"""
Wiki page scraping utilities for gear progression guides.

This module provides a scalable framework for scraping OSRS Wiki guide pages
to extract gear progression data for different combat styles.
"""

from __future__ import annotations

import asyncio
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from bs4 import BeautifulSoup
from bs4.element import Tag

import httpx

from backend.config import settings
from backend.services.wiki_guide_verification import WIKI_GUIDE_SLOT_ORDER

logger = logging.getLogger(__name__)


@dataclass
class SlotItem:
    """Represents a single equipment slot item."""

    name: str
    icon_override: str | None = None


@dataclass
class TierLoadout:
    """Represents a gear tier loadout."""

    label: str
    total_cost: int
    slots: dict[str, SlotItem | None] = field(default_factory=dict)


@dataclass
class ContentSpecificItem:
    """Represents a content-specific equipment recommendation."""

    name: str
    equipment: str | None
    use_case: str | None
    cost_buy: int | None
    cost_per_hour: int | None


@dataclass
class BonusTableRow:
    """Represents a bonus comparison table row."""

    item: str
    bonus: str
    cost: int | None
    delta: str
    cost_per_delta: str


@dataclass
class GuideSection:
    """Represents a game stage section (Mid Game, Late Game, etc.)."""

    id: str
    title: str
    tiers: list[TierLoadout] = field(default_factory=list)
    content_specific: list[ContentSpecificItem] = field(default_factory=list)


@dataclass
class GearGuide:
    """Represents a complete gear progression guide."""

    style: str
    cost_per_hour_label: str
    slot_order: list[str]
    game_stages: list[GuideSection] = field(default_factory=list)
    bonus_table: list[BonusTableRow] = field(default_factory=list)


class BaseWikiGuideScraper(ABC):
    """
    Base class for wiki guide scraping.

    Provides common functionality for fetching and parsing OSRS Wiki guide pages.
    Extend this class for specific combat styles (melee, ranged, magic).
    """

    # Subclasses should override these
    style: str = "base"
    cost_per_hour_label: str = "Cost (1 Hour)"
    guide_page: str = ""

    def __init__(self) -> None:
        """Initialize the scraper with HTTP client."""
        self.base_url = "https://oldschool.runescape.wiki"
        self.headers = {
            "User-Agent": settings.user_agent or "OSRS-Tool-Hub/1.0",
            "Accept": "text/html,application/xhtml+xml",
        }
        # Use canonical slot order from verification module
        self.slot_order = WIKI_GUIDE_SLOT_ORDER

    async def fetch_page(self, page_path: str) -> str:
        """
        Fetch a wiki page by its path.

        Args:
            page_path: Relative path to the wiki page (e.g., 'w/Guide:Ranged_Gear_Progression')

        Returns:
            HTML content of the page
        """
        url = f"{self.base_url}/{page_path}"
        logger.info(f"Fetching wiki page: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=30.0)
            response.raise_for_status()
            return response.text

    async def fetch_guide(self) -> GearGuide:
        """
        Fetch and parse a complete gear guide.

        Returns:
            Parsed GearGuide object with all sections
        """
        if not self.guide_page:
            raise ValueError("guide_page must be defined in subclass")

        html = await self.fetch_page(self.guide_page)
        soup = BeautifulSoup(html, "html.parser")

        guide = GearGuide(
            style=self.style,
            cost_per_hour_label=self.cost_per_hour_label,
            slot_order=self.slot_order.copy(),
        )

        # Parse game stages (sections)
        guide.game_stages = await self._parse_game_stages(soup)

        # Parse bonus table
        guide.bonus_table = await self._parse_bonus_table(soup)

        return guide

    @abstractmethod
    async def _parse_game_stages(self, soup: BeautifulSoup) -> list[GuideSection]:
        """
        Parse game stage sections from the page.

        Args:
            soup: BeautifulSoup parsed HTML

        Returns:
            List of parsed GuideSection objects
        """
        ...

    @abstractmethod
    async def _parse_bonus_table(self, soup: BeautifulSoup) -> list[BonusTableRow]:
        """
        Parse the bonus comparison table from the page.

        Args:
            soup: BeautifulSoup parsed HTML

        Returns:
            List of parsed BonusTableRow objects
        """
        ...

    def _parse_cost(self, cost_str: str) -> int | None:
        """
        Parse a cost string to integer.

        Handles formats like "1,234,567", "N/A", etc.

        Args:
            cost_str: String representation of cost

        Returns:
            Integer cost or None if invalid
        """
        if not cost_str or cost_str.upper() == "N/A":
            return None

        # Remove commas and whitespace
        cleaned = cost_str.replace(",", "").strip()

        try:
            return int(cleaned)
        except ValueError:
            return None

    def _create_slot_item(self, item_name: str | None) -> SlotItem | None:
        """
        Create a SlotItem from an item name.

        Args:
            item_name: Name of the item or None for empty slot

        Returns:
            SlotItem or None if item_name is empty
        """
        if not item_name or item_name.strip() == "":
            return None

        name = item_name.strip()

        # Check for icon override pattern (e.g., "Combat_bracelet" from display name)
        icon_override: str | None = None
        if "(" in name and ")" in name:
            # Extract potential icon name from parentheses
            paren_content = name[name.find("(") + 1 : name.find(")")]
            # Common icon override cases like (i), (u), (f)
            if paren_content in ["i", "u", "f"]:
                # Build icon name: remove parens and spaces
                icon_name = name.replace(f"({paren_content})", "").strip()
                icon_name = icon_name.replace(" ", "_")
                icon_override = icon_name

        return SlotItem(name=name, icon_override=icon_override)

    def _slots_to_dict(self, items: list[str | None]) -> dict[str, SlotItem | None]:
        """
        Convert a list of slot items to dictionary format.

        Args:
            items: List of item names in slot order

        Returns:
            Dictionary mapping slot names to SlotItem or None
        """
        result: dict[str, SlotItem | None] = {}
        for i, slot_name in enumerate(self.slot_order):
            if i < len(items):
                result[slot_name] = self._create_slot_item(items[i])
            else:
                result[slot_name] = None
        return result


class RangedGuideScraper(BaseWikiGuideScraper):
    """
    Scraper for Ranged Gear Progression guide.

    Parses the OSRS Wiki Guide:Ranged_Gear_Progression page.
    """

    style = "ranged"
    cost_per_hour_label = "Cost (Ammo, 1 hour, no pickup)"
    guide_page = "w/Guide:Ranged_Gear_Progression"

    async def _parse_game_stages(self, soup: BeautifulSoup) -> list[GuideSection]:
        """
        Parse game stage sections from the Ranged guide.

        Extracts tiers and content-specific equipment for each game stage.
        """
        sections: list[GuideSection] = []

        # Find all h3/h4 headings that indicate sections
        headings = soup.find_all(["h3", "h4"], recursive=True)

        current_section: GuideSection | None = None
        for heading in headings:
            heading_text = heading.get_text(strip=True)

            # Identify section by heading text
            if "Free-to-play" in heading_text:
                if current_section:
                    sections.append(current_section)
                current_section = GuideSection(
                    id="free_to_play",
                    title="Free-to-play",
                )
            elif "Mid Game" in heading_text:
                if current_section:
                    sections.append(current_section)
                current_section = GuideSection(
                    id="mid_game",
                    title="Mid Game / Members",
                )
            elif "Late Game" in heading_text:
                if current_section:
                    sections.append(current_section)
                current_section = GuideSection(
                    id="late_game",
                    title="Late Game / Bossing & Raiding",
                )
            elif "End Game" in heading_text:
                if current_section:
                    sections.append(current_section)
                current_section = GuideSection(
                    id="end_game",
                    title="End Game",
                )

            # Parse tiers from tables following headings
            if current_section:
                tier_data = await self._parse_tier_table(heading, current_section.id)
                if tier_data:
                    current_section.tiers.extend(tier_data)

                # Parse content-specific items
                content_data = await self._parse_content_specific_table(
                    heading, current_section.id
                )
                if content_data:
                    current_section.content_specific.extend(content_data)

        if current_section:
            sections.append(current_section)

        return sections

    async def _parse_tier_table(
        self, heading: Tag, section_id: str
    ) -> list[TierLoadout]:
        """
        Parse tier loadout tables following a heading.

        Args:
            heading: BeautifulSoup heading element
            section_id: ID of the current section

        Returns:
            List of parsed TierLoadout objects
        """
        tiers: list[TierLoadout] = []

        # Find the next table after the heading
        table = heading.find_next("table")

        if not table:
            return tiers

        rows = table.find_all("tr")

        for row in rows[1:]:  # Skip header row
            cells = row.find_all(["td", "th"])

            if len(cells) < 2:
                continue

            # Extract tier label (usually first cell)
            label_cell = cells[0].get_text(strip=True)

            # Skip empty rows or section headers
            if not label_cell or "Level" not in label_cell:
                continue

            # Extract cost (usually second cell)
            cost_text = cells[1].get_text(strip=True)
            total_cost = self._parse_cost(cost_text)

            # Create tier with empty slots (will be filled by detailed data)
            tier = TierLoadout(
                label=label_cell,
                total_cost=total_cost or 0,
                slots=self._slots_to_dict([None] * len(self.slot_order)),
            )

            tiers.append(tier)

        return tiers

    async def _parse_content_specific_table(
        self, heading: Tag, section_id: str
    ) -> list[ContentSpecificItem]:
        """
        Parse content-specific equipment tables.

        Args:
            heading: BeautifulSoup heading element
            section_id: ID of the current section

        Returns:
            List of parsed ContentSpecificItem objects
        """
        items: list[ContentSpecificItem] = []

        # Look for "Content specific equipment" heading
        heading_text = heading.get_text(strip=True)

        if "Content specific equipment" not in heading_text:
            # Check next sibling headings
            next_heading = heading.find_next_sibling(["h3", "h4"])
            if next_heading:
                next_text = next_heading.get_text(strip=True)
                if "Content specific equipment" not in next_text:
                    return items
                heading = next_heading  # type: ignore[assignment]

        # Find the table after the heading
        table = heading.find_next("table")

        if not table:
            return items

        rows = table.find_all("tr")

        for row in rows[1:]:  # Skip header row
            cells = row.find_all("td")

            if len(cells) < 3:
                continue

            # Parse content-specific item
            name = cells[0].get_text(strip=True)
            equipment = cells[1].get_text(strip=True) if len(cells) > 1 else None
            use_case = cells[2].get_text(strip=True) if len(cells) > 2 else None

            # Parse cost columns
            cost_buy: int | None = None
            cost_per_hour: int | None = None

            if len(cells) > 3:
                cost_buy = self._parse_cost(cells[3].get_text(strip=True))
            if len(cells) > 4:
                cost_per_hour = self._parse_cost(cells[4].get_text(strip=True))

            item = ContentSpecificItem(
                name=name,
                equipment=equipment if equipment else None,
                use_case=use_case if use_case else None,
                cost_buy=cost_buy,
                cost_per_hour=cost_per_hour,
            )

            items.append(item)

        return items

    async def _parse_bonus_table(self, soup: BeautifulSoup) -> list[BonusTableRow]:
        """
        Parse the bonus comparison table at the end of the guide.

        Args:
            soup: BeautifulSoup parsed HTML

        Returns:
            List of parsed BonusTableRow objects
        """
        rows: list[BonusTableRow] = []

        # Find "Ranged Strength bonus / Cost" or similar heading
        heading = soup.find("span", {"id": re.compile("Ranged", re.IGNORECASE)})
        if not heading:
            ranged_headings = soup.find_all(["h3", "h4"])
            for h in ranged_headings:
                text = h.get_text() or ""
                if "Ranged Strength" in text:
                    heading = h
                    break

        if not heading:
            # Try finding by table structure
            tables = soup.find_all("table")
            for table in tables:
                header_row = table.find("tr")
                if header_row:
                    headers = header_row.get_text().lower()
                    if "ranged strength" in headers or "bonus" in headers:
                        heading = table
                        break

        if not heading:
            return rows

        table: Tag | None
        if hasattr(heading, "find_all"):
            table = heading  # type: ignore[assignment]
        else:
            table = heading.find_next("table")

        if not table:
            return rows

        table_rows = table.find_all("tr")

        for row in table_rows[1:]:  # Skip header
            cells = row.find_all("td")

            if len(cells) < 2:
                continue

            item_name = cells[0].get_text(strip=True)
            bonus = cells[1].get_text(strip=True) if len(cells) > 1 else ""

            # Skip empty rows
            if not item_name or not bonus:
                continue

            cost: int | None = None
            delta = ""
            cost_per_delta = ""

            if len(cells) > 2:
                cost = self._parse_cost(cells[2].get_text(strip=True))
            if len(cells) > 3:
                delta = cells[3].get_text(strip=True)
            if len(cells) > 4:
                cost_per_delta = cells[4].get_text(strip=True)

            row_obj = BonusTableRow(
                item=item_name,
                bonus=bonus,
                cost=cost,
                delta=delta,
                cost_per_delta=cost_per_delta,
            )

            rows.append(row_obj)

        return rows


class MeleeGuideScraper(BaseWikiGuideScraper):
    """
    Scraper for Melee Gear Progression guide.

    Parses the OSRS Wiki Guide:Melee_Gear_Progression page.
    """

    style = "melee"
    cost_per_hour_label = "Cost (Upkeep, 1 Hour)"
    guide_page = "w/Guide:Melee_Gear_Progression"

    async def _parse_game_stages(self, soup: BeautifulSoup) -> list[GuideSection]:
        """Parse melee game stages - delegates to parent implementation pattern."""
        # TODO: Implement melee-specific parsing
        return []

    async def _parse_bonus_table(self, soup: BeautifulSoup) -> list[BonusTableRow]:
        """Parse melee bonus table - delegates to parent implementation pattern."""
        # TODO: Implement melee-specific bonus parsing
        return []


class MagicGuideScraper(BaseWikiGuideScraper):
    """
    Scraper for Magic Gear Progression guide.

    Parses the OSRS Wiki Guide:Magic_Gear_Progression page.
    """

    style = "magic"
    cost_per_hour_label = "Cost (Runes, 1 Hour)"
    guide_page = "w/Guide:Magic_Gear_Progression"

    async def _parse_game_stages(self, soup: BeautifulSoup) -> list[GuideSection]:
        """Parse magic game stages - delegates to parent implementation pattern."""
        # TODO: Implement magic-specific parsing
        return []

    async def _parse_bonus_table(self, soup: BeautifulSoup) -> list[BonusTableRow]:
        """Parse magic bonus table - delegates to parent implementation pattern."""
        # TODO: Implement magic-specific bonus parsing
        return []


# Convenience function for quick scraping
async def scrape_ranged_guide() -> GearGuide:
    """
    Quick function to scrape the Ranged Gear Progression guide.

    Returns:
        Parsed GearGuide object
    """
    scraper = RangedGuideScraper()
    return await scraper.fetch_guide()


async def scrape_all_guides() -> dict[str, GearGuide]:
    """
    Scrape all gear progression guides.

    Returns:
        Dictionary mapping style names to parsed GearGuide objects
    """
    guides: dict[str, GearGuide] = {}

    # Scrape guides concurrently
    tasks = [scrape_ranged_guide()]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, GearGuide):
            guides[result.style] = result

    return guides


def guide_to_json(guide: GearGuide) -> dict[str, Any]:
    """
    Convert a GearGuide to JSON-serializable dictionary.

    Args:
        guide: GearGuide object to convert

    Returns:
        Dictionary suitable for JSON serialization
    """
    return {
        "style": guide.style,
        "cost_per_hour_label": guide.cost_per_hour_label,
        "slot_order": guide.slot_order,
        "game_stages": [
            {
                "id": section.id,
                "title": section.title,
                "tiers": [
                    {
                        "label": tier.label,
                        "total_cost": tier.total_cost,
                        "slots": {
                            slot: (item.name if item else None)
                            for slot, item in tier.slots.items()
                        },
                    }
                    for tier in section.tiers
                ],
                "content_specific": [
                    {
                        "name": item.name,
                        "equipment": item.equipment,
                        "use_case": item.use_case,
                        "cost_buy": item.cost_buy,
                        "cost_per_hour": item.cost_per_hour,
                    }
                    for item in section.content_specific
                ],
            }
            for section in guide.game_stages
        ],
        "bonus_table": [
            {
                "item": row.item,
                "bonus": row.bonus,
                "cost": row.cost,
                "delta": row.delta,
                "cost_per_delta": row.cost_per_delta,
            }
            for row in guide.bonus_table
        ],
    }
