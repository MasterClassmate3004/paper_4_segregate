# ROOTATOM A Level question bank — handoff

Written 2026-10-20 for a colleague taking over. Read this first, then the skill for the phase you are working on
(`skills/` in this repo; also installed as Claude Code skills, see section 9).

---

## 1. What this project does

We turn Cambridge International A Level past papers into a question bank. For every past paper we:

1. collect the original PDFs (question paper "QP" and mark scheme "MS") with **zero third-party watermarks**;
2. split each QP into **one PNG per answerable part** (a "leaf", e.g. `Q3.b.ii`) plus separate **stem** PNGs for shared
   context (e.g. `Q3.stem`, `Q3.b.stem`);
3. split the MS into **one PNG per QP leaf** (multiple-choice papers get an answer letter instead);
4. check every crop by automated gates **and** by eye (100% visual review);
5. later: classify each leaf against the syllabus and upload to Supabase (new tables `questions_alevel_master` /
   `questions_alevel_stem`).

Subjects in scope: Physics **9702**, Chemistry **9701**, Biology **9700**, Mathematics **9709**, Further Mathematics **9231**.
For the sciences: Paper 1 (MCQ), Paper 2, Paper 4, Paper 5, and the old Paper 6 "Options" papers. **Paper 3 (practical) is out of scope.**

---

## 2. Where things are

