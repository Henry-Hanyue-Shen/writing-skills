---
name: stage-grid-figure
description: Draw a stage-aligned method-comparison figure for a paper in LaTeX/TikZ — rows are methods (baselines, then "Ours" in a shaded band), columns are pipeline stages, data objects are small icons and computations are boxes, all in black and white. Use this whenever the user asks for an overview figure, architecture figure, pipeline figure, "Fig. 1", method diagram, or a figure showing how their method differs from prior work or baselines in a LaTeX paper, and also when they ask to revise, extend or restyle such a figure, or say something like "draw it like the RISA-D / FedAvg-AFL-ours figure". Prefer this over a free-form block diagram whenever two or more methods share the same sequence of stages.
---

# Stage-aligned comparison figure (TikZ)

A figure that answers "how is our method different from the closest ones?" as a grid. Each row is one method; each column is one stage that every method passes through (for example: samples, client computation, upload, server computation, result). The reader compares methods by scanning down a column, so every difference has a fixed place to be found.

`assets/stage_grid_template.tex` is a complete worked example (FedAvg vs AFL vs an analytic detection head) and `assets/example.png` is its render. Look at the PNG first to see the target, then copy the template and rewrite it.

## Why this form

A side-by-side pair of block diagrams makes the reader hunt for what changed. Text in a table tells them, and they have to read it. The grid shows it: when one row has a single bar and the row below has four, or one matrix against a stack of matrices, the difference registers before any word is read. The whole design follows from that goal: the differences between methods should be visible as pictures, in the same position in every row.

## Step 1: fill in the grid before drawing

Write the content as a table first (in your head or in the chat, not as a file), one row per method and one column per stage. Read the paper's method section and the related work on the baselines for this; do not invent what a baseline does.

- **Rows:** 2 to 4. Order them from most different to the proposed method: the standard baseline first, the closest prior method directly above "Ours", so the hardest comparison is between adjacent rows.
- **Columns:** 3 to 5 stages plus the title column. Choose stages where at least one method differs. A stage in which all rows are identical earns no column; merge it into a neighbour.
- **Cells:** for each cell write (i) the object or operation and (ii) the one or two words that set it apart from the other rows. Those words are the only ones that go in bold.

A cell may be empty or spanned. An iterative method that has nothing to "upload once" gets a pair of opposite arrows crossing that column with the loop count on the return arrow (row (a) in the template). Do not force a box into every cell.

If the content of a cell is unclear from the paper, ask the user for that cell; a wrong baseline description in Fig. 1 is the kind of error reviewers catch.

## Step 2: draw

Copy `assets/stage_grid_template.tex` next to the paper's `main.tex` (e.g. `fig_overview.tex`) and edit it in this order.

1. **Layout block.** Set the separators `\sA…`, column centres `\cA…`, row centre lines `\ya…` and the horizontal rules. Total width 17.85 cm fits the IEEEtran two-column text width; for another class set `\xR` to the text width in cm minus about 0.3 and rescale the separators. Give the title column about 1.9 cm, which holds a bold row title of about 11 characters; widen it for longer method names, since a title that reaches the first separator is the most common first-render defect. Split the rest by how much each stage has to hold. Rows may differ in height: about 1.5 cm for a plain row, about 2.4 cm for a row with labels both above and below its icons.
2. **Frame.** Header names (bold, at most three words), the band behind the proposed method's row, the row titles (`\textbf{(a) Name}` plus a second line giving the task or setting).
3. **Rows, one section each.** Place everything relative to the row's centre line (`\yc-0.28`, `\yc+0.72`) so a row moves as a unit.

Conventions the template follows, and why:

