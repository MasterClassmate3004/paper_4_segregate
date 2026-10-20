---
name: alevel-mark-schemes
description: Phase 4 of the ROOTATOM A Level pipeline — splitting Cambridge mark schemes into one image per approved question-paper leaf (MCQ papers get answer letters), resolving holds with written overrides, paired QP|MS visual review, and enforcing the rule that no question part is stored without a mark scheme. Use whenever someone says "do the mark schemes", "run the MS split for Biology/Maths", "this MS crop shows the wrong part", "the MS is for a different paper", "parts without a mark scheme", "MS audit", or asks how QP leaves are mapped to mark-scheme rows.
---

# Mark schemes

Code `~/rootatom_data/alevel-pipeline/ALEVEL/scripts/`, Python `~/.venvs/alevel/bin/python -I`, data `~/rootatom_data/ALEVEL/`.
Input = the **approved** QP set only (unique, non-alias). MS work never starts on unapproved QPs.

## 1. Input list
Build `prefix,qp_run` for every approved unique paper: `manual` if a manual spec exists, else the auto run. Check the count
against the approved total. Example: `review/bio_b1/_ms_input.csv`.

## 2. Split
```
al_run_ms.py QP_RUN MS_RUN [--only PREFIX-QP ...] [--workers N]
```
- Finds the MS: exact component → pre-2010 single-digit component file → combined all-components booklet (filtered by page-header
  paper number). `--only` needs the full `...-QP` prefix (it refuses empty/unmatched lists).
- `al_ms_splitter.py` keys MS rows by their **printed label** (validated against the QP label tree; order + question column),
  drops the key column, writes `splits/MS_RUN/<PREFIX>-MS/AL-...-MS-<label>.png` per QP leaf; MCQ → `answers.csv`.
- Mapping status per leaf: `exact`, `parent_ms_covers_child_qp`, `children_ms_merged_for_parent_qp`, `ms_absent`, `unresolved`.
- Gate `al_verify_ms.py`: coverage, duplicates, pixel slices, overlap. PASS only on `MS_OK`. Summary: `review/MS_RUN/ms_summary.csv`.

## 3. Holds → overrides
Overrides with written reasons: `alevel-pipeline/ALEVEL/manual_specs/ms/<PREFIX>-MS.json` (fields used so far: `absent`,
`segments` (incl. column slices), `drop_keys`, `add_keys [page,y,xend]`, `masks`, `skip_pages`, `component_pages`,
`accept_sliced`, `reason`). Helper: `al_ms_lines.py` (MS text rows in splitter coordinates). Agent prompts:
`MS_OVERRIDE_AGENT_PROMPT.txt`, `MS_OVERRIDE_AGENT_PROMPT_BIO.txt` (same agent limits as review; one paper per agent list).
Scanned (2002) mark schemes: OCR full page + label-strip OCR (tesseract psm 6, x<140), snap key lines to ink in the label column,
cut on blank/least-ink rows; overrides per paper.

## 4. No mark scheme → not stored (user rule, 2026-10-16)
For every `ms_absent` part or paper without an MS: first look elsewhere — combined booklets, examiner reports' key tables
(`source_papers/raw_ms_search/*_er.pdf`, 2002 MCQ keys), a correct copy from another archive (user OK; e.g. Bio 08w-21 came from
PapaCambridge after the DP file turned out to be the other variant's MS). Only if none exists: remove the part from the QP set
and log it in `review/removed_no_ms.csv`. MS of aliased QPs are dropped (aliases share the canonical MS).
**Final audit:** every approved unique QP has a PASS MS covering every stored leaf (Biology: 383/383).

## 5. Paired review
`al_prepare_ms_review.py QP_RUN MS_RUN [--per 6] [--only PREFIX ...]` → paired QP|MS sheets (`al_ms_sheet.py`) + groups (keep ≤ 40
sheets per group; re-split if needed). Prompts: `MS_REVIEW_AGENT_PROMPT.txt`, `_BIO.txt`, `_CHEM*.txt`, second-pass
`MS_REVIEW_AGENT_PROMPT_CHEM_2ND.txt` (RUN/NN parameters). Checker `al_check_ms_verdicts.py` (requires `sheets_read`; agents
miscount entries). Verify flags by eye. Known by-design: Physics P5 uncertainty notes keyed at a parent appear on every child;
whole-question MS for some pre-2007 P5. Approve with `al_approve.py MS_RUN ...` (hashes in `reviewed_crop_hashes.json[MS_RUN]`).

## 6. Regressions
`al_ms_regress.py` — perceptual MS regression against a reference splitter (`git show <sha>:ALEVEL/scripts/al_ms_splitter.py`);
`al_rerun_chunked.py` re-runs an MS run in small chunks under a tight disk budget. **Open:** MS splitter changes 00bec90..abaec6b
not yet regressed on Chemistry/Physics MS — do it before any Chem/Phy MS re-run.

## Done when
All approved unique QPs have approved MS images (or MCQ keys), the audit passes, removed parts are logged → offload (`alevel-storage`).
