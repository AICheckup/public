import os
import psycopg2
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    """
    Handles database operations.
    """
    def __init__(self):
        """
        Initializes the database connection.
        """
        self.conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD")
        )
        self.cur = self.conn.cursor()

    def get_advice(self, diagnosis):
        """
        Retrieves health advice based on the diagnosis from the database.

        Args:
            diagnosis (str): The diagnosis.

        Returns:
            dict: Health advice and its source, or None if not found.
        """
        try:
            self.cur.execute("SELECT advice, source FROM health_advice WHERE diagnosis = %s", (diagnosis,))
            result = self.cur.fetchone()
            if result:
                return {"advice": result[0], "source": result[1]}
            else:
                return None
        except Exception as e:
            print(f"Error retrieving health advice: {e}")
            return None

    def find_hospitals(self, latitude, longitude):
        """
        Finds nearby medical institutions based on the location.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            list: List of nearby medical institutions, or an empty list if none found or an error occurred.
        """
        # This is a placeholder for a more complex query that might involve
        # calculating distances and filtering based on proximity.
        # For now, it just returns a list of all hospitals in the database.
        try:
            self.cur.execute("SELECT name, address, latitude, longitude FROM hospitals")
            results = self.cur.fetchall()
            hospitals = []
            for result in results:
                hospitals.append({
                    "name": result[0],
                    "address": result[1],
                    "latitude": result[2],
                    "longitude": result[3],
                    # In a real application, you'd calculate the distance
                    "distance": 0  # Placeholder for distance calculation
                })
            return hospitals
        except Exception as e:
            print(f"Error retrieving hospitals: {e}")
            return []

    def close(self):
        """
        Closes the database connection.
        """
        self.cur.close()
        self.conn.close()

class ExternalAPI:
    """
    Handles interactions with external APIs.
    """
    def __init__(self):
        """
        Initializes the API client.
        """
        self.api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

    def get_geocode(self, address):
        """
        Converts an address to geographic coordinates using Google Geocoding API.

        Args:
            address (str): The address to geocode.

        Returns:
            tuple: Latitude and longitude of the address, or None if an error occurred.
        """
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print(f"Geocoding API error: {data['status']}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error during Geocoding API request: {e}")
            return None
        

    def find_nearby_hospitals(self, latitude, longitude, radius=5000):
        """
        Finds nearby hospitals using Google Places API.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            radius (int): The search radius in meters.

        Returns:
            list: List of nearby hospitals, or an empty list if none found or an error occurred.
        """
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=hospital&key={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'OK':
                hospitals = []
                for result in data['results']:
                    hospitals.append({
                        "name": result['name'],
                        "address": result['vicinity'],
                        "latitude": result['geometry']['location']['lat'],
                        "longitude": result['geometry']['location']['lng'],
                        "place_id": result['place_id']
                    })
                return hospitals
            else:
                print(f"Places API error: {data['status']}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error during Places API request: {e}")
            return []

# Instantiate the database and API
db = Database()
api = ExternalAPI()

def get_health_advice(diagnosis):
    """
    Gets health advice based on the diagnosis.

    Args:
        diagnosis (str): The diagnosis.

    Returns:
        dict: Health advice from the database or a dummy advice.
    """
    return db.get_advice(diagnosis)

def find_nearby_hospitals(location):
    """
    Finds nearby medical institutions based on the location.

    Args:
        location (str): The location (latitude,longitude).

    Returns:
        list: List of nearby medical institutions from
