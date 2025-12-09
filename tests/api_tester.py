import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Load environment variables from .env file
load_dotenv(".env")

# 2. Check if key exists
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found. Please check your .env file.")
    exit()

print(f"✅ Key found: {api_key[:5]}... (hidden)")

# 3. Initialize the LLM
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=api_key,
        max_tokens=50
    )
    
    print("⏳ Connecting to Gemini...")
    response = llm.invoke("Hello! Are you ready to help me write a CV?")
    
    print("\n🎉 SUCCESS! Gemini replied:")
    print("-" * 40)
    print(response.content)
    print("-" * 40)

except Exception as e:
    print("\n❌ Connection Failed. Error details:")
    print(e)