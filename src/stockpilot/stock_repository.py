from src.stockpilot.models import StockLevel


def get_stock_level(session, store_id, item_id):
    """Return the stock level for one store-item pair."""
    return session.get(
        StockLevel,
        (store_id, item_id),
    )


def save_stock_level(
    session,
    store_id,
    item_id,
    current_stock,
    incoming_stock=0,
    safety_stock=0,
):
    """Create or update the stock level for one store-item pair."""
    if (
        current_stock < 0
        or incoming_stock < 0
        or safety_stock < 0
    ):
        raise ValueError("Stock quantities must be non-negative.")

    stock_level = get_stock_level(
        session,
        store_id,
        item_id,
    )

    if stock_level is None:
        stock_level = StockLevel(
            store_id=store_id,
            item_id=item_id,
            current_stock=current_stock,
            incoming_stock=incoming_stock,
            safety_stock=safety_stock,
        )
        session.add(stock_level)
    else:
        stock_level.current_stock = current_stock
        stock_level.incoming_stock = incoming_stock
        stock_level.safety_stock = safety_stock

    session.flush()

    return stock_level
