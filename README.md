# StudyBuddy AI

StudyBuddy AI is a local-first study assistant for Häme University of Applied Sciences students. It uses an Ollama-hosted language model to explain concepts, summarize pasted or uploaded notes, create practice quizzes, and draft flashcards grounded in retrieved course material.

## Team members

- Emmi Myrskyranta (emmi.myrskyranta@student.hamk.fi)
- Md Firoz Chowdhury (mdfiroz.chowdhury@student.hamk.fi)
- Bishnu Chaudhary (bishnu.chaudhary@student.hamk.fi)

## Team contributions

- **Emmi Myrskyranta** — Built the core application: Gradio UI, RAG retrieval, AI service, automated tests and initial documentation.
- **Md Firoz Chowdhury** — RAG evaluation: sample course notes, 12 evaluation cases, automatic retrieval checks, live evaluation run and results analysis; updated the decision log.
- **Bishnu Chaudhary** — Application review, Ollama connection testing, and development support. Developed a standalone Python script to verify   the Ollama server connection, check installed AI models, and handle connection errors. Performed positive and negative tests to confirm the reliability of the tool. Documented testing results and improved project setup guidance.

- GitHub Project link: https://github.com/myrskyranta/Artifical-Intelligence-Application-Project


## Problem

### Intended users
Students of Häme University of Applied Sciences.

### Problem statement
Students face a lot of scheduling conflicts in their studies due to a large amount of projects, assignments and materials to study. Manually making flashcards, practice quizzes and summaries for one's studies takes away hours that the student could use more efficiently. 

### Why AI is appropriate
This project requires AI and LLMs (Large Language Models) because studying is semantic, creative and unstructured and traditional deterministic software, e.g. databases or keyword search engines, rely on rules, exact matches and structured data. Traditional software works great in storing data and organizing it but AI is required to comprehend and synthesize and generate knowledge from said data. Without AI, this project's application would only be an expensive document storage solution rather than a usable study planner.

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

## Technologies

Python 3.12 · Gradio · Ollama (llama3.2) · BM25 keyword retrieval · pypdf · python-docx · Pydantic · python-dotenv · pytest

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

### 1. What We Measure and Why

StudyBuddy's RAG works mainly in 2 steps, one is Retrieval to search relevant text, and another one is Generation to write the answer. Error can be made in both steps, for this, we checked both separately.

### 2. Method

- Specific Documents (data/sample_course_notes.md), Based on the course's website chapter 4, called (Grounding and RAG), as summary made by AI based on this page's content- https://mazarbaloch.github.io/dev-ai-course/docs/chapters/04-grounding-and-rag

- 17 Test Cases (evaluation/test_cases.json)

1. 5 questions in Study-mode case, without providing note
2. 6 questions which have answers in the note
3. 2 questions asked in different way
4. 2 questions which have no information in the note
5. 2 wrong inputs, using spaces only, more than 16000 characters.

- Retrieval

Right answer are already noted in (test_cases.json) with expected key-words, BM25 used to rank the question's answer. when the answer meet rank 1 or 2, it will be pass, if not, it will be fail.

- Generation

Every answer is tested by 3 ways:
1. is information right
2. is it out of note (grounded)
3. is it followed by the instructions of study mode, configured in the file - (src/services/ai_service.py)
Finally, Considering the above steps, it will be verified by 3 forms like Pass, Partial or Fail.

- Model
Locally run llama3.2, Ollama, on 21.Oct. 2026

### 3. Results (evaluation_results.md)

| What was measured | Result |
| :--- | :--- |
| Retrieval: correct passage ranked first | 7 of 8 (88%) |
| Generation: all 17 cases | 10 pass, 6 partial, 1 fail |
| Generation: RAG questions only (10) | 4 pass, 5 partial, 1 fail |
| Invalid input rejected | 3 of 3 |
| Average response time | 19.6 s |
| Automated tests (`pytest`) | 23 of 23 pass |

### 4. With and without the uploaded notes

Same question: *"How many dimensions do the all-MiniLM-L6-v2 embeddings have?"*

- **Without notes:** 768 — wrong, but stated with full confidence
- **With notes:** 384 — correct

### 5. Key findings

- **RAG prevents wrong answers:** with the notes uploaded, the model gives the correct fact instead of inventing one.
- **Retrieval is strong, generation is the weak part:** most problems happened after the correct passage had already been retrieved.
- **The model receives the whole document:** our notes are split into 5 chunks and the app sends up to 5 chunks, so the model often summarises everything instead of answering the question.
- **BM25 matches words, not meaning:** it did not find the right passage for a paraphrased question ("small pieces of text" instead of "short chunks").
- **Citations are unreliable:** once the model cited "page 3" for a Markdown file that has no pages.

### 6. How to re-run

```bash
pytest
python -m evaluation.run_evaluation --skip-model   # retrieval checks only, no Ollama needed
python -m evaluation.run_evaluation                # full evaluation, Ollama must be running
```

Results are saved to `evaluation/latest_run.json` (not committed to Git).

### 7. Details

- Grade and reason for every case: [`evaluation/evaluation_results.md`](evaluation/evaluation_results.md)
- Evaluation guidelines: [`evaluation/README.md`](evaluation/README.md)




## Known limitations

- Uploaded documents and conversation history are session-local and are not persisted after the session ends.
- Scanned PDFs need OCR; OCR is not included. RAG retrieval can miss relevant passages or rank less relevant text.
- Model responses can be incorrect or inconsistent; verify important facts with course materials.
- Local inference speed and quality depend on the selected model and device.
- BM25 matches words, not meaning, so paraphrased questions can miss the right passage.
- With short documents the model receives almost the whole file and may summarise instead of answering.
- Model citations are unreliable and should be checked against the uploaded notes.


## Future improvements

- Send only the top 2–3 chunks and tell the model to answer only the question asked.
- Show the retrieved sources in the UI instead of relying on model citations.
- Add embedding-based or hybrid retrieval for paraphrased questions.

## Recorded presentation

Video: (link to be added)



## Ollama Connection Checker

As part of the application review and testing process, a standalone Python-based Ollama Connection Checker was developed by **Bishnu Chaudhary**.

The purpose of this tool is to verify that the local Ollama environment is properly configured before running StudyBuddy AI.

### Features

- Checks whether the Ollama server is running.
- Connects to the local Ollama API.
- Displays available AI models.
- Verifies whether the required Llama 3.2 model is installed.
- Provides clear error messages when the server or model is unavailable.
- Runs independently without modifying the main application.

### How to Run

Activate the project's Python environment and run the checker from the project root:

```powershell
python scripts/check_ollama.py
```

### Testing and Validation

The following tests were completed:

| Test ID | Description | Result |
|---|---|---|
| TC01 | Connect to Ollama using port 11434 | PASS |
| TC02 | Verify the required Llama 3.2 model | PASS |
| TC03 | Display locally installed AI models | PASS |
| TC04 | Detect an unavailable Ollama server using port 11435 | PASS |

During testing, the script successfully detected `llama3.2:latest` and `llama3.2:3b`.

A negative test was also performed using an incorrect server port. The script correctly displayed a connection error instead of crashing unexpectedly.

### Contribution to the Project

This diagnostic tool provides a simple method for developers to check their local Ollama setup and troubleshoot connection problems.

The checker is implemented separately from the existing AI application and does not modify the RAG pipeline, Gradio user interface, or AI service.