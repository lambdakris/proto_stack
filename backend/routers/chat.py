from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import os
import json

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

# Initialize the LLM with streaming enabled
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.7,
    streaming=True
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

@router.post("")
async def chat(message: ChatMessage):
    """
    Chat endpoint that provides streaming AI assistant responses using LangGraph and OpenAI.
    
    This implements a simple conversational AI that streams responses token-by-token.
    For multi-turn conversations with persistent state, additional session management would be needed.
    """
    async def generate_stream():
        """
        Generator function that streams the response from LangGraph.
        Uses the 'messages' stream mode to get message updates.
        """
        # Stream the graph with the user's message
        async for event in graph.astream({
            "messages": [("user", message.message)]
        }, stream_mode="messages"):
            # event is a tuple of (message, metadata)
            # We only want the message content chunks
            msg, metadata = event
            
            # Only stream content from AIMessage (not HumanMessage)
            if hasattr(msg, 'content') and msg.content:
                # Stream each chunk as a JSON line
                chunk_data = {"content": msg.content}
                yield f"data: {json.dumps(chunk_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
