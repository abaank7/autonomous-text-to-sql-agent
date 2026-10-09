import pytest
from graph.graph_builder import app

def test_basic_query():
    initial_state = {
        "user_query": "List all gaming products.",
        "retry_count": 0,
        "sql_error": None
    }
    result = app.invoke(initial_state)
    
    assert result.get("sql_query") is not None
    assert result.get("raw_data") is not None
    assert result.get("final_answer") is not None