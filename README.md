# writing-skills

Agent skills for writing tasks (Claude Code and Codex). Each skill lives in its own folder with a `SKILL.md` and is developed on its own branch. `main` holds this catalog.

## Catalog

| Skill | Branch | What it does | Use when | Source |
|-------|--------|--------------|----------|--------|
| [one-pager](https://github.com/Henry-Hanyue-Shen/writing-skills/tree/one-pager/one-pager) | `one-pager` | Writes a one-page project introduction from the user's material and a named template or purpose. | Research proposals, collaboration or funding outreach, project briefs, single-page pitches. | Original |
| [argument-tree](https://github.com/Henry-Hanyue-Shen/writing-skills/tree/argument-tree/argument-tree) | `argument-tree` | Builds a print-ready grayscale PDF that lays out a thesis as a hierarchy of claims, each backed by labelled theoretical, literature and numerical evidence plus caveats. Uses only the user's own results and sources. | Organizing the case for a paper, proposal or decision; claim trees and evidence maps. | Original |
| [research-editor-gate](https://github.com/Henry-Hanyue-Shen/writing-skills/tree/research-editor-gate/research-editor-gate) | `research-editor-gate` | Audits and revises research manuscripts as a single linguistics and methodology editor, preserving claims and returning missing research to the caller. Includes a gate-report validator and tests. | Final editorial gates, claim-evidence consistency, methodology reporting, terminology and scholarly prose. Not for literature search or running experiments. | Original (moved from its own repo) |
| [anti-defensive-writing](https://github.com/Henry-Hanyue-Shen/writing-skills/tree/anti-defensive-writing/anti-defensive-writing) | `anti-defensive-writing` | Removes unnecessary caveats, disclaimers, stacked hedges and apology-like framing while keeping limits needed for accuracy, method, ethics, law and safety. Covers English and Chinese, papers, technical plans and SOPs. | Drafting or revising abstracts, introductions, contribution statements, discussions, grants, reports. | Copy of [Kiterlin/anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing), MIT License, © 2026 Kiterlin |
| [stage-grid-figure](https://github.com/Henry-Hanyue-Shen/writing-skills/tree/stage-grid-figure/stage-grid-figure) | `stage-grid-figure` | Draws a black-and-white LaTeX/TikZ method-comparison figure: rows are methods (baselines, then "Ours" in a shaded band), columns are pipeline stages, data objects are icons and operations are boxes. Includes a worked template, its render, and a PowerShell preview script. | Overview, architecture or "Fig. 1" figures that show how a method differs from baselines stage by stage. | Original |
| [author-revision-loop](https://github.com/Henry-Hanyue-Shen/writing-skills/tree/author-revision-loop/author-revision-loop) | `author-revision-loop` | Revise a paper through one annotated PDF; Codex edits, Claude checks; away mode acts as the author. Editing skill: supervise its use. | Revising a LaTeX paper with its author through highlight notes on one reading PDF, or continuing revisions while the author is away. | Original |
| [paper-narrative](https://github.com/Henry-Hanyue-Shen/writing-skills/tree/paper-narrative/paper-narrative) | `paper-narrative` | Draws a paper's story on one landscape, grayscale, LaTeX-compiled page: a spine of 4 to 6 beats with 1 or 2 main claims, the literature, deduction and numerical evidence under the beat it supports, a supported / thin / open verdict per beat, and a short to-close list. Built from an argument tree or the paper's own material. | Checking whether a paper's story is held up by its evidence before submission; a one-page view of an argument tree. | Original |

## Install a skill

Copy the skill's folder into your skills directory, for example `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex):

```bash
git clone --branch <branch> --single-branch https://github.com/Henry-Hanyue-Shen/writing-skills.git
cp -r writing-skills/<skill-folder> ~/.claude/skills/
```

## Adding a skill

1. Create a branch named after the skill from `main`.
2. Put the skill in a folder of the same name with a `SKILL.md` (frontmatter `name` and `description`).
3. Add a row to the catalog above, on `main` and on the skill's branch.
4. For a skill copied from elsewhere, keep its license file and credit the source in the catalog.
