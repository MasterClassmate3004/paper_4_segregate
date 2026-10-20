# A Level Split → Markscheme → Classify → Upload: Pipeline Plan (DRAFT v1)

Status: **draft for approval**. Nothing has been downloaded, split, uploaded, or written to Supabase.
Date: 2026-10-09.

This plan reuses what already exists rather than reinventing it:

| Need | Existing asset reused |
|---|---|
| Semantic split contract (leaf / stem / inheritance) | `IGCSE/skills/igcse-split-spec` (newest, 2026-08-31) + `IB/STEM_RECLASSIFICATION_PROTOCOL.md` |
| Operational workflow, release gates A–D | `IGCSE/skills/igcse-split-workflow` |
| Automated QA + visual review | `IGCSE/skills/igcse-split-qa`, `igcse-split-visual-review`, `skills/exam-split-quality-auditor` |
| Marker-anchor + ink-projection cropping engine | `IB/scripts/ib_aa_p1_splitter.py` (engine behind `IGCSE/scripts/run_0580_qp_splitter.py`) |
| MCQ cropping | `anthropic-skills:igcse-mcq-cropper`, `IB/scripts/ib_physics_p1_mcq_splitter.py` |
| Markscheme splitting + QP↔MS mapping statuses | `IB/scripts/ib_sci_pipeline/split_ib_sci_markscheme.py`, `igcse-split-workflow` Phase 10 |
| Classification, dependencies, stems, CSV, upsert | `~/.claude/skills/igcse-topic-dep-stem-pipeline`, `IB/scripts/ib_sci_pipeline/CLASSIFY_AGENT_PROMPT.md` |
| DB pattern for a course with two tiers | `IB/scripts/ib_topic_pipeline/questions_ib_schema.sql` (SL/HL ≈ AS/A2) |

---

## 1. What papers exist (scope inventory)

Assumption: **Cambridge International AS & A Level** (same board as our IGCSE work). Confirm before Phase 0.

Sessions: `m` = Feb/March (only variant x2, from ~2016), `s` = May/June (variants x1, x2, x3), `w` = Oct/Nov (x1, x2, x3).
Variant numbering (`11/12/13`) starts ~w09/s10; earlier papers have a single component number (`1`, `2`, `4`…).
The exact year/session/variant list per component is produced by the Phase 0 inventory script, not assumed.

### Physics 9702

| Comp. | Paper | Level | Type | Split kind |
|---|---|---|---|---|
| 1 | Multiple Choice (40 Qs) | AS | MCQ | one crop per Q + answer key from MS |
| 2 | AS Level Structured Questions | AS | Structured | stem/subpart tree |
| 3 | Advanced Practical Skills (variants 31–36) | AS | Practical structured | **out of scope (D3)** |
| 4 | A Level Structured Questions | A2 | Structured | stem/subpart tree |
| 5 | Planning, Analysis and Evaluation | A2 | Structured | stem/subpart tree |

### Chemistry 9701 — same shape (P1 MCQ, P2 AS structured, P3 practical [out of scope], P4 A Level structured, P5 PAE).

### Biology 9700 — same shape (P1 MCQ, P2 AS structured, P3 practical [out of scope], P4 A Level structured, P5 PAE).

Pre-~2009 science syllabi had extra/different components (e.g. a P6 **Options** paper). Inventory will surface these; they classify with `outside_current_syllabus=true` where the option no longer exists.

### Mathematics 9709 — paper numbering CHANGED in 2020

| Comp. | 2020 onward | Before 2020 |
|---|---|---|
| 1 | Pure Mathematics 1 | Pure Mathematics 1 |
| 2 | Pure Mathematics 2 | Pure Mathematics 2 |
| 3 | Pure Mathematics 3 | Pure Mathematics 3 |
| 4 | **Mechanics** | **Mechanics 1** |
| 5 | **Probability & Statistics 1** | **Mechanics 2** |
| 6 | **Probability & Statistics 2** | **Probability & Statistics 1** |
| 7 | — | **Probability & Statistics 2** |

