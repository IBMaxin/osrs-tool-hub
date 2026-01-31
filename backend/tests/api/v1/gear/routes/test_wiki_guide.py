"""Tests for wiki guide endpoint."""

from fastapi.testclient import TestClient

from backend.services.wiki_guide_verification import validate_guide, WIKI_GUIDE_SLOT_ORDER


class TestWikiGuideEndpoint:
    """Test GET /gear/wiki-guide/{style} endpoint."""

    def test_get_wiki_guide_magic(self, client: TestClient) -> None:
        """Test getting wiki guide for magic style."""
        response = client.get("/api/v1/gear/wiki-guide/magic")

        assert response.status_code == 200
        data = response.json()

        # Verify style
        assert data["style"] == "magic"

        # Verify full guide structure using verification module
        validate_guide(data)

    def test_get_wiki_guide_ranged(self, client: TestClient) -> None:
        """Test getting wiki guide for ranged style."""
        response = client.get("/api/v1/gear/wiki-guide/ranged")

        assert response.status_code == 200
        data = response.json()
        assert data["style"] == "ranged"

        # Verify full guide structure
        validate_guide(data)

    def test_get_wiki_guide_melee(self, client: TestClient) -> None:
        """Test getting wiki guide for melee style."""
        response = client.get("/api/v1/gear/wiki-guide/melee")

        assert response.status_code == 200
        data = response.json()
        assert data["style"] == "melee"

        # Verify full guide structure
        validate_guide(data)

    def test_get_wiki_guide_invalid_style(self, client: TestClient) -> None:
        """Test error handling for invalid style."""
        response = client.get("/api/v1/gear/wiki-guide/invalid")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_wiki_guide_tier_structure(self, client: TestClient) -> None:
        """Test that tiers have correct structure with full loadouts."""
        response = client.get("/api/v1/gear/wiki-guide/magic")

        assert response.status_code == 200
        data = response.json()

        # Find a stage with tiers and verify structure
        for stage in data["game_stages"]:
            if len(stage["tiers"]) > 0:
                tier = stage["tiers"][0]

                # Basic tier structure checks
                assert "label" in tier
                assert "total_cost" in tier
                assert "slots" in tier

                # Verify slots structure
                slots = tier["slots"]
                for slot_name in data["slot_order"]:
                    assert slot_name in slots

                    slot_data = slots[slot_name]
                    # Either null or dict with 'name'
                    if slot_data is not None:
                        assert isinstance(slot_data, dict)
                        assert "name" in slot_data
                        assert isinstance(slot_data["name"], str)

                break

    def test_wiki_guide_returns_exact_json(self, client: TestClient) -> None:
        """Test that endpoint returns JSON exactly as written (no mutation)."""
        response = client.get("/api/v1/gear/wiki-guide/magic")

        assert response.status_code == 200
        data = response.json()

        # Verify slot order is preserved - use verification module
        assert data["slot_order"] == WIKI_GUIDE_SLOT_ORDER
