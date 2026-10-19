# Evaluation Framework

Systematic evaluation is essential for assessing whether your AI application reliably solves your target user's problem.

## How to Conduct Evaluation

The repository contains model-independent service tests and a live evaluation runner for the configured Ollama model. The live runner records generated text and checks whether expected requests succeeded or failed; it does not automatically grade semantic quality.

### Test Case Categories

Your evaluation dataset in [`test_cases.json`](test_cases.json) should cover three primary categories:

1. **Successful Cases (Typical Inputs):** Standard queries or inputs that your application is designed to handle successfully under normal operating conditions.
2. **Difficult Cases (Edge Cases):** Ambiguous queries, long inputs, unusual domain terms, or edge cases that test model robustness and retrieval/tool quality.
3. **Failure / Adversarial Cases:** Empty inputs, malformed requests, out-of-scope questions, or connection drops that verify controlled error handling.

## Evaluation Process

1. **Define Test Cases:** Maintain realistic inputs, study modes, expected behaviors, and expected service success in `test_cases.json`.
2. **Run fast checks:** Execute `pytest` from the project root; tests use injected clients and do not need Ollama.
3. **Run live cases:** Start Ollama with the configured model available, then execute `python -m evaluation.run_evaluation`. An optional `--output path.json` selects a report path.
4. **Review results:** Inspect `evaluation/latest_run.json`. `pass`/`fail` checks service success behavior; successful model responses are marked `needs_review` until a person evaluates relevance, factuality, and adherence to the expected behavior.
5. **Summarize findings:** Record the model, date, results, and limitations in [`evaluation_results.md`](evaluation_results.md). Do not report unrun cases or infer semantic quality from model-call success.
