# StudyBuddy AI

Starter template for the **Development of AI Applications** course final group project.

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

StudyBuddy AI addresses the challenges stated above by providing a study assistant where students can upload course materials and request source-grounded explanations, interactive quizzes, summaries, and flashcards. This reduces preparation time while keeping answers tied to the student's own material.

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

- **Model used:** e.g., `llama3.2` (or specified local Ollama model)
- **Selection rationale:** Why was this specific model chosen for your project (e.g., lightweight, performance, context size)?

## Additional AI capability

Select at least one additional capability to implement for your final project:

- [x] RAG (Retrieval-Augmented Generation)
- [ ] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [ ] Other: ______________________

### Capability justification
StudyBuddy implements lightweight RAG for uploaded course materials. It extracts and chunks text from TXT, Markdown, PDF, and DOCX files, ranks relevant chunks for each request, and passes them to the model through the AI service with source labels and grounding instructions. This encourages document-based answers but cannot eliminate hallucinations, so students should verify important information against the cited material.

Uploads are held for the active Gradio session and are not saved to a project database. Scanned PDFs without selectable text are not supported because OCR is not included.

## Setup

### 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate dev-ai-project
```

### 3. Configure environment variables

Copy `.env.example` to create your local `.env` configuration file:

On Linux / macOS:
```bash
cp .env.example .env
```

On Windows (Command Prompt / PowerShell):
```powershell
copy .env.example .env
```

Ensure `.env` contains valid values for `OLLAMA_BASE_URL` and `MODEL_NAME`:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2
```

### 4. Start Ollama

Make sure Ollama is installed and running locally, then pull your configured model:

```bash
ollama run llama3.2
```

### 5. Run the application

Run the application from the root directory of the project:

```bash
python -m app.main
```

Then open your browser at `http://localhost:7860`.

### 6. Run automated tests

```bash
pytest
```

## Evaluation

Describe your evaluation methodology and summarize key results. Starter test cases can be found in [`evaluation/test_cases.json`](evaluation/test_cases.json).

Refer to [`evaluation/README.md`](evaluation/README.md) for guidelines on defining success, edge cases, and failure scenarios.

## Known limitations

- Highlight known system limitations, unhandled edge cases, or boundaries of current capabilities.

## Future improvements

- List planned feature enhancements, architectural refactorings, or future capabilities.
