# How the author comments, and the rules behind the comments

Learned from one full read-through of a journal paper (November 2026): 66 PDF highlight notes and 112 chat turns. In away mode, Codex writes notes in this style, and Claude uses it to read the author's notes.

## Where

- **Highlights on the exact phrase**, with a note attached; no sticky notes or freehand. The highlighted words are the target: the text to delete, the text to replace, or the term being asked about.
- **Front matter gets the densest marking.** In that read-through, 37 of 66 notes were on page 1 (abstract and introduction), and the abstract was read twice.
- **Later pages get few notes**, mostly about figures, tables, columns and notation: "remove this col", "no need to mention seed, we can visualize layout", "can we draw f^min and f^max …".
- **One note can set a paper-wide change**, such as notation or a term. Apply it everywhere.

## When

- **Bursts of 5–23 notes over 5–15 minutes**, about 1–2 minutes apart, front to back. Then "new comments are in".
- **They keep annotating while a batch is being fixed** ("I will make comments as you revise; don't erase comments I made"). Hence the carry-over step.
- **Conceptual points are raised in chat, not on the PDF,** often before any editing: "Discuss first", "walk me through the introduction", "stop right there — what is the relation between our method and [closest prior method]?", "is it an extension, or sufficiently different?" Settle positioning in conversation before the text changes.

## How notes are written

They are terse and full of typos. Read the intent, not the spelling.

| Kind | Real examples | What to do |
|---|---|---|
| Delete | "rm", "rm clause", "remove.", "remove this col", "This looks unnecessary." | Delete exactly the highlighted clause; repair the grammar around it |
| The note is the new wording | "We close this gap by proving", "With this theory, this research develops", "an algorithm", "N finite observations", "the provided" | Replace the highlighted words with the note's text, then smooth the sentence |
| Template with gaps | "In the literature xxx did xxx, and xxx did xxx, but they considered it challenging to do it with xxx" | Fill the gaps from verified literature; quote verbatim |
| Demand | "citation!", "cite both", "explain", "put in italics", "regularity class? explain" | Do it; for citations, verify they exist |
| Question | "why this keyword?", "has anyone taken that route?", "is certificate an established wording here" | Answer in chat with evidence; propose wording; don't edit until answered |
| Structure | "should go to the very end … reorganize … explicitize the gap", "Remove this, there is already one problem statement before" | Move or merge; link back to the place where the thing is defined |
| Notation | "don't use C, use the notation we already have", "no need alpha and beta, keep notation", "small j_lower, j_upper might be good" | Apply paper-wide; record in `PAPER_DECISIONS.md` |
| Figure or table | "remove misses column", "remove this example, we already have the main test problem", "can we draw f^min and f^max" | Edit the figure script or table; Claude runs the scripts |
| Research request | "can we analytically present … one disproof (general, not specific)" | Treat as a QUESTION: say what it would take; don't start large work |
| Cross-reference | "I marked that earlier in the sentence, so restructure the sentence" | Read it together with the earlier note |

In away mode, the proxy's notes copy this: at most 15 words, imperative or a question, and anchored on a phrase. ("rm clause: repeats Eq. (3)", "step-by-step arithmetic here", "citation!", "defensive, cut".) The full justification goes in the notes file, not in the PDF note.

## The rules the author applies

1. **Wrong or unclear?** "He may be wrong, but if he is, it means our writing is unclear." Answer a reader's misreading by making the text clearer, never by defending it.
2. **No guarantee means remove it.** "This is mathematics, not probability … such guesses, if having no generality, don't stand." Heuristic comparisons and empirical rules without a proof get cut, not defended. An assumption the data can't check becomes a stated assumption, or is shown analytically on the example.
3. **Not defensive.** "Remove the exact, this is defensive writing." Cut hedges, "not X but Y", pre-emptive caveats and repeated limitations. State each limitation once, in its own section.
4. **Positioning by name and verbatim.** Name what prior work did; when you claim others found something hard, quote them word for word with the page ("citing verbatim is especially strong").
5. **Define once, then link back.** Remove explanations that repeat a definition, and point to the defining display. Show definitions as numbered displays, not crammed into prose.
6. **Every element must earn its place.** "What does this figure want to show? Removable?" "What is the point of this here? Is it already represented somewhere else?"
7. **Clarity through concrete examples.** Write out step-by-step arithmetic in examples. For anything confusing, use 1-D (ℝ→ℝ) pictures with simple numbers ("two given points (0,0), (1,0), then L = 1, 2, 4, 8").
8. **Plain professional wording.** No coined jargon, no word subscripts, "source function" rather than "source".
9. **Figures** are black and white, readable and compact, but not cramped ("way too compact, not clear"; "it doesn't need to be that long"). Rework completely when asked; aesthetics count.
10. **Don't redo what exists.** "Don't run, we already have literature." Reuse the evidence already there.
11. **The author can be wrong too.** Check every note before applying it.
