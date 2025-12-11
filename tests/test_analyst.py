from src.graph import app
from src.utils import load_master_data
from . import DUMMY_JD

print("🚀 STARTING TEST 1: ANALYST AGENT")
print("-" * 40)

# 2. Initialize State
initial_state = {
    "jd_text": DUMMY_JD,
    "master_cv": load_master_data(), # Loads your JSON
    "analysis": {},
    "summary": "",
    "experience_bullets": {},
    "selected_project_ids": [],
    "project_bullets": {},
    "skills": {},
    "review": {}
}

# 3. Run the Graph
output_state = app.invoke(initial_state)

# 4. Verify Output
print("-" * 40)
print("🤖 AGENT OUTPUT (Analysis):")
import json
print(json.dumps(output_state["analysis"], indent=2))
print("-" * 40)

if output_state["analysis"]:
    print("TEST PASSED: Keywords extracted successfully.")
    print(output_state["analysis"].get("tech_keywords"))
    print(output_state["analysis"].get("soft_keywords"))
    print(output_state["analysis"].get("role_focus"))
else:
    print("TEST FAILED: No keywords found.")