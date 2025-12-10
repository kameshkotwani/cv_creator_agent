import os
import json
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.state import CVState
from src.utils import get_llm,get_ollma_llm
# Initialize LLM
llm = get_ollma_llm()

def experience_node(state: CVState):
    print("--- EXPERIENCE AGENT: Tailoring Job History... ---")
    
    # 1. Prepare Data
    analysis = state["analysis"]
    keywords = analysis.get("tech_keywords")
    role_focus = analysis.get("role_focus")
    
    # Extract the 3 fixed jobs from Master CV
    # We send the WHOLE pool of bullets so the AI can choose.
    jobs_data = []
    # Ensure we are accessing the list correctly
    experience_list = state["master_cv"].get("experience",[])
    
    if not experience_list:
        raise ValueError("Empty experiences")
    
    for job in experience_list:
        jobs_data.append({
            "id": job.get("id"),
            "company": job.get("company"),
            "role": job.get("role"),
            "bullet_pool": job.get("bullet_pool", [])
        })

    # 2. Define Prompt
    prompt = ChatPromptTemplate.from_template(
        """
        You are an Expert CV Writer.
        
        TASK: Tailor the experience section for a specific Job Description.
        
        TARGET ROLE FOCUS: {focus}
        MUST-USE KEYWORDS: {keywords}
        
        CANDIDATE EXPERIENCE POOLS (Do not invent jobs, use these facts):
        {jobs_data}
        
        INSTRUCTIONS:
        For EACH of the 3 jobs provided in the data:
        1. Select the top 3 bullet points from the 'bullet_pool' that best match the Target Role.
           - If the role is Technical, pick technical bullets (Spark, APIs).
           - If the role is Managerial/Research, pick leadership/research bullets.
        2. REWRITE the selected bullets:
           - Use the STAR method (Situation, Task, Action, Result).
           - Incorporate the 'MUST-USE KEYWORDS' naturally if they fit the fact.
           - Keep each bullet under 25 words.
           - Start with strong action verbs.
           - Do not repeat the Action verbs.
           - Keep the language simple and in British English
        
        OUTPUT STRICT JSON:
        {{
            "content": {{
                "sheffield_research": ["Rewritten Bullet 1", "Rewritten Bullet 2", "Rewritten Bullet 3"],
                "iqvia": ["Rewritten Bullet 1", "Rewritten Bullet 2", "Rewritten Bullet 3"],
                "cdac": ["Rewritten Bullet 1", "Rewritten Bullet 2", "Rewritten Bullet 3"]
            }}
        }}
        """
    )
    
    # 3. Invoke Chain
    chain = prompt | llm | JsonOutputParser()
    
    try:
        # Convert list to JSON string for prompt
        jobs_json = json.dumps(jobs_data, indent=2)
        
        result = chain.invoke({
            "focus": role_focus,
            "keywords": ", ".join(keywords),
            "jobs_data": jobs_json
        })
        
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

# test_the node
# experience_node(state)