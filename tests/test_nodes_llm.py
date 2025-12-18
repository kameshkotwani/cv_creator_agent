from tests.node_cases import NODE_CASES
from tests.helpers.state_factory import make_state
import pytest
import json
from src.utils import get_ollma_llm


@pytest.mark.node
@pytest.mark.parametrize("case", NODE_CASES, ids=lambda c: c["name"])
def test_node_real_llm(case):
    llm = get_ollma_llm()

    state = make_state(**case["min_state"])

    patch = case["fn"](state, llm=llm)

    assert not patch.get("error")

    print(f"\nNODE: {case['name']}\n{json.dumps(patch, indent=2, ensure_ascii=False)}")
