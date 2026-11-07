---
name: one-pager
description: Write a one-page introduction to a project (research proposal, collaboration or funding outreach, project brief) from material the user provides. Use when the user asks for a "one-pager", "one-page summary/intro/proposal", or a single-page pitch of their project. Requires the user to name a template/purpose and supply source material.
---

# One-Pager

Turn the user's project material into a single page that a smart reader
with no background in the field can understand and act on.

## Required inputs: ask before writing if any are missing

1. **Template / purpose**: one of `research-proposal`, `outreach`
   (collaboration, job, or funding), `project-brief`, or a custom one the
   user describes. The template sets the tone and which section gets the
   most space (see "Template emphasis").
2. **Source material**: notes, draft paper, slides, data, results tables,
   code output. Everything on the page must trace back to this.
3. **Audience** (optional): who will read it. Default: an intelligent
   non-specialist.
4. **"What we need" section**: include only if the user asks for it.

If the template or the source material is missing, ask for it and stop.
Don't guess.

## Hard rules

- **No added information.** Every claim, number, and comparison must come
  from the user's material. If a section has nothing to support it, write
  `[NEEDS INPUT: <what is missing>]`. Don't fill the gap from general
  knowledge.
- **No citations or reference lists.** If the user's material attributes a
  claim to others (for example "X et al. report this is intractable"),
  paraphrase it as "prior work reports…" without a citation.
- **Assume no prior knowledge.** Define every technical term, symbol, and
  acronym when it first appears, in one short clause. Keep the field's
  standard terminology; explain it rather than replacing it.
- **Faithful results.** Report numbers exactly as the source gives them,
  with their conditions (dataset, sample size, baseline, error bars). Don't
  round in the flattering direction, don't drop caveats, and label
  preliminary results as preliminary.
- **Fits on one page.** About 450–650 words of body text plus the visuals
  (A4 or Letter, 11pt). If it runs over, cut prose before cutting the
  figure or the table.

## Presentation

- Mix short prose paragraphs with bullet lists unless the user specifies a
  style. Use prose for reasoning and bullets for lists of items or results.
- **At least one figure (required).** Plot real data from the source if
  there is any. Otherwise draw a diagram of the method or system. Don't
  plot numbers that aren't in the source. Every figure gets a one-line
  caption that says what to notice.
- **At least one table (preferred).** Good candidates: results against a
  baseline, a comparison with existing approaches along the gap dimensions,
  or a milestone timeline.
- Give the page a title and a one-sentence tagline at the top that states
  the project in plain language.

## Sections, in order

### 1. Problem statement
- The problem in plain words, then its formal version: inputs, outputs,
  objective, or hypothesis, in standard domain notation.
- Scope: what is in and what is explicitly out.
- Expected outcome or hypothesis, stated so it could be falsified.

### 2. Gap analysis
- **Research gap**: what existing approaches cannot do, or do poorly.
- Back it with at least one of the following, taken from the user's
  material only:
  - **Innovation evidence**: others have said this is hard or unsolved.
  - **Utility evidence**: others have said a solution would be valuable.
- End with one sentence that names both the novelty and the payoff.

### 3. Proposed methodology
- The overall design or pipeline, which is often where the diagram goes.
- The core theory or idea that makes it work.
- The one to three most important equations or derived results, each
  followed by a single sentence on what it means. Skip routine derivations.

### 4. Key results
- The headline results only (two to four), each with a number, its
  conditions, and the comparison point.
- If there are no results yet, say so and replace this section with
  "Preliminary evidence" or "Validation plan".

### 5. Conclusion and status
Three short lines:
- **Shown so far**: what the evidence currently supports.
- **Expected to show**: what the completed work should establish.
- **In progress**: what is underway now.

### 6. What we need (only on request)
Specific asks: data, compute, expertise, funding amount, introductions,
with a reason for each.

## Template emphasis

| Template            | Tone                  | Gets the most space        |
|---------------------|-----------------------|----------------------------|
| research-proposal   | formal, precise       | Problem, Methodology       |
| outreach            | direct, value-first   | Gap (utility), Results     |
| project-brief       | neutral, status-first | Results, Conclusion/status |

## Final check before returning
- [ ] Every claim traces to the source, and every gap is marked `[NEEDS INPUT]`
- [ ] Every term and symbol is defined at first use
- [ ] At least 1 figure (with caption); a table is present or its absence is deliberate
- [ ] Results quoted exactly, with their conditions and caveats
- [ ] Fits on one page
- [ ] "What we need" appears only if the user asked for it

After the draft, list every `[NEEDS INPUT]` item and any judgment call you
made, such as which results you chose as the headline.
