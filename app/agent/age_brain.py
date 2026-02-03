import json
from app.core.azure_openai_chat import chat_completion

async def decide_next_action(messages: list) -> dict:
    """
    Pure reasoning unit. No execution logic here.
    """
    system_message = {
        "role": "system", 
        "content": "You are a Financial Agent. Respond ONLY in JSON with 'thought' and either 'tool/tool_input' or 'answer'."
    }
    
    # Prepend system message if not present
    if messages[0]["role"] != "system":
        messages.insert(0, system_message)

    response_text = await chat_completion(
        system_prompt=messages[0]["content"],
        user_prompt=messages[-1]["content"] 
        # Note: In production, you'd pass the full 'messages' list 
        # to chat.completions.create directly for full context.
    )
    
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"thought": "JSON parse error", "answer": response_text}