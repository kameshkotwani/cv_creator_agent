import json
import os
from tests.helpers.utils import get_master_cv, get_dummy_jd
import pytest
from src.graph import build_app


@pytest.mark.llm
def test_graph_end_to_end_with_real_llm():
    # Safety gate to not run this test in CI/CD
    if os.getenv("RUN_LLM_TESTS") != "1":
        pytest.skip("Set RUN_LLM_TESTS=1 to run real LLM tests")

   
    # getting fake JD and CV
    master_cv = get_master_cv()
    dummy_jd = get_dummy_jd()

    app = build_app()
    final_state = app.invoke(
        {"jd_text": dummy_jd, "master_cv": master_cv, "error": None}
    )


    # 1) Should not fail
    assert not final_state.get("error"), (
        f"Graph failed with error: {final_state.get('error')}"
    )

    # 2) Analyst outputs
    assert "analysis" in final_state
    analysis = final_state["analysis"]
    assert isinstance(analysis, dict)

    assert "tech_keywords" in analysis and isinstance(analysis["tech_keywords"], list)
    assert "soft_keywords" in analysis and isinstance(analysis["soft_keywords"], list)
    assert "role_focus" in analysis and isinstance(analysis["role_focus"], str)

    # Loose bounds (real LLM varies)
    assert len(analysis["tech_keywords"]) >= 5
    assert len(analysis["soft_keywords"]) >= 3
    assert len(analysis["role_focus"].strip()) >= 30

    # Optional: check for at least one obvious keyword from the JD
    # (keep this very loose)
    tech_lower = {k.lower() for k in analysis["tech_keywords"]}
    assert any(x in tech_lower for x in ["python", "pytorch", "tensorflow"]), analysis[
        "tech_keywords"
    ]

    # 3) Summary outputs
    assert "summary" in final_state
    summary = final_state["summary"]
    assert isinstance(summary, str)
    assert len(summary.strip()) >= 20

    # Don’t make this too strict.
    approx_sentences = [s for s in summary.replace("\n", " ").split(".") if s.strip()]
    assert len(approx_sentences) >= 2  # use >=2, not ==3, to avoid flake

    # 4) Experience outputs (depends on your experience_node)
    assert "experience_bullets" in final_state
    exp = final_state["experience_bullets"]
    assert isinstance(exp, dict)
    assert len(exp) > 0

    assert not final_state.get("error")
    
    print("\nFINAL STATE:\n", json.dumps(final_state, indent=2, ensure_ascii=False))
    