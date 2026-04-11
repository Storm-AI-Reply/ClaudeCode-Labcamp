"""quiz-night — a trivia quiz builder and runner.

Entry point for the FastAPI app. Routes are registered from src/routes/.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.middleware.errors import register_exception_handlers
from src.routes import leaderboard, play, quizzes

# BUG 1: missing parentheses — FastAPI is the class, not an instance
app = FastAPI

app.include_router(quizzes.router)
app.include_router(leaderboard.router)
app.include_router(play.router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

register_exception_handlers(app)


@app.get("/")
def root():
    return {"app": "quiz-night", "status": "ok"}
