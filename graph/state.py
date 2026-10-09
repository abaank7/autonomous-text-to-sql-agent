from typing import TypedDict, Optional, List, Any

class GraphState(TypedDict):
    user_query: str
    db_schema: str
    sql_query: Optional[str]
    sql_error: Optional[str]
    retry_count: int
    raw_data: Optional[List[Any]]
    final_answer: str

