from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from graph.state import GraphState
from graph.prompts import sql_prompt, insight_prompt

load_dotenv()

# We use gpt-4o-mini as it is highly cost-effective and performs exceptionally well on SQL tasks
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def sql_generator_node(state: GraphState) -> dict:
    chain = sql_prompt | llm
    result = chain.invoke({
        "db_schema": state.get("db_schema", ""),
        "user_query": state.get("user_query", ""),
        "sql_error": state.get("sql_error", "None")
    })
    
    # Strip markdown block formatting if present
    clean_sql = result.content.replace("```sql", "").replace("```", "").strip()
    return {"sql_query": clean_sql}

def insight_generator_node(state: GraphState) -> dict:
    chain = insight_prompt | llm
    result = chain.invoke({
        "user_query": state.get("user_query", ""),
        "raw_data": state.get("raw_data", [])
    })
    return {"final_answer": result.content}