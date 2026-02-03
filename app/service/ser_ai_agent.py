import json
from app.core.agent_prompt import AGENT_SYSTEM_PROMPT, build_agent_prompt
from app.core.azure_openai_chat import chat_completion

async def decide_action(question: str) -> dict:
    resp = await chat_completion(
        AGENT_SYSTEM_PROMPT,
        build_agent_prompt(question),
    )

    try:
        return json.loads(resp)
    except Exception:
        # hard fallback: always search
        return {"action": "search", "reason": "failed to parse agent output"}
