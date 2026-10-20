# Biology 9700 QP visual review — handoff (2026-10-19)

Pipeline repo: ~/rootatom_data/alevel-pipeline (HEAD f4073be). Data: ~/rootatom_data/ALEVEL. Python: ~/.venvs/alevel/bin/python (always `-I`).

## State
- Auto run `bio_b1`: 292 PASS, aliases in review/bio_b1/duplicates.csv (aliases are never reviewed/approved).
  Approved so far (reviewed_crop_hashes.json["bio_b1"]): 64 papers.
- Manual run (`splits/manual`, specs `manual/AL-BIO-*.json`): all 130 Bio specs pass both gates at f4073be.
  17 approved unchanged (reviewed_crop_hashes.json["manual"]); 103 need review.
- Pending review groups (each <= 40 contact sheets — bigger groups stall agents):
  - review/bio_b1/_review_groups/group_46 .. group_104  (crops in splits/bio_b1)
  - review/bio_man/_review_groups/group_19 .. group_40  (crops in splits/manual; contact sheets in review/bio_man)
  Old oversized group files moved to _review_groups_old/ — ignore them.

## How to run a review group
Agent (general-purpose, model sonnet, background), prompt:
  Read /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/REVIEW_AGENT_PROMPT_QP.txt and follow it exactly. RUN=<bio_b1|bio_man>, NN=<nn>. (Cambridge A Level Biology 9700.) If an image Read comes back without the picture, wait briefly and Read it again; never record a verdict for a sheet you did not actually see.
- At most 4-5 agents at once (more -> image "request limit" -> incomplete verdicts).
- Verdict: review/<RUN>/_verdicts/group_NN.json. Check bio_b1 with `al_check_verdicts.py bio_b1`
  (for bio_man the checker looks in splits/bio_man and reports REDO — ignore that, check sheets_read in the JSON).
- Agent flags are real only ~50% of the time: open the crop PNG and judge against the house rules before fixing.
- Approve clean papers: `al_approve.py bio_b1 --groups NN [--except PREFIX]`;
  manual papers: `al_approve.py manual PREFIX ...` (crops live in splits/manual).
- Fix a real defect in a manual paper: edit manual/<PREFIX>.json, then `al_manual.py run <PREFIX>` (both gates must pass), view the crop.
  A real defect in an auto paper: `al_manual.py init <PREFIX> bio_b1` makes a spec from the auto split, then fix it as above.

## House rules decided during review (keep)
- Context printed after a part's [mark] and before the next label = the NEXT part's context (Qn.x.stem / top of next leaf).
- Labelled answer rows (numbered genotype rows, figure label lines, genetic-diagram scaffold rows, fill-in sentence blanks) keep their dots; only plain unlabelled dotted rows are dropped.
- Furniture: "Answer all the questions", "Write your answers in the spaces provided", Section B essay rubric, "Circle the number of the question...", "Question N continues on page M", "Question N [x minutes]", For Examiner's Use heading + column rule, teacher REPORT FORM page.
- A table used by two parts goes with the part that carries most of the marks / is printed after its text (07w-41 Q1 table -> (c)).

## Open items (review/bio_b1/_worklist.txt)
- 18s-41 Q3.a.i: vector-drawn dotted answer line left above [2] (auto paper; needs a spec mask).
- 11s-52 Q1.d.ii: "Use the space below for any diagrams ... (i)" + blank space at top of (ii) (11s-53 is its alias).
- Physics: f4073be (al_manual question-number rule, leaf checker) NOT verified on Physics — Drive sources/9702_canonical.zip read 0 bytes on 2026-10-17. Do not re-render Physics specs until tested.

## After Biology QP review
Biology mark schemes (same process as Chemistry: al_run_ms.py, MS review), no-mark-scheme rule, offload to Drive, then Maths 9709.

## Update 2026-10-19 (later session) — Biology QP review DONE
- Pipeline HEAD 24287db (d491981: fused_marks row-only char split, al_manual init carries dot masks, gate working-space rules; 24287db: gate 'Total: [n]', 'Space for table/diagram').
- All groups reviewed (bio_b1 46-104, bio_man 19-40). 386/386 non-alias Biology papers approved
  (reviewed_crop_hashes: bio_b1 249 entries; "manual" 242 entries across all subjects, incl. new Bio specs that supersede auto splits).
- Real-defect patterns found (all fixed by specs; see _worklist.txt): mark fused beside '[Turn over' dropped;
  completion-passage final blank '..... .' dropped or slot-masked; 'Space for working/table/diagram' labels;
  text-free ruled grid cut as blank (20s-41); agent-written manual specs often leave next part's context
  after a [mark] in the previous part, or masks clipping figures/marks.
- Splitter itself NOT changed for these (specs only) -> a Biology re-split would reintroduce them; fix the
  splitter (completion blanks, working-space labels, text-free grids) before any re-run.
- Gate code changed (relaxing only) -> the pending all-subject gate regression still applies; fused_marks
  change verified on all 9700/9701 QPs (only m18_42 p9, w16_53 p5 change). Physics still untested (no sources).
- Next: Biology mark schemes (al_run_ms.py), as in the original plan.
