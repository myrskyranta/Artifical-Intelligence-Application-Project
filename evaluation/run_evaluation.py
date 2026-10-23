"""Run the evaluation cases against the configured local Ollama model.

Cases with ``"use_documents": true`` load the fixed sample document
(``data/sample_course_notes.md``) through the same RAG library the UI uses and
are assessed in two separate parts:

1. Retrieval (automatic): is the passage that contains the answer among the
   top-ranked chunks? Measured by the rank of the first chunk that contains all
   ``expected_keywords``.
2. Generation (human review): is the model's answer correct, grounded in the
   notes and does it follow the study-mode instruction? Successful model calls
   are marked ``needs_review`` until a person grades them.

Use ``--skip-model`` to run only the retrieval checks without Ollama.
"""

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.capabilities.rag import DocumentLibrary
from src.config import config
from src.services.ai_service import STUDY_MODES, AIService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = PROJECT_ROOT / "evaluation" / "test_cases.json"
SAMPLE_DOCUMENT = PROJECT_ROOT / "data" / "sample_course_notes.md"
MAX_RANK_CHECKED = 5
HIT_AT = 2


def _case_input(case: dict) -> str:
    """Return the case input, repeated when the case tests very long prompts."""
    return case["input"] * int(case.get("input_repeat", 1))


def _retrieval_rank(library: DocumentLibrary, query: str, keywords: list[str]) -> Optional[int]:
    """Return the smallest k for which the top-k retrieved chunks contain every keyword."""
    wanted = [keyword.casefold() for keyword in keywords]
    for k in range(1, MAX_RANK_CHECKED + 1):
        context = library.retrieve(query, max_chunks=k).casefold()
        if all(keyword in context for keyword in wanted):
            return k
    return None


def _check_retrieval(library: DocumentLibrary, case: dict, query: str) -> dict:
    keywords = case.get("expected_keywords") or []
    if not keywords or not query.strip():
        return {"retrieval_status": "n/a", "retrieval_rank": None}
    rank = _retrieval_rank(library, query, keywords)
    status = "pass" if rank is not None and rank <= HIT_AT else "fail"
    return {"retrieval_status": status, "retrieval_rank": rank}


def _top_sources(library: DocumentLibrary, query: str, limit: int = 2) -> str:
    """Short preview of the top retrieved chunks, for the human reviewer."""
    if not query.strip():
        return ""
    return library.retrieve(query, max_chunks=limit)[:600]


def _ask_model(service: AIService, case: dict, query: str, library: Optional[DocumentLibrary]):
    """Send the request the same way the UI does: study-mode instruction plus retrieved context."""
    if not query.strip():
        return service.process_message(query)
    if library is None:
        return service.process_study_request(query, case["study_mode"])
    instruction = STUDY_MODES.get(case["study_mode"], STUDY_MODES["Study chat"])
    request = f"{instruction}\n\nStudent's latest request:\n{query.strip()}"
    return service.process_message(request, context=library.retrieve(query))


def run_evaluation(
    output_path: Path,
    skip_model: bool = False,
    service: Optional[AIService] = None,
    cases_path: Path = CASES_PATH,
) -> dict:
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    library = DocumentLibrary.from_files([SAMPLE_DOCUMENT])
    service = service or AIService()
    results = []

    for case in cases:
        query = _case_input(case)
        uses_documents = bool(case.get("use_documents"))
        result = {key: value for key, value in case.items() if key != "input"}
        result["input"] = query if len(query) <= 300 else f"{query[:300]}... ({len(query):,} characters)"
        result["input_chars"] = len(query)

        if uses_documents:
            result.update(_check_retrieval(library, case, query))
            result["top_sources_preview"] = _top_sources(library, query)
        else:
            result.update({"retrieval_status": "n/a", "retrieval_rank": None})

        if skip_model:
            result.update({"status": "skipped", "actual_result": None, "latency_seconds": None})
        else:
            started = time.perf_counter()
            response = _ask_model(service, case, query, library if uses_documents else None)
            latency = round(time.perf_counter() - started, 2)
            expected_success = case["expect_success"]
            if response.success != expected_success:
                status = "fail"
            elif expected_success:
                # Semantic quality needs human review; success only confirms the model call completed.
                status = "needs_review"
            else:
                status = "pass"
            result.update({
                "status": status,
                "actual_result": response.content,
                "success": response.success,
                "error_message": response.error_message,
                "latency_seconds": latency,
            })

        # Filled in by the human reviewer: pass / partial / fail, with a short reason.
        result.update({"human_grade": "", "review_notes": ""})
        results.append(result)
        print(
            f"\n[{case['id']}] {case['category']} | retrieval: {result['retrieval_status']}"
            f" (rank {result['retrieval_rank']}) | response: {result['status']}"
        )
        if result.get("actual_result"):
            print(result["actual_result"])

    retrieval_checked = [r for r in results if r["retrieval_status"] in {"pass", "fail"}]
    timed = [r["latency_seconds"] for r in results if r.get("latency_seconds") and r.get("success")]
    report = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "model": None if skip_model else config.model_name,
        "ollama_base_url": config.ollama_base_url,
        "sample_document": SAMPLE_DOCUMENT.relative_to(PROJECT_ROOT).as_posix(),
        "document_chunks": len(library.chunks),
        "results": results,
        "summary": {
            "total": len(results),
            "retrieval_checked": len(retrieval_checked),
            f"retrieval_hit_at_{HIT_AT}": sum(r["retrieval_status"] == "pass" for r in retrieval_checked),
            "retrieval_hit_at_1": sum(r["retrieval_rank"] == 1 for r in retrieval_checked),
            "pass": sum(r["status"] == "pass" for r in results),
            "needs_review": sum(r["status"] == "needs_review" for r in results),
            "fail": sum(r["status"] == "fail" for r in results),
            "skipped": sum(r["status"] == "skipped" for r in results),
            "average_latency_seconds": round(sum(timed) / len(timed), 2) if timed else None,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved report: {output_path}")
    print(f"Summary: {report['summary']}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "evaluation" / "latest_run.json",
        help="Path for the generated JSON report (default: evaluation/latest_run.json).",
    )
    parser.add_argument(
        "--skip-model",
        action="store_true",
        help="Run only the automatic retrieval checks; do not call Ollama.",
    )
    args = parser.parse_args()
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    run_evaluation(output_path, skip_model=args.skip_model)


if __name__ == "__main__":
    main()
