# StudyBuddy AI

StudyBuddy AI is a local-first study assistant for Häme University of Applied Sciences students. It uses an Ollama-hosted language model to explain concepts, summarize pasted or uploaded notes, create practice quizzes, and draft flashcards grounded in retrieved course material.

## Team members

- Emmi Myrskyranta (emmi.myrskyranta@student.hamk.fi)
- Md Firoz Chowdhury (mdfiroz.chowdhury@student.hamk.fi)
- Bishnu Chaudhary (bishnu.chaudhary@student.hamk.fi)

## Problem

### Intended users
Students of Häme University of Applied Sciences.

### Problem statement
Students face a lot of scheduling conflicts in their studies due to a large amount of projects, assignments and materials to study. Manually making flashcards, practice quizzes and summaries for one's studies takes away hours that the student could use more efficiently. 

### Why AI is appropriate
This project requires AI and LLM's (Large Language Models) because studying is semantic, creative and unstructured and traditional deterministic software, e.g. databases or keyword search engines, rely on rules, exact matches and structured data. Traditional software works great in storing data and organizing it but AI is required to comprehend and synthesize and generate knowledge from said data. Without AI, this project's application would only be an expensive document storage solution rather than a usable study planner.

## Solution

StudyBuddy AI provides a focused interface for students to upload course materials or paste notes and request source-grounded explanations, quizzes, summaries, and flashcards. Retrieved excerpts inform the local Ollama model, reducing preparation time while keeping answers tied to the student's material. Important facts should still be verified against course sources.

## Main user workflow

1. **Upload:** The user adds TXT, Markdown, PDF, or DOCX course material in the Gradio interface.
2. **Retrieve:** The application extracts and indexes the document text, then selects relevant excerpts for each question.
3. **Study:** The user chooses a mode, such as Quiz me, and continues in a chat session.
4. **Respond:** The service layer grounds the prompt in retrieved excerpts; the Ollama model generates a response with source references.

## Architecture

The document retrieval path augments the baseline architecture:

```text
User
  ↓
Gradio UI (app/ui.py) ── upload ──> Document parsing and lexical retrieval
  ↓
Application / AI Service (src/services/ai_service.py) <── source excerpts
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM Server)
```

> **Core Architectural Rule:** The user interface must NEVER communicate directly with the model client or Ollama. All interactions must pass through the service layer (`ai_service.py`).

## Model

- **Model used by default:** Meta Llama 3.2 (`llama3.2`) served locally through Ollama; override with `MODEL_NAME`.
- **Selection rationale:** A compact instruction-tuned model is practical for local inference on student hardware and keeps study prompts on the user's machine. Response quality and speed depend on the selected model and available hardware.
- **Model interaction:** The Ollama Python client sends chat prompts with a configurable timeout; failures and missing models are returned as friendly application messages.

## Additional AI capability

Implemented capability:

- [x] RAG (Retrieval-Augmented Generation)
- [ ] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [x] Other: Task-specific study modes (explain, quiz, summarize, and flashcards)

### Capability justification
StudyBuddy implements lightweight RAG for uploaded course materials. It extracts and chunks text from TXT, Markdown, PDF, and DOCX files, ranks relevant chunks for each request, and passes them to the model through the AI service with source labels and grounding instructions. This encourages document-based answers but cannot eliminate hallucinations, so students should verify important information against the cited material.

Uploads are held for the active Gradio session and are not saved to a project database. Scanned PDFs without selectable text are not supported because OCR is not included.

Task-specific study modes and session conversation history support continued explanations and quiz turns while keeping prompt construction in the application service rather than the UI.

## Setup

### 1. Create the Conda environment (Python 3.12)

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate dev-ai-project
```

### 3. Configure environment variables (optional)

Copy `.env.example` to create your local `.env` configuration file:

On Linux / macOS:
```bash
cp .env.example .env
```

On Windows (Command Prompt / PowerShell):
```powershell
copy .env.example .env
```

Defaults work for a standard local Ollama installation. To customize, set values in `.env`:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2
MODEL_TIMEOUT_SECONDS=120
MAX_PROMPT_CHARS=16000
```

`MODEL_TIMEOUT_SECONDS` bounds each model request. `MAX_PROMPT_CHARS` rejects excessively large prompts before inference.

### 4. Start Ollama

Make sure Ollama is installed and running locally, then pull your configured model:

```bash
ollama pull llama3.2
```

Ollama must remain running in the background. If you selected another model, pull that model instead.

### 5. Run the application

From the repository root, launch the application:

```bash
python -m app.main
```

Then open your browser at `http://localhost:7860`.

The UI delegates study prompts to the application service; only the model client communicates with Ollama. Document extraction and retrieval are local. Requests and inference are local by default, but the model provider and local Ollama deployment still determine data handling.

### 6. Run automated tests

```bash
pytest
```

## Evaluation

Run fast, model-independent regression tests with `pytest`. For live evaluation against the configured Ollama model, run `python -m evaluation.run_evaluation`; the script saves actual responses and connection-level results to `evaluation/latest_run.json`. Review the outputs manually for relevance, factuality, age-appropriateness, and instruction-following; successful inference is not a semantic-quality pass.

Refer to [`evaluation/README.md`](evaluation/README.md) for guidelines on defining success, edge cases, and failure scenarios.

## Known limitations

- Uploaded documents and conversation history are session-local and are not persisted after the session ends.
- Scanned PDFs need OCR; OCR is not included. RAG retrieval can miss relevant passages or rank less relevant text.
- Model responses can be incorrect or inconsistent; verify important facts with course materials.
- Local inference speed and quality depend on the selected model and device.

## Future improvements

- List planned feature enhancements, architectural refactorings, or future capabilities.
