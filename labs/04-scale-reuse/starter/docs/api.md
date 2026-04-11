# quiz-night API

## Endpoints

### `GET /quizzes`
List all quizzes.

### `POST /quizzes`
Create a quiz.
Body: `{ "title": str, "topic": str }`

### `GET /quizzes/{id}`
Fetch a quiz with its questions.

### `PATCH /quizzes/{id}/status`
Change status. Body: `{ "status": "draft" | "live" | "closed" }`

### `POST /quizzes/{id}/questions`
Add a question. Body: `QuestionCreate` (see `src/schemas/quiz.py`). Optional: `image_url` (HTTPS URL for a background image).

### `POST /quizzes/{id}/answer?question_id=...`
Submit a player answer. Body: `{ "player_name": str, "selected_index": int }`

### `GET /quizzes/{id}/scores`
Leaderboard sorted by score.

## Error format

All application errors flow through `register_exception_handlers` in
`src/middleware/errors.py`. `AppError` and its subclasses (e.g. `NotFoundError`)
are serialized by `format_error()` as:

```json
{
  "error": {
    "message": "quiz 999 not found",
    "code": 404
  }
}
```

Pydantic validation failures (missing `topic` on `POST /quizzes`, a
`QuestionCreate` with fewer than 4 options, `correct_index` outside 0..3)
return FastAPI's default 422 response with a `detail` array.
