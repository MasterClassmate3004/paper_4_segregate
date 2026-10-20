# Biology 9700 MARK SCHEMES — handoff (2026-10-19)

Pipeline repo: ~/rootatom_data/alevel-pipeline (HEAD 24287db). Data: ~/rootatom_data/ALEVEL. Python: ~/.venvs/alevel/bin/python (always `-I`).
Read first: review/bio_b1/_HANDOFF.md (QP review state + house rules) and the memory file project_alevel_pipeline_plan.md
(Chemistry MS entries 2026-10-15/16 describe the exact MS workflow this repeats).

## The approved Biology QP set (what needs mark schemes)
- 386 non-alias papers, all visually approved.
  - auto run `bio_b1`: reviewed_crop_hashes.json["bio_b1"] (249 entries) — crops in splits/bio_b1
  - manual run: reviewed_crop_hashes.json["manual"] keys starting AL-BIO (138) — crops in splits/manual, specs manual/AL-BIO-*.json
  - A paper with a manual spec SUPERSEDES its bio_b1 split: use the manual crops for it. Build the definitive list first:
    every AL-BIO prefix that is approved, mapped to its QP run (manual if a manual spec exists, else bio_b1), minus aliases
    (review/bio_b1/duplicates.csv column "alias"). Write it to review/bio_b1/_ms_input.csv (prefix,qp_run) and check the count = 386.
- 431 Biology QP sources and 443 MS sources are local in source_papers/canonical (9700_*_ms_*.pdf).

## Process (same as Chemistry)
1. Split: `al_run_ms.py QP_RUN MS_RUN [--only PREFIX ...] [--workers N]`
   - run once for the bio_b1 papers (QP_RUN bio_b1, MS_RUN bio_ms1) and once for the manual ones (QP_RUN manual, MS_RUN bio_ms2),
     restricting each with --only to the prefixes from _ms_input.csv (--only needs the full "...-QP" prefix, else it silently does nothing).
   - Output: splits/<MS_RUN>/<PREFIX>-MS/, review/<MS_RUN>/ms_summary.csv. Statuses: exact / parent_ms_covers_child_qp /
     children_ms_merged_for_parent_qp / ms_absent / unresolved. MCQ papers (Paper 1) -> answers.csv.
   - Gate: al_verify_ms.py (coverage/dup/pixel-slice/overlap). PASS only on MS_OK.
   - Disk guard al_space.py (AL_MIN_FREE_GB=4) is checked by the runner.
2. Holds: overrides with written reasons in alevel-pipeline/ALEVEL/manual_specs/ms (absent, segments, drop_keys, add_keys, masks).
   Tools: al_ms_lines.py; agent prompt ALEVEL/MS_OVERRIDE_AGENT_PROMPT.txt (make a Biology copy if it needs Biology notes).
   Scanned 2002 papers: OCR approach in the memory notes (2026-10-13 night).
3. Visual review: paired QP|MS sheets via al_prepare_ms_review.py; prompt ALEVEL/MS_REVIEW_AGENT_PROMPT*.txt
   (Chemistry variants exist — write MS_REVIEW_AGENT_PROMPT_BIO.txt from them); checker al_check_ms_verdicts.py (requires sheets_read).
4. RULE (user, 2026-10-16): a question part with no mark scheme must not be stored. First look for the MS elsewhere
   (combined booklets, examiner reports' key tables, source_papers/raw_ms_search). Only if none exists, remove the part and
   record it in review/removed_no_ms.csv. Audit at the end: every approved unique Biology QP has a PASS mark scheme.
   MS of aliased QPs are dropped (aliases share the canonical paper's MS).
5. When done: approve, then offload Biology QP+MS PNGs to Google Drive with al_offload.py push RUN (verify by reading back
   from the cloud before deleting anything locally).

## Lessons from this week (follow them)
- Run review waves from a small, fresh session. At most 4-5 agents at once, and each review group <= 40 sheets
  (bigger groups or more agents -> image "request limit" or 10-minute stalls).
- Before the first wave, time ONE quick test agent; if it takes more than ~2 minutes, stop and tell the user
  (check free RAM: vm_stat / sysctl vm.swapusage; disk: df -h).
- Agent-flagged defects are real only about half the time: open the PNG and judge before fixing.
- Never let two agents edit the same spec/override at once — check list overlaps first.
- Check df -h before each wave; pause below 8 GB free.
- Do NOT re-render or re-run anything for Physics (f4073be+ not verified on Physics; Drive 9702 sources zip unreadable).
- Commit pipeline code changes with clear messages; keep review/bio_b1/_worklist.txt updated.
