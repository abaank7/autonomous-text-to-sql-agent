from langchain_core.prompts import ChatPromptTemplate

SQL_SYSTEM_PROMPT = """You are an expert SQL coder. Given this schema:
{db_schema}

Write a SQLite query for this user query: {user_query}.
If you see an error from a previous attempt: {sql_error}, fix your query.
Return strictly the SQL string, nothing else."""

INSIGHT_SYSTEM_PROMPT = """The user asked: {user_query}.
The database returned this raw data: {raw_data}.
Write a short, friendly summary answering the question directly based on the data."""

sql_prompt = ChatPromptTemplate.from_messages([("system", SQL_SYSTEM_PROMPT)])
insight_prompt = ChatPromptTemplate.from_messages([("system", INSIGHT_SYSTEM_PROMPT)])