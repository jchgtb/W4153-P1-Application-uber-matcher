from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.matching_service import MatchingService
from app.utils.dependencies import get_db
from app.models.match_request import MatchRequest

router = APIRouter()


@router.post("/match", tags=["matching"])
def match_user(match_request: MatchRequest, db: Session = Depends(get_db)):
    user_id = match_request.user_id
    matching_service = MatchingService(db)
    match = matching_service.find_and_save_match(user_id)

    if not match:
        raise HTTPException(status_code=404, detail="No match found")

    return {"match": match}
