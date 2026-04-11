import pytest

pytestmark = pytest.mark.asyncio


async def test_create_quiz_returns_201_and_payload(client):
    response = await client.post(
        "/quizzes",
        json={"title": "90s games", "topic": "retro video games"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "90s games"
    assert body["status"] == "draft"


async def test_create_quiz_rejects_missing_fields(client):
    response = await client.post("/quizzes", json={"title": "oops"})
    assert response.status_code == 422


async def test_get_missing_quiz_returns_404(client):
    response = await client.get("/quizzes/999")
    assert response.status_code == 404


async def test_add_question_assigns_sequential_ids(client):
    quiz = (
        await client.post("/quizzes", json={"title": "q", "topic": "t"})
    ).json()

    first = await client.post(
        f"/quizzes/{quiz['id']}/questions",
        json={
            "text": "Q1?",
            "options": ["a", "b", "c", "d"],
            "correct_index": 0,
        },
    )
    second = await client.post(
        f"/quizzes/{quiz['id']}/questions",
        json={
            "text": "Q2?",
            "options": ["a", "b", "c", "d"],
            "correct_index": 1,
        },
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] == 1
    assert second.json()["id"] == 2


async def test_submit_answer_updates_score(client):
    quiz = (
        await client.post("/quizzes", json={"title": "q", "topic": "t"})
    ).json()
    question = (
        await client.post(
            f"/quizzes/{quiz['id']}/questions",
            json={
                "text": "Q1?",
                "options": ["a", "b", "c", "d"],
                "correct_index": 2,
            },
        )
    ).json()

    response = await client.post(
        f"/quizzes/{quiz['id']}/answer",
        params={"question_id": question["id"]},
        json={"player_name": "alice", "selected_index": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["correct"] is True
    assert body["score"] == 1


async def test_list_quizzes_returns_array(client):
    await client.post("/quizzes", json={"title": "a", "topic": "x"})
    await client.post("/quizzes", json={"title": "b", "topic": "y"})
    response = await client.get("/quizzes")
    assert response.status_code == 200
    assert len(response.json()) == 2
