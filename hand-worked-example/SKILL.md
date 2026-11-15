---
name: hand-worked-example
description: Write (or repair) a hand-worked example in a paper that carries an algorithm out step by step so a reader with a pencil can reproduce every number. Use when the user says "hand-worked example", "handwritten example", "followable steps", "trace the algorithm by hand", "walk me through it step by step", "derive it by hand", "this reads like a deduction, not an algorithm", "where does this number come from", or asks to make a numerical example mechanical, checkable or "like a programme".
---

# Hand-worked example

A hand-worked example is the **execution** of the paper's algorithm on one tiny instance. It is not an explanation, not a proof, and not pseudo-code. The test: a reader with pencil and paper, who has read the theory, can reproduce every number without guessing a single step.

"An algorithm is mechanistic, not jumpy." Every time the author asks "where does this come from?", "what is this?", "how did X pop out?", the paper has a defect at that spot. Fix the paper there; answering in chat is not enough.

## 1. Choose the instance

- **Small but complete.** The smallest instance in which every branch of the algorithm happens at least once: e.g. two candidates that compete, one candidate that is rejected, an answer that is not at an obvious place (not at a grid vertex, not at a data point).
- **Friendly numbers.** Dyadic values (1/2, 1/4, 1/8) or small integers (1, 2, 8). No decimals, no irrational constants.
- **Same dimension as the claim's first hard case** (if the paper's point is "several variables", use two variables, not one).
- Compute the whole example with an exact-fraction script first, and keep the script and its output in the evidence folder. The paper's numbers are copied from that output, never typed from memory.

## 2. Structure of the subsection

1. Data table **at the very start** of the subsection (pin it there; it must not float above the heading).
2. One opening sentence: "Consider Problem N for the data of Table T: …" plus "Each step below evaluates one formula of Sections X and Y, which is cited."
3. One run-in heading per action of the algorithm, **in the algorithm's order**, named by what is computed ("Compute the bound", "Construct the grid", "Fill the table", …).
4. Each step has exactly three parts:
   - **Rule**: one formula, with the citation of the numbered equation in the theory that it instantiates.
   - **Work**: a calculation table in which every entry is computed, with its arithmetic visible (`3/2 + 2(1) = 7/2`).
   - **Result**: the quantity obtained, named, and where it is used next.
5. End with the final output and (optionally) a short comparison paragraph.

## 3. Rules (each one is a correction an author actually had to make)

**Show, do not describe.**
- No sentence that describes what a table "holds" or "contains". Show the table being filled: one row per entry, in the order the entries are computed, with the earlier entries each one uses.
- No pseudo-code block inside the example. The algorithm box lives in the theory section; here it is carried out.
- No line-number references ("Line 11"). Nobody counts lines. Cite equations.
- For a search step, show one **rejected** candidate with the reason, and the **accepted** one.

**Every number has a visible origin.**
- If a table entry is the result of arithmetic, the arithmetic is in the table or in the column next to it.
- If a constraint, coefficient or intercept is assembled from parts, give a row or a general first row with the rule (for a constraint `a₁x₁ + a₂x₂ + t ≥ b`, list `a₁, a₂, 1, b` and say how each one is obtained).
- Do not put arithmetic in a summary table when the reader has already seen it; a summary table lists values only.
- Delete a table the moment the author says it is unnecessary.

**Every symbol is defined before use, and says what it is.**
- State what a quantity *is* in words the first time ("the constant term of the line is its intercept, denoted b").
- A symbol that appears once is not named: write it out (e.g. in vector form) where it is used.
- An index needs its object: not "indices 0, 1, 2" but "z₀ = 0, z₁ = 1/2, z₂ = 1".
- A rule must be usable in every case the example meets (e.g. a rule stated for a point inside a cell must also say what to do for a point outside it).
- Never compare unlike objects ("the function is at least a constant" when you mean its value at each point). Write the pointwise formula.

**Follow the implementation, not the proof.**
- Present what the algorithm does. Objects that exist only in the proof (an auxiliary program, an identity used to show optimality) are not steps. Offer them as a remark: "The result can be checked by computing …".
- If a condition can never fail when the procedure is followed, do not present it as a test.

**Scope.**
- When a step is carried out for one instance of several (one cell of a grid, one case of four), open with "Consider the case …" and say where the others are listed. Then give one table with the results for all.
- Say which objects are shared by all instances and which belong to one.

**Ground every action in the theory.**
- Each action cites a numbered equation, theorem part or algorithm of the theory sections.
- If the theory does not state the formula the example uses, **add it to the theory and number it**, then cite it. This is also a check that the theory is complete.
- Finish with an audit table: action → what it cites. Anything uncited is either added to the theory or flagged to the author.

**Typography.**
- Horizontal fractions (`3/2`) everywhere in the example; stacked fractions look messy in tables.
- Matrices and tables side by side, with equal column widths so entries line up. Check the rendered crop, not the source.
- Wide tables: drop columns whose content is visible elsewhere before shrinking the font.
- Every table and figure of a subsection sits inside that subsection (float barriers before the next heading).

**Words.**
- Plain words for implementation details ("M is rounded up to a fraction because the algorithm computes with exact fractions"), not jargon ("rational upper enclosure").
- Respect the author's banned words; grep for them before every build.

## 4. Working with the author

- If the author wants to be walked through it first: step 0 is the data; then one step per message, with the full arithmetic of the entry they ask about. Stop when told to stop.
- Treat each question as a bug report against the paper. After answering, change the paper so the next reader does not need to ask, and show the rendered crop.
- Do not swing to the opposite failure: "this is a programme" means "it is mechanical, so show it being run", not "paste pseudo-code". If two instructions seem to conflict, the constant is: **formula + filled-in table, in algorithm order**.
- Do not explain more than was asked in chat; the paper carries the detail.
- When the author says a shorter form is enough (keep only the left-hand side, remove a table), shorten at once and do not re-add later.

## 5. Verify before delivering

1. Recompute every number with an exact-fraction script independent of the one that produced it.
2. Have a second model (e.g. Codex, read-only) recompute the whole example and cross-check the surrounding numerics; fix what it confirms.
3. Compile; no errors, no undefined references, no overfull boxes; search the PDF text for banned words and for "Line N".
4. Render the pages of the example and look at every table.

## 6. The same spirit for the numerical experiments

Experiments need far less detail than the hand example. For each experiment say only: the source (one formula), the data and the fit (degree, fitting method, sizes), each parameter with its **value and its justification**, then the results. State plainly which runs are exact and which are numerical evaluations.

## Checklist

- [ ] Data table first; "Consider …" opening; steps in algorithm order
- [ ] Each step: cited formula → calculation table with visible arithmetic → named result
- [ ] No prose descriptions of tables, no pseudo-code, no line numbers
- [ ] Every symbol defined before use; one-off symbols written out
- [ ] One rejected and one accepted candidate for each search
- [ ] "Consider the case …" wherever one instance stands for several
- [ ] Proof-only facts appear as "can be checked by", not as steps
- [ ] Every action cites the theory; missing formulas added to the theory
- [ ] Horizontal fractions; aligned tables; floats inside the subsection
- [ ] Numbers recomputed independently; build clean; rendered pages inspected
