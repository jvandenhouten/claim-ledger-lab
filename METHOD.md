# Method

This lab treats a block of text — usually a model answer — as a set of **atomic claims**, not as a single verdict.

## Claim types

| Type | Meaning |
|---|---|
| fact | A checkable statement about the world or the source document |
| calculation | Arithmetic or a derived count that can be recomputed |
| assumption | Something treated as true without being shown |
| prediction | A future state |
| opinion | A value judgment |
| recommendation | An action someone should take |

## Claim states

| State | Meaning |
|---|---|
| verified | Independent evidence in the packet matches the claim |
| supported_uncertain | Some support exists; material doubt remains |
| disputed | Evidence points both ways |
| unsupported | No evidence was supplied |
| contradicted | Evidence directly conflicts |
| unverifiable | No legitimate source could settle it from this packet |
| stale | Once supportable; the cited source is outdated |

## Rules that make this governance, not styling

1. **Consensus is not verification.** A confidence field that says only “three models agreed” fails validation.
2. **Verified requires evidence.** Empty `evidence` on a `verified` claim is a hard fail.
3. **Recommendations inherit the weakest supporting claim.** If a recommendation rests on an unsupported fact, the release gate cannot be green.
4. **Abstention is a successful control** when the packet cannot support a consequential action.
5. **The human release authority is named.** The model does not close the case.

## Release gates

- **green** — consequential claims are verified or clearly scoped as opinion; a named human may release
- **amber** — material uncertainty remains; release only with documented residual risk
- **red** — at least one material claim is contradicted or would cause harm if acted on
- **abstain** — the honest output is that the question cannot be answered from this packet

## What this lab does not do

It does not call live models. It does not score accuracy against a gold benchmark. It does not implement a multi-agent product.
