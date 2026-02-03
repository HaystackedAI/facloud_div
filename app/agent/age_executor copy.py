import json
from app.agent.age_brain import decide_next_action
from app.agent.age_tools import get_dividend_data_tool
from app.core.ai_logging import log_event

async def run_agent_executor(question: str, trace_id: str):
    messages = [{"role": "user", "content": question}]
    max_turns = 3 
    
    for turn in range(max_turns):
        # 1. THINK
        decision = await decide_next_action(messages)
        log_event("agent_thought", trace_id=trace_id, turn=turn, decision=decision)

        # 2. FINISH if agent is ready
        if "answer" in decision:
            return decision["answer"]

        # 3. ACT if tool requested
        if decision.get("tool") == "get_dividend_data":
            tool_result = await get_dividend_data_tool(decision["tool_input"])
            
            # 4. OBSERVE (Add tool output back to conversation)
            messages.append({"role": "assistant", "content": json.dumps(decision)})
            messages.append({"role": "system", "content": f"Observation: {json.dumps(tool_result)}"})
            
            # If there was an error, the next 'decide_next_action' will see it and self-correct
            log_event("tool_observation", trace_id=trace_id, turn=turn, success="error" not in tool_result)

    return "I reached the maximum reasoning steps without a clear answer."