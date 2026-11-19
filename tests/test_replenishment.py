import unittest

import pandas as pd

from src.stockpilot.replenishment import (
    calculate_order_quantity,
    create_replenishment_recommendations,
)


class TestCalculateOrderQuantity(unittest.TestCase):
    def test_calculates_required_order_quantity(self):
        order_quantity = calculate_order_quantity(
            forecast_demand=100,
            current_stock=30,
            incoming_stock=20,
            safety_stock=10,
        )

        self.assertEqual(order_quantity, 60)

    def test_returns_zero_when_available_stock_is_sufficient(self):
        order_quantity = calculate_order_quantity(
            forecast_demand=50,
            current_stock=60,
            incoming_stock=10,
            safety_stock=5,
        )

        self.assertEqual(order_quantity, 0)

    def test_rounds_fractional_quantity_up(self):
        order_quantity = calculate_order_quantity(
            forecast_demand=10.2,
            current_stock=3,
            incoming_stock=2,
            safety_stock=1,
        )

        self.assertEqual(order_quantity, 7)

    def test_rejects_negative_values(self):
        invalid_inputs = [
            (-1, 10, 5, 2),
            (10, -1, 5, 2),
            (10, 5, -1, 2),
            (10, 5, 2, -1),
        ]

        for inputs in invalid_inputs:
            with self.subTest(inputs=inputs):
                with self.assertRaises(ValueError):
                    calculate_order_quantity(*inputs)


class TestCreateReplenishmentRecommendations(unittest.TestCase):
    def test_creates_recommendations_by_store_and_item(self):
        forecast = pd.DataFrame(
            {
                "store": [1, 1, 1, 1, 2, 2],
                "item": [1, 1, 2, 2, 1, 1],
                "prediction": [5.2, 6.1, 3.0, 4.0, 2.0, 3.0],
            }
        )

        stock = pd.DataFrame(
            {
                "store": [1, 1, 2],
                "item": [1, 2, 1],
                "current_stock": [3, 10, 1],
                "incoming_stock": [2, 0, 1],
                "safety_stock": [1, 2, 0],
            }
        )

        recommendations = create_replenishment_recommendations(
            forecast,
            stock,
        )

        expected = pd.DataFrame(
            {
                "store": [1, 1, 2],
                "item": [1, 2, 1],
                "forecast_demand": [11.3, 7.0, 5.0],
                "current_stock": [3, 10, 1],
                "incoming_stock": [2, 0, 1],
                "safety_stock": [1, 2, 0],
                "order_quantity": [8, 0, 3],
            }
        )

        pd.testing.assert_frame_equal(
            recommendations,
            expected,
        )

    def test_rejects_forecast_without_matching_stock(self):
        forecast = pd.DataFrame(
            {
                "store": [1],
                "item": [1],
                "prediction": [5.0],
            }
        )

        stock = pd.DataFrame(
            {
                "store": [2],
                "item": [1],
                "current_stock": [3],
                "incoming_stock": [0],
                "safety_stock": [1],
            }
        )

        with self.assertRaisesRegex(
            ValueError,
            "Missing stock data",
        ):
            create_replenishment_recommendations(
                forecast,
                stock,
            )