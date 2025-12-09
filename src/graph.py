from langgraph.graph import StateGraph, END
from src.state import CVState
from src.agents.analyst import analyst_node

# 1. Initialize Graph with our State
workflow = StateGraph(CVState)

# 2. Add the Node
workflow.add_node("analyst", analyst_node)

# 3. Define the Flow (Start -> Analyst -> End)
workflow.set_entry_point("analyst")
workflow.add_edge("analyst", END)

# 4. Compile the Graph
app = workflow.compile()