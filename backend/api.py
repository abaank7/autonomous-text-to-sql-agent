from fastapi import FastAPI, HTTPException
from backend.models import ChatRequest, ChatResponse
from graph.graph_builder import app as agent_app


app = FastAPI(title="Text-to-SQL Analyst API")

@app.post("/ask", response_model=ChatResponse)
async def ask_database(request: ChatRequest):
    try:
        initial_state = {
            "user_query": request.query,
            "retry_count": 0,
            "sql_error": None
        }
        
        final_state = agent_app.invoke(initial_state)
        
        if final_state.get("sql_error") and final_state.get("retry_count", 0) >= 3:
            return ChatResponse(
                answer="Failed to generate a valid query after multiple attempts.",
                sql_query=final_state.get("sql_query"),
                error=final_state.get("sql_error")
            )
            
        return ChatResponse(
            answer=final_state.get("final_answer", ""),
            sql_query=final_state.get("sql_query"),
            raw_data=final_state.get("raw_data")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))