# Maths 9709 QP — handoff (2026-10-20)

Pipeline repo: ~/rootatom_data/alevel-pipeline (HEAD 4ef7211). Data: ~/rootatom_data/ALEVEL. Python: ~/.venvs/alevel/bin/python (always `-I`).
Read first: review/mth/_worklist.txt, review/bio_b1/_HANDOFF.md (house rules + how review waves run), memory project_alevel_pipeline_plan.md.

## State
- Sources: 1478/1479 9709 files in source_papers/canonical (user-approved fetch 2026-10-19). 9709_s02_qp_6 failed (page count 4 vs Phase 0 3).
- NOT fetched (Phase 0 held, need user OK + current-scanner recheck): s19 (42), w24 (36), w25 (47) from Dynamic Papers held as
  'watermark_suspect' with no finding; ~10 2010s files held for rotated diagram labels (false positive since fixed); s26/m26 are
  PapaCambridge with 'Downloaded from PapaCambridge' (keep out). 10 Phase 0 read errors (al_fetch_sources --read-errors).
- Calibration mth_cal (7 papers) PASS + reviewed by eye. User decisions 2026-10-20: blank answer grids KEPT;
  separately marked (a)/(b) under a roman are leaves (Q6.ii.stem/.a/.b).
- Maths code is gated by IS_MATHS in al_qp_splitter.py (prefix AL-MTH-/AL-FMT-); leaf gate maths flag by prefix.
- Batch mth_b1 (730 QPs, --no-sheets): 479 PASS. Holds (251):
  166 coverage (mostly duplicated+sliced = tight compact 2010s layouts / tall maths crossing cuts; ~27 missing),
  27 leaves (splitter vs gate disagree on (a)/(b) under romans: separately-marked rule differs; both directions),
  ~38 REVIEW_REQUIRED (vertically overlapping crops, no whitespace around answer row, no Q anchor in 6 papers).
- Next: fix hold causes generically (IS_MATHS-gated; check 3 approved Bio papers stay byte-identical after each change), re-run
  holds (al_run_papers.py mth_b1 --list FILE --no-sheets merges into run_summary), then dedupe (al_dedupe + pixel scan of
  same-session variants), sheets for PASS (al_prepare_review / contact sheets), review groups <=40 sheets, 4-5 agents.

## Update 2026-10-20 (hold-reduction session)
- Pipeline HEAD 94420f5 (13b2f2e + 94420f5: Maths hold fixes, all IS_MATHS / maths-prefix gated; 3 approved Bio papers byte-identical after every change).
- mth_b1 now holds ALL 826 9709 QPs (730 + 96 newly fetched/rechecked, list review/mth/all_qp2.txt): 814 PASS, 12 HOLD.
- Holds = review/mth/manual_specs_needed.txt (reasons per paper). 09s-71 is a combined 71+72 source -> derive first.
- Decision taken (mine, report to user): bracketed hints '[The volume of a cone is ...]' go with the leaf printed directly above them (also at question end).
- Gate change (relaxing, all subjects): '[Question N continues on the next page.]' is furniture -> the all-subject gate regression item still applies.
- Next (needs user OK): dedupe aliases, contact sheets for the 814 PASS, review waves (4-5 agents, groups <=40 sheets, one timed test agent first).
