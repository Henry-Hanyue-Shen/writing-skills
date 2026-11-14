---
name: author-revision-loop
description: Revise a LaTeX paper with the author through one annotated reading PDF, with Codex making the edits and Claude checking them, changes in red and deletions red-struck; or act as the author while they are away. Use when the user says "new comments are in", "same drill", "codex fix you check", "refresh", "revise this paper with me", "set up the read-through", or "act as me", "instead of me run a batch", "I'm away, keep revising", or names the paper-revision loop.
---

# Author revision loop

This is an editing skill. It changes the user's manuscript, so keep everything reversible and visible: red markup, rollback copies, held questions. Never submit, send to co-authors, or start large new experiments.

Paths below are relative to the paper folder. `$SK` is this skill's folder (`$USERPROFILE/.claude/skills/author-revision-loop`). Run the scripts with a Python that has PyMuPDF (`py -3.11` on Windows, `python3` elsewhere). In Git Bash on Windows, `py` may not be on the PATH; use PowerShell or the interpreter's full path.

Read `references/comment-style.md` before the first batch. It describes how the author writes notes and the rules they apply.

## Files in the paper folder

- `delivery/<Paper>.pdf` is **the one reading PDF**. The author reads and annotates only this file. Rebuild into it; never give them a second file to read.
- `delivery/archive-before-<YYYYMMDD>-<tag>/` holds the annotated copy from before each rebuild (rollback).
- `audit/notes-<date>/PENDING.md` holds items agreed but not applied, held questions, and the extraction time of the last batch.
- `PAPER_DECISIONS.md` holds notation, wording and positioning decisions the author has made. Append to it whenever they decide something. Codex reads it in every brief.

## Setup (once per paper)

1. Find the main `.tex`, the build command and the current PDF. Copy the PDF to `delivery/<Paper>.pdf` if it isn't there yet.
2. Add the macros from `references/marking.tex` to the preamble of each document (main and supplement). Keep any existing `\rev`/`\rn` meaning.
3. Create `PAPER_DECISIONS.md` from `templates/PAPER_DECISIONS.md`, filled from memory and the paper's notes, and `audit/notes-<date>/PENDING.md`.
4. Tell the author the reading PDF's path and wait for notes. Don't push rewrites nobody asked for.

## Present mode: one batch

1. **Extract.** `notes.py delivery/<Paper>.pdf --exclude-author "Claude (as author)" --json audit/notes-<date>/batch-<n>.json`. Every author mark still in the reading PDF is unhandled, because handled ones disappear at rebuild. Record the printed `extracted_at` in `PENDING.md`.
2. **List** each note with the words it marks, front to back. Read each note's intent, not its spelling. A note may refer to an earlier note.
3. **Triage.**
   - Sure fixes go first, without waiting.
   - Questions get answered in chat, with a concrete explanation and proposed wording. Use 1-D (ℝ→ℝ) pictures and step-by-step arithmetic for anything that confused a reader.
   - Conceptual points wait for the author.
   - A note can be wrong ("I might make mistakes, check before any revision"). If applying it would make a statement false, say so instead of applying it.
   - Notation notes apply across the whole paper, not just at the marked spot.
4. **Edit.** Codex makes the edits with `templates/brief_apply.txt`: one file per run, runs in parallel, `bash "$USERPROFILE/.claude/skills/codex/cx.sh" -w -C "<paper dir>" < brief`. Each brief says which notes to apply and which to skip. Codex cannot run Python or LaTeX, so you run figure scripts and builds.
5. **Check every diff** against the note and the maths before building: numbers, inequalities, notation consistency, citations (verify they exist). Fix or revert anything wrong.
6. **Rebuild** (main and supplement if touched). Then:
   - copy the annotated reading PDF to `delivery/archive-before-<date>-<tag>/<Paper>_annotated.pdf`;
   - run `carry.py <archived> <new build> delivery/<Paper>.pdf --cutoff <extracted_at> --keep audit/notes-<date>/held-keys.txt`. This copies marks made during the batch and the marks you held onto the new PDF;
   - if proxy notes are still held, re-run `proxy_annotate.py`.

   If the overwrite fails because the PDF is open in a viewer, say so; don't write a differently named file.
7. **Notify:** "refresh `<path>`", a short list of what changed, what was held and why, and the archive folder.

Markup: new or changed text goes in `\rn{}`, deleted text in `\rdel{}` (red, struck through). It does not just disappear. Black only when the author asks (`\markupfalse`). Even then keep the macros in the source, so red can come back.

## Away mode: acting as the author

Use it when the author says they are away and asks you to continue ("instead of me, run a batch of revisions for the sections I didn't check yet").

1. **Scope.** Work only on the sections the author has not read yet. Check the batch history and `PENDING.md`. Back up each section file to `audit/author-pass-<date>/<file>.before.tex`.
2. **Author pass, notes only.** Run one Codex job per section in parallel with `templates/brief_author_pass.txt` (read-only except its own notes file). Each note is typed FIX, CUT or QUESTION, carries a PDF anchor and a short note in the author's voice, and gives the exact LaTeX to change.
3. **Vet every note yourself.**
   - **Apply** FIX and CUT notes that are sure and do not change a theorem, a proof step, a reported number or a result.
   - **Hold** anything that changes a claim, a hypothesis, a number or evidence, or that removes a whole experiment or figure. Holding means recording it in `PENDING.md`, not applying it.
   - **Reject** notes that contradict `PAPER_DECISIONS.md` or an earlier request from the author.
   - Redo the maths of every applied note by hand.
4. **Apply** with `templates/brief_apply.txt`, one file per run. Cuts become `\rdel{...}`, struck through in red. They must never just disappear.
5. **Check diffs and rebuild** exactly as in present mode, with archive and carry-over.
6. **Proxy highlights.** Write `audit/author-pass-<date>/proxy_notes.json` with one entry per applied, held or rejected note. Give each an anchor: words that appear in the new PDF, taken from the changed text. Then run `proxy_annotate.py delivery/<Paper>.pdf proxy_notes.json`. Applied notes show blue and held notes orange, and rejected notes appear only when they explain a kept passage. All are under the author name "Claude (as author)", so the author reviews them where they read.
7. **Summary**, waiting for the author's return: counts (notes, applied, held, rejected); the mathematical errors found; the held questions with your recommendation each; the rollback folder.

Proxy highlights are not the author's notes. `notes.py --exclude-author` skips them, and they are dropped at the next rebuild unless still held. If the author answers one, they add their own highlight, and you treat that as a normal note.

## Hard rules

- Never erase the author's marks. Archive before every overwrite and carry over anything made after extraction.
- One reading PDF, rebuilt in place.
- Don't rerun what already exists ("don't run, we already have literature").
- No new large experiments without approval. If the data for a requested number is missing, say so; don't fill it in.
- Verify every citation and quote prior work verbatim with its page.
- Report what you did faithfully, including what was held, reverted or not verified.
