from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import add_messages
from langgraph.checkpoint.memory import MemorySaver
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

checkpointer = MemorySaver()
graph = StateGraph(ChatState)

# Nodes
graph.add_node('chat_node', chat_node)

# Edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# Compile graph
chatbot = graph.compile(checkpointer=checkpointer)
chatBot = chatbot  # alias for convenience
