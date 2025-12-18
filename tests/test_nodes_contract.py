import pytest
from tests.helpers.state_factory import make_state
from tests.node_cases import NODE_CASES
from tests.helpers.fakes import fake_fail_llm

@pytest.mark.parametrize("case", NODE_CASES, ids=lambda c: c["name"])
def test_node_happy_path(case):
    state = make_state(**case["min_state"])
    patch = case["fn"](state, llm=case["fake_llm"])

    assert isinstance(patch, dict)
    assert not patch.get("error")

    for k in case["expected_keys"]:
        assert k in patch

@pytest.mark.parametrize("case", NODE_CASES, ids=lambda c: c["name"])
def test_node_failure_sets_error(case):
    state = make_state(**case["min_state"])
    patch = case["fn"](state, llm=fake_fail_llm("boom"))

    assert patch.get("error") == "boom"
