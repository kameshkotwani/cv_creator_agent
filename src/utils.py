import json
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


def load_master_data()->dict:
    """Loads the Master CV JSON from the data directory."""
    # Build path relative to this file
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "data", "master_cv.json")

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


# using gemini API, however its free tier is reaching rate limit.
def get_llm():
    """
    returns the GoogleGenerativeAI model
    """
    return ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.8,  # Creative enough to write good prose, but factual
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        max_retries=3,      # Retry up to 3 times
        request_timeout=30,  # Wait longer for a response
    )


def get_ollma_llm():
    return ChatOllama(
        model="gemma3:12b",
        temperature=0.8,
        # 'keep_alive' keeps the model loaded in RAM for 5 minutes 
        # so subsequent requests are instant.
        keep_alive="5m" 
    )

def template_loader(name:str)->ChatPromptTemplate:
    """
    Loads the templates from prompts directory.
    
    :param name: Description
    :type name: str
    """
    import tomllib
    
    with open(f"src/agents/prompts/{name}.toml", 'rb') as f:
        prompt = tomllib.load(f)['prompt']['template']

    return ChatPromptTemplate.from_template(prompt)
    

