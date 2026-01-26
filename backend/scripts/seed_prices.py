"""Script to manually seed/update prices from Wiki API."""
import asyncio
from sqlmodel import Session
from backend.database import engine
from backend.services.wiki_client import WikiAPIClient

async def seed_prices():
    client = WikiAPIClient()
    print("Connecting to Wiki API...")
    
    with Session(engine) as session:
        print("1. Syncing Item Mapping...")
        await client.sync_items_to_db(session)
        
        print("2. Syncing Latest Prices...")
        await client.sync_prices_to_db(session)
        
    print("✅ Price Sync Complete!")

if __name__ == "__main__":
    asyncio.run(seed_prices())
