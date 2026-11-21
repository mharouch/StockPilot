import unittest

from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError

from src.stockpilot.database import (
    create_session_factory,
    initialize_database,
)
from src.stockpilot.models import StockLevel
from src.stockpilot.stock_repository import (
    get_stock_level,
    save_stock_level,
)


class TestStockLevelPersistence(unittest.TestCase):
    def setUp(self):
        self.engine = initialize_database(
            "sqlite:///:memory:"
        )
        self.Session = create_session_factory(self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_creates_stock_levels_table(self):
        table_names = inspect(self.engine).get_table_names()

        self.assertIn("stock_levels", table_names)

    def test_saves_and_reads_stock_level(self):
        with self.Session() as session:
            save_stock_level(
                session=session,
                store_id=1,
                item_id=15,
                current_stock=40,
                incoming_stock=20,
                safety_stock=10,
            )
            session.commit()

        with self.Session() as session:
            saved_stock_level = get_stock_level(
                session,
                store_id=1,
                item_id=15,
            )

            self.assertIsNotNone(saved_stock_level)
            self.assertEqual(saved_stock_level.store_id, 1)
            self.assertEqual(saved_stock_level.item_id, 15)
            self.assertEqual(saved_stock_level.current_stock, 40)
            self.assertEqual(saved_stock_level.incoming_stock, 20)
            self.assertEqual(saved_stock_level.safety_stock, 10)

    def test_updates_existing_stock_level(self):
        with self.Session() as session:
            save_stock_level(
                session=session,
                store_id=1,
                item_id=15,
                current_stock=40,
            )
            session.commit()

            save_stock_level(
                session=session,
                store_id=1,
                item_id=15,
                current_stock=55,
                incoming_stock=10,
                safety_stock=8,
            )
            session.commit()

            stock_levels = session.scalars(
                select(StockLevel)
            ).all()

            self.assertEqual(len(stock_levels), 1)
            self.assertEqual(stock_levels[0].current_stock, 55)
            self.assertEqual(stock_levels[0].incoming_stock, 10)
            self.assertEqual(stock_levels[0].safety_stock, 8)

    def test_save_rejects_negative_stock(self):
        with self.Session() as session:
            with self.assertRaisesRegex(
                ValueError,
                "Stock quantities must be non-negative.",
            ):
                save_stock_level(
                    session=session,
                    store_id=1,
                    item_id=15,
                    current_stock=-1,
                )

    def test_database_rejects_negative_stock(self):
        invalid_stock_level = StockLevel(
            store_id=1,
            item_id=15,
            current_stock=-1,
            incoming_stock=0,
            safety_stock=0,
        )

        with self.Session() as session:
            session.add(invalid_stock_level)

            with self.assertRaises(IntegrityError):
                session.commit()
