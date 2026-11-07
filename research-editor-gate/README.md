# Research Editor Gate

Research Editor Gate is a portable Codex skill for one narrow job: audit and revise an existing research manuscript as its single linguistics and methodology editor.

It edits what the supplied evidence supports. When a revision depends on a missing source, experiment, analysis, or protocol fact, it returns a structured request to the calling agent or conversation instead of inventing the missing research or launching an autoresearch workflow.

Maintained by Hanyue Shen, Founder at YH Intelligence Technology, Co., Ltd. Contact: [hanyueshen@yh-intel.com](mailto:hanyueshen@yh-intel.com).

## What it does

- audits claim-evidence alignment, numbers, citations, terminology, and methodology reporting;
- revises English or Chinese scholarly prose while preserving meaning and disciplinary register;
- makes safe revisions directly rather than returning only suggestions;
- keeps one editor responsible for the complete editorial decision;
- emits a portable `EDITOR_GATE.json` handoff for unresolved research additions;
- resumes the gate after the caller returns the requested evidence.

## What it does not do

It does not discover literature, design or run experiments, implement research code, choose a research direction, simulate a reviewer panel, or act as a full autoresearch system. It does not guess authorship or optimize writing for AI-detector evasion.

## Install

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/Henry-Hanyue-Shen/research-editor-gate.git ~/.codex/skills/research-editor-gate
```

On Windows PowerShell:

```powershell
git clone https://github.com/Henry-Hanyue-Shen/research-editor-gate.git "$env:USERPROFILE\.codex\skills\research-editor-gate"
```

Restart or refresh Codex skill discovery after installation.

## Use

```text
Use $research-editor-gate as the sole language and methodology editor for this manuscript. Revise everything supported by the supplied evidence and return any missing research to this conversation.
```

For a resumed pass:

```text
Use $research-editor-gate to resume the gate. Here is the revised manuscript, the previous EDITOR_GATE.json, and the evidence returned for packets R1 and R2.
```

The default verdicts are:

- `PASS`
- `PASS_WITH_NOTES`
- `RETURN_FOR_RESEARCH`
- `HOLD_FOR_INTEGRITY`

See [`references/gate-contract.md`](references/gate-contract.md) for the handoff format and [`examples/return-for-research.json`](examples/return-for-research.json) for a complete example.

Validate a report without external dependencies:

```bash
python scripts/validate_gate_report.py examples/return-for-research.json
```

## Design lineage

This is an original, deliberately narrow implementation informed by recurring needs seen across CCFA-Skills, no-ai-slop, academic humanization workflows, and ARIS-style evidence gates. It does not vendor their code or private prompts. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## License

MIT. Copyright 2026 Hanyue Shen.
