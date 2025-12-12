# CV Creator Agent

A lightweight LLM-powered pipeline to tailor a master CV to a target Job Description.

This repository provides a small workflow of LLM-driven processing steps (called "agents") that analyze a job description, draft a concise professional summary, and rewrite experience bullets to align with the target role and ATS keywords.

## Key Concepts

- Workflow (pipeline) — not an autonomous planning agent. Orchestration is explicit and deterministic via a `StateGraph`.
- Agents — independent processing nodes that accept the shared state, call an LLM with a prompt, parse outputs, and return updates to the state.
- State — a TypedDict (`src/state.py`) representing inputs, analysis, generated outputs, and errors.

## Features

- Extracts tech and soft keywords and role focus from a Job Description.
- Generates a 3-sentence professional summary tuned to the JD.
- Rewrites experience bullets for three roles using an ATS-friendly prompt.
- Tests to validate basic pipeline runs (no external orchestration required).

## Tech Stack

- Python 3.10+
- LangChain-style primitives (`langchain_core`) for prompts and parsers
- Providers: `langchain_google_genai` and `langchain_ollama` (LLM clients) — configured in `src/utils.py`
- Orchestration: `langgraph` (StateGraph) at `src/graph.py`
- Tests: `pytest` (see `tests/`)

## Repository Layout (important files)

- `src/graph.py` — the orchestrator: builds the `StateGraph` and compiles `app`.
- `src/agents/analyst.py` — extracts keywords and role focus from JD.
- `src/agents/summary.py` — drafts the professional summary.
- `src/agents/experience.py` — rewrites experience bullets using an ATS prompt.
- `src/agents/prompts/experience.toml` — canonical experience prompt template.
- `src/utils.py` — LLM client factory and helper functions.
- `src/state.py` — `CVState` TypedDict describing the workflow state.
- `tests/` — integration-style tests that invoke `app.invoke(initial_state)`.

## Getting Started

Prerequisites

- Add any LLM provider keys to a `.env` file in the repo root (see `src/agents/__init__.py` which loads `.env`). Common vars:
  - `GOOGLE_API_KEY` (for `langchain_google_genai`)
  - Any Ollama/local model host configuration if applicable

Install dependencies (example using pip):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Note: This repo uses provider-specific packages (`langchain_google_genai`, `langchain_ollama`, `langchain_core`, `langgraph`). If you rely on a `pyproject.toml`, install via that (`pip install -e .`) or adapt to your environment.

Running tests

```bash
# from repo root
python -m pytest -q
```

Quick usage (interactive)

```python
from src.graph import app
from src.utils import load_master_data

initial_state = {
    "jd_text": "<PASTE JOB DESCRIPTION>",
    "master_cv": load_master_data(),
    "analysis": {},
    "summary": "",
    "experience_bullets": {},
    "selected_project_ids": [],
    "project_bullets": {},
    "skills": {},
    "review": {}
}

output = app.invoke(initial_state)
print(output["analysis"])   # analyst output
print(output["summary"])    # generated summary
print(output["experience_bullets"])  # tailored bullets
```

## Design Notes

- The project intentionally implements a pipeline: each node is responsible for a single transformation and returns only the portion of state it owns. The compiled `app` runs the nodes in sequence and stops on error.
- Each agent uses a prompt-driven pattern: prepare data → call LLM → parse output → return state diff.
- `src/agents/prompts/experience.toml` contains a stricter, production-ready prompt for the experience rewriting step.

## Recommendations / Next Steps

- Harden LLM calls with timeouts, retries, and backoff (wrap SDK calls with `tenacity` or provider-native retry configs).
- Add a circuit-breaker or rate-limiter to avoid hammering providers.
- Add an orchestration entrypoint (CLI or HTTP worker) to queue runs, persist intermediate state, and resume failures.
- If you want an autonomous agent (planner + tools), provide a toolset (search, retriever, file access) and an action interpreter; otherwise keep the clean pipeline model for reproducibility.

## Contributing

- Open issues or PRs; keep prompts and state shape explicit.

## License

MIT
