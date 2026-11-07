# Editorial standard

Use this standard for substantive manuscript gates. The priority order is fixed: evidence and meaning, locked material, terminology identity, methodological accuracy, argument structure, scholarly register, then local style.

## Linguistic audit

Check the complete editable scope rather than treating isolated words as defects.

- Preserve every material proposition and its logical relation to adjacent claims.
- Preserve meaningful uncertainty, attribution, negation, comparison direction, causal strength, and scope.
- Use one canonical term per concept while retaining declared abbreviations, grammatical variants, and intentional distinctions.
- Repair ambiguous pronouns, dangling modifiers, hidden agents, broken parallelism, overloaded sentences, and paragraph order when the intended meaning is established.
- Remove process leakage, empty throat-clearing, repetitive caveats, unsupported importance claims, generic summaries, synonym cycling, mechanical rhetorical templates, and decorative formatting.
- Preserve functional hedging, passive voice in methods, field-specific nominalization, and necessary repetition. Academic prose need not sound conversational.
- Judge document-level patterns by function and distribution. A word list or frequency threshold is never sufficient evidence of poor writing or AI authorship.
- Preserve the author's recognizable level of directness and disciplinary voice. Do not introduce artificial roughness or random sentence variation.

For bilingual material, establish explicit mappings between translated technical terms. Do not translate proper names, model names, dataset identifiers, citation keys, formulas, or code unless instructed.

## Methodology audit

This is an audit of how the supplied research is reported, not a mandate to redesign it.

Check whether the manuscript states, where relevant:

- research question, estimand, hypothesis, or engineering objective;
- data provenance, inclusion/exclusion rules, splits, preprocessing, and leakage controls;
- method components, assumptions, training/inference conditions, and implementation-defining settings;
- baselines, comparator identity, full configurations, and the distinction between main methods and ablations;
- metrics, units, directionality, aggregation, uncertainty, sample size, seeds, and statistical procedures;
- resource and reproducibility details needed to interpret reported results;
- limitations and external-validity boundaries that materially affect the claim.

Cross-check text, equations, tables, figures, captions, appendix, and bibliography. Recalculate simple deltas and rounding deterministically when possible. Classify an issue as:

- `reporting-defect`: the needed information exists in the supplied bundle and can be edited in;
- `evidence-gap`: the manuscript makes a claim that the supplied bundle does not support;
- `research-gap`: resolving the issue requires a new source, experiment, analysis, or recovered artifact;
- `integrity-conflict`: supplied sources materially disagree or provenance is broken;
- `author-choice`: more than one scientifically faithful presentation remains possible.

Fix reporting defects directly. Return research gaps to the caller. Do not turn a preferred experiment or extra citation into a blocking requirement unless the current claim actually depends on it.

## Claim and citation audit

- Map each central claim to a supplied result, source, or explicitly labeled hypothesis.
- Metadata existence does not prove that a citation supports its surrounding sentence.
- Do not cite a search snippet, social post, or secondary summary when the primary record is available.
- Separate `unsupported`, `overstated`, `not comparable`, and `internally inconsistent`; they require different remedies.
- Preserve negative results and known limitations. Do not improve the story by omission.
- Never create a reference entry from memory. A missing or questionable source becomes a return packet.

## Final comparison

Read source and revision side by side. The revision fails if it adds an unsupported proposition, drops a material source claim, changes a number or unit without evidence, changes causal/modal force, alters a locked span, merges distinct concepts, leaks process text, or silently resolves an evidence conflict.
