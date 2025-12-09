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
	$(PIP) install -r requirements.txt

# --- RUNNING THE APP ---
run:
	streamlit run app.py

# Running Agents
run_graph:
	$(PYTHON) -m src.graph

# --- TESTING AGENTS ---

# Analyst Agent (Mapped to the file we created: tests/test_step1.py)
test_analyst:
	$(PYTHON) -m tests.test_analyst

# Summary Agent Isolated (Mapped to: tests/test_summary_isolated.py)
test_summary:
	$(PYTHON) -m tests.test_summary


# Experience Agent (Mapped to: tests/test_step3.py)
test_experience:
	$(PYTHON) -m tests.test_experience

# Experience Agent (Mapped to: src/experience.py)
experience:
	$(PYTHON) -m src.agents.experience

# --- CLEANUP ---
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f *.pdf
	rm -f *.log
	rm -f *.aux