IDs keep the **printed** component number; a per-era map (`component_era_map.json`) converts it to a syllabus strand for classification. Old Mechanics 2 content is now largely Further Maths (9231) → `outside_current_syllabus=true` in 9709.

### Further Mathematics 9231 — also renumbered in 2020 (in scope, D3)

| Comp. | 2020 onward | Before 2020 (to confirm in Phase 0) |
|---|---|---|
| 1 | Further Pure Mathematics 1 | Paper 1 (Further Pure) |
| 2 | Further Pure Mathematics 2 | Paper 2 (Mechanics + Statistics sections, with an either/or last question) |
| 3 | Further Mechanics | — |
| 4 | Further Probability & Statistics | — |

Old P2 needs a section-aware adapter (Mechanics vs Statistics questions) and must keep the "EITHER / OR" alternatives as separate leaves (`Q11.EITHER.a`, `Q11.OR.a`, format confirmed on the calibration sheet).

### Old science Options papers (in scope, D3)

Pre-~2009 P6 Options papers (e.g. Physics Astrophysics/Medical/Environmental/Telecommunications; Chemistry Biochemistry/Environmental/Phase equilibria/Spectroscopy/Transition elements; Biology option topics) are split like any structured paper. Each option section becomes a recorded `option` attribute. Classification uses the nearest current code + `outside_current_syllabus=true` when the option no longer exists.

### Rough volume (to be replaced by real Phase 0 counts)

~120 papers per component per subject across 2002–2025 → roughly **2,500 QP PDFs + 2,500 MS PDFs**, on the order of **80–120k leaf/stem crops** and a similar number of MS crops. This size drives the batching, ledger and review design below.

---

## 2. Identifiers and naming

IGCSE and A Level share paper codes (e.g. Physics `24s-42` exists in both), so every A Level ID carries an `AL` qualifier.

```
Filename : AL-<SUBJ>-<YY><s|w|m>-<VV>-<QP|MS>-Q<path>.png
           AL-PHY-24s-42-QP-Q3.b.ii.png
           AL-PHY-24s-42-QP-Q3.b.stem.png
           AL-MTH-19w-62-MS-Q5.ii.png
question_id : AL-PHY-24s-42-Q3.b.ii           (stems: AL-PHY-24s-42-Q3.b.stem)
SUBJ     : PHY | CHE | BIO | MTH
```

- `Q<path>` follows the IGCSE tree grammar: `Q4`, `Q4.stem`, `Q4.a`, `Q4.a.stem`, `Q4.a.i`, `Q4.a.i.b`. No fixed maximum depth.
- 9709 before 2020 uses **roman numerals as the first level** (`3 (i) … (ii)`). Keep native labels (`Q3.i`, `Q3.ii`) so QP and MS keys match exactly.
- Pre-variant papers (single-digit component) map to the first variant (`4` → `41`), the same rule used for 0580; the printed component is kept in provenance.
- MCQ: `AL-PHY-24s-12-QP-Q17.png`, with no MS image (answer letter is stored in the row).

---

## 3. Folder layout (mirrors `IB/` and `IGCSE/`)

```
ALEVEL/
  source_papers/canonical/            original PDFs, canonical names, never modified
  source_papers/source_manifest.csv   name, drive/url, sha256, size, pages, watermark_status, text_layer
  adapters/<subject>_<era>.yaml       layout profile per subject+era (Phase 1)
  scripts/                            all working scripts (NEVER /tmp or scratchpad: work was lost that way)
  Topic Hierarchies/<subj>_al_canonical_topics.json
  splits/<SUBJ>/<YYs>/<VV>/{qp,ms}/   PNGs + per-paper provenance JSON
  review/<batch>/                     contact sheets, neighbour sheets, audit reports
  ledger.csv                          one row per paper × stage, written only under fcntl lock, committed to git daily
```

The ledger and manifests go under git (the IB ledger was once wiped with no backup).

---

## 4. Phases

### Phase 0: Source acquisition, inventory, watermark gate

