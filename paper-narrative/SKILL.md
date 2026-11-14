---
name: paper-narrative
description: Draw a paper's story on one landscape page as a LaTeX-compiled, grayscale PDF - a left-to-right spine of 4 to 6 beats (gap, idea, one or two main claims, payoff) with the literature, deduction and numerical evidence hanging under the beat it supports, a supported / thin / open verdict per beat, and a short list of what to close. Use when the user asks for a paper narrative, story map, storyline plot, "does the story hold", "where is the paper weak", a one-page view of an argument tree, or a pre-submission check of what the paper claims against what it has. An internal diagnostic for the authors, built from an argument tree or the paper's own material; never invents evidence.
---

# Paper Narrative

One page that answers two questions in under a minute: *what is the story of
this paper*, and *which parts of the story are not yet held up by evidence*.

The story runs left to right as a few boxes. Under each box hang the pieces
of evidence it rests on, drawn so their kind and their state are visible
before any word is read. A beat with nothing solid under it stands out, and
that is the point of the page.

It sits on top of the `argument-tree` skill. The tree is the complete,
auditable record (every claim, every number, every caveat, many pages). The
narrative is the reduction of that record to the handful of sentences a
reader will remember. If an argument tree exists, build from it and do not
re-derive anything. If none exists, build from the draft and the results,
under the same honesty rules.

`assets/paper_narrative_template.tex` is a complete worked example on a toy
study and `assets/example.pdf` is its output. Look at the PDF first, then
copy the template and overwrite its content.

## Inputs: ask if missing

1. **The argument tree** for the paper, or failing that the draft plus its
   results, proofs and reference list.
2. **Status date and purpose** (e.g. "before submission", "advisor meeting").

Without the paper's own material, ask for it and stop.

## The budget (hard limits)

A real paper has one or two main claims. The page is useful only if it holds
that line, so these are limits, not guidelines. Shorten or cut to meet them;
do not shrink the font or add a second page.

| Item | Limit |
|------|-------|
| Pages | 1, landscape |
| Beats on the spine | 4 to 6 |
| Main claims (heavy boxes) | 1 or 2 |
| Beat sentence | one sentence, at most 110 characters (100 with six beats) |
| Evidence items under a beat | at most 4 |
| Evidence label | at most 45 characters (40 with six beats), plus a pointer |
| Verdict reason | at most 12 words |
| To-close list | at most 4 items |

When the argument tree has more than two top-level claims, decide which one
or two the paper would be cited for. Each remaining claim becomes either an
evidence item under a main claim (it is support, not a headline), a
mechanism beat, or is left off the page. Tell the user which went where.

When a beat has more than four pieces of evidence, keep the strongest three
and merge the rest into one item ("+3 ablations", pointer "Tab. 5-7").

## Building the page

### 1. Write the spine

The default beats, in order:

- **GAP**: what is missing or wrong in the field. Rests mostly on literature.
- **IDEA**: what the paper does about it, in plain words.
- **CLAIM 1** (and **CLAIM 2**): what the paper shows. Scope each to the
  evidence, the same way the argument tree's root thesis is scoped.
- **PAYOFF**: what the reader can now do or believe that they could not.

Optional sixth beat, between the claims and the payoff: **WHY IT WORKS** (a
mechanism that is not itself a main claim) or **LIMIT** (where the result
stops holding, when the paper states that as a finding). Rename a beat when
the paper's own word is clearer (TRANSFER for a payoff that is a transfer
test). If the paper has no payoff sentence at all, say so to the user; do
not write one for it.

Six beats make narrow columns. Use the second set of sizes given at the top
of the template, and write numbers as plain text rather than in math mode
so they stay in the page's sans font.

Then write the "In one breath" line: one sentence that reads the beats in
order. If it will not go into one sentence, the beats are wrong; fix them
before drawing anything.

### 2. Hang the evidence

Each item is one `\ev` line: kind, state, a short label, and a pointer to
where it lives (`Thm. 2`, `Tab. 3`, `Fig. 4`, `[7]`).

**Kind** (same letters as the argument tree):

- `L` square: published work.
- `T` diamond: deduction, a proof or derivation.
- `N` circle: this study's own measurements.

**State**:

- `solid` (filled): in hand and checked. For `L`, the citation was verified
  and says what the label says. For `T`, a complete proof. For `N`, the run
  exists with the conditions the beat's sentence implies.
- `partial` (outline): exists but is weaker than the sentence needs. One
  seed, one dataset where the sentence says "datasets", a proof sketch, a
  citation not yet verified, a search not finished.
- `missing` (dashed): planned or absent.

Put an item under the beat whose sentence it supports, not where it appears
in the paper. Do not upgrade a state to make the page look better: the page
is for the authors, and a flattering one is useless.

### 3. Give each beat a verdict

Read the beat's sentence phrase by phrase and ask what each phrase rests on.

- **SUPPORTED**: every phrase rests on at least one solid item.
- **THIN**: some phrase rests only on partial items.
- **OPEN**: some phrase rests on nothing, or only on missing items.

Two further rules. A claim beat needs at least one solid `T` or `N` item of
the paper's own; literature alone cannot support what the paper says it
shows. A gap beat needs at least one solid `L` item.

Under the verdict, write the reason by quoting the phrase that is short of
support ("\"Without retraining\" has no evidence of its own").

A missing item that no phrase of the sentence depends on (a held-out check,
a second seed count) does not lower the verdict. Keep it under the beat,
name it in the reason, and give it a to-close entry.

### 4. To close, and scope

- **To close**: one action per thin or open beat, ordered by how much the
  story loses if it stays undone. Offer the cheap alternative where there is
  one: run the experiment, *or* cut the phrase. Number them and put
  "close n" in the pointer of the evidence item each would fix.
- **Scope of the claims**: two lines at most on where the claims hold
  (datasets, settings) and any wording that must not be read as more than it
  is. Caveats live in the argument tree; only the ones that bound a main
  claim come here.

### 5. Compile and look

Copy the template next to the paper, rename it, set `\NB` and `\colw` for
the number of beats (table at the top of the file), and fill in the
`\beat`, `\claim`, `\ev`, `\stem` and `\verdict` lines. You edit content,
not coordinates.

```
powershell -ExecutionPolicy Bypass -File <skill dir>\scripts\build.ps1 -Tex <path>\narrative.tex
```

It compiles with `pdflatex`, reports warnings and the page count, and writes
a PNG beside the PDF. Read the PNG and check:

- one page; nothing below the bottom margin;
- no beat sentence runs out of its box (shorten the sentence);
- no evidence label collides with the item below it (shorten the label);
- every arrow between beats is visible;
- every `\stem` reaches its last item and no further;
- grayscale only.

On Windows with MiKTeX, `pdflatex` and `pdftoppm` are usually on the
PowerShell path and not on the Git Bash one.

## Hard rules

- **No invented evidence.** Every item traces to the argument tree or the
  user's material. A citation that has not been verified is `partial`.
- **States are honest.** When unsure between two states, take the weaker.
- **The budget holds.** One page, one or two main claims.
- **The sentence on the page is the sentence in the paper.** If a beat had
  to be narrowed to earn its verdict, say so, so the abstract and
  introduction can be narrowed to match.

## After the PDF

Tell the user, briefly:

1. which claims from the argument tree were made main claims, and where the
   others went;
2. every thin and open beat with the phrase that is short of support;
3. any beat sentence that differs from what the draft currently says.
