from app.service.ser_ai_rag import rag_query

async def get_dividend_data_tool(tool_input: str):
    """
    Wrapper for the RAG service to ensure standardized output for the agent.
    """
    try:
        result = await rag_query(question=tool_input, top_k=3)
        
        if not result.get("sources"):
            return {"error": "No data found for this query in the dividend database."}
            
        return {
            "data": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        return {"error": f"Tool execution failed: {str(e)}"}