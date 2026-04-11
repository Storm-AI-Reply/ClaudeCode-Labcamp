from pydantic import BaseModel


class QuizCreate(BaseModel):
    title: str
    topic: str


class QuizRead(QuizCreate):
    id: int
    status: str
    created_at: str


class QuestionCreate(BaseModel):
    text: str
    options: list[str]
    correct_index: int
    image_url: str | None = None


class QuestionRead(QuestionCreate):
    id: int
    quiz_id: int


class PlayerAnswer(BaseModel):
    player_name: str
    selected_index: int
