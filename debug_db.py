from sqlmodel import Session, select
from backend.database import engine
from backend.models import Item, PriceSnapshot

with Session(engine) as session:
    item_count = session.exec(select(Item)).all()
    price_count = session.exec(select(PriceSnapshot)).all()
    print(f"Items in DB: {len(item_count)}")
    print(f"Prices in DB: {len(price_count)}")

    # Show a few sample items if they exist
    if item_count:
        print("\nSample items (first 3):")
        for item in item_count[:3]:
            print(f"  - {item.name} (ID: {item.id}, Limit: {item.limit})")

    # Show a few sample prices if they exist
    if price_count:
        print("\nSample prices (first 3):")
        for price in price_count[:3]:
            print(f"  - Item ID: {price.item_id}, Low: {price.low_price}, High: {price.high_price}")
