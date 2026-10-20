---
name: alevel-manual-specs
description: Hand-authored crop specs for Cambridge A Level question papers that the automatic splitter cannot handle, and for fixing a defect in one paper's crops, using al_manual.py (lines / init / run) in the ROOTATOM A Level pipeline. Use whenever a paper is on HOLD, a reviewer found a real defect in a crop (context in the wrong part, furniture visible, mark missing, figure sliced, dotted lines left, question number showing), an old paper has an unusual layout (2002-04 Paper 5, Options papers, essay sections), or when briefing hand-spec agents — e.g. "write specs for the 49 Biology holds", "fix Q2.c.ii in 16m-42", "this crop shows For Examiner's Use".
---

# Manual specs (held papers and per-paper fixes)

Code `~/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_manual.py`, Python `~/.venvs/alevel/bin/python -I`.
Specs: `~/rootatom_data/ALEVEL/manual/<PREFIX>.json` → crops in `splits/manual/<PREFIX>/`, sheets `review/manual/<PREFIX>_NN.jpg`.
A manual spec **supersedes** the automatic split of the same paper (the approved crops are the manual ones).

## Commands
```
al_manual.py lines SOURCE.pdf PAGE      # text rows: y0 y1 x0 text (PDF points, page 1-based)
al_manual.py init PREFIX RUN            # draft spec from an existing split's provenance (keeps dot masks)
al_manual.py run PREFIX                 # render, run BOTH gates, make contact sheets; read gates.log
al_manual.py render SPEC OUTDIR         # render only (regressions)
```
Page picture for judging: `python -c "import pymupdf as f; d=f.open('<src>'); d[P-1].get_pixmap(dpi=70).save('p.png')"`
(zoom: `clip=f.Rect(0,Y0,595,Y1)`, dpi 110).

## Spec format
```json
{"source": "9700_s19_qp_42.pdf", "prefix": "AL-BIO-19s-42-QP",
 "crops": {"Q3.b.ii": [[page, y0, y1, x0, x1], ...]},          // segments in reading order; x usually 40-560 (525 if an examiner column)
 "masks": [[page, x0, y0, x1, y1]],                              // white-outs (dots of a fused-mark row, credits, column rules)
 "accept_blank": {"Q2.a": "reason"},                             // a real printed drawing box / grid / figure whitespace
 "accept_plain": {"12:286": "reason"},                           // a dotted row that must stay (labelled row, table/scaffold dots)
 "accept_absent_leaves": {"Q1.c.i": "reason"},                   // checker expects a label that is not a real part
 "no_mark_box_pages": {"13": "reason"}}                          // figure shapes at the margin mistaken for examiner mark boxes
```
Every accept/mask carries a written reason (recorded in provenance, honoured by the gates). An `auto:` reason is never final.

## Done
`gates.log` shows `expected=N produced=N missing=[] extra=[]` and `missing=0 duplicated=0 sliced_boundaries=0`, **and** every
contact sheet was read after the last edit and follows the house rules.

## House rules that specs most often get wrong
- Text printed **after a part's `[n]` and before the next label** is the **next** part's context (`Qn.x.stem`, or top of the next roman).
- Shared context before (a) → `Qn.stem`; before (b)(i) → `Qn.b.stem`; context-only pages between parts → next part's stem.
- A figure/table goes to the first leaf that refers to it; a table/grid/diagram the candidate completes goes with that leaf.
- Plain unlabelled dotted rows are cut out with segments (not masked into a blank gap). Labelled rows, figure label lines,
  genetic-diagram scaffold rows and fill-in blanks keep their dots (`accept_plain`). A mark fused to a dotted row: keep the row,
  mask the dots up to just left of the `[`.
- Never cut the question number in; never include furniture: "Answer all the questions", "Write your answers in the spaces
  provided", Section B rubric, "Circle the number of the question...", `Question N continues on page M`, `Question N [x minutes]`,
  "For Examiner's Use" heading + its column rule (mask the rule above/below a wide figure; never cut an axis label),
  teacher REPORT FORM pages, BLANK PAGE, copyright credits (mask the credit line only).
- Segment edges on blank rows only; a figure wider than the text column keeps its full width.

## Hand-spec agents
Prompt files: `ALEVEL/MANUAL_SPEC_AGENT_PROMPT.txt` (Chem/Phy), `MANUAL_SPEC_AGENT_PROMPT_BIO.txt` (Biology notes incl. report form).
Agent brief: "Read <prompt> and follow it exactly. Your papers (PREFIX SOURCE) are in <list file>. ..." — 5 papers per agent
(3 if writing from scratch), ≤ 5 agents. Include current house-rule notes in the brief. Each paper in exactly one agent's list;
if you edit a file an agent owns, message it to re-read from disk. Agents may not edit `.py` files — if a gate/renderer is wrong
they report STUCK and you fix the code (then regression, see `alevel-qp-split`).

## Fixing a defect found in review
Manual paper: edit its spec, `run`, view the crop. Auto paper: `al_manual.py init PREFIX <auto run>` then fix as above (the paper
moves to the manual set). Afterwards the paper needs re-review/approval (its hashes changed).
