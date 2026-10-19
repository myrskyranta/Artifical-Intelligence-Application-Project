# Evaluation Results Summary

## Live integration run — 2026-10-19

- **Configured model:** `llama3.2` (Ollama)
- **Cases executed:** 5
- **Service behavior passed:** 1 (empty input rejected without contacting the model)
- **Model responses awaiting semantic review:** 0
- **Connection failures:** 4

Ollama was not reachable at the configured local endpoint during this run. The four model-backed cases therefore did not produce model outputs and are recorded as failed integration checks, not as evidence about model quality. Re-run `python -m evaluation.run_evaluation` after starting Ollama and pulling the configured model. The generated response report is written to the ignored `evaluation/latest_run.json` file.

| Category | Cases | Result |
| :--- | :---: | :--- |
| Successful study tasks | 2 | Both blocked by Ollama connection failure |
| Difficult study tasks | 2 | Both blocked by Ollama connection failure |
| Empty-input failure case | 1 | Passed; friendly validation response |

## Automated regression tests

The service test suite passed **9 tests** with mocked model clients. This verifies validation, mode instructions, and service-level failures; it does not measure actual model quality.

## Findings and next steps

- Empty input is handled locally without a model request.
- Local Ollama availability remains a runtime dependency and is surfaced with a friendly message.
- Re-run the live cases with Ollama available, then manually grade factuality, relevance, and instruction-following before calling model-backed cases passes.
