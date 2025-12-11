import sys
import os
import json
from src.graph import app
from src.utils import load_master_data
from . import DUMMY_JD



# Test Case: A "Senior Lead" role (Should prioritize Mentorship/Strategy bullets)

print("🚀 STARTING TEST 3: EXPERIENCE AGENT")
print("-" * 40)

initial_state = {
    "jd_text": DUMMY_JD,
    "master_cv": load_master_data(),
    "analysis": {},
    "summary": "",
    "experience_bullets": {}, "selected_project_ids": [], "project_bullets": {}, "skills": {}, "review": {}
}

output = app.invoke(initial_state)

print(f"ROLE FOCUS: {output['analysis']['role_focus']}")
print("-" * 40)

# Print Sheffield Bullets
print("👔 TAILORED EXPERIENCE (Sheffield Job):")
bullets = output['experience_bullets'].get('sheffield_research', [])
for bullet in bullets:
    print(f"- {bullet}")

# Print CDAC Bullets
print("\nTAILORED EXPERIENCE (CDAC Job):")
bullets = output['experience_bullets'].get('cdac', [])
for bullet in bullets:
    print(f"- {bullet}")

# Print IQVIA Bullets
print("\nTAILORED EXPERIENCE (IQVIA Job):")
bullets = output['experience_bullets'].get('iqvia', [])
for bullet in bullets:
    print(f"- {bullet}")