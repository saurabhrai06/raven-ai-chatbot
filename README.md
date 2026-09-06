# 🐦 RAVEN AI — Conversational AI Chatbot

RAVEN AI is a conversational AI chatbot built with **LangGraph, LangChain, Groq, Streamlit, and SQLite**.

The project focuses on building a production-style conversational system with **persistent conversation memory, multiple chat threads, streaming responses, and an interactive frontend**.

---

## 🚀 Features

- 🤖 Conversational AI powered by an LLM
- 🧠 Persistent conversation memory
- 🧵 Multiple conversation threads
- 🔄 Switch between previous conversations
- 🆕 Create new conversations dynamically
- 🏷️ AI-generated conversation titles
- ⚡ Streaming AI responses
- 💾 SQLite-based persistence
- 🕸️ LangGraph-based chatbot workflow
- 🎨 Custom Streamlit frontend
- 🔐 Environment variables for API key management
- 🆔 UUID-based thread management

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │                     │
                    │ • Chat interface    │
                    │ • Conversations     │
                    │ • Streaming         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     LangGraph       │
                    │                     │
                    │ • State management  │
                    │ • Message flow      │
                    │ • Checkpointing     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Groq LLM      │
                    │                     │
                    │  openai/gpt-oss-120b│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       SQLite        │
                    │                     │
                    │ • Chat history      │
                    │ • Thread state      │
                    └─────────────────────┘


raven-ai-chatbot/

│

├── langgraph_bot.py

├── langgraph_database_backend.py

│

├── streamlit_frontend.py

├── streamlit_frontend_streaming.py

├── streamlit_frontend_threading.py

├── streamlit_database_frontend.py

│

├── Langraph_bot.ipynb

│

├── .gitignore

├── README.md

│

└── chatbot_memory.db


git clone https://github.com/saurabhrai06/raven-ai-chatbot.git
cd raven-ai-chatbot
python3 -m venv myenv
source myenv/bin/activate
