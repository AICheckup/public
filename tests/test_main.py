import unittest
from app.main import create_app

class MainTestCase(unittest.TestCase):
    def setUp(self):
        """
        Setup before each test.
        """
        self.app = create_app()
        self.client = self.app.test_client()

    def test_index_route(self):
        """
        Test the index route.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Welcome to AI Checkup!")

    # Add more tests for main.py if needed
