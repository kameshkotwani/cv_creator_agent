from langgraph.graph import StateGraph, END
from src.state import CVState
from src.agents.analyst import analyst_node
from src.agents.summary import summary_node

# 1. Initialize Graph with our State schema
workflow = StateGraph(CVState)

# 2. Add Nodes (The Workers)

workflow.add_node("analyst", analyst_node)
workflow.add_node("summary", summary_node)

# 3. Define the Flow (The Assembly Line)
# Start -> Analyst -> Summary -> End
workflow.set_entry_point("analyst")
workflow.add_edge("analyst", "summary")
workflow.add_edge("summary", END)

# 4. Compile
app = workflow.compile()