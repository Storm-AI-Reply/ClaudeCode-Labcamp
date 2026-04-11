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

*TODO: describe the shape of error responses returned by the app.*
