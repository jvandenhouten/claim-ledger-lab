from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from validate_ledger import governance_validate, validate_path  # noqa: E402

CASES = ROOT / "cases"
BAD = ROOT / "tests" / "fixtures" / "bad-vote-count.json"


def _base(**overrides) -> dict:
    ledger = {
        "ledger_id": "CL-TEST",
        "title": "Synthetic unit ledger for regression tests",
        "source_type": "model_output",
        "source_text": "Synthetic packet used only inside unit tests.",
        "analyst": "test",
        "release_gate": "amber",
        "release_authority": "Director of Corporate Security",
        "claims": [
            {
                "claim_id": "C1",
                "text": "A checkable statement about the packet.",
                "claim_type": "fact",
                "state": "supported_uncertain",
                "evidence": ["Packet blotter line 1."],
                "confidence_basis": "Single primary document in the packet.",
                "alternatives": ["The blotter date could be wrong."],
            }
        ],
    }
    ledger.update(overrides)
    return ledger


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
    assert "vote" in blob or "consensus" in blob or "model" in blob


def test_vote_language_fails_even_if_word_evidence_present() -> None:
    ledger = _base()
    ledger["claims"][0]["confidence_basis"] = (
        "three models agreed and that is the evidence"
    )
    errors = governance_validate(ledger)
    assert any("vote" in e.lower() or "consensus" in e.lower() for e in errors)


def test_green_weak_fact_without_recommendation_fails() -> None:
    ledger = _base(
        release_gate="green",
        release_authority="VP Customer Operations",
    )
    ledger["claims"][0]["state"] = "unsupported"
    ledger["claims"][0]["evidence"] = []
    errors = governance_validate(ledger)
    assert any("green gate is invalid" in e for e in errors)


def test_amber_and_red_require_release_authority() -> None:
    for gate in ("amber", "red"):
        ledger = _base(release_gate=gate, release_authority="   ")
        errors = governance_validate(ledger)
        assert any("release" in e.lower() or "owner" in e.lower() for e in errors), gate


def test_abstain_may_omit_release_authority() -> None:
    ledger = _base(release_gate="abstain", release_authority="")
    errors = governance_validate(ledger)
    assert errors == []


def test_verified_prediction_fails() -> None:
    ledger = _base()
    ledger["claims"][0]["claim_type"] = "prediction"
    ledger["claims"][0]["state"] = "verified"
    ledger["claims"][0]["evidence"] = ["A prior quarter result is not a future proof."]
    errors = governance_validate(ledger)
    assert any("predictions cannot be marked verified" in e for e in errors)