- **Data objects are icons, operations are boxes.** Images, feature vectors, matrices and weights are drawn with the small glyph macros (`\imgicon`, `\vecbar`, `\gram`, `\wmat`); anything that computes is a `blk` node with text. This separation lets the reader tell "what flows" from "what is done" without a legend. Add a new glyph macro when a new kind of object appears; keep each glyph under about 0.75 cm.
- **Quantity is shown by count.** One feature per image is one bar; many proposals are four bars; per-class statistics are a stack of four offset squares; a different kind of statistic gets a darker fill. Reuse the same glyph across rows so that only the count or shade changes.
- **Bold marks what is specific, nothing else.** Bold the words that distinguish a cell from the same cell in other rows (`\textbf{one} feature per \textbf{image}` against `\textbf{300 proposals} per image`). If everything is bold, the bold stops pointing at anything.
- **Black and white only.** White boxes, `black!9` for the band, `black!30` to `black!70` for glyph fills, `black!45` for the dashed separators. The figure must survive a grayscale print, and the user's house style for paper figures is B&W.
- **Text stays small and short.** `\scriptsize` throughout, at most two lines per box and about four words per line. Symbols go under the glyph they name (`$W$`, `$X_k^\top X_k$`); a short phrase above or below a cell says what the glyphs are.
- **Arrows run left to right along the row's centre line**, from node anchors (`b2.east`) to explicit coordinates just short of the next glyph. Leave at least 2 mm between two boxes that an arrow connects, or the arrowhead disappears. When several boxes share one cell, add up their widths (text width + 1.4 mm each) plus the gaps and check the sum against the cell width before compiling.
- **Absolute coordinates** rather than `positioning` chains. Columns have to line up across rows, and relative placement drifts.

**Caption.** One sentence saying what is compared, then one sentence per reading the figure supports, naming the stages in the order of the columns. The caption tells the reader what to look for; it does not restate the cell contents.

## Step 3: render and look

A TikZ figure placed by hand is wrong on the first compile more often than not, and the errors are only visible in the render. Compile the figure alone and read the PNG:

```
powershell -ExecutionPolicy Bypass -File <skill dir>\scripts\preview.ps1 -Fig <path>\fig_overview.tex
```

It copies the figure into `_figpreview\` beside it, compiles it in a one-page wrapper (pass `-Class '\documentclass{article}'` or the paper's class line if it is not IEEEtran, and `-Preamble` for any paper macros the figure uses), prints the warnings and writes `_figpreview\preview.png`. `\cite` shows as [?] in the preview; that is expected. On this machine pdflatex (MiKTeX) is on the PowerShell path, not the Bash one.

Read the PNG and check, cell by cell:

- no box, label or glyph crosses a dashed separator or touches the band's frame;
- no two labels overlap, and every label is nearer to its own glyph than to a neighbour's;
- every arrow has a visible shaft and head, and ends short of its target;
- the same stage sits at the same x in every row;
- the differences are the first thing visible: cover the text mentally and see whether the rows still look different. If they do not, replace a text difference with a count or shade difference;
- bold appears only on distinguishing words;
- no `Overfull` warning (the picture is wider than the text).

Fix and re-render until a pass finds nothing. Two or three rounds is normal. Delete `_figpreview\` when done, or leave it out of the submission archive.

## Step 4: put it in the paper

- Preamble: `\usepackage{tikz}` and `\usetikzlibrary{arrows.meta}`.
- `\input{fig_overview}` right after the contribution list at the end of the introduction, so it lands at the top of page 2 in a two-column paper.
- Replace the placeholder cite key with the paper's key and check it against the bibliography.
- Compile the paper and confirm the figure number, its page, and that the first reference to it in the text comes before it.

## Variations

- **Single-column figure** (`figure` instead of `figure*`): at about 8.8 cm there is room for three stages and very short cells; drop the phrases above and below and keep glyphs plus one-word boxes. If it does not fit without shrinking the font below `\scriptsize`, use the two-column form.
- **Two methods only:** keep the grid; the rule between baseline rows goes away and the band still marks the proposed method.
- **Venues without a two-column layout** (ICLR, NeurIPS; text width about 14 cm): four stages at most, or tighten the title column to 1.5 cm.
- Avoid `\resizebox` to make an oversized picture fit: it shrinks the text below the caption size and the figure stops matching the paper's type.
