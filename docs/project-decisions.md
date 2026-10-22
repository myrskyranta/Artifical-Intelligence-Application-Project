# Project decisions

This log records the main technical and architectural choices made by the team.

## Decision 1 — Model selection

**Decision:** Use Meta Llama 3.2 (`llama3.2`) through Ollama by default, with `MODEL_NAME` available to select another locally installed model.

**Alternatives considered:** Hosted API models and larger local models.

**Why we chose this:** A compact instruction-following model runs on ordinary student laptops without a paid API, and study material stays on the user's machine. Users can trade speed for quality by choosing a different local model.

**Trade-off seen in evaluation:** The small model answered correctly when given the right passage, but often added unrelated content or unreliable citations (see `evaluation/evaluation_results.md`).

---

## Decision 2 — Additional AI capability: RAG over uploaded course materials

**Decision:** Implement retrieval-augmented generation (RAG). Students upload TXT, Markdown, PDF or DOCX files; the app extracts and chunks the text, retrieves the most relevant chunks for each question and passes them to the model with grounding instructions. Task-specific study modes (explain, quiz, summarize, flashcards) are added as prompt instructions.

**Why it is needed:** Course-specific details are not in the model's training data. In our manual check the model answered "768" for the embedding size without the notes and the correct "384" with them.

**Alternatives considered:** Pasting whole documents into the prompt (does not scale beyond short notes), persistent memory and external tools (not needed for the core study task).

---

## Decision 3 — Retrieval method: BM25 keyword ranking instead of embeddings

**Decision:** Rank chunks with a local BM25-style keyword score (`src/capabilities/rag.py`) and keep the index in memory for the session.

**Alternatives considered:** Embedding-based semantic search with a vector store such as Chroma, as in the course chapter.

**Why we chose this:** No extra model, database or download is needed, setup stays simple, and results are easy to inspect and test.

**Trade-off seen in evaluation:** Retrieval ranked the correct chunk first in 7 of 8 cases, but missed a paraphrased question that avoided the word "chunk". Hybrid or embedding retrieval is the main future improvement.

---

## Decision 4 — Architecture

**Decision:** Keep Gradio presentation, retrieval, AI orchestration, Ollama transport and request/response schemas in separate layers. The UI never calls the model client or Ollama directly.

**Why:** The service can be tested with mock clients, and transport failures become predictable user-facing messages.

---

## Decision 5 — Evaluation approach

**Decision:** Evaluate retrieval and generation separately: retrieval automatically with expected keywords, generation by human review (pass, partial, fail), using a fixed reference document so results can be reproduced.

**Why:** A wrong answer can come from retrieving the wrong passage or from misusing the right one, and the fix is different for each.
