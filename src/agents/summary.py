import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.state import CVState
from src.utils import get_llm

# Initialize LLM
llm = get_llm()

def summary_node(state: CVState):
    print("--- SUMMARY AGENT: Drafting Profile (Smart Mode)... ---")
    
    # 1. Prepare Data
    # We dump the raw experience and projects so the LLM can "see" everything
    master_cv = state["master_cv"]
    
    # We convert lists to JSON strings to keep the prompt clean
    experience_json = json.dumps(master_cv.get("experience", []), indent=2)
    projects_json = json.dumps(master_cv.get("projects", []), indent=2)
    skills_json = json.dumps(master_cv.get("skills_pool", {}), indent=2)
    
    # Get Analyst Strategy
    role_focus = state["analysis"].get("role_focus")
    keywords = state["analysis"].get("tech_keywords")
    
    # 2. Define Prompt
    prompt = ChatPromptTemplate.from_template(
        """
        You are an Expert Executive Resume Writer.
        Your goal is to write a high-impact, 3-sentence Professional Summary.
        
        THE GOAL: 
        Connect the candidate's past achievements to the Target Role's needs.
        
        TARGET ROLE FOCUS: {focus}
        TARGET KEYWORDS: {keywords}
        
        CANDIDATE HISTORY:
        Profile: {profile_title}
        Experience: {experience}
        Projects: {projects}
        Skills: {skills}
        
        INSTRUCTIONS:
        1. Analyze the 'Experience' and 'Projects' to find the 2 biggest "Wins" (Metrics, Deliverables, or Innovations) that prove the candidate fits the Target Role.
        2. Draft the Summary:
           - Sentence 1: Hook. State Title + Years of Exp + Core Expertise (using Keywords).
           - Sentence 2: Proof. Mention the specific "Wins" you found (e.g., "Reduced latency by 40%..." or "Built RAG systems...").
           - Sentence 3: Value. State the immediate value you bring to the new company.
           - The whole summary should not be more than 40-50 words.
        
        CONSTRAINT:
        - Strict 3 sentence limit.
        - Do not hallucinate. Use ONLY facts from the provided History.
        - Do not use I or first person mentioning.
        
        Output ONLY the summary text.
        """
    )
    
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
        print(f"Summary Generated.")
        return {"summary": summary_text}
        
    except Exception as e:
        print(f"Error in Summary Agent: {e}")
        return {"summary": "FAILED."}