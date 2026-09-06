from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import add_messages
import sqlite3
# pyrefly: ignore [missing-import]
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import os

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

# SQLite checkpointer
conn = sqlite3.connect("chatbot_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
graph = StateGraph(ChatState)

# Nodes
graph.add_node('chat_node', chat_node)

# Edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# Compile graph
chatbot = graph.compile(checkpointer=checkpointer)
chatBot = chatbot

CONFIG = {'configurable': {'thread_id': 'thread-1'}}
response = chatbot.invoke({'messages': [HumanMessage(content='hi, i am Saurabh')]}, config=CONFIG)

#EXTRACTS VALues basically messages from any thread_id like this
print(chatbot.get_state(config=CONFIG).values['messages'])

