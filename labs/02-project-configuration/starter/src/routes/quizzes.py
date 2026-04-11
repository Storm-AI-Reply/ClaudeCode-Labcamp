from fastapi import APIRouter, status

from src.schemas.quiz import (
    QuestionCreate,
    QuestionRead,
    QuizCreate,
    QuizRead,
)
from src.services import quiz_service

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.get("", response_model=list[QuizRead])
def list_quizzes():
    return quiz_service.list_quizzes()


@router.post("", response_model=QuizRead, status_code=status.HTTP_201_CREATED)
def create_quiz(body: QuizCreate):
    return quiz_service.create_quiz(body)


@router.get("/{quiz_id}")
def get_quiz(quiz_id: int):
    return quiz_service.get_quiz(quiz_id)


@router.patch("/{quiz_id}/status", response_model=QuizRead)
def patch_status(quiz_id: int, body: dict):
    return quiz_service.set_status(quiz_id, body.get("status", ""))


@router.post(
    "/{quiz_id}/questions",
    response_model=QuestionRead,
    status_code=status.HTTP_201_CREATED,
)
def add_question(quiz_id: int, body: QuestionCreate):
    return quiz_service.add_question(quiz_id, body)
