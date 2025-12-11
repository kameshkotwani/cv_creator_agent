import os
import json
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.state import CVState
from src.utils import get_llm, get_ollma_llm
from src.agents.prompts import EXPERIENCE_PROMPT
# Initialize LLM
llm = get_ollma_llm()


def experience_node(state: CVState):
    print("--- EXPERIENCE AGENT: Tailoring Job History... ---")

    # 1. Prepare Data
    analysis = state["analysis"]
    keywords = analysis.get("tech_keywords")
    role_focus = analysis.get("role_focus")

    # getting the complete job_description
    jd_text = state["jd_text"]

    # Extract the 3 fixed jobs from Master CV
    # We send the WHOLE pool of bullets so the AI can choose.
    jobs_data = []
    # Ensure we are accessing the list correctly
    experience_list = state["master_cv"].get("experience", [])

    if not experience_list:
        raise ValueError("Empty experiences")

    for job in experience_list:
        jobs_data.append(
            {
                "id": job.get("id"),
                "company": job.get("company"),
                "role": job.get("role"),
                "bullet_pool": job.get("bullet_pool", []),
            }
        )

    # 2. prompts currently in prompts.py
    prompt = EXPERIENCE_PROMPT

    # 3. Invoke Chain
    chain = prompt | llm | JsonOutputParser()

    try:
        # Convert list to JSON string for prompt
        jobs_json = json.dumps(jobs_data, indent=2)

        result = chain.invoke(
            {
                "focus": role_focus,
                "keywords": ", ".join(keywords),
                "jobs_data": jobs_json,
                "jd_text": jd_text,
            }
        )

        # Validate output has the content key
        if "content" in result:
            print(f"Experience Tailored for {len(result['content'])} roles.")
            return {"experience_bullets": result["content"]}
        else:
            print("Output missing 'content' key, returning raw.")
            return {"experience_bullets": {}}

    except Exception as e:
        print(f"Error in Experience Agent: {e}")
        # stop the execution if there is an error
        return {"error": e}
