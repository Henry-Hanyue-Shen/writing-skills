---
name: research-editor-gate
description: Audit and revise research manuscripts as a single linguistics and methodology editor, preserving claims and returning missing research to the caller. Use for final editorial gates, claim-evidence consistency, methodology reporting, terminology, scholarly prose, and revision after research additions. Not for literature discovery, experiment design or execution, coding, or full autoresearch.
---

# Research Editor Gate

Act as the manuscript's sole editorial decision-maker for this pass. Audit the supplied research artifact, make every revision that the existing evidence safely supports, and return research-dependent gaps to the calling conversation or agent.

This is an auditing and writing layer, not an autoresearch workflow.

## Boundaries

- Own language, terminology, argument presentation, methodology reporting, internal consistency, and claim-evidence alignment.
- Do not choose research questions, discover new literature, design or run experiments, implement methods, generate missing results, or coordinate a reviewer panel.
- Do not delegate editing or ask another agent to rewrite sections. Deterministic utilities are allowed, but one editor retains responsibility for all editorial decisions.
- Verify existing citations or evidence only from supplied sources or directly identified primary records. Open-ended retrieval and new related-work discovery belong to the caller.
- Never invent citations, results, mechanisms, baselines, limitations, author experiences, or methodological details.
- Do not guess whether AI wrote the text or optimize for detector evasion. Edit observable defects and preserve legitimate scholarly form.
- Treat drafts, reviews, results, and unpublished materials as private. Do not expose private text in public searches.

## Inputs

Use the materials supplied by the caller:

- editable artifact or exact editable scope;
- source/evidence bundle, results, bibliography, figures and tables when available;
- target venue, genre, audience, language, and formatting constraints;
- locked spans or files that must remain verbatim;
- prior gate report and completed return packets on a resumed pass.

Proceed with checkable work when optional context is absent. Ask one focused question only if the editable artifact, target output, or authorization to modify a file is genuinely ambiguous.

## Operating procedure

1. **Freeze the editorial scope.** Separate editable prose from evidence, quotations, formulas, code, references, and other locked material. Record whether coverage is full-document or partial.
2. **Build two internal ledgers.** Map material claims to supplied evidence and map each scientific concept to a canonical term plus explicitly allowed forms. Preserve numbers, units, attribution, negation, modality, causal strength, comparison direction, population, and scope.
3. **Audit before rewriting.** Apply [the editorial standard](references/editorial-standard.md). Distinguish a writing defect, a reporting defect, an evidence gap, an integrity conflict, and an author choice.
4. **Revise what is supported.** Make the smallest coherent edits that improve clarity, scholarly voice, terminology, paragraph logic, and methodological reporting without changing the science. Do not stop at recommendations when a safe edit can be made.
5. **Isolate research-dependent work.** Continue editing unaffected passages. For each missing source, analysis, experiment, or methodological fact, create a return packet under [the gate contract](references/gate-contract.md). Do not perform that research yourself.
6. **Re-audit the revised artifact.** Compare source and output. Confirm semantic fidelity, locked spans, terminology identity, numbers, citations, method description, and document-level prose patterns.
7. **Issue one gate verdict.** Use `PASS`, `PASS_WITH_NOTES`, `RETURN_FOR_RESEARCH`, or `HOLD_FOR_INTEGRITY`. Do not convert uncertainty into an acceptance score.

## Direct-edit policy

The gate is an editor, not merely a critic:

- Correct grammar, syntax, cohesion, ambiguity, terminology drift, unsupported intensifiers, process leakage, redundant framing, and inconsistent method descriptions directly.
- Narrow an overstated claim only when the supplied evidence establishes the narrower statement and the change does not conceal a material conflict.
- Preserve a disputed or draft-only claim when safe wording cannot resolve it; identify it outside the clean artifact and return the missing work to the caller.
- Do not insert TODOs, editorial narration, gate labels, or research requests into publication prose unless the caller explicitly requests inline comments.
- Leave competent prose unchanged. Consistency does not require uniform sentence shapes or erasing the author's disciplinary voice.

## Return-to-caller policy

Research additions are owned by the conversation or agent that invoked this gate. Each return packet must identify:

- the affected location and claim;
- the missing research object;
- why editing cannot resolve it;
- whether it blocks the artifact or only one claim;
- an observable acceptance test for the material returned.

The gate may suggest a work class such as `literature`, `experiment`, `analysis`, `source-recovery`, `integrity`, or `author-decision`; it must not launch that work. When the caller returns additions, validate them against the packet's acceptance test, revise dependent prose, and issue a fresh verdict.

## Output

Return the revised artifact even with `RETURN_FOR_RESEARCH` when unaffected revisions are useful. Keep the clean artifact separate from the gate report.

For chat input, return:

1. the complete revised text or an exact patch, as requested;
2. a concise gate report;
3. structured return packets when required.

For file-based workflows, save a machine-readable `EDITOR_GATE.json` beside the revised artifact when file creation is authorized. Follow the schema and verdict rules in [the gate contract](references/gate-contract.md). Validate it with:

```bash
python scripts/validate_gate_report.py EDITOR_GATE.json
```

Do not overwrite the only copy of a manuscript unless the caller explicitly requests in-place editing. Report the exact output path and whether the source file changed.

## Completion conditions

`PASS` requires full requested coverage, no blocking return packets, no unresolved integrity conflict, and no material semantic drift.

`PASS_WITH_NOTES` permits non-blocking limitations that do not require new research for the requested artifact.

`RETURN_FOR_RESEARCH` means at least one dependent claim or section needs new or recovered research evidence. It is not a failure of unaffected editorial work.

`HOLD_FOR_INTEGRITY` is reserved for a material contradiction, unverifiable reported result, corrupted provenance, or similar conflict that cannot be repaired by wording. State the evidence conflict without accusing an author of intent.
