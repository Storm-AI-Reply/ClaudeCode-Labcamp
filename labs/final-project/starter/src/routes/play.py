import base64
import io
from pathlib import Path

import qrcode
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

    play_url = str(request.url_for("play_page", quiz_id=quiz_id))
    img = qrcode.make(play_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_data_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return templates.TemplateResponse(
        "join.html", {"request": request, "quiz": quiz, "qr_data_uri": qr_data_uri}
    )


@router.post("/{quiz_id}/answer")
def submit_answer(quiz_id: int, question_id: int, body: PlayerAnswer):
    return quiz_service.submit_answer(
        quiz_id, question_id, body.player_name, body.selected_index
    )
