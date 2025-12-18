import json

from langchain_core.output_parsers import StrOutputParser

from src.state import CVState
from src.utils import get_ollma_llm, template_loader


def summary_node(state: CVState,*,llm=None):
    print("--- SUMMARY AGENT: Drafting Profile (Smart Mode)... ---")
    
    llm = llm or get_ollma_llm()
    
    # 1. Prepare Data
    # We dump the raw experience and projects so the LLM can "see" everything
    master_cv = state.get("master_cv",{})
    if not master_cv:
        raise ValueError("Empty Master CV")
    
    
    # We convert lists to JSON strings to keep the prompt clean
    experience_json = json.dumps(master_cv.get("experience", []), indent=2)
    projects_json = json.dumps(master_cv.get("projects", []), indent=2)
    skills_json = json.dumps(master_cv.get("skills_pool", {}), indent=2)
    
    # Get Analyst Strategy
    role_focus:list = state.get("analysis",{}).get("role_focus",[])
    keywords:list = state.get("analysis",{}).get("tech_keywords",[])
    
    # adding soft skills in the keywords to increase context
    keywords.extend(state.get("analysis",{}).get("soft_keywords",[]))
    
    # 2. prompt is coming from agents.prompts
    prompt = template_loader("summary")
    
    # 3. Invoke Chain
    chain = prompt | llm | StrOutputParser()
    
    try:
        summary_text = chain.invoke({
            "profile_title": master_cv["profile"]["title"],
            "experience": experience_json,
            "projects": projects_json,
            "skills": skills_json,
            "focus": role_focus,
            "keywords": ", ".join(keywords)
        })
        return {"summary": summary_text}
        
    except Exception as e:
        #TODO: remove this after testing
        print(f"Error in Summary Agent: {e}")
        return {"error": str(e)} 