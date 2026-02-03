import pytest
from app.agent.age_brain import decide_next_action


@pytest.mark.asyncio
async def test_brain_tool_selection():
    """
    Test that the brain correctly identifies a dividend query.
    """
    messages = [{"role": "user", "content": "What is the yield for MSFT?"}]

    # We test the pure reasoning unit
    decision = await decide_next_action(messages)

    # Production expectation: It must call the tool
    assert "tool" in decision
    assert decision["tool"] == "get_dividend_data"
    assert "MSFT" in decision["tool_input"]


@pytest.mark.asyncio
async def test_brain_direct_answer():
    """
    Test that the brain doesn't use tools for greetings.
    """
    messages = [{"role": "user", "content": "Hello, bot!"}]
    decision = await decide_next_action(messages)

    assert "answer" in decision
    assert "tool" not in decision
