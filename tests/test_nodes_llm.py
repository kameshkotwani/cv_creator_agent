import json
import os

import pytest

from src.utils import get_ollma_llm
from tests.helpers.state_factory import make_state
from tests.node_cases import NODE_CASES


@pytest.mark.node
@pytest.mark.parametrize("case", NODE_CASES, ids=lambda c: c["name"])
def test_node_real_llm(case):
    # Safety gate to not run this test in CI/CD
    if os.getenv("RUN_LLM_TESTS") != "1":
        pytest.skip("Set RUN_LLM_TESTS=1 to run real LLM tests")
    llm = get_ollma_llm()

    state = make_state(**case["min_state"])

    patch = case["fn"](state, llm=llm)

    assert not patch.get("error")

    print(f"\nNODE: {case['name']}\n{json.dumps(patch, indent=2, ensure_ascii=False)}")
