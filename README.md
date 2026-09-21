# Claim Ledger Lab

**Decompose a model answer into claims. Score the claims. Record the accountable human role or named decision owner who may release — or abstain.**

This is a method lab, not a product and not a benchmark. It shows how AI implementation governance works on the *output* of a model: atomic claims, evidence, competing reads, and a release gate.

> All cases are synthetic. No live model calls. No accuracy percentage is claimed.

**Method:** [METHOD.md](METHOD.md)

Companion portfolio:

- [GRC Risk Register](https://github.com/jvandenhouten/grc-risk-register-tracker) — how you *own* an AI use case
- [Abuse Investigation Portfolio](https://github.com/jvandenhouten/openai-abuse-investigator-portfolio) — how you *contest* an automated label

## Why this exists

Fluent text hides mixed claim types. A single paragraph can contain a fact, an assumption, and a recommendation. Governance fails when those are scored as one blob, or when “several models agreed” is treated as verification.

## Three worked cases

| ID | File | Gate | Lesson |
|---|---|---|---|
| CL-001 | `cases/01-customer-ops-policy-invention.json` | red | Model invents a refund policy and speaks as if it already posted a credit |
| CL-002 | `cases/02-security-summary-source-collapse.json` | amber | Two reprints are not two independent sources |
| CL-003 | `cases/03-unanswerable-abstain.json` | abstain | Pre-approving an unevaluated tool for employee investigations is not answerable from the packet |

## Rules the validator enforces

- JSON matches `schema/claim-ledger.schema.json`
- `verified` requires at least one evidence string
- Confidence may not use model-vote or model-consensus language, even if the word “evidence” also appears
- Every claim lists at least one alternative read
- Predictions cannot be marked `verified`
- `green` is invalid while any claim is unsupported, contradicted, or unverifiable — including ledgers with no recommendation
- An accountable human role or named decision owner is required on `release_authority` unless the gate is `abstain`

## Run locally

```bash
git clone https://github.com/jvandenhouten/claim-ledger-lab.git
cd claim-ledger-lab
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/validate_ledger.py cases/*.json
python -m pytest tests/ -q
```

## What this is not

- Not a multi-model council product
- Not a published accuracy study
- Not legal advice
- Not affiliated with any model vendor

## Author

Joel L. Vandenhouten — retired U.S. Army Major; intelligence, investigations, enterprise security, and GRC. Master of Legal Studies and graduate certificate in Cybersecurity Law & Policy, both in progress at Texas A&M University School of Law; expected 2027.
