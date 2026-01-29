#!/usr/bin/env python
"""Script to extract WIKI_PROGRESSION data from wiki_data.py to JSON files.

Run this once to complete the migration from Python dict to JSON files.

Usage:
    python scripts/migrate_wiki_data_to_json.py
"""
import json
import sys
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from backend.services.wiki_data import WIKI_PROGRESSION
except ImportError as e:
    print(f"❌ Error: Could not import WIKI_PROGRESSION: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)

# Define output directory
DATA_DIR = Path(__file__).parent.parent / "backend" / "data" / "wiki_progression"


def migrate():
    """Extract progression data from Python dict to JSON files."""
    print("🚀 Starting wiki progression data migration...\n")

    # Ensure directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    total_size = 0

    for style, data in WIKI_PROGRESSION.items():
        output_file = DATA_DIR / f"{style}.json"

        # Write JSON with pretty formatting
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        file_size = output_file.stat().st_size
        total_size += file_size

        print(f"✅ Created {output_file.name}")
        print(f"   Size: {file_size:,} bytes")
        print(f"   Slots: {len(data)} equipment slots")
        print()

    print("\n✅ Migration complete!")
    print(f"📁 Data files created in: {DATA_DIR}")
    print(f"💾 Total size: {total_size:,} bytes ({total_size / 1024:.1f} KB)")
    print("\n📝 Next steps:")
    print("1. Review the generated JSON files")
    print("2. Run: git add backend/data/wiki_progression/*.json")
    print("3. The wiki_data.py loader will automatically use these files")
    print("4. Run tests: poetry run pytest")
    print("5. If tests pass, commit the changes")


if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
