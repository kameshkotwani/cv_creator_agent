from typing import Any

from typing_extensions import TypedDict


class CVState(TypedDict, total=False):
    # INPUTS
    jd_text: str  # The raw Job Description
    master_cv: dict[str, Any]  # The loaded master_cv.json content

    # ANALYSIS (From Analyst Agent)
    analysis: dict[str, Any]  # {"tech_keywords": [], "role_focus": "..."}

    # GENERATED CONTENT (From Parallel Agents)
    summary: str  # The generated profile summary
    experience_bullets: dict[str, list[str]]  # {"iqvia": ["bullet1", ...]}
    selected_project_ids: list[str]  # ["rag_chatbot", "nlp_project"]
    project_bullets: dict[str, list[str]]  # {"rag_chatbot": ["bullet1", ...]}
    skills: dict[str, str]  # {"ML": "Python, ..."}

    # REVIEW (From Evaluator Agent)
    review: dict[str, Any]  # {"score": 85, "feedback": "..."}

    # NEW: Error Flag to stop the execution
    error: str | None
