from sqlalchemy import CheckConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.stockpilot.database import Base


class StockLevel(Base):
    """Store the current stock state for one store-item pair."""

    __tablename__ = "stock_levels"

    __table_args__ = (
        CheckConstraint(
            "current_stock >= 0",
            name="check_current_stock_non_negative",
        ),
        CheckConstraint(
            "incoming_stock >= 0",
            name="check_incoming_stock_non_negative",
        ),
        CheckConstraint(
            "safety_stock >= 0",
            name="check_safety_stock_non_negative",
        ),
    )

    store_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    item_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    current_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    incoming_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    safety_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )