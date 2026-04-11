"""In-memory quiz store. Not thread-safe — fine for a workshop app."""
from datetime import datetime, timezone

from src.errors import NotFoundError
from src.schemas.quiz import (
    QuestionCreate,
    QuestionRead,
    QuizCreate,
    QuizRead,
)

_quizzes: dict[int, dict] = {}
_questions: dict[int, list[dict]] = {}
_scores: dict[int, dict[str, int]] = {}

_quiz_seq = 0
_question_seq = 0


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def reset() -> None:
    global _quiz_seq, _question_seq
    _quizzes.clear()
    _questions.clear()
    _scores.clear()
    _quiz_seq = 0
    _question_seq = 0


def create_quiz(data: QuizCreate) -> QuizRead:
    global _quiz_seq
    _quiz_seq += 1
    quiz = {
        "id": _quiz_seq,
        "title": data.title,
        "topic": data.topic,
        "status": "draft",
        "created_at": _now(),
    }
    _quizzes[_quiz_seq] = quiz
    _questions[_quiz_seq] = []
    _scores[_quiz_seq] = {}
    return QuizRead(**quiz)


def list_quizzes() -> list[QuizRead]:
    return [QuizRead(**q) for q in _quizzes.values()]


def get_quiz(quiz_id: int) -> dict:
    if quiz_id not in _quizzes:
        raise NotFoundError("quiz", quiz_id)
    quiz = dict(_quizzes[quiz_id])
    quiz["questions"] = list(_questions.get(quiz_id, []))
    return quiz


def set_status(quiz_id: int, status: str) -> QuizRead:
    if quiz_id not in _quizzes:
        raise NotFoundError("quiz", quiz_id)
    if status not in {"draft", "live", "closed"}:
        from src.errors import AppError
        raise AppError(f"invalid status: {status}", status_code=422)
    _quizzes[quiz_id]["status"] = status
    return QuizRead(**_quizzes[quiz_id])


def add_question(quiz_id: int, data: QuestionCreate) -> QuestionRead:
    # BUG 4: _question_seq is read but never incremented — every question gets id=1
    global _question_seq
    if quiz_id not in _quizzes:
        raise NotFoundError("quiz", quiz_id)
    question = {
        "id": _question_seq + 1,
        "quiz_id": quiz_id,
        "text": data.text,
        "options": data.options,
        "correct_index": data.correct_index,
        "image_url": data.image_url,
    }
    _questions[quiz_id].append(question)
    return QuestionRead(**question)


def list_questions(quiz_id: int) -> list[QuestionRead]:
    if quiz_id not in _quizzes:
        raise NotFoundError("quiz", quiz_id)
    return [QuestionRead(**q) for q in _questions[quiz_id]]


def submit_answer(
    quiz_id: int, question_id: int, player_name: str, selected_index: int
) -> dict:
    if quiz_id not in _quizzes:
        raise NotFoundError("quiz", quiz_id)
    question = next(
        (q for q in _questions[quiz_id] if q["id"] == question_id), None
    )
    if question is None:
        raise NotFoundError("question", question_id)
    correct = selected_index == question["correct_index"]
    _scores[quiz_id].setdefault(player_name, 0)
    if correct:
        _scores[quiz_id][player_name] += 1
    return {
        "correct": correct,
        "correct_index": question["correct_index"],
        "score": _scores[quiz_id][player_name],
    }


def get_scores(quiz_id: int) -> list[dict]:
    if quiz_id not in _quizzes:
        raise NotFoundError("quiz", quiz_id)
    scores = _scores.get(quiz_id, {})
    rows = [{"player_name": name, "score": score} for name, score in scores.items()]
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows
