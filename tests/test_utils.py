import unittest
from app.utils import get_health_advice, find_nearby_hospitals

class UtilsTestCase(unittest.TestCase):
    def test_get_health_advice(self):
        """
        Test the get_health_advice function.
        """
        advice = get_health_advice("Dummy Diagnosis")
        self.assertIsInstance(advice, dict)
        self.assertIn("advice", advice)
        self.assertIn("source", advice)

    def test_find_nearby_hospitals(self):
        """
        Test the find_nearby_hospitals function.
        """
        hospitals = find_nearby_hospitals("Dummy Location")
        self.assertIsInstance(hospitals, list)
        self.assertTrue(all(isinstance(hospital, dict) for hospital in hospitals))
        self.assertTrue(all("name" in hospital and "address" in hospital and "distance" in hospital for hospital in hospitals))

    # Add more tests for utils.py if needed
