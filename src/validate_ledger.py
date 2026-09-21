"""Validate claim ledgers against schema and governance rules."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "claim-ledger.schema.json"
VOTE_MARKERS = (
    "models agreed",
    "majority vote",
    "vote count",
    "2 of 3 models",
    "three models",
    "consensus of models",
)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_ledger(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_validate(ledger: dict) -> None:
    if jsonschema is None:
        return
    jsonschema.validate(instance=ledger, schema=load_schema())


def governance_validate(ledger: dict) -> list[str]:
    errors: list[str] = []
    claims = ledger.get("claims") or []
    if not claims:
        errors.append("ledger has no claims")

    for claim in claims:
        cid = claim.get("claim_id", "?")
        state = claim.get("state")
        evidence = claim.get("evidence") or []
        basis = (claim.get("confidence_basis") or "").lower()
        alternatives = claim.get("alternatives") or []

        if state == "verified" and not evidence:
            errors.append(f"{cid}: verified claims require at least one evidence string")

        if any(marker in basis for marker in VOTE_MARKERS) and "evidence" not in basis:
            errors.append(
                f"{cid}: confidence_basis may not rely on model-vote count alone"
            )

        if not alternatives:
            errors.append(f"{cid}: alternatives must include at least one competing read")

        if state == "verified" and claim.get("claim_type") == "prediction":
            errors.append(f"{cid}: predictions cannot be marked verified")

    recs = [c for c in claims if c.get("claim_type") == "recommendation"]
    weak = {"unsupported", "contradicted", "unverifiable"}
    if recs and ledger.get("release_gate") == "green":
        material_weak = [c["claim_id"] for c in claims if c.get("state") in weak]
        if material_weak:
            errors.append(
                "green gate is invalid while material claims remain "
                + ", ".join(material_weak)
            )

    if ledger.get("release_gate") in {"green", "amber", "red"}:
        if not (ledger.get("release_authority") or "").strip():
            errors.append("named release_authority is required unless gate is abstain")

    return errors


def validate_path(path: Path) -> list[str]:
    ledger = load_ledger(path)
    try:
        _schema_validate(ledger)
    except Exception as exc:
        return [f"schema: {exc}"]
    return governance_validate(ledger)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate claim ledger JSON files")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)
    failed = 0
    for path in args.paths:
        errors = validate_path(path)
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