0. **Source (D5 = public archive):** shortlist archives that serve the original UCLES PDFs, sample-check ~10 files from each across eras for watermarks/re-encoding, then show you the chosen archive, file counts and total size. **Nothing is downloaded until you OK it.** Files go into a fresh untrusted-download folder and are only opened by our scripts (Python `-I`), never executed.
1. Enumerate every QP and MS for 9702/9701/9700/9709/9231 (+ old Options papers) before downloading. Record source URL/Drive ID, canonical name `<code>_<s><yy>_<qp|ms>_<vv>.pdf`, duplicates, and the chosen copy.
2. Download atomically (temp → verify PDF opens → rename), hash, record page count and whether a text layer exists.
3. **Watermark gate (zero tolerance).** For every PDF:
   - text-layer scan for third-party strings (`papacambridge`, `xtremepapers`, `dynamicpapers`, `gceguide`, `savemyexams`, `maxpapers`, `www.`, any non-UCLES URL);
   - image-layer scan: render each page, find light diagonal/large-font overlays and non-Cambridge logos;
   - outcome per file: `clean` | `watermark_removable` (a separate text/vector/image object not overlapping content, removed by object-level redaction before rendering, then re-scanned) | `watermark_blocking` (look for a clean copy; never ship).
   - Lesson from IGCSE BIO 15m-12: a light watermark does not count as "ink" for the cropper but **is visible** in the PNG. Pixel thresholds alone don't catch it.
4. Scanned (no text layer) PDFs: flag `scanned`. Recommendation: same as IB 1999, keep out of the first release and handle later with an OCR adapter if wanted.
5. Bundles: detect PDFs holding several papers, and older combined MS booklets covering several components. Split them by cover page / header before anything else.
6. Completeness proof: expected × found matrix per subject/year/session/component/variant, QP and MS paired. Every gap is listed explicitly.
7. Archive every canonical source PDF with its hash in Storage (`alevel-source-papers` private bucket). The IGCSE audit could not verify Biology because original PDFs were never stored.

**Exit:** `source_manifest.csv` with 100% of in-scope files `clean` or `watermark_removed_verified`, plus a gap list you sign off.

### Phase 1: Layout adapters and calibration

Each subject × era gets an adapter (YAML): page content bounds, furniture patterns, label grammar, stop rows, answer-area patterns, MS table profile. Calibration papers (one full paper per regime, all crops reviewed):

| Subject | Calibration set (indicative) |
|---|---|
| 9702 | s04 P2, s12 P42, s19 P22, s24 P42, m24 P52, s24 P12 (MCQ) |
| 9701 | s05 P2, w13 P42, s21 P22, s24 P42, s24 P52, s24 P12 |
| 9700 | s05 P2, w13 P42, s21 P22, s24 P42, s24 P52, s24 P12 |
| 9709 | s05 P1, w14 P32, s19 P62 (old S1), s21 P12, s24 P42, s24 P52 |
| 9231 | s08 P2 (old, EITHER/OR), s19 P11, s24 P12, s24 P32, s24 P42 |
| Options | one old P6 per science (e.g. s05 P6) |

Furniture specific to A Level (must never appear in a crop):
- `© UCLES …`, `9702/42/M/J/24`, `[Turn over`, page numbers, `BLANK PAGE`, cover barcode, `* 1234567890 *`;
- the rotated **"DO NOT WRITE IN THIS MARGIN"** strips on both side margins (2018+ papers);
- Physics data + formulae pages (pages 2–3) and the Chemistry Periodic Table / data pages. These are not part of any question. Store them once per paper as `AL-PHY-24s-42-DATA.png` if we want them later (decision);
- copyright-acknowledgement page and source credits under figures (mask only the credit text, never crop into the figure);
- 9709 2020+ printed answer lines after each question and the "Additional page" at the end;
- dotted answer leaders and empty answer boxes.

Content that must be kept: `Fig. x.x` diagrams with captions, tables the candidate must complete, graph grids the candidate must plot on, all axes/borders, the `[n]` mark at line end, and units on answer lines (`v = ………… m s⁻¹`). The convention for answer-line rows is decided on the first calibration contact sheet (see Open decision D6) and then frozen.

**Exit:** each calibration paper passes all Phase 3 gates and you approve its contact sheet.

