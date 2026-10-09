from pydantic import BaseModel
from typing import Optional, List, Any

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sql_query: Optional[str] = None
    raw_data: Optional[List[Any]] = None
    error: Optional[str] = None