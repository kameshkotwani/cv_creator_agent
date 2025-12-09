#!/bin/bash

echo "🚀 Setting up 'src' directory architecture..."

# 1. Create Directories
mkdir -p src/agents

# 2. Create Root SRC Files
echo "Creating core logic files..."
touch src/__init__.py
touch src/models.py      # Pydantic Schemas
touch src/state.py       # LangGraph State Definition
touch src/graph.py       # The Main Orchestrator
touch src/utils.py       # Helper functions

# 3. Create Agent Files
echo "Creating agent files..."
touch src/agents/__init__.py
touch src/agents/analyst.py     # Agent 1: JD Parser
touch src/agents/summary.py     # Agent 2: Profile Writer
touch src/agents/experience.py  # Agent 3: Experience Architect
touch src/agents/projects.py    # Agent 4: Project Matchmaker
touch src/agents/skills.py      # Agent 5: Skill Ranker
touch src/agents/evaluator.py   # The "Matcher" / Critic

# 4. Success Message
echo "✅ Architecture created successfully!"
echo "-------------------------------------"
echo "Your 'src' folder now looks like this:"
find src -maxdepth 2 -not -path '*/.*'