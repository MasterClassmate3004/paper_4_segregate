# Visual review of A Level question-paper crops (reviewer agent instructions)

You review contact sheets of crops that ALREADY passed the automated gates
(exact part set, every question word in exactly one crop, no crop edge through
ink, no page furniture). Your job is what automation cannot see. Use only the
Read tool on the PNG files named below and the Write tool for your one output
file. Do not run scripts, do not modify any other file, do not spawn agents.

## Inputs (per paper)
- Contact sheets: `/Users/nitya/rootatom_data/ALEVEL/review/<RUN>/<PREFIX>_01.png`, `_02.png`, ...
  Each tile = one crop; the blue header shows the crop label (e.g. `Q3.b.ii`,
  `Q4.stem`) and its pixel size. Read EVERY sheet of the paper.
- If a crop looks wrong, open the single crop at full resolution:
  `/Users/nitya/rootatom_data/ALEVEL/splits/<RUN>/<PREFIX>/<PREFIX>-<LABEL>.png`

## The contract every crop must meet
1. Exactly one item: a stem (shared context, label ends `.stem`) or one answerable part. Never two sibling parts (e.g. both (i) and (ii) prompts) in one crop.
2. No question NUMBER visible (part labels like (a), (ii), "1." are fine and expected). For multiple-choice (`-1x-QP`) crops: no number at all; stem + figure + all options A-D present.
3. Nothing cut: no sliced letters, formula, fraction, table border, graph axis, figure part, or option at any edge.
4. No page furniture: page numbers, barcodes, "© UCLES", paper codes, "[Turn over", "BLANK PAGE", "DO NOT WRITE IN THIS MARGIN", "[Total: n]", "Space for working", copyright text, examiner columns.
5. Answer area convention: blank working space and plain dotted lines are removed; a LABELLED answer line ("speed = ........ m s-1 [2]") or a lone "[n]" mark directly under the prompt is CORRECT and expected.
6. A figure/table/graph appears with the stem or part that introduces it; a stem contains no answerable instruction-with-mark.
7. No watermark or third-party text (PapaCambridge, Dynamic Papers, XtremePapers, URLs).
8. Reasonable whitespace: no huge empty area inside a crop unless it is part of a printed figure/grid.

## Output
Write `/Users/nitya/rootatom_data/ALEVEL/review/<RUN>/_verdicts/<PREFIX>.json`:
```json
{"prefix": "<PREFIX>", "sheets_read": <n>, "crops_seen": <n>, "verdict": "PASS" | "DEFECT",
 "defects": [{"label": "Q3.b.ii", "rule": 3, "what": "bottom of fraction in last line cut"}]}
```
`crops_seen` must equal the number of tiles across all sheets. Report only real
contract violations, each with the rule number; if unsure, include it with
"what" starting "UNSURE:". Do not quote question text beyond a few words.

Reply with one line per paper: `<PREFIX> <verdict> crops=<n> defects=<k>`.
