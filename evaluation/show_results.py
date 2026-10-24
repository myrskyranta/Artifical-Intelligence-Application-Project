"""Print retrieval and human-review results side by side from evaluation/latest_run.json.

Usage:  python -m evaluation.show_results
"""

import json
from pathlib import Path

REPORT = Path(__file__).resolve().parent / "latest_run.json"


def main() -> None:
    if not REPORT.is_file():
        print(f"No report found at {REPORT}. Run: python -m evaluation.run_evaluation")
        return

    results = json.loads(REPORT.read_text(encoding="utf-8"))["results"]
    print(f"{'case':<9}{'retrieval':<11}{'rank':<6}answer")
    for r in results:
        rank = r.get("retrieval_rank") or "-"
        grade = r.get("human_grade") or "not reviewed"
        print(f"{r['id']:<9}{r['retrieval_status']:<11}{str(rank):<6}{grade}")

    found = [r for r in results if r["retrieval_status"] == "pass"]
    weak = [r["id"] for r in found if r.get("human_grade") in {"partial", "fail"}]
    print(f"\nCorrect passage retrieved: {len(found)} cases; answer still partial/fail in {len(weak)}: {', '.join(weak)}")


if __name__ == "__main__":
    main()
