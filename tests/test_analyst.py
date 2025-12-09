from src.graph import app
from src.utils import load_master_data

# 1. Dummy Job Description
dummy_jd = """
Full job description
Remote
Full Time
Experienced
FTC or Permanent
UK-wide, Remote

About the role
Olive Jar Digital is seeking a Machine Learning Engineer to help design, build, and refine AI prototypes across multiple Discovery and Alpha initiatives. You will work at the intersection of engineering and data science - transforming experimental models into high-quality, scalable prototypes, shaping technical architecture, and ensuring robust deployment, testing, and documentation.

This role is ideal for someone who enjoys hands-on technical problem-solving, rapid iteration, and collaborating closely with data scientists, engineers, product managers, and researchers.

About Olive Jar Digital
As we grow, we empower our teams to develop their roles and functions and offer support to get you from where you are now, to where you want to be. Moving towards our 10th year, we are now an established brand, building digital products and services and championing the provision of expert talent to enhance customer and in-house teams, satisfying all user needs.

We are a professional, fun, fully Inclusive and diverse digital consultancy, valuing everyone’s opinion. With a huge growth plan over the next two years, we are looking to expand our client facing delivery team with designers, developers, and testers as we continue to expand our project portfolio.


Responsibilities

Build, refine, and optimise AI/ML prototypes, ensuring they meet quality, security, and performance standards.
Develop and maintain technical design documentation, including architecture, model pipelines, and integration patterns.
Implement automated deployment pipelines, CI/CD flows, unit/regression testing, and monitoring/telemetry for prototypes.
Deploy models into development and test environments and support iterative updates based on feedback.
Collaborate with data scientists on model integration, feature engineering, and evaluation frameworks.
Ensure codebases follow best practices in engineering, documentation, security, and accessibility. Support playback sessions, technical reviews, and knowledge-transfer activities.

About You
Strong experience as an ML Engineer or similar role within AI/ML product development.
Proficiency in building ML pipelines, APIs, cloud-based deployments, and automated testing.
Solid software engineering skills (e.g., Python, version control, CI/CD, cloud platforms).
Ability to work collaboratively with data scientists, engineers, and product teams.
Comfortable producing clear, structured technical documentation.
Experience with LLMs, vector databases, retrieval-augmented generation, or intelligent search.
Familiarity with MLOps tooling, containerisation, and cloud-native environments.
Exposure to rapid prototyping in Discovery/Alpha phases.

Benefits
25 Days Annual Leave per annum (plus 8 Bank Holidays as standard)
Health Insurance
Pension Scheme
Annual Bonus Scheme
Annual Salary Review
Electric Car Scheme
"""

print("🚀 STARTING TEST 1: ANALYST AGENT")
print("-" * 40)

# 2. Initialize State
initial_state = {
    "jd_text": dummy_jd,
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