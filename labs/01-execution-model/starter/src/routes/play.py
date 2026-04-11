from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.schemas.quiz import PlayerAnswer
from src.services import quiz_service

router = APIRouter(prefix="/quizzes", tags=["play"])

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


@router.get("/{quiz_id}/play", response_class=HTMLResponse)
def play_page(request: Request, quiz_id: int):
    quiz = quiz_service.get_quiz(quiz_id)
    return templates.TemplateResponse(
        "play.html", {"request": request, "quiz": quiz}
    )


@router.get("/{quiz_id}/join", response_class=HTMLResponse)
def join_page(request: Request, quiz_id: int):
    quiz = quiz_service.get_quiz(quiz_id)
    return templates.TemplateResponse(
        "join.html", {"request": request, "quiz": quiz}
    )


@router.post("/{quiz_id}/answer")
def submit_answer(quiz_id: int, question_id: int, body: PlayerAnswer):
    # BUG 5: comparing str(quiz_id) to int — always falls through to NotFoundError
    if str(quiz_id) not in quiz_service._quizzes:
        from src.errors import NotFoundError
        raise NotFoundError("quiz", quiz_id)
    return quiz_service.submit_answer(
        quiz_id, question_id, body.player_name, body.selected_index
    )
