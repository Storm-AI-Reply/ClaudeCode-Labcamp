# Agentic AI Coding with Claude Code

A hands-on labcamp where you build a **live trivia quiz app** using Claude Code, then the whole room plays it.

> **[Open the labcamp site](https://storm-ai-reply.github.io/ClaudeCode-Labcamp/)** for the best reading experience, or follow the markdown guides below.

---

## Quick start

```bash
git clone https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp.git
cd ClaudeCode-Labcamp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Full instructions in [SETUP.md](SETUP.md). Prefer the web version: **[setup on the labcamp site](https://storm-ai-reply.github.io/ClaudeCode-Labcamp/setup/)**.

## Labs

| # | Lab | Time | What you learn |
|---|-----|------|----------------|
| 1 | [The Execution Model](labs/01-execution-model/) | 30 min | Agentic loop, Plan Mode, context management |
| 2 | [Project Configuration](labs/02-project-configuration/) | 25 min | CLAUDE.md, custom slash commands |
| 3 | [Control & Connect](labs/03-control-connect/) | 30 min | Hooks, permission modes, MCP servers |
| 4 | [Scale & Reuse](labs/04-scale-reuse/) | 25 min | Subagents, skills (SKILL.md) |
| | [Final Project](labs/final-project/) | 30 min | Assemble everything, compete |

Work through them in order. Each lab builds on the previous one.

## The competition

At the end, every group hosts their quiz. The room joins via QR code and plays a round.

| Criterion | Points |
|-----------|--------|
| Works end-to-end (join, answer, leaderboard) | 25 |
| Claude Code config (CLAUDE.md, commands, hooks, skills, MCP) | 25 |
| Quiz content (creative, entertaining, on-theme) | 25 |
| Beautiful UI (visual craft, polish, identity) | 25 |

## labcamp format

- 60 participants, **12 groups of 5**
- Each group has **1 laptop + 1 Claude Code account**
- Mob coding: rotate the driver every exercise
- 2 hours of hands-on labs + final showdown

## Repository structure

```
├── labs/                   Lab exercises with starter code
│   ├── 01-execution-model/
│   ├── 02-project-configuration/
│   ├── 03-control-connect/
│   ├── 04-scale-reuse/
│   └── final-project/
├── docs/                   MkDocs source (GitHub Pages); `docs/labs/lab-0N/` = one page per exercise
├── SETUP.md                Pre-labcamp setup instructions
├── requirements.txt        Python dependencies for the labs (`.venv`)
├── requirements-docs.txt   MkDocs Material only (local: `.venv-docs`; CI installs this on the runner)
└── mkdocs.yml              Site configuration
```
