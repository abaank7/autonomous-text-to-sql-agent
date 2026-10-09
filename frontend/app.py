import streamlit as st
import requests

st.set_page_config(page_title="SQL Data Analyst", layout="centered")
st.title("🤖 Autonomous Text-to-SQL Analyst")
st.markdown("Ask natural language questions. The agent generates SQL, catches syntax errors, self-corrects, and fetches data.")

API_URL = "http://127.0.0.1:8000/ask"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("E.g., 'What are our top products by category?'")



if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing schema and generating/testing SQL..."):
            try:
                response = requests.post(API_URL, json={"query": user_input})
                response.raise_for_status()
                data = response.json()
                
                if data.get("error"):
                    st.error(f"Failed to query database: {data['error']}")
                    answer = "I could not resolve the SQL query."
                else:
                    st.success("Query Executed Successfully!")
                    st.code(data.get("sql_query"), language="sql")
                    if data.get("raw_data"):
                        st.dataframe(data["raw_data"])
                    st.write(data.get("answer"))
                    answer = data.get("answer")
                    
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except requests.exceptions.RequestException:
                st.error("Cannot connect to API. Is FastAPI running? (uvicorn backend.api:app --reload)")