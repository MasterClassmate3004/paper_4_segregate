# A Level classification — handover (Chemistry 9701 + Physics 9702)

Written 2026-10-16 by the splitting session, which keeps working on Biology 9700 in parallel.
Read the plan first: `/Users/nitya/Documents/Nitya/Projects/rootatom/paper_4_segregate/.claude/worktrees/a-level-papers-splitting-plan-6b3cde/ALEVEL_PIPELINE_PLAN.md` — **Phase 5** (classification) and **Phase 6** (release gates).

## 1. What is finished and approved

| | Chemistry 9701 | Physics 9702 |
|---|---|---|
| Unique approved QPs (aliases excluded) | 396 | 443 |
| Manifest rows (crops) | 18,040 = 10,481 leaves + 3,154 stems + 4,320 MCQ items + 85 MCQ Section-B stems | 17,754 = 9,840 leaves + 3,034 stems + 4,880 MCQ items |
| Every leaf has a mark scheme | yes (exact 10,262 / parent covers child 219) | yes (exact 9,419 / parent covers 414 / children merged 7) |

Every QP part without a mark scheme has been removed (user rule); the list is `~/rootatom_data/ALEVEL/review/removed_no_ms.csv`.
Identical variant papers are aliases of one canonical paper: `review/{chem_b1,chem_b2,manual,phy_batch9}/duplicates.csv` (alias -> canonical). They are not in the manifest; the DB may later record them as aliases of the canonical rows.

## 2. Inputs: start from the manifests

`~/rootatom_data/ALEVEL/classification/manifest_chem.csv` and `manifest_phy.csv` (rebuild with
`~/.venvs/alevel/bin/python ~/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_class_manifest.py chem|phy OUT.csv`).
One row per crop:

- `qp_id` (= image file stem, e.g. `AL-CHE-14s-21-QP-Q1.b.i`), `paper`, `label` (`Q1.b.i`, `Q1.b.stem`, `Q14` for MCQ, `SecB...` MCQ stems)
- `kind`: `leaf` | `stem` | `mcq` | `mcq_stem`. Stems have no mark scheme; they inherit the dominant topic of their children (plan Phase 5.4).
- `source_pdf` + `segments` — JSON `[[page, x0, y0, x1, y1], ...]` (1-based page, PDF points, **after `page.remove_rotation()`**). Native text of the crop: `page.get_text("text", clip=fitz.Rect(x0,y0,x1,y1))` per segment. This is the classifier's main input (better than OCR).
- `ms_status`, `ms_pdf` + `ms_segments` (same format) — the mark-scheme text for the leaf (it often names the concept); `ms_png` = the MS crop image.
- `mcq_answer` for MCQ items. 2002 Paper 1 keys came from examiner reports (`ms_pdf` = `*_er.pdf`, in `source_papers/raw_ms_search/`).
- `qp_zip` / `ms_zip` — where the PNGs are: relative to `~/Library/CloudStorage/GoogleDrive-nityajain113@gmail.com/My Drive/ROOTATOM_ALEVEL/`.

### Where the files are (and storage)

- **Source PDFs**: Chemistry in `~/rootatom_data/ALEVEL/source_papers/canonical/9701_*` (local). Physics PDFs were moved to Drive: `ROOTATOM_ALEVEL/sources/9702_canonical.zip` (941 MB, 1,006 files; hashes in `review/sources_offload_ledger.csv`). For Physics, extract it once into a scratch folder **under `~/rootatom_data/ALEVEL/classification/`** (needs ~1 GB) and delete it when done — do **not** put it back into `source_papers/canonical/` (the splitting session's runners read that folder).
- **Crop images**: only on Drive (zips, ~1-2 MB per paper). Read single members on demand with `zipfile.ZipFile(path).read(member)` — Drive (Stream mode) downloads just that zip; nothing needs to be kept locally. Only leaves with figures/graphs/structures need the image at all.
- Classification output is small (CSV/JSON). The disk floor is **4 GB free** (`al_space.py`); free space is ~9 GB now and the Biology session also uses it. Check before extracting.

## 3. Rules that carry over (user decisions)

- Never upload to Supabase or write the DB without the user's explicit approval. Tables: `questions_alevel_master` / `questions_alevel_stem` (IB-style; see `IB/scripts/ib_topic_pipeline/questions_ib_schema.sql`).
- Before **any** download (e.g. syllabus guides), show source, count and size and get an OK. Never type passwords.
- IDs keep the `AL-` prefix and the printed component number. Stems are always separate `.stem` rows.
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Classification agent prompts/patterns to reuse: `IB/scripts/ib_sci_pipeline/CLASSIFY_AGENT_PROMPT.md` and `~/.claude/skills/igcse-topic-dep-stem-pipeline` (topic + dependency + stem pipeline, CSV, validators).

## 4. What still has to be built (plan Phase 5)

1. **Canonical topic files** from the current syllabus guides (9701 and 9702, 2025-2027): code, AS|A level, chapter, topic, subtopic, learning outcomes. Not built yet; the guides are a download (ask first).
2. Hard constraints: Paper 1/2 -> AS topics only; Paper 4/5 -> any; Paper 5 (planning) primary code from the practical-skills chapter + content topic as secondary; pre-2009 Paper 6 Options (Physics Astrophysics/Medical/..., Chemistry Biochemistry/Environmental/Phase equilibria/Spectroscopy/Transition elements) -> nearest current code + `outside_current_syllabus=true`; old Paper 1/2/4/5/6 numbering via a component-era map.
3. Per leaf: topic fields + `outside_current_syllabus`, `confidence`, `needs_review`; dependencies ("hence", "using your answer to (a)", MS `ecf`) separate from stems.
4. Validation (plan Phase 5.7) and a stratified human spot-check + 100 % of `needs_review`.

## 5. Running in parallel with the Biology session

- **Do not touch** the splitting state: `~/rootatom_data/ALEVEL/splits/`, `review/` (except reading), `review/reviewed_crop_hashes.json`, `review/offload_ledger.csv`, the Drive `splits/` zips, `source_papers/canonical/`, `manual_specs/`, and the `al_*` splitter/runner scripts. Write only under `~/rootatom_data/ALEVEL/classification/` and new files of your own.
- Git: `~/rootatom_data/alevel-pipeline` is shared and the Biology session commits on `master`. Work in your own worktree/branch (`git -C ~/rootatom_data/alevel-pipeline worktree add ../alevel-classify -b classify`) and merge later, or only add new files under `ALEVEL/classification/`.
- Rate limits: the plan's lesson is "never two subjects classifying in parallel". The Biology session runs <= 4 review sub-agents at a time; keep classification at <= 4 sub-agents (batches of <= 10 papers), Chemistry then Physics, or use the Message Batches API fallback (plan D5, needs the user's OK).
