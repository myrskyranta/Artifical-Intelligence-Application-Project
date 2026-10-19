# Architecture Documentation

This document describes the baseline architectural layer of the application and provides guidance on extending it for your team project.

## Baseline Architecture

The application separates presentation, study prompt orchestration, and model transport:

```text
User
  ↓
Gradio UI (app/ui.py: rendering and input handling)
  ↓
Application Service (src/services/ai_service.py: validation, mode instructions, friendly errors)
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local Inference Server)
  ↓
Local Model (default: llama3.2; configured via MODEL_NAME)
```

### Core Design Rules

1. **Strict UI Isolation:** The Gradio user interface (`app/ui.py`) MUST NOT directly instantiate `OllamaModelClient` or make direct API calls to Ollama. It delegates all operations to `generate_response()` in `src/services/ai_service.py`.
2. **Controlled Failure Handling:** The model client handles low-level runtime exceptions (e.g., connection errors or missing models). The service layer converts technical exceptions into structured, user-understandable responses.
3. **Data Schemas:** Request inputs and response structures are validated using Pydantic models in `src/schemas/responses.py`.
4. **Bounded model calls:** The Ollama client's HTTP timeout is configurable with `MODEL_TIMEOUT_SECONDS`. Connection, timeout, missing-model, empty-response, and other client failures are normalized for the service layer.
5. **No implicit RAG:** Current inputs are supplied directly by the student. File upload, indexing, retrieval, persistent memory, and conversation history are not implemented.

---

## Extension Points for Course Projects

As your project team designs and implements your additional AI capability, extend this baseline architecture. Potential capability extensions include:

- **RAG (Retrieval-Augmented Generation):** Insert document parsing, chunking, vector embeddings, and vector database retrieval into the service layer to ground model responses in domain documents.
- **Tools & External APIs:** Integrate tool execution functions into the service layer allowing the model to query web services or local python utilities.
- **Model Context Protocol (MCP):** Connect your service layer to standard MCP servers to access external tools and context providers.
- **Agent Workflows:** Implement observation-action loops controlled by application code to handle dynamic multi-step tasks.
- **Memory & Conversation State:** Store session history or persistent state across user interactions.
- **Multimodal Models:** Update the model client and UI payload to pass image data to vision-enabled local models.

Study-mode prompt construction belongs to the service layer, keeping application behavior testable without launching Gradio or requiring an Ollama server. Tests inject mock model clients; live model evaluation is run separately using the representative cases in `evaluation/test_cases.json`.
