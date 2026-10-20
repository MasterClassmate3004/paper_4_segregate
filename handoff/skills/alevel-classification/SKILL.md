---
name: alevel-classification
description: Phases 5–6 of the ROOTATOM A Level pipeline — building the per-crop classification manifest for a finished subject, classifying every leaf against the current Cambridge syllabus (topic, AS/A level, dependencies, stems), validating, and releasing to storage and the Supabase tables questions_alevel_master / questions_alevel_stem through Gates A–D. Use whenever someone says "classify Chemistry/Physics/Biology", "build the manifest", "map A Level questions to syllabus topics", "detect dependencies", "upload the A Level questions", "create the A Level tables", or asks what the classifier's inputs and constraints are.
---

# Classification and release

Status (2026-10-20): manifests exist for Chemistry and Physics; the classifier, topic files and release are **not built yet**.
Read `~/rootatom_data/alevel-pipeline/ALEVEL/CLASSIFICATION_HANDOVER.md` first (written for this phase).

## Inputs: the manifest
```
al_class_manifest.py SUBJECT OUT.csv      # chem | phy today — add bio (and later mth/fmt) before classifying those subjects
```
Outputs `~/rootatom_data/ALEVEL/classification/manifest_<subj>.csv`, one row per approved crop: `qp_id`, `paper`, `label`,
`kind` (leaf | stem | mcq | mcq_stem), `source_pdf` + `segments` (`[[page,x0,y0,x1,y1]]`, PDF points after `page.remove_rotation()`),
`ms_status`, `ms_pdf` + `ms_segments`, `ms_png`, `mcq_answer`, `qp_zip`/`ms_zip` (relative to the Drive `ROOTATOM_ALEVEL/` folder).
Aliases are excluded (they can later be recorded as aliases of the canonical rows).
**Main classifier input = native PDF text** of the segments (`page.get_text("text", clip=Rect)`), plus the MS text for the leaf; the PNG
only when there is a figure/graph/structure (read zip members on demand; see `alevel-storage`).

## Build (plan Phase 5)
1. **Canonical topic files** from the current syllabus guides (9702/9701/9700 2025–27, 9709, 9231): syllabus code, level (AS | A),
   chapter, topic, subtopic, learning outcomes. The guides are a download → **ask the user first**. Agents may only choose codes from these files.
2. **Hard constraints** (validator rejects violations): sciences P1/P2 → AS topics only, P4/P5 → any; P5 planning → primary code from the
   practical-skills chapter + content topic secondary; pre-2009 Options papers (Physics Astrophysics/Medical/..., Chemistry Biochemistry/
   Environmental/Phase equilibria/Spectroscopy/Transition elements) → nearest current code + `outside_current_syllabus=true`;
   9709 component (via the 2020 era map) fixes the block (P1 Pure 1, P3 Pure 3, P4 Mechanics, P5 Stats 1, P6 Stats 2; old M2 → nearest +
   flag); 9231 P1/P2 Further Pure, P3 Further Mechanics, P4 Further Stats.
3. **Per leaf output:** topic fields + `outside_current_syllabus`, `confidence`, `needs_review`. Stems inherit the dominant topic of their children.
4. **Dependencies** separate from stems: "hence", "using your answer to (a)", "show that … hence", MS `ecf`/`ft` (many in 9709).
5. **Execution:** one subject at a time, batches ≤ 10 papers, ≤ 4 sub-agents (or the Message Batches API fallback with the user's OK).
   Reuse: `IB/scripts/ib_sci_pipeline/CLASSIFY_AGENT_PROMPT.md` and the `igcse-topic-dep-stem-pipeline` skill (CSV + validators).
6. **Validation:** row count == manifest, every code exists, constraints respected, topic drift normalised (one chapter/topic tuple per code),
   stratified human spot-check + 100% of `needs_review`.

## Release (plan Phase 6) — every gate needs the user's explicit approval
- **Gate A (local):** per-subject CSVs (master + stem), review package, QA report; URLs blank; nothing uploaded.
- **Gate B (storage):** new private `alevel-` buckets; upload with `upsert=false`, list back, re-download, compare SHA-256, sign URLs (10-year).
- **Gate C (DB):** show the schema SQL first (IB-style: `level`, dual syllabus code, `outside_current_syllabus`, `option`, mapping status,
  `ms_signed_url`; template `IB/scripts/ib_topic_pipeline/questions_ib_schema.sql`); back up in-scope rows; dry run with counts; insert
  leaves → stems → stem mapping → zero dangling references.
- **Gate D (read-back):** exact counts and ID sets, mappings, signed URLs return the right bytes, RLS/bucket privacy unchanged; on failure restore and report.

## Working alongside splitting sessions
Read-only on `splits/`, `review/`, `reviewed_crop_hashes.json`, ledgers, `source_papers/canonical/`, specs and `al_*` scripts. Write only
under `~/rootatom_data/ALEVEL/classification/`; use a git worktree/branch (`git -C ~/rootatom_data/alevel-pipeline worktree add ../alevel-classify -b classify`).
IDs keep the `AL-` prefix and printed component; stems stay separate rows.

## Bundled references
- `references/CLASSIFICATION_HANDOVER.md` — copy of `alevel-pipeline/ALEVEL/CLASSIFICATION_HANDOVER.md` (repo copy is authoritative).
