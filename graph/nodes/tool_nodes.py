import sqlite3
from graph.state import GraphState

DB_PATH = "database/retail_shop.db"

# function to get the database schema
def get_schema_node(state: GraphState) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schema = "\n\n".join([row[0] for row in cursor.fetchall() if row[0]])
    conn.close()
    return {"db_schema": schema}

# Function that ONLY executes the ALLOWED SQL CODE : SECURITY
def execute_sql_node(state: GraphState) -> dict:
    query = state["sql_query"]
    
    # Block destructive DDL statements
    if any(keyword in query.upper() for keyword in ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']):
        return {"sql_error": "Security violation. Only SELECT allowed.", "retry_count": state.get("retry_count", 0) + 1}

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return {"raw_data": data, "sql_error": None} # Success! Clear error.
    except sqlite3.Error as e:
        return {"sql_error": str(e), "retry_count": state.get("retry_count", 0) + 1} # Capture exact error string