### Phase 2: QP splitting

- **Structured (science P2/P4/P5/old P6, all 9709 and 9231):** extend the marker-anchor + ink-projection engine (`ib_aa_p1_splitter.py`) with A Level adapters. Do not write a new engine. Per paper:
  1. anchors from the text layer only (question numbers, `(a)`, `(i)`, inline `1(a)(i)`, `[n]`, stop rows), rejecting false anchors (axis ticks, variables `i`/`v`, table cells, `Fig. 1.1` numbers, page numbers);
  2. build the full label tree **before** cropping; check it against expected sequences;
  3. leaf/stem classification per the spec (Section 5 rules);
  4. boundaries inside verified whitespace, one shared cut between neighbours, cross-page segments concatenated into one logical image;
  5. render (same DPI/padding as the current IGCSE PNG output), strip borders, write provenance JSON (pages, rects, masks, render scale, sha256).
- **MCQ (P1):** one crop per question with options A–D included; extract `question_text`/`option_a..d`/`has_image` like the IGCSE MCQ pipeline; answer letters come from the MS key.
- Question numbers and part labels: the question number is never visible (crop starts after it or it's whited out); part labels such as `(b)` / `(ii)` stay, matching IGCSE/IB.

### Phase 3: QP quality gates (per paper, all must pass before MS work)

Automated (blocking):
1. Independent leaf verifier: expected leaf set == produced leaf set, exactly (`_verify_independent.py`).
2. Stem contract: zero missing/empty/orphan stems; every leaf's `stems` chain is nearest-first and exact (`verify_ib_stem_contract.py`, `validate_0580_hierarchy.py` logic).
3. Text-loss check: every text span inside the paper's question region is covered by exactly one crop (no span lost, no span in two crops), excluding furniture. This is the main test for "no question text is cut".
4. Edge-ink check: no ink touching any crop edge (catches sliced glyphs, fractions, diagrams).
5. Forbidden content: OCR + text layer on every crop finds no question number at top-left, no `[Maximum…]`/`© UCLES`/page codes/`DO NOT WRITE`/watermark strings, and no second sibling label.
6. Geometry outliers: abnormal height/whitespace ratio unless the crop contains a figure/table/grid.

Visual (blocking):
7. Labelled contact sheet of **every** crop of every paper, plus neighbour sheets (crop N vs N+1 with the source page). 100% of crops get looked at. Automated gates are guardrails, not proof.
8. Native-resolution review of every complex crop: diagrams, tables, multi-page, tall maths, last part before an answer area.
9. Defects get fixed globally in the adapter/engine, the whole affected batch is re-run, and every earlier gate is repeated.

### Phase 4: Markscheme splitting and mapping

MS layouts to support (profiles in the adapter):
- ~2002–2009: prose/list style, `1 (a) (i) … [1]`;
- ~2010–2017: `Page n | Mark Scheme | Syllabus | Paper` header + `Question | Answer | Marks` grid;
- 2018+: generic marking principles front pages (skip) + `Question | Answer | Marks | Guidance` tables; 9709 adds abbreviation pages (skip) and M1/A1/B1 columns;
- MCQ: answer key table → `answer_letter` only, no crops.

Rules (from IGCSE Phase 10 + IB):
- Split raw MS rows by their **printed key** (`3(b)(ii)`), never by order.
- A row spanning a page break is concatenated into one image; table header rows never leak into a crop.
- Map only answerable QP leaves (not stems). Mapping status per leaf: `exact`, `parent_ms_covers_child_qp`, `children_ms_merged_for_parent_qp`, `ocr_manual`, `unresolved`.
- Gate: mapped-MS ID set == QP-leaf ID set; every non-`exact` status is reviewed visually; `unresolved` blocks release of that paper.
- MS contact sheet review on the same 100% basis.

### Phase 5: Classification, dependencies, stems

1. **Canonical topic files** from the current syllabus guides (9702/9701/9700 2025–2027, 9709 and 9231 current guides): `syllabus_code`, `level` (AS | A), `chapter_num/title`, `topic`, `subtopic`, learning outcomes. Agents may only choose codes from these files (same rule as IGCSE).
2. **Hard constraints** (validator rejects violations):
   - 9231: P1/P2 (2020+) → Further Pure; P3 → Further Mechanics; P4 → Further Stats; old P2 by section.
   - Sciences: P1/P2 → AS topics only; P4/P5 → any topic (A-level content expected).
   - 9709: component (via era map) fixes the topic block: P1→Pure 1, P3→Pure 3, P4→Mechanics, P5→Stats 1, P6→Stats 2 (2020+); old P5 (M2) → nearest code + `outside_current_syllabus`.
   - Planning papers (P5): primary code from a "Practical skills" chapter, secondary code = the content topic (dual-code fields as in the IB table).
3. **Inputs to the classifier:** the crop's **native PDF text** (from provenance rects, better than tesseract for born-digital papers) + the PNG when there's a figure/graph/structure + the MS text for that leaf (it often names the concept).
4. **Output per leaf:** IGCSE/IB fields + `outside_current_syllabus`, `confidence`, `needs_review`. Stems inherit the dominant topic of their children.
5. **Dependencies** (separate from stems): "hence", "using your answer to (a)", "show that … hence", MS `ecf`/`ft`. Expect many in 9709.
6. **Execution:** batches of ≤10 papers, one subject at a time, never two subjects in parallel (rate-limit lesson). Sub-agents stalled in the IB sessions; fallback is a scripted run against the Claude API (Message Batches) with the same prompt and JSON schema (needs your OK, see D5).
7. **Validation:** row count == manifest, codes exist, constraints respected, `normalize_topic_drift.py` run so every code has one chapter/topic tuple, and a human spot-check of a stratified sample plus 100% of `needs_review`.

### Phase 6: Review package and release

- **Gate A (local only):** per-subject CSVs (master + stem), review package, QA report. URLs blank, nothing uploaded.
- **Gate B (storage):** after your approval, upload to the agreed buckets/prefixes with `upsert=false`, list back, re-download, compare SHA-256, then sign URLs (10-year expiry, as IGCSE).
- **Gate C (DB):** confirm project + table schema, back up in-scope rows, dry run with insert/update counts, insert leaves → stems → `stems/has_stem` mapping → zero dangling references.
- **Gate D (read-back):** exact counts and ID sets, mappings, signed URLs fetch the right bytes, RLS/bucket privacy unchanged. On any failure: restore and report.

### Phase 7: Rollout order

1. **Pilot:** Physics 9702, year 2024, all in-scope components and variants. Full gates, contact sheets to you, and then a pause until you approve.
2. Physics 2025 → 2016 (current-ish layout), then 2015 → 2010, then pre-2010 era by era. Each era starts with one approved calibration paper.
3. Chemistry 9701, then Biology 9700, the same way (shares most of the Physics adapter).
4. Mathematics 9709, then Further Mathematics 9231: two layouts each (pre/post-2020), roman first-level labels, renumbering, and the 9231 EITHER/OR questions.
5. Old Options papers for each science once that subject's pre-2010 era is done.
6. Classification and upload run per completed subject-era, so the DB fills progressively and is never blocked on the oldest years.

---

## 5. Split rules (frozen once D2 is decided)

- One image per answerable leaf; a parent with answerable children is never also a leaf.
- **Stem rule (D2 = always separate, IB protocol):** any non-answerable context (prose, data, figure, table, constants) before an answerable child is a `.stem`, **even when only one child uses it**. Context is stored exactly once and never folded into the child crop. Never create a stem for a bare label or empty space.
- Consequence for tooling: the IGCSE validator's "every stem has ≥2 consumers" check is switched off for A Level; `verify_ib_stem_contract.py` (zero missing stems) and the audit's `possible_missing_shared_stem` flag become blocking gates instead.
- Context after a part's `[mark]` that introduces the next part = next part's `.stem` (named for the next part).
- A figure/table the leaf asks the candidate to complete belongs to that leaf.
- A graphic after a mark stays with the earlier part only if that part uses it.
- No two siblings in one crop; no crop overlap; no question number; no furniture; no watermark.
- Uncertain ownership → `review_required`, never a guessed success.

---

## 6. Known risks and how the plan handles them

| Risk | Handling |
|---|---|
| Watermarked sources | Phase 0 gate, object-level removal only, re-scan, final OCR scan of every crop for watermark strings |
| 9709 renumbering 2020 | printed component in IDs + era map for classification |
| ID collision with IGCSE (`24s-42`) | `AL-` prefix everywhere (filename, question_id, storage path) |
| Long-tail layouts (pre-2009, combined MS) | per-era adapters + calibration paper per era; scanned papers deferred |
| Silent text loss | text-span coverage gate (Phase 3, #3) + 100% contact-sheet review |
| MS granularity ≠ QP granularity | explicit mapping statuses, visual review of every non-exact |
| Old-syllabus topics | nearest code + `outside_current_syllabus` flag (as IB) |
| Shared ledger corruption | fcntl lock + ledger in git |
| Agent stalls / rate limits | ≤10-paper batches, one subject at a time, API batch fallback |
| Production DB writes | Gates A–D, backups, dry runs, explicit approval per release |

---

## 7. Decisions

Decided 2026-10-09:
- **D2 Stems:** always a separate `.stem`, even for one consumer (IB protocol).
- **D3 Scope:** sciences P1 MCQ, P2, P4, P5 + all 9709 papers + **old Options papers** + **Further Maths 9231**. P3 Advanced Practical Skills is **out of scope**.
- **D4 Database:** new tables `questions_alevel_master` / `questions_alevel_stem` (IB-style: `level` AS|A, dual syllabus code, `outside_current_syllabus`, `option`, mapping status, `ms_signed_url`). Schema SQL is drafted and shown to you before it is run.
- **D5 Sources:** public archive. Archive choice, file counts and size are shown to you before any download.

Still open (defaults applied unless you say otherwise):
- **D1 Board:** Cambridge International assumed.
- **D6 Answer-line rows:** keep `quantity = ……… unit` lines, remove pure dotted lines; confirmed on the first contact sheet.
- **D7 Data/formulae/periodic-table pages:** drop from question crops; optionally store once per paper as a reference image.
- **D8 Year range:** every born-digital year the archive has (expected ~2002+); scanned papers deferred.
- **Storage buckets:** new private buckets prefixed `alevel-` (source PDFs, QP subparts, stems, markschemes), confirmed at Gate B.

---

## 8. Phase 0 findings (2026-10-09)

Sources checked (samples downloaded with approval into `ALEVEL/source_papers/_samples/`):

| Source | Coverage | What it adds to files | Verdict |
|---|---|---|---|
| cambridgeinternational.org | latest series, variant 1 only | nothing (official) | ground truth for comparisons |
| PapaCambridge | 9702/9701/9700/9709/9231, 2001–2026, 5,441 in-scope files, 2.65 GB | recent files byte-identical to official; some older files carry layered third-party watermarks: "A-PDF Watermark" PapaCambridge ribbon + footer banners, Acrobat-tagged XtremePapers diagonal text, StudentBounty links | usable only with the exact overlay stripper; fallback / 9231 source |
| Dynamic Papers (password page, unlocked by user) | 9702/9701/9700/9709 (no 9231), canonical names under `wp-content/uploads/2015/09|11/` | one plain-text line "www.dynamicpapers.com" in the top header strip of every page; text layer otherwise identical; only sub-pixel anti-aliasing differences vs official; no older third-party layers seen | preferred source for the four subjects (user choice) |
| BestExamHelp | 2010+ | not yet sampled | possible fallback |

Handling of the Dynamic Papers stamp: it sits in the page-furniture band above the page number, so crops never include it. The splitter's header exclusion is the first defence. The stamp is also a separate text object that is cut out before rendering, and the final crop gate OCR-checks every crop for "dynamicpapers". Scanned papers (e.g. 9702 s03 P2) are scans on every site and stay deferred.

Tools: `ALEVEL/scripts/enumerate_alevel_sources.py`, `check_source_watermarks.py`, `strip_overlay_watermarks.py` (pixel-footprint verified), `probe_dynamicpapers.py`.
