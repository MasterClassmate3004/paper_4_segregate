---
name: alevel-qp-review
description: 100% visual review of Cambridge A Level question-paper crops in the ROOTATOM pipeline — building contact sheets and review groups, running review sub-agents safely, cross-checking their verdicts, verifying each flagged defect by eye, fixing real ones and recording approvals in reviewed_crop_hashes.json. Use whenever a run has gate-passing papers that are not yet approved, someone says "review the PASS papers", "launch the review agents", "check the verdicts", "approve group 12", "agents are stalling / request limit", or wants to know whether a flagged crop is really wrong.
---

# QP visual review

Code `~/rootatom_data/alevel-pipeline/ALEVEL/scripts/`, Python `~/.venvs/alevel/bin/python -I`, data `~/rootatom_data/ALEVEL/`.
The gates prove structure and coverage; only eyes catch the rest. **Every crop of every unique paper is looked at.**

## 1. What to review
- Unique (non-alias) PASS papers whose crops are not already approved byte-for-byte in `review/reviewed_crop_hashes.json[RUN]`.
- Auto run crops: `splits/<RUN>/<PREFIX>/`; manual specs: `splits/manual/<PREFIX>/` (a manual spec supersedes the auto split).
- After a regression: `al_prepare_review.py NEW [--per 6] [--classes newpass,changed] [--summary]` (`--summary` skips approved+unchanged).

## 2. Sheets and groups
```
al_groups_from_list.py CROPS_RUN REVIEW_RUN LIST [--start N] [--max-sheets 40]
```
Renders labelled contact sheets (`al_contact_sheet.py`, 1400 px wide, blue label bars) into `review/REVIEW_RUN/` and writes
`_review_groups/group_NN.txt` (one line per paper: PREFIX + sheet paths). **Keep ≤ 40 sheets per group.**
Contact sheets are regenerable — delete them once the run is approved (disk).

## 3. Running review agents
Agent: `general-purpose`, `model: sonnet`, background. Prompt:
> Read /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/REVIEW_AGENT_PROMPT_QP.txt and follow it exactly. RUN=<run>, NN=<nn>.
> (Cambridge A Level <Subject> <code>.) If an image Read comes back without the picture (e.g. "media removed" / request limit),
> wait briefly and Read it again; never record a verdict for a sheet you did not actually see.

(Chem had `REVIEW_AGENT_PROMPT_CHEM*.txt`; `REVIEW_AGENT_INSTRUCTIONS.md` is the long-form contract.)
- **4–5 agents at once**, refill as they finish. One timed test agent before the first wave (> 2 min → stop, see `alevel-pipeline`).
- An agent that runs far longer than ~2–3 minutes per 6 papers is stuck: stop it and relaunch (smaller group if needed).
- Verdict file: `review/<RUN>/_verdicts/group_NN.json` — list of `{"prefix","sheets_read","crops_seen","defects":[{"label","rule","what"}]}`.

## 4. Checking verdicts
`al_check_verdicts.py RUN` → accepted / redo / pending + the defect list. It compares `sheets_read` with the real sheets.
For a run whose crops live elsewhere (manual) it reports REDO on crop counts — check `sheets_read` in the JSON instead.
An agent that admits it could not see sheets: move its verdict aside and re-run the group.

## 5. Verifying flags (agents are right only ~half the time)
Open the crop: `splits/<run>/<PREFIX>/<PREFIX>-<LABEL>.png`. Judge against the contract (one item, no question number, nothing cut,
no furniture, every mark, no plain dotted lines) and the house rules (`HANDOFF_ALEVEL_PIPELINE.md` §4). Frequent false alarms:
labelled answer lines and genetic-diagram scaffolds (kept by design), a part's own lead-in context, a stem holding only context.
Frequent real defects: next part's context left after a mark, furniture (rubrics, examiner column), a missed duplicate paper
(two papers with identical content → alias, see `alevel-qp-split`), a dropped completion blank, a leftover vector-drawn dotted line.
Record each decision with its reason in the subject worklist.

## 6. Fix and approve
- Real defect → fix (`alevel-manual-specs`; a recurring cause → generic fix + regression in `alevel-qp-split`), re-render, view.
- Approve clean papers:
```
al_approve.py RUN --groups NN [NN ...] [--except PREFIX ...]     # auto runs
al_approve.py manual PREFIX ...                                  # manual-spec papers
al_approve.py RUN --revoke PREFIX                                # undo
```
Approval stores current crop hashes; any later change to a crop un-approves the paper automatically.
- Done when every unique PASS paper of the subject is approved (count it against `run_summary.csv` minus aliases).
