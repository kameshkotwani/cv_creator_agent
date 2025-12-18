from pydantic import BaseModel, Field

# --- Output Models (What the Agents Generate) ---


class TailoredSummary(BaseModel):
    content: str = Field(description="A 3-sentence professional summary tailored to the JD.")


class TailoredExperience(BaseModel):
    # Map 'company_id' (e.g., 'iqvia') -> List of rewritten bullets
    # Example: {"iqvia": ["Bullet 1", "Bullet 2"], "sheffield": [...]}
    content: dict[str, list[str]] = Field(description="Dictionary mapping Company IDs to a list of tailored bullets.")


class TailoredProjects(BaseModel):
    # List of project IDs selected (e.g. ['rag_chatbot', 'whatsapp_analyzer'])
    project_ids: list[str] = Field(description="The IDs of the 3 selected projects.")
    # Map 'project_id' -> List of bullets
    content: dict[str, list[str]] = Field(description="Dictionary mapping Project IDs to a list of tailored bullets.")


class TailoredSkills(BaseModel):
    # Example: {"Machine Learning": "Python, PyTorch...", "Cloud": "Azure, AWS..."}
    content: dict[str, str] = Field(description="Dictionary mapping Skill Categories to a comma-separated string of skills.")


class CVReview(BaseModel):
    score: int = Field(description="Match score from 0 to 100.")
    missing_keywords: list[str] = Field(description="List of critical keywords missing from the CV.")
    feedback: str = Field(description="Constructive feedback on how to improve the CV.")
