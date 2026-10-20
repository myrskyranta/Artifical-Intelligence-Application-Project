import json
from pathlib import Path
from unittest.mock import MagicMock

from evaluation.run_evaluation import CASES_PATH, SAMPLE_DOCUMENT, run_evaluation
from src.services.ai_service import AIService


def test_evaluation_cases_are_well_formed():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    ids = [case["id"] for case in cases]

    assert len(ids) == len(set(ids))
    assert SAMPLE_DOCUMENT.is_file()
    for case in cases:
        assert {"id", "category", "study_mode", "input", "expected_behavior", "expect_success"} <= case.keys()


def test_retrieval_only_run_needs_no_model(tmp_path: Path):
    report = run_evaluation(tmp_path / "report.json", skip_model=True)

    assert (tmp_path / "report.json").is_file()
    assert report["summary"]["skipped"] == report["summary"]["total"]
    assert report["summary"]["retrieval_checked"] > 0
    assert all(result["actual_result"] is None for result in report["results"])


def test_rag_cases_send_retrieved_context_to_the_model(tmp_path: Path):
    mock_client = MagicMock()
    mock_client.generate.return_value = "Grounded answer [Source: sample_course_notes.md]"

    report = run_evaluation(tmp_path / "report.json", service=AIService(model_client=mock_client))
    results = {result["id"]: result for result in report["results"]}

    assert results["rag-01"]["status"] == "needs_review"
    assert results["rag-11"]["status"] == "pass"  # whitespace input rejected
    assert results["rag-12"]["status"] == "pass"  # over-long input rejected
    prompts = [call.args[0] for call in mock_client.generate.call_args_list]
    assert any("<uploaded_study_material>" in prompt and "sample_course_notes.md" in prompt for prompt in prompts)
