# Agentic AI Coding with Claude Code

A hands-on workshop where you build a **live trivia quiz app** using Claude Code, then the whole room plays it.

> **[Open the workshop site](https://YOUR_GITHUB_PAGES_URL/)** for the best reading experience, or follow the markdown guides below.

---

## Publishing the workshop site (GitHub Pages)

Documentation under `docs/` is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). Hosting follows Material’s [publishing guide](https://squidfunk.github.io/mkdocs-material/publishing-your-site/): **GitHub Actions** builds the static site and **GitHub Pages** serves it (no `gh-pages` branch required).

**One-time (on GitHub):** **Settings → Pages → Build and deployment** → set **Source** to **GitHub Actions**.

**Deploy:** push to **`main`** or **`master`**, or run the workflow manually (**Actions → Deploy documentation → Run workflow**). The workflow [`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml) installs `requirements-docs.txt`, runs `mkdocs build` with `SITE_URL` / `REPO_URL` set for your repo, and publishes the `site/` output. The live URL is shown on the workflow run and under **Settings → Pages** (`https://<owner>.github.io/<repo>/`).

### Local preview (use `.venv-docs`, not `.venv`)

Keep **lab dependencies** in `.venv` (`requirements.txt`) and **documentation tooling** in a separate **`.venv-docs`** (`requirements-docs.txt` only). Do not install MkDocs into the lab venv.

**macOS / Linux**

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install -r requirements-docs.txt
mkdocs serve
```

**Windows (PowerShell)**

```powershell
py -3 -m venv .venv-docs
.\.venv-docs\Scripts\Activate.ps1
pip install -r requirements-docs.txt
mkdocs serve
```

Open **http://127.0.0.1:8000**. Optional: `export REPO_URL=https://github.com/<you>/<repo>` (Unix) or `set REPO_URL=...` (Windows) before `mkdocs serve` so the theme can show **view/edit on GitHub** links.

**Optional:** `mkdocs gh-deploy` (pushes to a `gh-pages` branch) if you prefer that over Actions; the workflow above matches current Material recommendations.

---

## Quick start

```bash
git clone <repo-url>
cd ClaudeCode-Labcamp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Full instructions in [SETUP.md](SETUP.md).

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

## Workshop format

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
├── SETUP.md                Pre-workshop setup instructions
├── requirements.txt        Python dependencies for the labs (`.venv`)
├── requirements-docs.txt   MkDocs Material only (local: `.venv-docs`; CI installs this on the runner)
└── mkdocs.yml              Site configuration
```
