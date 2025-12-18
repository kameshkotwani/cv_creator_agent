import pytest
from langchain_core.prompts import ChatPromptTemplate

from src.utils import template_loader


# testing template loader
@pytest.mark.parametrize(
    "name",
    [
        "analyst",
        "summary",
        "experience",
    ],
)
def test_template_loader(name):
    template = template_loader(name)
    assert isinstance(template, ChatPromptTemplate)
