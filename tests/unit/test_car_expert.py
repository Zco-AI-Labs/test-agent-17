import unittest
from unittest.mock import MagicMock
from app.core import hubscape_adk
from app.scripts.compare_cars import compare_cars
from app.scripts.get_car_recommendations import get_car_recommendations
from app.scripts.save_hub_vehicle import save_hub_vehicle
from app.scripts.list_hub_vehicles import list_hub_vehicles
from app.scripts.delete_hub_vehicle import delete_hub_vehicle

class TestCarExpert(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_tool_context_with_hub = hubscape_adk.RemoteContext(
            user_id="user_123",
            agent_id="car_expert_agent",
            org_id="org_456",
            hub_id="hub_456"
        )
        self.mock_tool_context_with_hub.auth.name = "Test User"
        self.mock_db = MagicMock()
        self.mock_tool_context_with_hub._db = self.mock_db

        self.mock_tool_context_no_hub = hubscape_adk.RemoteContext(
            user_id="user_123",
            agent_id="car_expert_agent",
            hub_id=None
        )
        self.mock_tool_context_no_hub.auth.name = "Test User"

    async def test_compare_cars_two_vehicles(self):
        res = await compare_cars(self.mock_tool_context_no_hub, "Toyota Camry", "Honda Accord")
        self.assertEqual(res["action"], "compare_cars")
        self.assertIn("Toyota Camry", res["vehicles"])
        self.assertIn("Honda Accord", res["vehicles"])
        self.assertEqual(len(res["vehicles"]), 2)
        self.assertEqual(res["widget"], "car_comparison_card")

    async def test_compare_cars_three_vehicles(self):
        res = await compare_cars(self.mock_tool_context_no_hub, "Toyota Camry", "Honda Accord", "Mazda 6")
        self.assertEqual(len(res["vehicles"]), 3)
        self.assertIn("Mazda 6", res["vehicles"])

    async def test_get_car_recommendations(self):
        res = await get_car_recommendations(
            self.mock_tool_context_no_hub,
            budget=30000,
            use_case="family",
            fuel_type="hybrid"
        )
        self.assertEqual(res["action"], "get_car_recommendations")
        self.assertEqual(res["budget"], 30000)
        self.assertEqual(res["use_case"], "family")
        self.assertEqual(res["fuel_type"], "hybrid")
        self.assertEqual(res["widget"], "car_recommendations_card")

    async def test_save_hub_vehicle_success(self):
        mock_doc_ref = MagicMock()
        self.mock_db.document.return_value = mock_doc_ref
        
        mock_snap = MagicMock()
        mock_snap.exists = False
        mock_doc_ref.get.return_value = mock_snap

        res = await save_hub_vehicle(
            self.mock_tool_context_with_hub,
            make="Ford",
            model="Explorer",
            year=2023,
            notes="Leased"
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["doc_id"], "ford_explorer_2023")
        self.mock_db.document.assert_called_with("organizations/org_456/hubs/hub_456/agent_data/car_expert_agent/hub_garage/ford_explorer_2023")
        mock_doc_ref.set.assert_called_once()

    async def test_save_hub_vehicle_no_hub(self):
        res = await save_hub_vehicle(
            self.mock_tool_context_no_hub,
            make="Ford",
            model="Explorer",
            year=2023
        )
        self.assertFalse(res["success"])
        self.assertIn("No hub context", res["error"])

    async def test_list_hub_vehicles(self):
        mock_col_ref = MagicMock()
        self.mock_db.collection.return_value = mock_col_ref
        mock_doc = MagicMock()
        mock_doc.to_dict.return_value = {"make": "Ford", "model": "Explorer", "year": 2023}
        mock_doc.id = "ford_explorer_2023"
        mock_col_ref.stream.return_value = [mock_doc]

        res = await list_hub_vehicles(self.mock_tool_context_with_hub)
        self.assertTrue(res["success"])
        self.assertEqual(len(res["vehicles"]), 1)
        self.assertEqual(res["vehicles"][0]["make"], "Ford")
        self.assertEqual(res["widget"], "hub_garage_card")

    async def test_delete_hub_vehicle(self):
        mock_doc_ref = MagicMock()
        self.mock_db.document.return_value = mock_doc_ref

        res = await delete_hub_vehicle(self.mock_tool_context_with_hub, "ford_explorer_2023")
        self.assertTrue(res["success"])
        mock_doc_ref.delete.assert_called_once()
