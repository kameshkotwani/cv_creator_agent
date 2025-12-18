"""
Fake LLM implementations for testing purposes.

These provide mock language model runnables that return predefined outputs
or raise exceptions, useful for unit testing without calling actual LLMs.

"""
# tests/helpers/fakes.py
from langchain_core.runnables import RunnableLambda

def fake_json_llm(json_text: str):
    # Works with JsonOutputParser
    return RunnableLambda(lambda _input: json_text)

def fake_text_llm(text: str):
    # Works with StrOutputParser
    return RunnableLambda(lambda _input: text)

def fake_fail_llm(msg: str = "boom"):
    def _raise(_input):
        raise RuntimeError(msg)
    return RunnableLambda(_raise)

