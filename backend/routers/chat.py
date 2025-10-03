from fastapi import APIRouter
from pydantic import BaseModel
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import os

# Router setup
router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# Pydantic Models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# LangGraph State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.7
)

# Define the chatbot node
def chatbot(state: State):
    """
    Simple chatbot node that calls the LLM with the conversation history.
    """
    return {"messages": [llm.invoke(state["messages"])]}

# Build the LangGraph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

@router.post("", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat endpoint that provides AI assistant responses using LangGraph and OpenAI.
    
    This implements a simple conversational AI that maintains context within a single request.
    For multi-turn conversations with persistent state, additional session management would be needed.
    """
    # Invoke the graph with the user's message
    result = graph.invoke({
        "messages": [("user", message.message)]
    })
    
    # Extract the assistant's response
    assistant_message = result["messages"][-1].content
    
    return ChatResponse(response=assistant_message)
