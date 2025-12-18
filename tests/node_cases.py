from src.agents.analyst import analyst_node
from src.agents.experience import experience_node
from src.agents.summary import summary_node
from tests.helpers.fakes import fake_json_llm, fake_text_llm
from tests.helpers.utils import get_dummy_jd, get_master_cv

DUMMY_JD = get_dummy_jd()
MASTER_CV = get_master_cv()

NODE_CASES = [
    {
        "name": "analyst",
        "fn": analyst_node,
        "min_state": {"jd_text": DUMMY_JD},
        "fake_llm": fake_json_llm('{"tech_keywords":["Python"],"soft_keywords":["Communication"],"role_focus":"x"}'),
        "expected_keys": {"analysis"},
    },
    {
        "name": "summary",
        "fn": summary_node,
        "min_state": {
            "jd_text": DUMMY_JD,
            "analysis": {"tech_keywords": ["Python"]},
            "master_cv": MASTER_CV,
        },
        "fake_llm": fake_text_llm('{"summary":"Profile summary"}'),
        "expected_keys": {"summary"},
    },
    {
        "name": "experience",
        "fn": experience_node,
        "min_state": {
            "analysis": {"tech_keywords": ["Python"]},
            "master_cv": MASTER_CV,
            "jd_text": DUMMY_JD,
            "keywords": ["Python", "Communication"],
            "focus": [],
        },
        "fake_llm": fake_json_llm('{"content":{"company":["b1","b2"]}}'),
        "expected_keys": {"experience_bullets"},
    },
]
