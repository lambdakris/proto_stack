# Backend Routers

This directory contains FastAPI routers that organize the API endpoints by feature.

## Chat Router (`chat.py`)

The chat router implements a LangGraph-based conversational AI using OpenAI's GPT models with **streaming support**.

### Architecture

```
User Message → FastAPI Router → LangGraph StateGraph → OpenAI LLM (streaming) → SSE Response
```

### LangGraph Flow

```
START
  ↓
[chatbot node]
  ↓ (streams from OpenAI)
  ↓
END
```

### Streaming Implementation

The chat endpoint uses:
- **LangGraph's `.astream()` method** with `stream_mode="messages"` for token-by-token streaming
- **FastAPI's `StreamingResponse`** to send Server-Sent Events (SSE)
- **OpenAI's streaming mode** enabled in the ChatOpenAI client

This provides real-time token-by-token response streaming for a better user experience.

### Key Components

- **State**: Manages conversation messages using LangGraph's message history
- **LLM**: ChatOpenAI with gpt-4.1-mini model (streaming enabled)
- **Graph**: Simple linear flow that can be extended with additional nodes
- **Streaming**: Server-Sent Events (SSE) format for real-time responses

### Configuration

Set the `OPENAI_API_KEY` environment variable in the `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

### Extending the Chatbot

The LangGraph architecture makes it easy to add:

1. **Conversation Memory**: Add a checkpointer to maintain state across requests
2. **RAG (Retrieval Augmented Generation)**: Add a retrieval node before the chatbot
3. **Tool Calling**: Add tool nodes for external API calls
4. **Multi-Agent**: Add specialized agent nodes for different tasks
5. **Guardrails**: Add validation nodes for content filtering

### Example Extension

```python
# Add a retrieval node for RAG
def retrieve_context(state: State):
    query = state["messages"][-1].content
    docs = vector_store.similarity_search(query)
    return {"context": docs}

graph_builder.add_node("retrieve", retrieve_context)
graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "chatbot")
```

### Streaming Details

The endpoint uses LangGraph's message streaming mode:
- Streams individual tokens as they're generated
- Uses Server-Sent Events (SSE) format
- Each event contains a JSON payload with the content chunk
- Frontend can display tokens in real-time using `st.write_stream()`

## Future Routers

Additional routers can be added for:
- User management (`users.py`)
- Authentication (`auth.py`)
- Analytics (`analytics.py`)
- Admin operations (`admin.py`)
