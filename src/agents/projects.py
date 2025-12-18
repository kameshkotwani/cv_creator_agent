import json

from langchain_core.output_parsers import JsonOutputParser

from src.state import CVState
from src.utils import get_ollma_llm, template_loader


def projects_node(state: CVState, *, llm=None):
    """
    Docstring for projects_node

    :param state: Description
    :type state: CVState
    :param llm: Description
    """
    # get ollama llm
    llm = llm or get_ollma_llm()

    # 1. Prepare Data
    analysis: dict = state.get("analysis", {})
    keywords = analysis.get("tech_keywords", [])
    role_focus = analysis.get("role_focus")

    # getting the complete job_description
    jd_text: str = state.get("jd_text", "")

    # Ensure we are accessing the list correctly
    projects_list = state.get("master_cv").get("projects")

    if not projects_list:
        return {"error": "projects list empty"}

    projects_data: list[dict] = []

    for project in projects_list:
        projects_data.append(
            {
                "id": project.get("id"),
                "title": project.get("title"),
                "bullet_pool": project.get("bullet_pool", []),
            }
        )

    # 2. prompts in agents/prompts
    prompt = template_loader("projects")

    # 3. Invoke Chain
    chain = prompt | llm | JsonOutputParser()

    try:
        # Convert list to JSON string for prompt
        projects_json = json.dumps(projects_data, indent=2)

        result = chain.invoke(
            {
                "focus": role_focus,
                "keywords": ", ".join(keywords),
                "project_bullets": projects_json,
                "jd_text": jd_text,
            }
        )
        print(result)
        # TODO: create prompt for the chain, add unit testing for projects node

    except Exception as e:
        print(f"Error in Experience Agent: {e}")
        # stop the execution if there is an error
        return {"error": str(e)}
