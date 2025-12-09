import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from src.state import CVState

# 1. Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0.0, # Zero temp for strict analysis
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Define the Agent Function
def analyst_node(state: CVState):
    print("--- ANALYST AGENT: Reading Job Description... ---")
    
    jd_text = state["jd_text"]
    
    # Prompt: Extract hard/soft skills and the core focus
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert Technical Recruiter.
        Analyze the following Job Description to extract critical requirements.
        
        JOB DESCRIPTION:
        {jd}
        
        INSTRUCTIONS:
        1. "tech_keywords": Extract top 8-10 hard technical skills (e.g., Python, AWS, Spark).
        2. "soft_keywords": Extract top 5-6 soft skills (e.g., Leadership, Communication).
        3. "role_focus": Write a summary of the role summarizing the primary goal of this role.
        
        OUTPUT STRICT JSON FORMAT ONLY:
        {{
            "tech_keywords": ["Skill1", "Skill2"],
            "soft_keywords": ["Soft1", "Soft2"],
            "role_focus": "The focus is..."
        }}
        """
    )
    
    # Chain: Prompt -> LLM -> JSON Parser
    chain = prompt | llm | JsonOutputParser()
    
    try:
        analysis_result = chain.invoke({"jd": jd_text})
        print(f"Analysis Complete: Found {len(analysis_result['tech_keywords'])} tech keywords.")
        
        # Update State: We only update the 'analysis' key
        return {"analysis": analysis_result}
        
    except Exception as e:
        print(f"Error in Analyst Agent: {e}")
        # Return empty analysis on failure to prevent crash
        return {"analysis": {"tech_keywords": [], "soft_keywords": [], "role_focus": "Error parsing JD"}}