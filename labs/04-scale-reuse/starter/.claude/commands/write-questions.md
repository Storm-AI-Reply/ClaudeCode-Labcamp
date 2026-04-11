---
description: Generate 5 quiz questions on a topic, using the group's voice & tone from CLAUDE.md.
argument-hint: <topic>
---

Generate **exactly 5 quiz questions** about: $ARGUMENTS

Before writing, read `CLAUDE.md` and extract:
- the **voice & tone** rules (default: playful and slightly dry)
- the schema constraints (4 options, `correct_index` in 0..3)

Each question must:
- be answerable from general knowledge, no trick questions
- have **exactly 4 options**, one of which is unambiguously correct
- avoid "all of the above" / "none of the above"
- match the voice from CLAUDE.md

Output format, a JSON array that can be passed directly to
`POST /quizzes/{id}/questions`:

```json
[
  {
    "text": "...",
    "options": ["...", "...", "...", "..."],
    "correct_index": 0
  }
]
```

After the JSON, add a one-line note explaining any editorial choices
(difficulty level, angle on the topic). Do **not** write the questions to
disk, the user will decide which ones to insert.
