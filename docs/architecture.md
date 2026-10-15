# Architecture Documentation

This document describes the baseline architectural layer of the application and provides guidance on extending it for your team project.

## Baseline Architecture

The starter application follows a clean layered separation of concerns:

```text
User
  ↓
Gradio UI (app/ui.py) ── uploads ──> Document parser and lexical index
  ↓
Application / AI Service (src/services/ai_service.py) <── retrieved chunks
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local Inference Server)
  ↓
Local Model (e.g., llama3.2)
```

### Core Design Rules

1. **Strict UI Isolation:** The Gradio user interface (`app/ui.py`) MUST NOT directly instantiate `OllamaModelClient` or make direct API calls to Ollama. It delegates all operations to `generate_response()` in `src/services/ai_service.py`.
2. **Controlled Failure Handling:** The model client handles low-level runtime exceptions (e.g., connection errors or missing models). The service layer converts technical exceptions into structured, user-understandable responses.
3. **Data Schemas:** Request inputs and response structures are validated using Pydantic models in `src/schemas/responses.py`.

---

## Uploaded study materials (RAG)

The UI accepts TXT, Markdown, PDF, and DOCX materials. The RAG capability in `src/capabilities/rag.py` extracts text, chunks it, and ranks chunks with local lexical retrieval. The selected excerpts and their source labels are passed to the AI service, which adds grounding instructions before calling the model. The in-memory index is scoped to the active Gradio session; scanned PDFs require OCR and are not supported.

Conversation turns are kept in the Gradio chat session so quiz answers can be evaluated in context. The model is instructed to treat document content as reference material rather than as instructions. Grounding reduces unsupported answers but does not guarantee correctness.

## Further extension points

Other capabilities can be added later:

- **Tools & External APIs:** Integrate tool execution functions into the service layer allowing the model to query web services or local python utilities.
- **Model Context Protocol (MCP):** Connect your service layer to standard MCP servers to access external tools and context providers.
- **Agent Workflows:** Implement observation-action loops controlled by application code to handle dynamic multi-step tasks.
- **Persistent Memory:** Store approved session history or study progress across application restarts.
- **Multimodal Models:** Update the model client and UI payload to pass image data to vision-enabled local models.
