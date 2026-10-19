"""Run representative prompts against the configured local Ollama model."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from src.config import config
from src.services.ai_service import AIService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = PROJECT_ROOT / "evaluation" / "test_cases.json"


def run_evaluation(output_path: Path) -> dict:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    service = AIService()
    results = []

    for case in cases:
        response = service.process_study_request(case["input"], case["study_mode"])
        expected_success = case["expect_success"]
        if response.success != expected_success:
            status = "fail"
        elif expected_success:
            # Semantic quality needs human review; success only confirms the model call completed.
            status = "needs_review"
        else:
            status = "pass"

        results.append({
            **case,
            "actual_result": response.content,
            "success": response.success,
            "error_message": response.error_message,
            "status": status,
        })
        print(f"\n[{case['id']}] {status.upper()} — {case['study_mode']}\n{response.content}")

    report = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "model": config.model_name,
        "ollama_base_url": config.ollama_base_url,
        "results": results,
        "summary": {
            "total": len(results),
            "pass": sum(result["status"] == "pass" for result in results),
            "needs_review": sum(result["status"] == "needs_review" for result in results),
            "fail": sum(result["status"] == "fail" for result in results),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved report: {output_path}")
    print(f"Summary: {report['summary']}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "evaluation" / "latest_run.json",
        help="Path for the generated JSON report (default: evaluation/latest_run.json).",
    )
    args = parser.parse_args()
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    run_evaluation(output_path)


if __name__ == "__main__":
    main()
