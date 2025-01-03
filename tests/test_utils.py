import unittest
from unittest.mock import patch
from app.utils import get_health_advice, find_nearby_hospitals, Database, ExternalAPI

class TestUtils(unittest.TestCase):

    @patch.object(Database, 'get_advice')
    def test_get_health_advice_success(self, mock_get_advice):
        """
        Test get_health_advice function when a valid diagnosis is provided.
        """
        # Mock the database response
        mock_get_advice.return_value = {"advice": "Drink plenty of fluids and rest.", "source": "WHO"}

        # Call the function with a dummy diagnosis
        advice = get_health_advice("Dummy Diagnosis")

        # Assert that the database method was called with the correct diagnosis
        mock_get_advice.assert_called_once_with("Dummy Diagnosis")

        # Assert that the function returns the expected advice
        self.assertEqual(advice, {"advice": "Drink plenty of fluids and rest.", "source": "WHO"})

    @patch.object(Database, 'get_advice')
    def test_get_health_advice_not_found(self, mock_get_advice):
        """
        Test get_health_advice function when an invalid diagnosis is provided.
        """
        # Mock the database response to return None (no advice found)
        mock_get_advice.return_value = None

        # Call the function with a dummy diagnosis
        advice = get_health_advice("Invalid Diagnosis")

        # Assert that the database method was called with the correct diagnosis
        mock_get_advice.assert_called_once_with("Invalid Diagnosis")

        # Assert that the function returns None
        self.assertIsNone(advice)

    @patch.object(ExternalAPI, 'find_nearby_hospitals')
    @patch.object(Database, 'find_hospitals')
    def test_find_nearby_hospitals_success(self, mock_find_hospitals_db, mock_find_hospitals_api):
        """
        Test find_nearby_hospitals function when valid location is provided.
        """
        # Mock the database response
        mock_find_hospitals_db.return_value = []

        # Mock the API response
        mock_find_hospitals_api.return_value = [
            {"name": "Hospital A", "address": "123 Main St", "latitude": 34.0522, "longitude": -118.2437, "place_id": "ChIJ2eUgeAK6j4ARbn5u_wAGqWA"},
            {"name": "Hospital B", "address": "456 Oak Ave", "latitude": 34.0532, "longitude": -118.2447, "place_id": "ChIJ2eUgeAK6j4ARbn5u_wAGqWB"}
        ]

        # Call the function with a dummy location
        hospitals = find_nearby_hospitals("34.0522,-118.2437")

        # Assert that the database and API methods were called with the correct location
        mock_find_hospitals_db.assert_called_once_with(34.0522, -118.2437)
        mock_find_hospitals_api.assert_called_once_with(34.0522, -118.2437)

        # Assert that the function returns the expected list of hospitals
        self.assertEqual(len(hospitals), 2)
        self.assertEqual(hospitals[0]["name"], "Hospital A")
        self.assertEqual(hospitals[1]["name"], "Hospital B")

    @patch.object(ExternalAPI, 'find_nearby_hospitals')
    @patch.object(Database, 'find_hospitals')
    def test_find_nearby_hospitals_invalid_location(self, mock_find_hospitals_db, mock_find_hospitals_api):
        """
        Test find_nearby_hospitals function when invalid location is provided.
        """
        # Call the function with an invalid location format
        hospitals = find_nearby_hospitals("invalid_location")

        # Assert that neither the database nor the API methods were called
        mock_find_hospitals_db.assert_not_called()
        mock_find_hospitals_api.assert_not_called()

        # Assert that the function returns an empty list
        self.assertEqual(hospitals, [])

if __name__ == '__main__':
    unittest.main()
