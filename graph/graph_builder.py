from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from graph.nodes.tool_nodes import get_schema_node, execute_sql_node
from graph.nodes.llm_nodes import sql_generator_node, insight_generator_node


def router_edge(state: GraphState) -> str:
    # If error exists and we haven't hit retry limit, loop back
    if state.get("sql_error") and state.get("retry_count", 0) < 3:
        return "sql_generator"
    # End the loop to prevent infinite token burn
    elif state.get("sql_error") and state.get("retry_count", 0) >= 3:
        return "max_retries_reached"
    # If no error, proceed to final answer
    return "insight_generator"

def build_graph():
    workflow = StateGraph(GraphState)

    # Register Nodes
    workflow.add_node("get_schema", get_schema_node)
    workflow.add_node("sql_generator", sql_generator_node)
    workflow.add_node("execute_sql", execute_sql_node)
    workflow.add_node("insight_generator", insight_generator_node)
    

    # Wire Standard Edges
    workflow.add_edge(START, "get_schema")
    workflow.add_edge("get_schema", "sql_generator")
    workflow.add_edge("sql_generator", "execute_sql")
    
    # Wire Conditional Edges for Self-Correction Loop
    workflow.add_conditional_edges(
        "execute_sql",
        router_edge,
        {
            "sql_generator": "sql_generator",           
            "insight_generator": "insight_generator",   
            "max_retries_reached": END                  
        }
    )
    workflow.add_edge("insight_generator", END)

    return workflow.compile()

app = build_graph()

print(app)

