# 🤖 Autonomous Text-to-SQL Analyst

An enterprise-grade, multi-agent Text-to-SQL pipeline built with **LangGraph**, **LangChain**, **FastAPI**, and **Streamlit**. 

This system enables non-technical business users to query relational databases using natural language. Unlike standard LLM wrappers that crash when databases throw syntax errors, this architecture utilizes a genuine cyclic state machine to autonomously write SQL, execute it securely against a local SQLite database, catch its own syntax errors, and self-correct without human intervention.

## ✨ Key Features
* **Cyclic Error-Correction Loop:** If the database throws a syntax error, the agent intercepts the exact error message and loops back to rewrite the query, utilizing a retry limit to prevent infinite loops.
* **Deterministic Security Guardrails:** Database execution is strictly isolated in a deterministic Python node, utilizing a regex check to block destructive DDL statements like `DROP` or `DELETE` before execution[cite: 1].
* **Explicit State Management:** Uses LangGraph's `TypedDict` to explicitly control the flow of variables—including the database schema, generated queries, error strings, and retry counts—between nodes[cite: 1].
* **Full-Stack Decoupled Architecture:** A FastAPI backend orchestrates the LangGraph agents and exposes API endpoints, while a Streamlit frontend provides an intuitive chat interface and renders the resulting data tables[cite: 1].
* **Observability:** Native integration with LangSmith to trace state changes, visualize conditional routing, and monitor prompt performance[cite: 1].

## 🏗️ Architecture Flow

```text
START ──→ Schema Extractor (Deterministic) ──→ SQL Generator (LLM) ──→ DB Executor (Deterministic)
                                                  ↑                                │
                                                  └─────────(If SQL Error)─────────┘
                                                                                   │ (If Success)
                                                                                   ↓
                                                                Insight Generator (LLM) ──→ END