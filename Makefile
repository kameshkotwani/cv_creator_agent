# Variables
PYTHON = python3
PIP = pip

# The .PHONY rule tells make that these are commands, not files
.PHONY: help install run test_analyst test_summary test_experience clean

# Default target: Print help
help:
	@echo "🤖 AI CV BUILDER - COMMANDS"
	@echo "==========================="
	@echo "Setup:"
	@echo "  make install         : Install requirements.txt"
	@echo ""
	@echo "Run App:"
	@echo "  make run             : Start the Streamlit Dashboard"
	@echo ""
	@echo "Testing Agents:"
	@echo "  make test_analyst    : Test JD Analyst Agent (Step 1)"
	@echo "  make test_summary    : Test Summary Agent (Isolated Mock)"
	@echo "  make test_summary_jd : Test Summary Agent (Integration with JD)"
	@echo "  make test_experience : Test Experience Agent"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean           : Remove __pycache__ and temp files"

# --- SETUP ---
install:
	$(PIP) install uv
	uv sync

# --- RUNNING THE APP ---
run:
	streamlit run app.py

# Running Agents
run_graph:
	$(PYTHON) -m src.graph

# --- TESTING AGENTS ---
test_nodes:
	pytest -q -s tests.test_nodes_contract

test_smoke:
	pytest  -s -m smoke

test_llm:
	pytest -s -m llm 


# --- CLEANUP ---
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f *.pdf
	rm -f *.log
	rm -f *.aux