# Project decisions

Use this decision log to document significant technical and architectural choices made by your team during development.

## Decision 1 — Model selection

**Decision:** Use Meta Llama 3.2 (`llama3.2`) through Ollama by default, with `MODEL_NAME` available to select another locally installed model.

**Alternatives considered:** Hosted API models and larger local models.

**Why we chose this:** A compact instruction-following model enables local inference without requiring a paid hosted API; users can trade speed and quality by choosing a different local model.

---

## Decision 2 — Additional AI capability

**Decision:** Implement task-specific study modes (concept explanation, quiz, summary, flashcards) as service-layer prompt instructions. RAG is not implemented in this release.

**Why it is needed:** Students can use one model for common study activities while keeping prompt construction out of the UI.

**Alternatives considered:** File upload and RAG, persistent conversation memory, external tools. These are future work and are not advertised as current features.

---

## Decision 3 — Architecture

**Decision:** Keep Gradio presentation, AI orchestration, Ollama transport, and request/response schemas in separate layers.

**Why:** The service can be tested with mock clients, and transport failures are translated to predictable user-facing messages.
