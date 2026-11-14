# author-revision-loop

> [!WARNING]
> **This is an editing skill. Supervise it.**
> It changes your manuscript's source files and rebuilds the PDF you read. In away mode, Codex acts as you and Claude applies what it accepts without asking you first.
> - Check every batch before you treat it as done. Read the red text and the struck-out deletions in the PDF, and the held questions in `PENDING.md`.
> - Do not submit, share or send a version the loop produced until you have read it yourself.
> - Every rebuild keeps a rollback copy in `delivery/archive-before-<date>-<tag>/`. Use it if a batch went wrong.
> - The skill never submits a paper, messages a co-author or runs new large experiments. If a session tries to, stop it.

## What it does

It runs a paper revision loop worked out on a real journal-paper revision (November 2026).

- **You read one PDF and highlight phrases with short notes.** Claude reads the notes and Codex makes the edits. Claude checks every edit against the source and the maths, then rebuilds the same PDF. Changes show in red, and deletions show red and struck out. Your marks are never lost.
- **When you're away**, Codex reads the sections you haven't read yet, acting as you, and writes notes in your style. Claude vets each note. Sure fixes and cuts are applied in red, and anything that touches a claim, a proof or a number is held for you. The proxy's notes then appear as blue (applied) or orange (held) highlights in the same PDF, under the author name "Claude (as author)".

## Modes

| Mode | Say | What happens |
|---|---|---|
| Setup | "revise this paper with me", "set up the read-through" | Reading PDF, archive folder, `PENDING.md`, `PAPER_DECISIONS.md`, red-markup macros |
| Present | "new comments are in", "same drill", "fix the ones you are sure first" | Extract notes → triage → Codex edits, Claude checks → rebuild, carry over your new marks → "refresh" |
| Away | "act as me", "instead of me, run a batch", "I'm away" | Codex as author (notes only) → Claude vets → apply in red → proxy highlights in the PDF → summary |

## Layout

```
SKILL.md                      the loop Claude follows
references/comment-style.md   how the author comments (real examples) and the judgment rules
references/marking.tex        \rn (new, red), \rdel (deleted, red + struck), \rdelnote; one switch for black
scripts/notes.py              read the author's highlight notes (marked words, page, time)
scripts/carry.py              copy unhandled/new author marks onto a rebuilt PDF
scripts/proxy_annotate.py     put the away-mode notes into the PDF as highlights under a separate author
scripts/finalize.py           clean source for submission: drop deletions, unwrap red
templates/                    PAPER_DECISIONS.md, the two Codex briefs
```

Needs Python 3.11 with PyMuPDF (`py -3.11`), a LaTeX install with `ulem` and `xcolor`, and the `codex` skill (`~/.claude/skills/codex/cx.sh`).

Version 0.1, 2026-11-13.
