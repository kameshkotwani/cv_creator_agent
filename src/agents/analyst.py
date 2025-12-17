import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.state import CVState
from src.utils import get_ollma_llm,template_loader


# 2. Define the Agent Function
def analyst_node(state: CVState, *, llm=None):
    print("--- ANALYST AGENT: Reading Job Description... ---")

    # Safely access the job description; return an error if it's missing or empty.
    jd_text = state.get("jd_text")
    if not isinstance(jd_text, str) or not jd_text.strip():
        return {"error": "jd_text is missing or empty in state"}

    llm = llm or get_ollma_llm()  # lazy init

    # Prompt: Extract hard/soft skills and the core focus
    prompt = template_loader("analyst")
    # Chain: Prompt -> LLM -> JSON Parser
    chain = prompt | llm | JsonOutputParser()

    try:
        analysis_result = chain.invoke({"jd": jd_text})
        
        # Update State: We only update the 'analysis' key
        return {"analysis": analysis_result}

    except Exception as e:
        return {"error": str(e)}
