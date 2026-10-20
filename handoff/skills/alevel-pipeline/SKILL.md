---
name: alevel-pipeline
description: Entry point for ROOTATOM's Cambridge A Level question-bank pipeline (Physics 9702, Chemistry 9701, Biology 9700, Maths 9709, Further Maths 9231) — splitting past-paper question papers and mark schemes into per-part PNGs, reviewing them, and preparing them for classification and upload. Use this skill whenever someone asks about the A Level pipeline's status, wants to "continue" A Level work, pick up a handoff, start the next subject, run review agents, or asks how the A Level split/review/mark-scheme/offload process works — even if they only say "continue the A Level work", "where are we on Biology/Maths", "start Further Maths", or "agents are stalling". It explains the layout, the current state, the operating rules for agents and sessions, and routes to the phase skills (alevel-sources, alevel-qp-split, alevel-manual-specs, alevel-qp-review, alevel-mark-schemes, alevel-storage, alevel-classification).
---

# A Level pipeline — start here

## Read first
1. `~/rootatom_data/alevel-pipeline/HANDOFF_ALEVEL_PIPELINE.md` — project overview, status table, house rules, open items.
2. The subject's own handoff/worklist: `~/rootatom_data/ALEVEL/review/<subject run>/_HANDOFF*.md`, `_worklist.txt`
   (Biology: `review/bio_b1/`; Maths: `review/mth/`).
3. `git -C ~/rootatom_data/alevel-pipeline log --oneline | head -20` — recent changes and what was verified.

## Layout (never deviate)
- Code: `~/rootatom_data/alevel-pipeline/ALEVEL/scripts/` (git). Data: `~/rootatom_data/ALEVEL/` (not git).
- Python: `~/.venvs/alevel/bin/python -I` (always `-I`; source PDFs are untrusted downloads).
- **Nothing under `~/Documents`** (iCloud evicts files; scripts then read nothing). The old worktree under Documents is stale.
- Approval record: `ALEVEL/review/reviewed_crop_hashes.json` (`{run: {prefix: {png: sha256}}}`). Approved = hashes match.

## Route to the right phase skill
| Task | Skill |
|---|---|
| Download/fetch sources, watermark checks, A3 pages, missing files | `alevel-sources` |
| Calibrate a subject, batch-split QPs, gates, aliases, hold causes, splitter/gate code changes, regressions | `alevel-qp-split` |
| A paper the splitter holds, or a defect in one paper's crops | `alevel-manual-specs` |
| Visual review of QP crops, verdicts, approvals | `alevel-qp-review` |
| Mark schemes (split, overrides, paired review, no-MS rule) | `alevel-mark-schemes` |
| Google Drive offload/restore, disk space | `alevel-storage` |
| Topic classification, manifests, DB upload | `alevel-classification` |

Subject order: Physics → Chemistry → Biology (all done) → Maths 9709 (in progress) → Further Maths 9231.
Per subject: sources → calibration → batch split → aliases → holds/manual specs → QP review → mark schemes → MS review →
no-MS audit → offload → classification → release.

## Operating rules for agents and sessions (hard-won)
- Use sub-agents (`general-purpose`, `model: sonnet`, background) for visual review and hand-spec work. **4–5 at once max.**
- **Review groups ≤ 40 contact sheets** (`al_groups_from_list.py --max-sheets 40`). Bigger groups stall; more agents →
  "media removed: request limit" and incomplete verdicts.
- **Before each wave run one timed test agent** ("Read <group file>, Read the first .jpg, describe it in one sentence").
  If it takes > 2 minutes: stop. Check RAM (`vm_stat`, `sysctl vm.swapusage`) and disk (`df -h`), and tell the user.
- A wave that stalls for an hour is almost never the API limit (a real limit errors immediately). Usual cause: a huge session
  (hundreds of MB transcript, GBs of `subagents/` logs) plus a Mac out of RAM. Fix: write a handoff file and continue in a
  **fresh session**; the user deletes old `~/.claude/projects/*/<session>/subagents/` (Claude may not delete transcripts).
- Agent-flagged defects are real ~50% of the time — open the PNG and judge it yourself before changing anything.
- Never give two agents the same spec/override file; check list overlaps before launching; if you edit a file an agent owns,
  message the agent ("re-read from disk").
- Check `df -h` before each wave (pause below 8 GB). Delete contact sheets after a run is approved (regenerable).
- After any generic code change: regression on all approved papers of all subjects (see `alevel-qp-split`), commit with a
  message that states what was and was not verified.
- Keep the subject worklist and handoff file current; at the end of a session, append the state to the handoff.

## What needs the user's OK
Any download or new source archive; deleting anything on Drive; storage/DB uploads and schema; scope changes; layout
conventions not already in the house rules (`HANDOFF_ALEVEL_PIPELINE.md` §4). Generic fixes, specs and review verdicts are
the operator's call — report them.

## Bundled references
- `references/HANDOFF_ALEVEL_PIPELINE.md` — full colleague handoff (copy of `~/rootatom_data/alevel-pipeline/HANDOFF_ALEVEL_PIPELINE.md`; the repo copy is authoritative when available).
