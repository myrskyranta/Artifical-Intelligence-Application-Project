# Evaluation Results Summary

## Live RAG evaluation — 2026-10-21

- **Model:** `llama3.2` via local Ollama (Windows laptop, CPU inference)
- **Reference document:** [`data/sample_course_notes.md`](../data/sample_course_notes.md) — our own study notes on Chapter 4 "Grounding and RAG Applications", split into 6 searchable chunks
- **Cases:** 17 in [`test_cases.json`](test_cases.json) — 5 general study-mode cases without documents, 10 RAG questions with the notes uploaded, 2 extra input-validation cases
- **Reproduce:** `python -m evaluation.run_evaluation` (or `--skip-model` for the retrieval checks only)
- **Average response time:** 19.6 s per successful model call

We assessed the two parts of RAG separately, because they fail for different reasons:

1. **Retrieval** (automatic): does BM25 rank the chunk containing the answer in the top 2? Checked with `expected_keywords`.
2. **Generation** (human review): is the answer correct, grounded in the notes, and does it follow the study mode? Graded *pass*, *partial* or *fail*.

### Retrieval

| Metric | Result |
| :--- | :---: |
| Answer chunk ranked 1st (hit@1) | **7 / 8 (88%)** |
| Answer chunk in top 2 (hit@2) | **7 / 8 (88%)** |

The only miss was `rag-06`, a paraphrased question ("cut the text into very small pieces") that avoids the word *chunk*. BM25 matches words, not meaning, so the right chunk was ranked 5th. Unanswerable questions (`rag-09`, `rag-10`) have no answer chunk and are not counted.

### Generation and error handling

| Case | Category | Grade | Reviewer note |
| :--- | :--- | :---: | :--- |
| case-01 | summary, no document | Pass | Accurate two-point summary |
| case-02 | explain to a 5-year-old | Partial | Too long, uses hard terms, presents the analogy as exact |
| case-05 | quiz, no document | Pass | One question, waits for the answer |
| case-04 | flashcards, no document | Pass | Accurate, keeps the mitosis/meiosis distinction |
| case-03 | empty input | Pass | Rejected without calling the model |
| rag-01 | RAG explain | Partial | Correct definition, but summarises the whole document and gives no citation |
| rag-02 | RAG fact | Pass | Correct: 384 dimensions |
| rag-03 | RAG explain | Partial | Correct final answer, but first claims the notes do not mention Chroma |
| rag-04 | RAG summary | Pass | Five ingestion steps in the right order |
| rag-05 | RAG flashcards | **Fail** | States that overlap *avoids* duplicates; the notes say it *duplicates* text |
| rag-06 | RAG paraphrased | Partial | One correct reason, two unsupported reasons cited to the notes |
| rag-07 | RAG paraphrased | Pass | Correct distinction between adding documents and training |
| rag-08 | RAG quiz | Partial | One question, but adds a placeholder "Answer:" line |
| rag-09 | unanswerable | Pass | Says the notes contain no exam date; invents nothing |
| rag-10 | unanswerable | Partial | Admits the notes do not cover it, then answers from general knowledge |
| rag-11 | whitespace input | Pass | Rejected without calling the model |
| rag-12 | 18,400-char input | Pass | Rejected with the length limit message |

| Group | Pass | Partial | Fail |
| :--- | :---: | :---: | :---: |
| All 17 cases | 10 | 6 | 1 |
| RAG questions (rag-01 to rag-10) | 4 | 5 | 1 |
| Input validation (3 cases) | 3 | 0 | 0 |

### With and without the uploaded notes (manual UI check)

| Question | Without notes | With notes |
| :--- | :--- | :--- |
| How many dimensions do the all-MiniLM-L6-v2 embeddings have? | "768" — wrong, stated confidently | "384" — correct |

In the same manual session the model correctly refused to invent an exam date. Two problems from the automatic run also appeared in the UI: it cited a "page 3" that does not exist in a Markdown file, and in *Quiz me* mode it explained the answer before asking the question.

## Findings

1. **RAG prevents confident wrong answers.** The same question went from a hallucinated 768 to the correct 384 once the notes were uploaded.
2. **Retrieval is strong; generation is the weak part.** Retrieval found the answer in 7 of 8 cases, but only 4 of 10 RAG answers were fully correct. Most problems happen after the right passage was already retrieved.
3. **Answers drift to the whole context.** The app sends up to 5 chunks; with a short document that is almost the entire file, so the model often summarises everything instead of answering the question (rag-01, rag-03, rag-05).
4. **Citations are unreliable.** The model rarely names the source even though the prompt asks for it, and sometimes cites the notes for statements that are not in them (rag-06, the "page 3" citation).
5. **Keyword retrieval misses paraphrases.** BM25 cannot match "small pieces of text" to "short chunks".
6. **Unanswerable questions are handled inconsistently.** Correct refusal for the exam date, but general-knowledge answer for the World Cup question.
7. **Input validation is reliable.** All 3 invalid inputs were rejected before reaching the model.

## Limitations of this evaluation

- One reference document and 17 cases; results show patterns, not precise accuracy rates.
- Generation grades come from one reviewer. A second independent reviewer would make them more reliable.
- Model output varies between runs; the grades describe the 2026-10-21 run.

## Possible improvements

- Send fewer chunks (top 2–3) and tell the model to answer only the question asked.
- Show the retrieved sources in the UI so the student can check them, instead of relying on model citations.
- Add embedding-based or hybrid retrieval for paraphrased questions.
- Stricter instruction for unanswerable questions: say the notes do not cover it, without answering from general knowledge.

## Automated regression tests

`pytest` runs 23 tests with mocked model clients (service validation, model client errors, RAG ingestion and retrieval, UI wiring and the evaluation runner). All 23 pass. They check application behaviour, not model quality.

## Earlier run — 2026-10-19

The first live run used 5 cases without documents. Ollama was not reachable at that time, so 4 cases ended in connection errors and only the empty-input check passed. Those cases were kept and re-run successfully on 2026-10-21.
