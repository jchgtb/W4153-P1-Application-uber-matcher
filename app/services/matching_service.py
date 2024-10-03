import requests
from sqlalchemy.orm import Session
from app.repository.match_repository import MatchRepository
from datetime import datetime

class MatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.match_repository = MatchRepository(db)

    def find_and_save_match(self, user1_id: int):
        current_flight = self.get_flight_by_user_id(user1_id)
        if not current_flight:
            return None

        nearby_flights = self.get_nearby_flights(current_flight["flight_id"])

        if not nearby_flights:
            return None

        nearest_flight = self.find_nearest_flight(current_flight, nearby_flights)

        if nearest_flight:
            return self.match_repository.create_match(user1_id, nearest_flight["user_id"])
        return None

    def get_flight_by_user_id(self, user1_id: int):

        url = f"http://127.0.0.1:8000/flights/{user1_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch flight data for user {user1_id}: {e}")
            return None

    def get_nearby_flights(self, flight_id: int):
        url = "http://127.0.0.1:8000/flights/nearby"
        try:
            response = requests.post(url, json={"flight_id": flight_id})
            response.raise_for_status()
            return response.json().get("nearby_flights", [])
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch nearby flights for flight {flight_id}: {e}")
            return None

    def find_nearest_flight(self, current_flight, nearby_flights):
        current_flight_datetime = datetime.combine(
            datetime.strptime(current_flight["flight_date"], "%Y-%m-%d").date(),
            datetime.strptime(current_flight["flight_time"], "%H:%M:%S").time()
        )

        nearest_flight = min(nearby_flights, key=lambda f: abs(
            (datetime.combine(
                datetime.strptime(f["flight_date"], "%Y-%m-%d").date(),
                datetime.strptime(f["flight_time"], "%H:%M:%S").time()
            ) - current_flight_datetime).total_seconds()
        ))

        return nearest_flight
