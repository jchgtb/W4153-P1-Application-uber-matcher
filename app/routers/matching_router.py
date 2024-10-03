from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.matching_service import MatchingService
from app.utils.dependencies import get_db

router = APIRouter()


@router.post("/match", tags=["matching"])
def match_user(user_id: int, db: Session = Depends(get_db)):
    matching_service = MatchingService(db)
    match = matching_service.find_and_save_match(user_id)

    if not match:
        raise HTTPException(status_code=404, detail="No match found")

    return {"match": match}
