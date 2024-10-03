from sqlalchemy.orm import Session
from app.models.match_entity import Match

class MatchRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_match(self, user1_id: int, user2_id: int):
        match = Match(
            user1_id=user1_id,
            user2_id=user2_id,
            user1_status="PENDING",
            user2_status="PENDING"
        )
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match
