from pydantic import BaseModel, Field, field_validator


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
    correct_index: int = Field(ge=0, le=3)
    image_url: str | None = None

    @field_validator("options")
    @classmethod
    def options_must_have_four(cls, v: list[str]) -> list[str]:
        if len(v) != 4:
            raise ValueError("options must contain exactly 4 entries")
        return v


class QuestionRead(QuestionCreate):
    id: int
    quiz_id: int


class PlayerAnswer(BaseModel):
    player_name: str
    selected_index: int
