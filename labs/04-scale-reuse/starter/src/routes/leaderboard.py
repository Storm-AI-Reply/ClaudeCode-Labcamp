from fastapi import APIRouter

from src.services import quiz_service

router = APIRouter(prefix="/quizzes", tags=["leaderboard"])


@router.get("/{quiz_id}/scores")
def get_scores(quiz_id: int):
    return quiz_service.get_scores(quiz_id)
