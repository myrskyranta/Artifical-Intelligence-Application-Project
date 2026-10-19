# StudyBuddy AI

StudyBuddy AI is a local-first study assistant for Häme University of Applied Sciences students. It uses an Ollama-hosted language model to explain concepts, summarize pasted notes, create practice quizzes, and draft flashcards.

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

StudyBuddy AI provides a focused interface for working with course material pasted by the student. Study modes add task-specific instructions before the application sends the prompt to a locally running Ollama model. This version does not upload files, store a course library, retain conversation history, or implement RAG; students should verify generated content against their course sources.

## Main user workflow

1. **User Input:** The user submits a prompt or query via the Gradio user interface.
2. **Processing & Guardrails:** The application service layer (`src/services/ai_service.py`) validates and formats the request.
3. **Model Response:** The model client calls Ollama locally and returns the response back through the service layer to the UI.

## Architecture

Below is the initial starter architecture. As your project evolves with additional capabilities, replace or extend this diagram in [`docs/architecture.md`](docs/architecture.md).

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
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

- [ ] RAG (Retrieval-Augmented Generation; planned, not implemented)
- [ ] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [x] Other: Task-specific study modes (explain, quiz, summarize, and flashcards)

### Capability justification
Task-specific study modes make the same model useful for different learning activities while keeping prompt construction in the application service rather than the UI. RAG remains a future improvement: this release has no upload, indexing, or retrieval pipeline, and prompting alone cannot guarantee factual accuracy.

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

The UI delegates study prompts to the application service; only the model client communicates with Ollama. Requests and inference are local by default, but the model provider and local Ollama deployment still determine data handling.

### 6. Run automated tests

```bash
pytest
```

## Evaluation

Run fast, model-independent regression tests with `pytest`. For live evaluation against the configured Ollama model, run `python -m evaluation.run_evaluation`; the script saves actual responses and connection-level results to `evaluation/latest_run.json`. Review the outputs manually for relevance, factuality, age-appropriateness, and instruction-following; successful inference is not a semantic-quality pass.

Refer to [`evaluation/README.md`](evaluation/README.md) for guidelines on defining success, edge cases, and failure scenarios.

## Known limitations

- No file upload, persistent course library, retrieval-augmented generation, or multi-turn conversation memory.
- Model responses can be incorrect or inconsistent; verify important facts with course materials.
- Local inference speed and quality depend on the selected model and device.

## Future improvements

- List planned feature enhancements, architectural refactorings, or future capabilities.
