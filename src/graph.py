# src/graph.py

from langgraph.graph import END, StateGraph

from src.agents.analyst import analyst_node
from src.agents.experience import experience_node
from src.agents.summary import summary_node
from src.state import CVState


# --- ROUTER LOGIC ---
# return an error if there is a problem with one of the nodes
def check_status(state: CVState):
    return "error" if state.get("error") else "continue"


def build_app():
    # 1. Initialize Graph
    workflow = StateGraph(CVState)

    # 2. Add Nodes
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("summary", summary_node)
    workflow.add_node("experience", experience_node)

    # 3. Define Conditional Flow
    workflow.set_entry_point("analyst")

    # Analyst -> (Check) -> Summary
    workflow.add_conditional_edges(
        "analyst",  # Source
        check_status,  # Logic Function
        {"continue": "summary", "error": END},
    )

    # Summary -> (Check) -> Experience
    workflow.add_conditional_edges("summary", check_status, {"continue": "experience", "error": END})

    # Experience -> (Check) -> End
    workflow.add_conditional_edges(
        "experience",
        check_status,
        {
            "continue": END,  # (Later this will go to Projects)
            "error": END,
        },
    )

    # 4. Compile
    return workflow.compile()