| What | Where |
|---|---|
| Pipeline code (git repo) | `~/rootatom_data/alevel-pipeline` → scripts in `ALEVEL/scripts/`, agent prompts in `ALEVEL/*.txt`, manual MS overrides in `ALEVEL/manual_specs/ms/` |
| Data (not in git) | `~/rootatom_data/ALEVEL/` |
| Source PDFs | `ALEVEL/source_papers/canonical/<code>_<s|w|m><yy>_<qp|ms>_<vv>.pdf` (e.g. `9700_s19_qp_42.pdf`); originals replaced by derived/normalised files are kept in `canonical_original/`, listed in `derived_sources.csv` |
| Splits (PNGs + provenance JSON + gate logs) | `ALEVEL/splits/<RUN>/<PREFIX>/` (QP) and `ALEVEL/splits/<MS_RUN>/<PREFIX>-MS/` |
| Manual QP specs (hand-authored crops) | `ALEVEL/manual/<PREFIX>.json` → rendered into `ALEVEL/splits/manual/<PREFIX>/` |
| Review material | `ALEVEL/review/<RUN>/` → `run_summary.csv`, `duplicates.csv`, contact sheets `*.jpg`, `_review_groups/`, `_verdicts/` |
| Approval record (source of truth) | `ALEVEL/review/reviewed_crop_hashes.json` → `{run: {prefix: {png_name: sha256}}}`; a paper is approved only while its crops stay byte-identical |
| Worklists / per-subject handoffs | `review/bio_b1/_worklist.txt`, `_HANDOFF.md`, `_HANDOFF_MS.md`; `review/mth/_HANDOFF.md`, `_worklist.txt` |
| Parts removed for having no mark scheme | `ALEVEL/review/removed_no_ms.csv` |
| Classification inputs | `ALEVEL/classification/manifest_chem.csv`, `manifest_phy.csv`; handover `alevel-pipeline/ALEVEL/CLASSIFICATION_HANDOVER.md` |
| Python | `~/.venvs/alevel/bin/python` — **always run with `-I`** (isolated mode; sources are untrusted downloads) |
| Frozen code copies for regressions | `~/rootatom_data/frozen/<sha>/` (made with `git archive`) |
| Google Drive offload | `~/Library/CloudStorage/GoogleDrive-*/My Drive/ROOTATOM_ALEVEL/` (`splits/<RUN>/<PREFIX>.zip`, `sources/`), ledgers `review/offload_ledger.csv`, `review/sources_offload_ledger.csv` |
| Original plan (phases, decisions) | `~/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/a-level-papers-splitting-plan-6b3cde/ALEVEL_PIPELINE_PLAN.md` (that worktree's code is **stale** — never run it) |

**Why everything lives in `~/rootatom_data`:** `~/Documents` is synced by iCloud ("Desktop & Documents"). iCloud evicted the repo and
data, so scripts silently read empty files. Nothing for this pipeline may live under `~/Documents`.

### Naming

```
QP crop   AL-<SUBJ>-<YY><s|w|m>-<VV>-QP-<label>.png    AL-BIO-19s-42-QP-Q3.b.ii.png, AL-BIO-19s-42-QP-Q3.b.stem.png
MS crop   AL-<SUBJ>-<YY><s|w|m>-<VV>-MS-<label>.png    one per QP leaf (same label)
MCQ       AL-PHY-24s-12-QP-Q17.png (no MS image; the answer letter is in answers.csv); Section B stem SecB.stem
SUBJ      PHY | CHE | BIO | MTH | FMT     (s = May/June, w = Oct/Nov, m = Feb/March)
```
Labels follow the tree `Q4`, `Q4.stem`, `Q4.a`, `Q4.a.stem`, `Q4.a.i`, `Q4.a.i.1` (numbered tasks only if each has its own mark).
Maths 9709 before 2020 uses romans first (`Q3.i`, `Q3.ii`); separately marked (a)/(b) under a roman are leaves (`Q6.ii.a`).
The `AL-` prefix is mandatory: IGCSE uses the same paper codes.

---

## 3. Status (2026-10-20)

| Subject | QP split + review | Mark schemes | Classification / DB | Notes |
|---|---|---|---|---|
| Physics 9702 | **done** — 447 unique papers approved (run `phy_b10`, manual specs) | **done** (`phy_ms4`) | manifest built (`manifest_phy.csv`) — classifier not built yet | PNGs + sources offloaded to Drive; Drive currently broken (section 8) |
| Chemistry 9701 | **done** — 396 unique approved (`chem_b2` + `manual`) | **done** (`chem_ms1`, `chem_ms2`) | manifest built (`manifest_chem.csv`) | PNGs on Drive |
| Biology 9700 | **done** — 383 unique approved (`bio_b1` + `manual`) | **done** — 383/383 have a PASS MS (`bio_ms1`, `bio_ms2`; 104 MCQ keys) | manifest not built yet (`al_class_manifest.py` supports chem/phy only — add bio) | PNGs **local only** (Drive offload blocked) |
| Maths 9709 | split: `mth_b1` 814/826 PASS, **12 holds** (`review/mth/manual_specs_needed.txt`); dedupe + visual review **not started** | not started | — | Maths code paths gated by `IS_MATHS`; see `review/mth/_HANDOFF.md` |
| Further Maths 9231 | not started | — | — | prefix `AL-FMT-`; scope confirmed in plan (D3) |

Counts are **unique** papers: identical variant papers (Cambridge reuses e.g. 41 = 43) are kept once; the others are
**aliases** (`review/<run>/duplicates.csv`, `alias` column) and skip review, MS and classification.

---

## 4. The pipeline, phase by phase

Each phase has a skill with the full procedure. Short version:

| Phase | What | Main scripts | Skill |
|---|---|---|---|
| 0 Sources | fetch, watermark-strip, verify, canonical names, A3→A4 | `al_fetch_sources.py`, `strip_overlay_watermarks.py`, `check_source_watermarks.py`, `al_normalise_a4.py` | `alevel-sources` |
| 1–3 QP split + gates | calibration, batch split, gates, aliases, hold triage, generic fixes, regressions | `al_run_papers.py`, `al_qp_splitter.py`, `al_mcq_splitter.py`, `al_verify_leaves.py`, `al_verify_coverage.py`, `al_dedupe.py`, `al_regress.py`, `al_qp_regress.py`, `al_compare_runs.py` | `alevel-qp-split` |
| Holds → manual specs | hand-authored crop specs for papers the splitter cannot do | `al_manual.py`, `al_autofix.py`, `al_addmarks.py`, `MANUAL_SPEC_AGENT_PROMPT*.txt` | `alevel-manual-specs` |
| QP visual review | contact sheets, review agents, verify flags, fix, approve | `al_groups_from_list.py`, `al_prepare_review.py`, `al_check_verdicts.py`, `al_approve.py`, `REVIEW_AGENT_PROMPT_QP.txt` | `alevel-qp-review` |
| 4 Mark schemes | split MS per leaf, overrides, paired review, no-MS rule | `al_run_ms.py`, `al_ms_splitter.py`, `al_verify_ms.py`, `al_ms_lines.py`, `al_prepare_ms_review.py`, `al_check_ms_verdicts.py` | `alevel-mark-schemes` |
| Storage | Drive offload/restore, disk guard | `al_offload.py`, `al_space.py` | `alevel-storage` |
| 5–6 Classify + release | manifest, topic classification, DB gates A–D | `al_class_manifest.py`, `CLASSIFICATION_HANDOVER.md` | `alevel-classification` |
| Cross-cutting | running agents safely, sessions, worklists | — | `alevel-pipeline` (start here) |

### The quality contract (every crop, every subject)

1. One item per crop: one stem **or** one answerable part. Never two sibling parts.
2. The bare **question number is never visible**; part labels `(a)`, `(ii)` stay.
3. Nothing cut at any edge (text, fraction, axis, table border, figure, MCQ option).
4. No page furniture: `© UCLES`, paper codes, page numbers, `[Turn over`, `BLANK PAGE`, `DO NOT WRITE IN THIS MARGIN`,
   `[Total: n]`, "Space for working", barcodes, examiner columns, website stamps, copyright credits.
5. Every printed `[n]` mark is inside some crop.
6. Every word of question content is in exactly one crop (the coverage gate proves this).

### House rules decided with the user (do not re-litigate)

- **Stems always separate** (IB protocol), even with one consumer. Context before part (a) → `Qn.stem`; before (b)(i) → `Qn.b.stem`.
- Context printed **after a part's mark and before the next label** belongs to the **next** part (`Qn.x.stem`, or the top of the
  next roman's crop) — never the end of the previous crop. (The most common defect agents introduce.)
- A figure/table goes to the **first leaf that refers to it**; a table or grid the candidate **completes** goes with that leaf.
  A table used by two parts goes with the part that carries most of the marks / is printed after its text.
- **D6 answer lines:** plain unlabelled dotted lines are removed. **Labelled** answer lines stay with their dots:
  `pH = ...... [2]`, numbered genotype rows, figure label lines, genetic-diagram scaffold rows, fill-in sentence blanks.
  A mark fused to the end of a dotted row: keep the row, white out only the dots, keep the `[n]`.
- Numbered tasks `1.` / `2.` are separate leaves only if each has its own mark.
- Maths: blank answer grids are kept; separately marked (a)/(b) under a roman are leaves; bracketed hints `[The volume of a cone is ...]` go with the leaf directly above them.
- Identical variant papers → keep the lowest variant, record the alias.
- **No mark scheme → not stored.** First look for the MS elsewhere (combined booklets, examiner reports' key tables,
  `source_papers/raw_ms_search/`, a second archive with user OK). Only if none exists, remove the part and log it in
  `review/removed_no_ms.csv`.
- Sources: user prefers Dynamic Papers; PapaCambridge files need the exact overlay stripper; **zero watermarks**;
  2026 PapaCambridge files with a tiled "PapaCambridge PDF pipeline" watermark stay out. Show archive + counts + size and get
  the user's OK before any download.

---

## 5. How work is run (lessons that cost us days)

- **Agents:** visual review and hand-spec work are done by sub-agents (`general-purpose`, model `sonnet`, background).
  - At most **4–5 at once**. More → "media removed: request limit" on image reads → incomplete verdicts.
  - Review groups **≤ 40 contact sheets**. Bigger groups stall.
  - **Before each wave, time one tiny test agent.** If 3 tool calls take > 2 minutes, stop.
  - Agent-flagged defects are real only **~50%** of the time. Open the crop PNG and judge against the house rules before fixing.
  - Never let two agents edit the same spec/override (check list overlaps first); tell an agent if you changed its file.
- **Sessions:** run long waves from a **fresh, small Claude session** with a handoff file. On 2026-10-18 a session with a
  194 MB transcript and 12 GB of sub-agent logs, on a Mac with no free RAM, made every agent stall for 20–70 min. It looked
  like an API limit but wasn't. Each review agent writes a 300–570 MB log under `~/.claude/projects/<project>/<session>/subagents/`;
  delete finished ones (Claude's auto mode is not allowed to delete transcripts — a human must).
- **Disk:** keep > 8 GB free. `al_space.py` stops runners below `AL_MIN_FREE_GB` (default 4). Free space moves by GBs on its own
  (iCloud CloudKit cache, Claude/Codex data). Contact sheets are regenerable: delete them after review.
- **Code changes:** every generic splitter/gate change needs a regression on **all approved papers of all subjects**
  (`al_regress.py` / `al_qp_regress.py` from a frozen `git archive` copy; never edit scripts under a running unfrozen run).
  Maths-only changes must be gated by `IS_MATHS`. Commit with a message that says what was verified and what was not.
- **Write state down:** worklist + handoff file per subject; memory notes (`~/.claude/projects/-Users-nitya-Documents-Nitya-Projects-rootatom-paper-4-segregate/memory/project_alevel_pipeline_plan.md`).

---

## 6. Known problems and open items

| # | Item | Impact | What to do |
|---|---|---|---|
| 1 | **Google Drive for desktop broken since 2026-10-17** (macOS File Provider: `CANNOT_START_CORE` / `FILE_PROVIDER_ACTIVATION_FAILED`). Files in the Drive folder read as 0 bytes. | Bio offload blocked (662 zips written locally, nothing uploaded); Physics sources zip unreadable; Physics PNGs on Drive unreachable | A real Mac **reboot** (check `sysctl kern.boottime`), then re-sign-in to Drive. Then follow `alevel-storage`. Check for stale pending zips from the 2026-10-19 21:41 push. |
| 2 | Pipeline changes f4073be → HEAD **not verified on Physics** (al_manual question-number rule, leaf checker, MS splitter 00bec90..abaec6b) | A Physics re-render/re-split could change approved crops | When Drive works: pull Physics sources, run QP + MS regressions on all approved Physics papers; only intended changes allowed. Same for Chemistry MS (00bec90..abaec6b). |
| 3 | **All-subject gate regression** pending (coverage/leaf gates relaxed several times for Bio/Maths) | Gate verdicts of approved Chem/Phy papers might differ | Re-run both gates on every approved paper; differences must be explained. |
| 4 | Biology fixes were **spec-only**; the splitter still drops completion-passage final blanks, keeps "Space for working/table/diagram" labels, cuts text-free ruled grids | A Biology re-split would reintroduce them | Fix generically in `al_qp_splitter.py` before any Bio re-run. |
| 5 | `al_class_manifest.py` supports chem/phy only | Bio (and later Maths) manifests missing | Add `bio`, then `mth`. |
| 6 | Maths 9709: 12 holds; dedupe, contact sheets, review not started; some sources still held (s19, w24, w25 Dynamic Papers "watermark_suspect"; s26/m26 PapaCambridge stay out) | — | `review/mth/_HANDOFF.md`; get user OK for held fetches. |
| 7 | Further Maths 9231 not started | — | Calibration first (plan Phase 1 table), `AL-FMT-` prefix, EITHER/OR questions. |
| 8 | Classification (Phase 5) and release (Phase 6, Gates A–D) not built | — | `alevel-classification` skill + `CLASSIFICATION_HANDOVER.md`. Schema SQL must be shown to the user before running. |
| 9 | Disk: `~/.claude/projects` ≈ 28 GB of finished agent logs | Disk pressure | User deletes old `subagents/` folders. |

---

## 7. Next steps, in order

1. Fix Google Drive (item 1) → resume Bio offload, then the Physics regressions (item 2).
2. All-subject gate regression (item 3).
3. Maths 9709: holds → dedupe → visual review → mark schemes → offload.
4. Further Maths 9231 (same path; calibrate first).
5. Classification + release per finished subject (start with Chemistry/Physics manifests).

---

## 8. Who decides what

The user (Nitya) decides: sources and any download, scope, anything that deletes data on Drive, storage/DB releases, schema,
layout conventions not covered by the house rules. Everything else (generic fixes, specs, review verdicts) the operator decides,
then reports. Keep decisions in the worklist with the date.

---

## 9. Skills

Stored in this repo under `skills/`, installed for Claude Code in `~/.claude/skills/`, zipped for claude.ai in `skills/dist/`.

| Skill | Use it for |
|---|---|
| `alevel-pipeline` | Start here: orientation, status, routing to the phase skill, running agents and sessions safely |
| `alevel-sources` | Phase 0: fetching, watermark gate, canonical names, derived/normalised sources |
| `alevel-qp-split` | Calibration, batch QP split, gates, aliases, hold triage, generic splitter fixes, regressions |
| `alevel-manual-specs` | Hand-authored crop specs for held papers; fixing a defect in one paper |
| `alevel-qp-review` | 100% visual review of QP crops with review agents; verifying flags; approving |
| `alevel-mark-schemes` | MS split, overrides, paired QP/MS review, no-mark-scheme rule, audit |
| `alevel-storage` | Drive offload/restore, ledgers, disk guard, freeing space |
| `alevel-classification` | Manifest, syllabus classification, dependencies, DB release gates |
