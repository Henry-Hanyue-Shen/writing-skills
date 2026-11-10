---
name: argument-tree
description: Build a print-ready, grayscale PDF "argument tree" that lays out a research thesis as a hierarchy of claims, each backed by separately labelled theoretical, literature, and numerical evidence plus explicit caveats. Use when the user asks for an argument tree, claim tree, evidence map, "organize the arguments/evidence", or a structured case for a paper, proposal, or decision. Requires the user's own results and sources; never invents evidence.
---

# Argument Tree

Turn a body of research (results, proofs, related work) into a document a
reviewer can audit in minutes: page 1 is a tree from one root thesis down
to tagged sub-claims; the following pages give, claim by claim, the evidence
that supports each node and the boundaries where it stops holding.

The LaTeX template is in `assets/argument_tree_template.tex`. Always start
from it so the visual style stays identical: grayscale, square corners,
sans-serif headings, serif body, boxed evidence tags.

## Required inputs: ask before writing if any are missing

1. **The thesis or goal**: what the document must argue (a paper's main
   claim, a go/no-go decision, a proposal's case).
2. **Source material**: result tables, logs, analysis output, proofs or
   formal-check logs, draft text, and the references the user relies on.
3. **Audience and purpose** (optional): e.g. co-authors, reviewer
   rehearsal, advisor meeting. Sets how much detail goes into each box.

If the thesis or the source material is missing, ask for it and stop.

## Hard rules

- **No invented evidence.** Every number, proof status, and literature
  statement must trace to the user's material or to a source you verified.
  Where support is missing, write `[NEEDS INPUT: <what>]` in the box.
- **Tag honestly.** `[T]` only for statements that are actually proved
  (say how: a formal proof assistant, a written proof, or "proposed"). `[N]` only
  for this study's own measurements. `[L]` only for published work you have
  checked.
- **Verify every citation** before it goes in the reference list: confirm
  authors, title, venue, year, and that the paper says what the box claims.
  Read the full text, not just the abstract, for any work cited as
  "closest prior work" or as the basis for a novelty claim. Put the
  verification date in the references heading.
- **Scope the root thesis to the evidence.** If a result is not significant,
  say "not significantly different", not "equivalent". If a result holds on
  one dataset only, say so in the claim, not just in a caveat.
- **Compare like with like.** Best configuration vs best configuration with
  seeds aggregated within each; never average across configurations, and
  never compare a historical default against a tuned best as if they were
  the same comparison. State whether "best" was picked on validation or test.
- **Every claim gets a caveats box** unless it truly has no boundary.
  Negative or mixed results go in the document, not out of it.
- **Report numbers with their conditions**: dataset, n, seeds, SD or CI,
  test used. Don't round in the flattering direction.

## Structure

### Page 1
- Title line: `Argument Tree: <short title>`, a subtitle with venue or
  purpose, scope, and status date, and the evidence-type legend.
- **Root thesis box**: one to three sentences; bold the load-bearing phrases.
- **The tree** (forest, growing left to right):
  - Level 0: the root (2–4 words).
  - Level 1: 3–6 claims `C1…Cn`, each a short noun phrase.
  - Level 2: 2–4 sub-claims `Ck.j` per claim, ≤ ~60 characters, each
    ending with its evidence tags.
  - The tree must fit on page 1. Shorten labels before shrinking the font.

### Following pages: one section per claim, in this order
1. `claimbox`: the claim title and a one-sentence precise statement.
2. `thbox`: propositions, the exact statement, assumptions, and how each
   was checked (theorem names if formally verified).
3. `nubox`: a two-column table (`Ck.j` | result) or a results table.
4. `libox`: what each cited work shows, the closest prior work, and the
   exact difference from it.
5. `cabox`: where the claim stops holding; failed controls; untested scope.

Omit a box type a claim genuinely lacks; don't fill it with filler.

### End
- A `cabox` titled `GLOBAL LIMITATIONS AND SOURCES`: significance status of
  each headline comparison, seed counts, which claims are proved vs numerical
  only, citation-verification date, and where the raw results live.
- `References (verified <date>)`: numbered list, every entry checked.

## Building the PDF

1. Copy `assets/argument_tree_template.tex` next to the user's work, rename
   it, and replace every `<<…>>` placeholder and all example content.
2. Compile twice with `pdflatex`. Packages: forest, tcolorbox (most),
   tabularx, booktabs, enumitem, mathptmx, helvet, microtype. Keep `helvet`:
   without it T1 sans fonts may fall back to bitmap fonts that fail to build.
3. Forest pitfalls: wrap every node in `{…}` (commas break parsing); use
   manual `\\` in level-0/1 labels; don't define macros named `\TH`, `\L`,
   etc. (clashes); the tags are `\EvT`, `\EvL`, `\EvN`.
4. Render page 1 to an image (e.g. `pdftoppm -r 60 -png`) and look at it: the
   tree must be on one page with no overlapping nodes, and no box may overflow.
5. Keep it grayscale. If figures are needed, draw them in black and white
   with line styles and markers rather than converting colour plots.

## Optional companion: data compendium

If the user wants the evidence itself, build a second PDF in the same
style (same preamble, boxes, and tags) that reproduces every number cited in
the tree with its full source table, per-run listings, figures, and a
provenance table mapping each section to its files. Generate tables from
the raw files with a script rather than retyping numbers.

## Final check before returning
- [ ] Root thesis claims no more than the evidence shows
- [ ] Every leaf has at least one tag, and every tag is justified
- [ ] Every number has its conditions; significance stated where relevant
- [ ] Every citation verified (date in the heading); closest prior work read in full
- [ ] Every claim has its caveats; negative results included
- [ ] Tree fits on page 1; PDF compiles without errors; grayscale only

After the PDF, list every `[NEEDS INPUT]` item, any claim you narrowed to
fit the evidence, and any citation you could not verify.
