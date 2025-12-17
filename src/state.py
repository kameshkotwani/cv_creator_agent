from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class CVState(TypedDict,total=False):
    # INPUTS
    jd_text: str                # The raw Job Description
    master_cv: Dict[str, Any]   # The loaded master_cv.json content

    # ANALYSIS (From Analyst Agent)
    analysis: Dict[str, Any]    # {"tech_keywords": [], "role_focus": "..."}

    # GENERATED CONTENT (From Parallel Agents)
    summary: str                # The generated profile summary
    experience_bullets: Dict[str, List[str]] # {"iqvia": ["bullet1", ...]}
    selected_project_ids: List[str]          # ["rag_chatbot", "nlp_project"]
    project_bullets: Dict[str, List[str]]    # {"rag_chatbot": ["bullet1", ...]}
    skills: Dict[str, str]                   # {"ML": "Python, ..."}
    
    # REVIEW (From Evaluator Agent)
    review: Dict[str, Any]      # {"score": 85, "feedback": "..."}
    
    # NEW: Error Flag to stop the execution 
    error: Optional[str]