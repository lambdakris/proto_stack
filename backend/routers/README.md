# Backend Routers

This directory contains FastAPI routers that organize the API endpoints by feature.

## Chat Router (`chat.py`)

The chat router implements a LangGraph-based conversational AI using OpenAI's GPT models.

### Architecture

```
User Message → FastAPI Router → LangGraph StateGraph → OpenAI LLM → Response
```

### LangGraph Flow

```
START
  ↓
[chatbot node]
  ↓ (invokes OpenAI)
  ↓
END
```

### Key Components

- **State**: Manages conversation messages using LangGraph's message history
- **LLM**: ChatOpenAI with gpt-4o-mini model (configurable)
- **Graph**: Simple linear flow that can be extended with additional nodes

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

## Future Routers

Additional routers can be added for:
- User management (`users.py`)
- Authentication (`auth.py`)
- Analytics (`analytics.py`)
- Admin operations (`admin.py`)
