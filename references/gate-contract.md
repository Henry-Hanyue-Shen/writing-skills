# Gate contract

`EDITOR_GATE.json` is the portable handoff between the editor and its calling conversation or agent. It records editorial state; it is not a research plan or an autonomous task queue.

## Required structure

```json
{
  "schema_version": "1.0",
  "gate_id": "manuscript-short-id",
  "artifact": {
    "input": "paper/main.tex",
    "output": "paper/main.edited.tex",
    "scope": "full",
    "language": "en"
  },
  "verdict": "RETURN_FOR_RESEARCH",
  "checks": {
    "semantic_fidelity": {"status": "pass", "detail": "No claim drift detected."},
    "methodology": {"status": "warn", "detail": "Dataset exclusion rule is absent."},
    "terminology": {"status": "pass", "detail": "Canonical method name is consistent."},
    "citations": {"status": "warn", "detail": "One claim lacks a supplied primary source."},
    "numbers": {"status": "pass", "detail": "Reported deltas agree with Table 2."},
    "prose": {"status": "pass", "detail": "Document-level revision completed."}
  },
  "edits": [
    {
      "location": "Methods, paragraph 3",
      "kind": "clarity",
      "summary": "Made the sampling sequence explicit using supplied protocol text.",
      "claim_change": "none"
    }
  ],
  "return_to_caller": [
    {
      "id": "R1",
      "type": "source-recovery",
      "blocking": true,
      "affected_location": "Methods, paragraph 4",
      "need": "The recorded dataset exclusion rule.",
      "reason": "The current sample size cannot be interpreted without it.",
      "acceptance_test": "Return a dated protocol or code/config excerpt that states the exclusion rule and applies to the reported run."
    }
  ],
  "unresolved": [],
  "notes": []
}
```

## Enums

- `artifact.scope`: `full` or `partial`.
- `verdict`: `PASS`, `PASS_WITH_NOTES`, `RETURN_FOR_RESEARCH`, or `HOLD_FOR_INTEGRITY`.
- check status: `pass`, `warn`, `fail`, or `not_checked`.
- `claim_change`: `none`, `narrowed`, or `author_confirmation_required`.
- return type: `literature`, `experiment`, `analysis`, `source-recovery`, `integrity`, or `author-decision`.

## Verdict invariants

- `PASS`: every required check is `pass`; no blocking packet; no unresolved item.
- `PASS_WITH_NOTES`: no check is `fail`; no blocking packet; at least one non-blocking note, warning, or unresolved coverage limitation.
- `RETURN_FOR_RESEARCH`: at least one blocking packet exists and at least one blocking packet has type `literature`, `experiment`, `analysis`, or `source-recovery`.
- `HOLD_FOR_INTEGRITY`: at least one blocking `integrity` packet exists.

Use the most severe applicable verdict: `HOLD_FOR_INTEGRITY` precedes `RETURN_FOR_RESEARCH`, which precedes `PASS_WITH_NOTES`, which precedes `PASS`.

## Resumption

The caller should return each completed packet with its `id`, the new artifact/source, provenance, and the acceptance-test result. On resumption, the gate:

1. checks that the returned material satisfies the original acceptance test;
2. revises only the newly unblocked passages plus any terminology-dependent occurrences;
3. re-runs affected checks and the final semantic comparison;
4. replaces the prior report with a new report while preserving resolved packet IDs in `notes` or caller history.

The gate never marks a packet resolved merely because the caller says work was done; it checks the returned artifact.
