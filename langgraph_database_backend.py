import os
import sqlite3
from dotenv import load_dotenv
from typing import TypedDict, Annotated
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
# pyrefly: ignore [missing-import]
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

# SQLite checkpointer (persists across restarts)
conn = sqlite3.connect("chatbot_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

conn.execute("""
CREATE TABLE IF NOT EXISTS chat_titles (
    thread_id TEXT PRIMARY KEY,
    title TEXT NOT NULL
)
""")

conn.commit()

graph = StateGraph(ChatState)

# Nodes
graph.add_node('chat_node', chat_node)

# Edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# Compile graph
chatbot = graph.compile(checkpointer=checkpointer)
chatBot = chatbot  # alias for convenience


def retrieve_all_thread():
    all_thread = set()

    for checkpoint in checkpointer.list(None):
        all_thread.add(
            checkpoint.config['configurable']['thread_id']
        )

    return list(all_thread)


