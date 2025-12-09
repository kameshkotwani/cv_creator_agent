
from src.graph import app
from src.utils import load_master_data
from . import DUMMY_JD

# JD requiring GenAI (Testing if Summary adapts)
dummy_jd =DUMMY_JD

print("🚀 RUNNING INTEGRATION TEST: Analyst -> Summary")
state = {
    "jd_text": dummy_jd, 
    "master_cv": load_master_data(),
    "analysis": {}, "summary": "", "experience_bullets": {}, 
    "selected_project_ids": [], "project_bullets": {}, "skills": {}, "review": {}
}

output = app.invoke(state)

print(f"✅ Analyst Found Keywords: {output['analysis'].get('tech_keywords')}")
print(f"📝 Final Summary:\n{output['summary']}")