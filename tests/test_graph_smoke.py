import pytest
@pytest.mark.smoke
def test_graph_happy_path(monkeypatch):
    import src.graph as graph_mod

    ran = []

    def analyst_stub(state):
        ran.append("analyst")
        return {
            "analysis": {
                "tech_keywords": ["Python"],
                "soft_keywords": ["Communication"],
                "role_focus": "x"
            }
        }

    def summary_stub(state):
        ran.append("summary")
        return {
            "summary": "Sentence one. Sentence two. Sentence three."
        }

    def experience_stub(state):
        ran.append("experience")
        return {
            "experience_bullets": {
                "company": ["b1", "b2", "b3"]
            }
        }

    # Patch nodes exactly where graph.py uses them
    monkeypatch.setattr(graph_mod, "analyst_node", analyst_stub)
    monkeypatch.setattr(graph_mod, "summary_node", summary_stub)
    monkeypatch.setattr(graph_mod, "experience_node", experience_stub)

    app = graph_mod.build_app()
    final_state = app.invoke({
        "jd_text": "JD",
        "master_cv": {"profile": {"title": "DS"}}
    })

    assert ran == ["analyst", "summary", "experience"]
    assert not final_state.get("error")
    assert "analysis" in final_state
    assert "summary" in final_state
    assert "experience_bullets" in final_state


@pytest.mark.smoke
def test_graph_stops_on_error(monkeypatch):
    import src.graph as graph_mod

    ran = []

    def analyst_stub(state):
        ran.append("analyst")
        return {"error": "boom"}

    def summary_stub(state):
        ran.append("summary")
        return {"summary": "should not run"}

    monkeypatch.setattr(graph_mod, "analyst_node", analyst_stub)
    monkeypatch.setattr(graph_mod, "summary_node", summary_stub)

    app = graph_mod.build_app()
    final_state = app.invoke({"jd_text": "JD", "master_cv": {}})

    assert ran == ["analyst"]
    assert final_state["error"] == "boom"
