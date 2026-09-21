from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from validate_ledger import validate_path  # noqa: E402

CASES = ROOT / "cases"
BAD = ROOT / "tests" / "fixtures" / "bad-vote-count.json"


def test_published_cases_pass() -> None:
    files = sorted(CASES.glob("*.json"))
    assert len(files) == 3
    for path in files:
        errors = validate_path(path)
        assert errors == [], path.name + ": " + "; ".join(errors)


def test_vote_count_and_empty_verified_fail() -> None:
    errors = validate_path(BAD)
    blob = " ".join(errors).lower()
    assert errors, "invalid fixture must fail"
    assert "verified" in blob or "evidence" in blob
    assert "vote" in blob or "model" in blob
