import json
from time import time
import uuid
from app.agent.agent_loop import run_agent_loop
from app.core.ai_logging import log_event
from app.core.azure_openai_chat import chat_completion
from app.service.ser_ai_rag import rag_query

async def run_agent_executor(question: str):
    # 1. Ask the "Brain" what to do
    trace_id = f"tr-{uuid.uuid4().hex[:8]}" # Short, unique trace ID
    start_time = time.perf_counter()
    
    log_event("agent_request_received", trace_id, question=question)

    # 1. Brain Decision
    decision = await run_agent_loop(question)
    log_event("agent_decision", trace_id, decision=decision)
    
    # 2. Tool Execution
    rag_response = None
    if "tool" in decision and decision["tool"] == "get_dividend_data":
        print(f"Executing tool with input: {decision['tool_input']}")
        
        # Call your existing RAG without changing a single line of it
        # We pass the 'tool_input' (the refined query) to your RAG
        rag_result = await rag_query(question=decision["tool_input"], top_k=3)
        
        # 3. Final Polish: Give the tool results back to the LLM
        # In production, this ensures the answer sounds natural and is grounded in the data
        final_prompt = f"""
        The user asked: {question}
        Based on the retrieval tool, we found this data: {rag_result['answer']}
        Sources used: {rag_result['sources']}
        
        Provide a concise final answer to the user.
        """
        
        final_answer = await chat_completion(
            system_prompt="You are a helpful financial assistant.",
            user_prompt=final_prompt
        )
        
        return {
            "answer": final_answer,
            "intermediate_steps": decision, # For production logging
            "raw_rag_data": rag_result
        }

    # 4. Handle Direct Answer (Greetings, etc.)
    return {"answer": decision.get("answer"), "intermediate_steps": decision}