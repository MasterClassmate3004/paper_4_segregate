---
name: alevel-qp-split
description: Automatic splitting of Cambridge A Level question papers (9702/9701/9700/9709/9231) into one PNG per answerable part plus separate stems, with the blocking QA gates, alias detection, hold triage, generic splitter/gate fixes and the regressions that protect already-approved papers. Use whenever someone wants to calibrate a new subject or era, batch-split a subject's papers, understand why papers are HOLD, change al_qp_splitter.py / al_mcq_splitter.py / the gates, re-run papers after a fix, check that a code change did not alter approved crops, or find duplicate variant papers — e.g. "split the 9231 papers", "why are 250 Maths papers on hold", "the splitter keeps dropping marks", "run the regression", "are 41 and 43 the same paper".
---

# A Level QP split, gates and regressions (Phases 1–3)

Code: `~/rootatom_data/alevel-pipeline/ALEVEL/scripts/`. Python: `~/.venvs/alevel/bin/python -I`. Data: `~/rootatom_data/ALEVEL/`.

## 1. Calibration (new subject or era)
Pick ~6 papers covering each layout regime (plan Phase 1 table; e.g. one MCQ, P2, P4, P5, an old pre-2009 paper).
`al_run_papers.py <subj>_cal NAME.pdf ...` → fix the splitter generically until all gates pass, then the user looks at the
contact sheets (`review/<subj>_cal/*.jpg`) and approves. Freeze conventions there (answer lines, grids, label shapes).
Subject-specific behaviour must be gated (Maths: `IS_MATHS` in `al_qp_splitter.py`, prefixes `AL-MTH-`/`AL-FMT-`) so other
subjects stay byte-identical.

## 2. Batch split
```
al_run_papers.py RUN [names ...] [--list FILE] [--workers N] [--no-sheets]
```
- One paper at a time per worker; science Paper 1 routes to `al_mcq_splitter.py` (one crop per question, A–D included,
  Section B stem `SecB.stem`).
- Output: `splits/RUN/<PREFIX>/` (PNGs, `<PREFIX>-split-provenance.json`, `gates.log`, `splitter.log`),
  `review/RUN/run_summary.csv` (`status` PASS/HOLD + reason). Re-running a `--list` subset **merges** into run_summary.
- Fail-closed: PASS only on explicit gate success lines. Disk guard `al_space.py` (`AL_MIN_FREE_GB`, default 4) is checked per paper.
- Use `--no-sheets` for big runs; make contact sheets only for what will be reviewed.

## 3. The gates (all blocking)
- `al_verify_leaves.py` — expected leaf set (read independently from the PDF) == produced set. Knows: roman/letter columns,
  numbered tasks with own marks, answer-slot romans, report-form pages, `Question N [x minutes]` headings (old P5),
  `3 = key` figure rows, Maths roman-first trees.
- `al_verify_coverage.py` — every question word in exactly one crop (`missing=0 duplicated=0`), no crop edge through ink
  (`sliced_boundaries=0`), every `[n]` visible, no furniture in crops, figure ownership, trailing pages only reference/furniture.
  Furniture patterns live in `INSTRUCTION_RE`, `ESSAY_RUBRIC_RE`, `LINE_FURNITURE_RE`, `REF_PAGE_RE`.
A paper is PASS only with `expected=N produced=N missing=[] extra=[]` and `missing=0 duplicated=0 sliced_boundaries=0`.

## 4. Aliases (identical variant papers)
`al_dedupe.py RUN` → `review/RUN/duplicates.csv` (`canonical,alias,crops`; byte-identical-ish crop sets with per-crop word-multiset
equality). **It misses some** (Biology: 8 missed). Also scan question **text** of same-session variants with paper codes,
control chars and whitespace normalised (NFKC); add confirmed pairs to `duplicates.csv` with a note. Keep the lowest variant.
Aliases skip review, mark schemes and classification.

## 5. Holds
Read reasons in `run_summary.csv` / `gates.log`. Order of preference:
1. **Generic fix** in the splitter/gate when a cause repeats across papers (gate it per subject if needed) → re-run the holds.
2. `al_autofix.py PREFIX SOURCE.pdf [--rounds 6]` — draft-and-repair: writes a manual spec draft and repairs it until gates pass.
   Check its output: it used to accept blank bands as `auto:` (hid masked dotted rows) — every `auto:` accept must be judged.
3. Hand-authored spec → `alevel-manual-specs`.

## 6. Changing code safely (regressions)
- Never edit scripts under a running unfrozen run. Freeze the approved code: `git archive <sha> | tar -x -C ~/rootatom_data/frozen/<sha>`.
- `al_regress.py BASE NEW LIST [--chunk 80] [--workers 6]` — re-split a list in chunks, keep only what changed.
- `al_qp_regress.py APPROVED_RUN NEW_RUN [--prefix AL-CHE-] [--chunk 40]` — against approved hashes, under the disk guard.
- `al_compare_runs.py BASE NEW` — classes `same / changed / newpass / regressed / hold`; falls back to provenance hashes when
  base PNGs are offloaded.
- Manual specs: render every spec with old and new `al_manual.py` and compare PNG hashes.
- Every `changed` approved paper is looked at by eye; only intended changes are allowed. Commit message states what was verified
  (e.g. "Chem+Bio identical; Physics not verified").
- **Open (2026-10-20):** changes after f4073be are not verified on Physics (Drive sources unreadable) and an all-subject gate
  regression is pending — see `HANDOFF_ALEVEL_PIPELINE.md` §6.

## Known splitter weaknesses (fixed per paper by specs, not yet in the splitter)
Completion-passage final blank `..... .` dropped; "Space for working/table/diagram" labels kept; text-free ruled grids cut as
blank; context after a mark attached to the previous part in some layouts. Fix generically before re-splitting Biology.

## Next step
PASS papers → aliases → contact sheets + review (`alevel-qp-review`); holds → `alevel-manual-specs`.
