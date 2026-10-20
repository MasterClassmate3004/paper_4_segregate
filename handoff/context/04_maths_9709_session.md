# Maths 9709 calibration + hold-reduction session

Source: `917c70ae-0181-4fb4-89e3-cc8427b293bc.jsonl` · 2026-10-20 10:38:05 → 2026-10-20 17:51:31 (UTC) · images and internal reasoning omitted, long outputs trimmed, key-like strings redacted.

### User — 2026-10-20 10:38:05

<system-reminder>
The worktree at /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e may have been reassigned to another session by the worktree pool. The branch and working tree may not match what earlier turns observed. Run `git status` and `git rev-parse --abbrev-ref HEAD` before relying on prior file reads, and avoid `git checkout`, `git reset`, or committing until you have confirmed the branch is the one this session was working on. If it is not, tell the user the worktree was recycled and ask whether to switch back.
</system-reminder>

Background (from the session that started this one):
Biology 9700 QPs and mark schemes are finished (383 papers approved; images local, Drive offload pending because Google Drive for desktop cannot start). Maths 9709 started 2026-10-20: 1478 sources fetched with user OK, calibration of 7 papers approved by the user with two decisions (keep blank answer grids; separately marked (a)/(b) under a roman are leaves), full QP batch run once. Phase 0 held s19/w24/w25 sources need a separate user OK before fetching.

Task:
Continue the Cambridge A Level Maths 9709 question-paper split. Read /Users/nitya/rootatom_data/ALEVEL/review/mth/_HANDOFF.md first and follow it (also review/mth/_worklist.txt and review/bio_b1/_HANDOFF.md for house rules and how review waves run). Pipeline repo ~/rootatom_data/alevel-pipeline (HEAD 4ef7211), data ~/rootatom_data/ALEVEL, Python ~/.venvs/alevel/bin/python -I. Do not edit anything in this worktree folder; all work is in those two paths.
Goal: reduce the 251 HOLD papers of run mth_b1 (479/730 PASS) with generic splitter/gate fixes gated by IS_MATHS (al_qp_splitter.py) or the maths prefix flag (al_verify_leaves.py), largest buckets first: 166 coverage (duplicated+sliced in compact 2010s layouts), 27 leaf mismatches (separately-marked (a)/(b) under a roman: splitter and gate must apply the same rule), ~38 REVIEW_REQUIRED. After each change: re-run the affected holds (al_run_papers.py mth_b1 --list FILE --no-sheets), confirm 3 approved Biology papers (9700_s24_qp_22, 9700_w17_qp_42, 9700_s13_qp_52 in run bio_regchk) re-split byte-identical to reviewed_crop_hashes['bio_b1'], view a few changed crops, and commit with a clear message. Do not touch Physics. Keep review/mth/_worklist.txt updated and give the user a short status after each stage.
Done = holds reduced to the papers that need manual specs, a list of those papers with reasons, then (with user OK) dedupe aliases and start the visual review waves (4-5 agents, groups <=40 sheets, time one test agent first, df -h before each wave).

Shared notes folder for this group of sessions (outside the repo; read siblings' notes there, leave hand-over notes or large findings there instead of pasting them into messages): /Users/nitya/Library/Application Support/Claude/side-session-notes/local_ee3092d5-d44b-47ae-8f13-bbfe18e328ce

**Tool `mcp__ccd_turn__update_plan`**

```
{"items": [{"content": "Read handoff, worklist, house rules, notes", "status": "in_progress"}, {"content": "Analyze HOLD buckets of mth_b1", "status": "pending"}, {"content": "Fix coverage bucket (duplicated/sliced)", "status": "pending"}, {"content": "Fix leaf mismatch bucket", "status": "pending"}, {"content": "Triage REVIEW_REQUIRED holds", "status": "pending"}, {"content": "List papers needing manual specs", "status": "pending"}], "scope": "first_task"}
```

<details><summary>result</summary>

```
Plan shown (6 steps).
```
</details>

**Tool `Bash`**

```
cat /Users/nitya/rootatom_data/ALEVEL/review/mth/_HANDOFF.md; echo ======; wc -l /Users/nitya/rootatom_data/ALEVEL/review/mth/_worklist.txt; tail -60 /Users/nitya/rootatom_data/ALEVEL/review/mth/_worklist.txt; echo =====; ls "/Users/nitya/Library/Application Support/Claude/side-session-notes/local_ee3092d5-d44b-47ae-8f13-bbfe18e328ce"
```

<details><summary>result</summary>

```
Exit code 1
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
  ~38 REVIEW_REQUIRED (vertically overlapping cr
… [458 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd /Users/nitya/rootatom_data/ALEVEL/review/mth; ls -la; cat _worklist.txt; echo =====; ls "/Users/nitya/Library/Application Support/Claude/side-session-notes/local_ee3092d5-d44b-47ae-8f13-bbfe18e328ce/"
```

<details><summary>result</summary>

```
Exit code 1
total 56
drwxr-xr-x@   6 nitya  staff    192 Oct 20 14:37 .
drwxr-xr-x@ 152 nitya  staff   4864 Oct 20 14:26 ..
-rw-r--r--@   1 nitya  staff   1923 Oct 20 14:37 _HANDOFF.md
-rw-r--r--@   1 nitya  staff   1530 Oct 20 14:37 _worklist.txt
-rw-r--r--@   1 nitya  staff   1232 Oct 20 14:36 foot_holds.txt
-rw-r--r--@   1 nitya  staff  13770 Oct 20 14:25 qp_list.txt
# Maths 9709 worklist (started 2026-10-19)
[done] sources: al_fetch_sources.py 9709 -> 1478/1479 fetched (Phase 0 approved, DP 1417 + PapaCambridge 62); FAIL 9709_s02_qp_6.pdf (stripped 4 pages vs Phase 0 3) -> check
[open] Phase 0 held 225 9709 files: watermark_suspect 215 = whole sessions s19 (42), w24 (36), w25 (47), s26 (48, out of scope?) + strays; 10 iCloud read errors (al_fetch_sources --read-errors) -> look before the batch (s19/w24/w25 QPs absent)
[done] calibration run mth_cal (7 papers: 24s-12/32/42/52, 17w-12, 13s-62, 07w-41): 7/7 PASS both gates after splitter b590d85 (IS_MATHS-gated; 3 approved Bio papers byte-identical); 23 contact sheets reviewed by eye, clean
[decided 2026-10-20] blank answer grids (24s-52 Q4.b graph paper) are KEPT in their leaf
[decided 2026-10-20] separately marked (a)/(b) under a roman are leaves (Q6.ii.stem + Q6.ii.a/b) -> splitter + leaf gate changed (commit above); calibration 7/7 PASS again
[note] context placement: after a part's answer lines before the next label -> top of next leaf (Q8.b) or Qn.x.stem (page head / roman-as-part) -- both per house rule
[next] after u
… [427 more characters trimmed]
```
</details>

**Tool `Bash`**

```
ls -la "/Users/nitya/Library/Application Support/Claude/side-session-notes/local_ee3092d5-d44b-47ae-8f13-bbfe18e328ce/"; cat /Users/nitya/rootatom_data/ALEVEL/review/mth/foot_holds.txt; head -5 /Users/nitya/rootatom_data/ALEVEL/review/mth/qp_list.txt; cat /Users/nitya/rootatom_data/ALEVEL/review/bio_b1/_HANDOFF.md
```

<details><summary>result</summary>

```
total 0
drwx------@ 2 nitya  staff  64 Oct 20 16:08 .
drwx------@ 3 nitya  staff  96 Oct 20 16:08 ..
9709_s04_qp_1.pdf
9709_s10_qp_12.pdf
9709_s10_qp_41.pdf
9709_s10_qp_42.pdf
9709_s11_qp_11.pdf
9709_s11_qp_43.pdf
9709_s11_qp_51.pdf
9709_s11_qp_53.pdf
9709_s12_qp_11.pdf
9709_s12_qp_12.pdf
9709_s12_qp_32.pdf
9709_s12_qp_43.pdf
9709_s12_qp_51.pdf
9709_s13_qp_11.pdf
9709_s13_qp_12.pdf
9709_s13_qp_41.pdf
9709_s14_qp_42.pdf
9709_s14_qp_43.pdf
9709_s14_qp_53.pdf
9709_s15_qp_11.pdf
9709_s15_qp_13.pdf
9709_s15_qp_42.pdf
9709_s15_qp_43.pdf
9709_s15_qp_51.pdf
9709_s16_qp_11.pdf
9709_s16_qp_12.pdf
9709_s16_qp_13.pdf
9709_s16_qp_52.pdf
9709_w02_qp_4.pdf
9709_w08_qp_5.pdf
9709_w09_qp_41.pdf
9709_w09_qp_42.pdf
9709_w10_qp_31.pdf
9709_w10_qp_32.pdf
9709_w10_qp_43.pdf
9709_w10_qp_53.pdf
9709_w10_qp_63.pdf
9709_w11_qp_11.pdf
9709_w11_qp_12.pdf
9709_w11_qp_42.pdf
9709_w11_qp_53.pdf
9709_w12_qp_11.pdf
9709_w12_qp_53.pdf
9709_w13_qp_31.pdf
9709_w13_qp_32.pdf
9709_w13_qp_41.pdf
9709_w13_qp_42.pdf
9709_w13_qp_51.pdf
9709_w13_qp_52.pdf
9709_w14_qp_11.pdf
9709_w14_qp_12.pdf
9709_w14_qp_13.pdf
9709_w14_qp_42.pdf
9709_w14_qp_51.pdf
9709_w14_qp_52.pdf
9709_w15_qp_11.pdf
9709_w15_qp_42.pdf
9709_w15_qp_43.pdf
9709_w15_qp_51.pdf
9709_w15_qp_52.pdf
9709_w16_qp_11.pdf
9709_w16_qp_13.pdf
9709_w16_qp_33.pdf
9709_w16_qp_52.pdf
9709_w16_qp_73.pdf
9709_m16_qp_12.pdf
9709_m16_qp_22.pdf
9709_m16_qp_32.pdf
9709_m16_qp_42.pdf
9709_m16_qp_62.pdf
# Biology 9700 QP visual review — handoff (2026-10-19)

Pipeline repo: ~
… [4830 more characters trimmed]
```
</details>

**Tool `Bash`**

```
ls /Users/nitya/.claude/projects/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate/memory/; cat /Users/nitya/.claude/projects/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate/memory/MEMORY.md; cd ~/rootatom_data/alevel-pipeline; git log --oneline | head -8; git status --short | head; ls; ls ALEVEL | head -50
```

<details><summary>result</summary>

```
cat: /Users/nitya/.claude/projects/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate/memory/MEMORY.md: No such file or directory
4ef7211 QP splitter + coverage gate: '[Question(s) N ... is/are printed on the next page / overleaf.]' is furniture
1fecba5 Maths: separately marked (a)/(b) under a roman are leaves (user decision 2026-10-20)
b590d85 QP splitter: Maths 9709 calibration (IS_MATHS-gated; Phy/Chem/Bio unchanged)
abaec6b MS splitter: column-slice override segments, page-margin cap never cuts words; Biology MS review fixes
06220df MS splitter: pasted pictures are never rules (wide answer images kept whole); Bio review fixes
00bec90 MS splitter: component_pages override, Marks digits never cut at the right edge; Biology MS overrides
a764242 MS splitter: MCQ keys honour override 'absent' for discounted questions
04e1d24 al_fetch_sources: --read-errors fetches files Phase 0 could not open
ALEVEL
CLASSIFICATION_HANDOVER.md
MANUAL_SPEC_AGENT_PROMPT.txt
MANUAL_SPEC_AGENT_PROMPT_BIO.txt
MS_OVERRIDE_AGENT_PROMPT.txt
MS_OVERRIDE_AGENT_PROMPT_BIO.txt
MS_REVIEW_AGENT_PROMPT.txt
MS_REVIEW_AGENT_PROMPT_BIO.txt
MS_REVIEW_AGENT_PROMPT_CHEM1.txt
MS_REVIEW_AGENT_PROMPT_CHEM2.txt
MS_REVIEW_AGENT_PROMPT_CHEM_2ND.txt
REVIEW_AGENT_INSTRUCTIONS.md
REVIEW_AGENT_PROMPT.txt
REVIEW_AGENT_PROMPT_CHEM.txt
REVIEW_AGENT_PROMPT_CHEMFIX.txt
REVIEW_AGENT_PROMPT_QP.txt
manual_specs
scripts
source_papers
source_papers_phase0_ledger.csv
source_papers_phase0_manifest.csv
Shell cwd wa
… [121 more characters trimmed]
```
</details>

**Tool `Bash`**

```
find /Users/nitya/.claude/projects -name "project_alevel_pipeline_plan.md" 2>/dev/null; P=~/rootatom_data/alevel-pipeline; ls $P/ALEVEL $P/scripts | head -80; wc -l $P/scripts/*.py 2>/dev/null | sort -n | tail -30
```

<details><summary>result</summary>

```
/Users/nitya/.claude/projects/-Users-nitya-Documents-Nitya-Projects-rootatom-paper-4-segregate/memory/project_alevel_pipeline_plan.md
ls: /Users/nitya/rootatom_data/alevel-pipeline/scripts: No such file or directory
/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL:
CLASSIFICATION_HANDOVER.md
MANUAL_SPEC_AGENT_PROMPT.txt
MANUAL_SPEC_AGENT_PROMPT_BIO.txt
MS_OVERRIDE_AGENT_PROMPT.txt
MS_OVERRIDE_AGENT_PROMPT_BIO.txt
MS_REVIEW_AGENT_PROMPT.txt
MS_REVIEW_AGENT_PROMPT_BIO.txt
MS_REVIEW_AGENT_PROMPT_CHEM1.txt
MS_REVIEW_AGENT_PROMPT_CHEM2.txt
MS_REVIEW_AGENT_PROMPT_CHEM_2ND.txt
REVIEW_AGENT_INSTRUCTIONS.md
REVIEW_AGENT_PROMPT.txt
REVIEW_AGENT_PROMPT_CHEM.txt
REVIEW_AGENT_PROMPT_CHEMFIX.txt
REVIEW_AGENT_PROMPT_QP.txt
manual_specs
scripts
source_papers
source_papers_phase0_ledger.csv
source_papers_phase0_manifest.csv
(eval):1: no matches found: /Users/nitya/rootatom_data/alevel-pipeline/scripts/*.py
```
</details>

### Assistant — 2026-10-20 10:38:25

Reading the handoff and pipeline layout; next I'll bucket the 251 holds.

**Tool `Bash`**

```
cat /Users/nitya/.claude/projects/-Users-nitya-Documents-Nitya-Projects-rootatom-paper-4-segregate/memory/project_alevel_pipeline_plan.md; P=~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ls $P; wc -l $P/al_qp_splitter.py $P/al_verify_leaves.py $P/al_run_papers.py
```

<details><summary>result</summary>

```
---
name: project_alevel_pipeline_plan
description: A Level (Cambridge 9702/9701/9700/9709/9231) split→MS→classify→upload plan and user decisions (2026-10-09)
metadata:
  type: project
---

Plan drafted 2026-10-09 in worktree branch claude/a-level-papers-splitting-plan-6b3cde, file ALEVEL_PIPELINE_PLAN.md (commit cb945612). Nothing downloaded/split yet.

User decisions:
- Stems: ALWAYS a separate .stem even with one consumer (IB protocol), NOT the IGCSE >=2-consumer rule.
- Scope: science P1 MCQ, P2, P4, P5 + all 9709 + old pre-2009 Options papers + Further Maths 9231. P3 practical OUT.
- DB: new tables questions_alevel_master / questions_alevel_stem (IB-style), not questions_master_v2.
- Sources: download from a public archive, but show archive + counts + size and get OK before downloading; zero watermarks.
- IDs need AL- prefix (paper codes like 24s-42 collide with IGCSE). 9709/9231 renumbered components in 2020.

**Why:** avoid re-asking settled decisions. **How to apply:** follow the plan's phases; pilot is Physics 9702 2024 with contact-sheet approval before batching. Related: [[project_ib_sci_pipeline_state]]

Phase 0 source findings (2026-10-09): user prefers Dynamic Papers (DP) as source; its A Level pages are WordPress-password-protected (user unlocks in browser themselves; never type it). DP files live at dynamicpapers.com/wp-content/uploads/2015/09|11/<canonical name> and are fetchable directly; each page has one "www.dynamicpapers.com" text stamp in the top header
… [24175 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ls review/mth_b1 | head; df -h ~ | tail -1; head -3 review/mth_b1/run_summary.csv; ~/.venvs/alevel/bin/python -I -c "
import csv,collections
r=list(csv.DictReader(open('review/mth_b1/run_summary.csv')))
print(len(r), r[0].keys())
print(collections.Counter(x['status'] for x in r))
"
```

<details><summary>result</summary>

```
run_summary.csv
/dev/disk3s5   228Gi   180Gi    19Gi    91%    2.4M  197M    1%   /System/Volumes/Data
source,prefix,status,crops,leaves,coverage,reason
9709_m16_qp_12.pdf,AL-MTH-16m-12-QP,HOLD,29,expected=21 produced=21 missing=[] extra=[],pages 2-5: missing=0 duplicated=1 sliced_boundaries=5 answer_row_words=1 (in a crop: 1),coverage
9709_m16_qp_22.pdf,AL-MTH-16m-22-QP,HOLD,17,expected=13 produced=13 missing=[] extra=[],pages 2-3: missing=0 duplicated=1 sliced_boundaries=3 answer_row_words=0 (in a crop: 0),coverage
730 dict_keys(['source', 'prefix', 'status', 'crops', 'leaves', 'coverage', 'reason'])
Counter({'PASS': 479, 'HOLD': 251})
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv,collections,re
r=[x for x in csv.DictReader(open('review/mth_b1/run_summary.csv')) if x['status']=='HOLD']
c=collections.Counter(x['reason'][:40] for x in r); print(c.most_common(20))
for x in r:
  if not x['reason'].startswith('coverage'): print(x['prefix'], x['reason'][:200], '|', x['leaves'][:150])
" | head -80; ls splits/mth_b1 | head -3; ls splits/mth_b1 | wc -l
```

<details><summary>result</summary>

```
[('coverage', 166), ('splitter: RuntimeError: REVIEW_REQUIRED:', 58), ('leaves ', 19), ('leaves coverage', 8)]
AL-MTH-16m-72-QP leaves  | expected=16 produced=15 missing=['Q6.ii.a', 'Q6.ii.b'] extra=['Q6.ii']
AL-MTH-17m-72-QP leaves coverage | expected=20 produced=19 missing=['Q7.ii.a', 'Q7.ii.b'] extra=['Q7.ii']
AL-MTH-02s-21-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper | 
AL-MTH-02s-31-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper | 
AL-MTH-04s-11-QP splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q2 and Q3.i on page 2 have no proven separator; cur_crop=215.52..225.60 cur_ink=216.00..225.12 cur_semantic=215.52..225.60 | 
AL-MTH-06s-41-QP leaves  | expected=18 produced=19 missing=['Q4.i'] extra=['Q4.i.a', 'Q4.i.b']
AL-MTH-08s-01-QP splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q1 and Q2.i on page 2 have no proven separator; cur_crop=130.08..142.56 cur_ink=132.00..141.12 cur_semantic=130.08..142.56 | 
AL-MTH-08s-11-QP splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q1 and Q2.i on page 2 have no proven separator; cur_crop=130.08..142.56 cur_ink=132.00..141.12 cur_semantic=130.08..142.56 | 
AL-MTH-08s-21-QP splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q3 and Q4 on page 2 have no proven separator; cur_crop=225.60..238.56 cur_ink=228.00..237.60 cur_semantic=225.60..238.56;  | 
AL-MTH-09s-11-QP
… [11122 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv,collections,re
r=[x for x in csv.DictReader(open('review/mth_b1/run_summary.csv')) if x['status']=='HOLD' and 'coverage' in x['reason']]
c=collections.Counter()
for x in r:
  m=dict((k,int(v)) for k,v in re.findall(r'(missing|duplicated|sliced_boundaries|answer_row_words)=(\d+)',x['coverage']))
  key=tuple(k for k in ('missing','duplicated','sliced_boundaries','answer_row_words') if m.get(k))
  c[key]+=1
print(c)
"; ls splits/mth_b1/AL-MTH-16m-22-QP | head -30; wc -l ~/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_verify_coverage.py
```

<details><summary>result</summary>

```
Counter({('duplicated', 'sliced_boundaries', 'answer_row_words'): 33, ('duplicated', 'sliced_boundaries'): 30, ('sliced_boundaries', 'answer_row_words'): 27, ('sliced_boundaries',): 26, ('missing',): 18, ('missing', 'duplicated', 'sliced_boundaries', 'answer_row_words'): 13, ('missing', 'answer_row_words'): 10, ('missing', 'duplicated', 'sliced_boundaries'): 9, ('duplicated', 'answer_row_words'): 5, ('missing', 'sliced_boundaries'): 2, ('missing', 'sliced_boundaries', 'answer_row_words'): 1})
AL-MTH-16m-22-QP-Q1.png
AL-MTH-16m-22-QP-Q2.png
AL-MTH-16m-22-QP-Q3.png
AL-MTH-16m-22-QP-Q4.i.png
AL-MTH-16m-22-QP-Q4.ii.png
AL-MTH-16m-22-QP-Q4.stem.png
AL-MTH-16m-22-QP-Q5.png
AL-MTH-16m-22-QP-Q6.i.png
AL-MTH-16m-22-QP-Q6.ii.png
AL-MTH-16m-22-QP-Q6.stem.png
AL-MTH-16m-22-QP-Q7.i.png
AL-MTH-16m-22-QP-Q7.ii.png
AL-MTH-16m-22-QP-Q7.stem.png
AL-MTH-16m-22-QP-Q8.i.png
AL-MTH-16m-22-QP-Q8.ii.a.png
AL-MTH-16m-22-QP-Q8.ii.b.png
AL-MTH-16m-22-QP-Q8.ii.stem.png
AL-MTH-16m-22-QP-split-provenance.json
gates.log
splitter.log
     506 /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_verify_coverage.py
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b1/AL-MTH-16m-22-QP; cat gates.log | head -60
```

<details><summary>result</summary>

```
expected=13 produced=13 missing=[] extra=[]
  SLICED-BOUNDARY (2, 'Q4.ii', 352.4, 14)
  SLICED-BOUNDARY (2, 'Q5', 347.4, 14)
  SLICED-BOUNDARY (2, 'Q6.ii', 623.4, 10)
  DUPLICATE (2, 343, 'a', ['Q4.ii', 'Q5'])
pages 2-3: missing=0 duplicated=1 sliced_boundaries=3 answer_row_words=0 (in a crop: 0)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b1/AL-MTH-16m-22-QP; ~/.venvs/alevel/bin/python -I -c "
import json;d=json.load(open('AL-MTH-16m-22-QP-split-provenance.json'));print(d.keys())
for k,v in list(d.items()):
  if isinstance(v,list): print(k, json.dumps(v[:3])[:1500])
  elif isinstance(v,dict): print(k, json.dumps(v)[:800])
  else: print(k,v)
"
```

<details><summary>result</summary>

```
dict_keys(['source_pdf', 'prefix', 'normalized_geometry', 'response_furniture_masks', 'outputs', 'manual_masks'])
source_pdf /Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_m16_qp_22.pdf
prefix AL-MTH-16m-22-QP
normalized_geometry False
response_furniture_masks {}
outputs {"Q1": [{"pdf_page": 2, "clip_points": [40.0, 60.44, 560.0, 82.32], "semantic_bounds_points": [60.44, 85.34], "two_dimensional_seam": false}], "Q2": [{"pdf_page": 2, "clip_points": [40.0, 99.6, 560.0, 121.68], "semantic_bounds_points": [99.44, 124.34], "two_dimensional_seam": false}], "Q3": [{"pdf_page": 2, "clip_points": [40.0, 138.96, 560.0, 173.04], "semantic_bounds_points": [138.44, 176.3], "two_dimensional_seam": false}], "Q4.stem": [{"pdf_page": 2, "clip_points": [40.0, 190.8, 560.0, 260.4], "semantic_bounds_points": [190.4, 261.5], "two_dimensional_seam": false}], "Q4.i": [{"pdf_page": 2, "clip_points": [40.0, 263.76, 560.0, 298.32], "semantic_bounds_points": [261.5, 299.52], "two_dimensional_seam": false}], "Q4.ii": [{"pdf_page": 2, "clip_points": [40.0, 302.64, 560.0, 352.36], "se
manual_masks []
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:38:43

Looking at a sample coverage hold (16m-22) to see what "duplicated/sliced" really is.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b1/AL-MTH-16m-22-QP; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; mkdir -p $S; ~/.venvs/alevel/bin/python -I -c "
import json,fitz
d=json.load(open('AL-MTH-16m-22-QP-split-provenance.json'))
for k,v in d['outputs'].items():
  for s in v: print(k,s['pdf_page'],s['clip_points'],s['semantic_bounds_points'])
doc=fitz.open(d['source_pdf']); p=doc[1]
p.get_pixmap(dpi=100,clip=fitz.Rect(0,280,595,420)).save('$S/p2.png')
for b in p.get_text('words'):
  if 330<b[1]<360: print(b)
"
```

<details><summary>result</summary>

```
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
Q1 2 [40.0, 60.44, 560.0, 82.32] [60.44, 85.34]
Q2 2 [40.0, 99.6, 560.0, 121.68] [99.44, 124.34]
Q3 2 [40.0, 138.96, 560.0, 173.04] [138.44, 176.3]
Q4.stem 2 [40.0, 190.8, 560.0, 260.4] [190.4, 261.5]
Q4.i 2 [40.0, 263.76, 560.0, 298.32] [261.5, 299.52]
Q4.ii 2 [40.0, 302.64, 560.0, 352.36] [300.72, 352.36]
Q5 2 [40.0, 347.36, 560.0, 376.56] [347.36, 378.08]
Q6.stem 2 [40.0, 409.38, 560.0, 550.32] [409.38, 553.44]
Q6.i 2 [40.0, 553.44, 560.0, 574.8] [553.44, 576.48]
Q6.ii 2 [40.0, 579.12, 560.0, 623.44] [577.68, 623.44]
Q7.stem 2 [40.0, 618.44, 560.0, 640.56] [618.44, 644.88]
Q7.i 2 [40.0, 644.88, 560.0, 677.52] [644.88, 678.72]
Q7.ii 2 [40.0, 680.88, 560.0, 702.48] [679.44, 705.38]
Q8.i 3 [40.0, 58.8, 560.0, 81.84] [58.8, 83.52]
Q8.ii.stem 3 [40.0, 86.16, 560.0, 107.81] [84.0, 107.81]
Q8.ii.a 3 [40.0, 107.81, 560.0, 171.84] [107.81, 171.84]
Q8.ii.b 3 [40.0, 171.84, 560.0, 212.96] [171.84, 212.96]
(49.320556640625, 352.3593444824219, 55.20555877685547, 363.7378234863281, '5', 15, 0, 0)
(72.84022521972656, 352.87957763671875, 101.0452651977539, 364.2580871582031, 'Given', 15, 1, 0)
(103.92024993896484, 352.87957763671875, 121.597412109375, 364.2580871582031, 'that', 15, 1, 1)
(124.55999755859375, 346.9342041015625, 130.88499450683594, 370.606201171875, 'Ó', 15, 1, 2)
(133.07989501953125, 343.3317565917969, 137.56907653808594, 352.011474609375, 'a', 16, 0, 0)
(139.91934204101562, 
… [1556 more characters trimmed]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/p2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "SLICED\|DUPLICATE\|def \|IS_MATHS\|maths" al_verify_coverage.py | head -80
```

<details><summary>result</summary>

```
80:def shift29(t: str) -> str:
86:def is_furniture(span_font: str, text: str, x0: float, y0: float, x1: float, y1: float) -> bool:
104:def main() -> int:
129:        def font_of(x0, y0, x1, y1):
374:    def crop_words(label):
494:        print("  SLICED-BOUNDARY", sl)
498:        print("  DUPLICATE", d)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 280,506p al_verify_coverage.py
```

<details><summary>result</summary>

```
    for pno, segs in regions.items():
        page = doc[pno - 1]
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for sp in line["spans"]:
                    if is_barcode_span(sp["text"], sp["bbox"][1], sp["bbox"][3]):
                        r = fitz.Rect(sp["bbox"])
                        page.draw_rect(fitz.Rect(r.x0 - 2, 18 if r.y1 < 100 else r.y0 - 1, r.x1 + 2, r.y1 + 1.5),
                                       color=None, fill=(1, 1, 1), overlay=True)
        for d in page.get_drawings():          # 2025+ corner crop-marks (furniture)
            r = d.get("rect")
            if r is not None and r.y0 > 785 and max(r.width, r.height) <= 25 and (r.x1 < 62 or r.x0 > 533):
                page.draw_rect(r + (-2.5, -2.5, 2.5, 2.5), color=None, fill=(1, 1, 1), overlay=True)
        # 2010s examiner mark boxes in the right margin (furniture): an
        # independent copy of the splitter's rule -- >=4 text-free drawings
        # confined to x 528-568, spanning 15-35 pt, not joined to a body line
        pw_ = page.get_text("words")
        margin = [d["rect"] for d in page.get_drawings() if d.get("rect") is not None
                  and d["rect"].x0 >= 528 and d["rect"].x1 <= 572 and 60 < d["rect"].y0 and d["rect"].y1 < 790
                  and d["rect"].height <= 40 and d["rect"].width <= 35
                  and not [w for w in pw_ if fitz.Rect(w[:4]).intersects(d["rect"] + (-2, -2, 2, 2))]]
        if len
… [11777 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "IS_MATHS" al_qp_splitter.py | head -60; grep -n "^def \|^class " al_qp_splitter.py | wc -l
```

<details><summary>result</summary>

```
47:IS_MATHS=PREFIX.startswith(('AL-MTH-','AL-FMT-'))
1235:    if IS_MATHS:
1250:    if IS_MATHS:
3139:            elif IS_MATHS and len([v for v in ws if re.search(r'[A-Za-z]{4,}',v[4])])>=2:
3152:        if not IS_MATHS and not CAPTION_RE.fullmatch(' '.join(w[4] for w in cap).strip()):
3215:                    prose=len([w for w in ws if re.search(r'[A-Za-z]{4,}',w[4])])>=(2 if IS_MATHS else 3)
3226:            if IS_MATHS:
4120:        if IS_MATHS:
      19
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "^def \|^class \|^# \|^[A-Z_]* *=" al_qp_splitter.py | head -80; sed -n 1,60p al_qp_splitter.py
```

<details><summary>result</summary>

```
34:SRC    = sys.argv[1] if len(sys.argv) > 1 else '/Users/nitya/Documents/Nitya/Projects/rootatom/paper_4_segregate/IB/scripts/_test_AAHL_P1_M22.pdf'
35:OUTDIR = Path(sys.argv[2] if len(sys.argv) > 2 else '/Users/nitya/Documents/Nitya/Projects/rootatom/paper_4_segregate/IB/scripts/_out')
36:PREFIX = sys.argv[3] if len(sys.argv) > 3 else 'IB-MAAHL-M22-P1-QP'
39:# A Level fork (2026-10-10): Cambridge AS & A Level papers share the IGCSE
40:# house layout (UCLES footer, margin strips, (a)/(i) columns, [n] marks), so
41:# the Cambridge code path is enabled for AL- prefixes too.  Source of the
42:# fork: IB/scripts/ib_aa_p1_splitter.py (unchanged copy in ~/rootatom_data/ref).
43:IS_IGCSE=PREFIX.startswith(('IG-MTH-', 'AL-'))
44:IS_ALEVEL=PREFIX.startswith('AL-')
45:# A Level Mathematics / Further Mathematics (9709/9231): uncaptioned diagrams printed above
46:# 'The diagram shows ...', short symbolic context lines ('The function h is defined by ...')
47:IS_MATHS=PREFIX.startswith(('AL-MTH-','AL-FMT-'))
48:DPI=220; HEADER_Y=58; FOOTER_Y=790 if IS_IGCSE else 802; CONTENT_L=float(__import__('os').environ.get('IB_CONTENT_L',40)); CONTENT_R=float(__import__('os').environ.get('IB_CONTENT_R',560))
49:CONTENT_BOTTOM=782 if IS_IGCSE else 774  # stay above Cambridge/IB footer furniture
71:PAD_PT=6; RDPI=150; SC=RDPI/72.0; BIGGAP_PX=13
72:PART_X_MAX=88 if IS_IGCSE else 96
73:# A continuation-page roman can be outdented a few points (86.97 pt in
74:# 0580_w15_qp_41) while remaining clearly to t
… [5481 more characters trimmed]
```
</details>

### Assistant — 2026-10-20 10:39:07

Reading the splitter's cut logic (main() is ~3700 lines) to find where a question's top edge is set.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "semantic\|no proven separator\|no whitespace around answer row\|duplicat" al_qp_splitter.py | head -60
```

<details><summary>result</summary>

```
204:        # extent detection.  `semantic` is stricter about visible glyph
208:        self.semantic=self.gray<230
363:        semantic_prompt_row=bool(Q_RE.match(first_token) or
387:        has_trailing_leader=(trailing_dot_run_w>150 and not semantic_prompt_row)
389:                     has_trailing_leader) and not semantic_prompt_row
400:                            semantic_prompt_row))
526:    for idx,(ry0,ry1,rtext,rx0,ris_dot,rsemantic) in enumerate(row_records):
527:        if ris_dot or rsemantic: continue
569:    # actual y-distance first, then apply semantic rank within the cluster.
664:            # children instead of emitting a duplicate outer part as a leaf.
740:        # appears later with the same label, prefer the duplicate that sits
745:            better_duplicate=next((candidate for candidate in
754:            if better_duplicate is not None:
1277:    # item.  In that case the two semantic owners overlap in y while remaining
1320:        local=ink.semantic[ya:yb+1,xa:xb+1]
1966:    def semantic_cut_before_anchor(pno,y_prev,anchor,owner_pair=None):
1971:        block before the child's marker block, then compare the two semantic
2002:        semantic_right=INK[pno].content_r
2022:            # preceding owner creates a false semantic collision.
2055:        upper=[w for w in page_words if CONTENT_L<=w[0]<=semantic_right
2059:        lower=[w for w in page_words if CONTENT_L<=w[0]<=semantic_right
2071:        # Images and vector diagrams are indivisible sem
… [3146 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 1960,2110p al_qp_splitter.py
```

<details><summary>result</summary>

```
        if require_separation:
            note_seam(pno,y_prev,y_next,owner_pair=owner_pair,
                      next_anchor=next_anchor)
            return (y_prev+y_next)/2
        s,e=runs[-1]
        return ink._p(a+(s+e)//2)
    def semantic_cut_before_anchor(pno,y_prev,anchor,owner_pair=None):
        """Separator between a known shared stem and its labelled child.

        Internal paragraph/diagram whitespace is not an ownership boundary.
        Use raw PDF content-flow block ids to include every fragmented maths
        block before the child's marker block, then compare the two semantic
        hulls.  If the hulls interleave vertically, register a 2-D seam.
        """
        token=f'({anchor["label"]})'
        page_words=W[pno]
        marker=[] if '_split_block' in anchor else [
            w for w in page_words if w[4]==token
            and abs(w[1]-anchor['y'])<4 and abs(w[0]-anchor['x'])<12]
        if '_split_block' in anchor:
            split_block=int(anchor['_split_block'])
            split_line=anchor.get('_split_line')
        elif marker:
            split_block=min(int(w[5]) for w in marker)
            split_line=min(int(w[6]) for w in marker
                           if int(w[5])==split_block)
        else:
            return boundary(pno,y_prev,anchor['y'],require_separation=True,
                            owner_pair=owner_pair,next_anchor=anchor)
        def aligned_child_mark(w):
            return ('_split_block' not in anchor and
   
… [6933 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "def boundary\|def note_seam\|-5\b\|- *5)" al_qp_splitter.py | head -40
```

<details><summary>result</summary>

```
883:        known_answer_border=any(page_y-5<=s<=page_y+22 for s in (known_stops or []))
1396:                            answer_word[1]-5<=word[1]<=row_bottom+4):
1892:    def note_seam(pno,y_prev,y_next,cut=None,next_anchor=None,owner_pair=None,
1911:    def boundary(pno,y_prev,y_next,require_separation=False,
2980:                      and d['rect'].x0>=CONTENT_L-5 and d['rect'].x1<=CONTENT_R+15]
2985:                       and d['rect'].x0>=CONTENT_L-5 and d['rect'].x1<=CONTENT_R+15
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 1880,1960p al_qp_splitter.py
```

<details><summary>result</summary>

```
        # Extend a crop's start UPWARD from the anchor's own text-row y to
        # catch inline content that is visually taller than one text line and
        # sits ABOVE the anchor's baseline on the SAME logical row -- a
        # multi-row column vector/matrix, a tall fraction, etc. (e.g.
        # "(a) (i) Show that AB x AV = -10(matrix)..." where the matrix's top
        # row renders well above the "(a)"/"(i)" token's own y). Safe because
        # `floor` is always the true end of whatever precedes this anchor
        # (previous mark-bottom, or the question-number row), and a genuinely
        # separate block is followed by a real blank-line gap that exceeds
        # the small contiguity tolerance, so the scan stops there rather than
        # bleeding into unrelated earlier content.
        return INK[pno].content_top(anchor_y, floor)
    def note_seam(pno,y_prev,y_next,cut=None,next_anchor=None,owner_pair=None,
                  split_block=None,split_line=None,upper_graphic_regions=None,
                  upper_graphic_word_regions=None):
        cut=float(cut if cut is not None else (y_prev+y_next)/2)
        for c in seam_candidates:
            if c['pno']==pno and abs(c['cut']-cut)<0.5:
                return
        nearby=[a for a in A[pno] if abs(a['y']-y_next)<4]
        anchor=next_anchor or (min(nearby,key=lambda a:abs(a['y']-y_next)) if nearby else None)
        seam_candidates.append({
            'pno':pno,'lo':float(y_prev),'hi':float(y_next),
   
… [3164 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "semantic_bounds_points\|def crop_start\|content_top\|AL_DEBUG\|environ.get('AL" al_qp_splitter.py | head -40
```

<details><summary>result</summary>

```
217:    def content_top(self,y,floor,thr=1):
1044:            if os.environ.get('AL_DEBUG_MARGIN'):
1093:                    if os.environ.get('AL_DRAFT'):
1127:                    if os.environ.get('AL_DEBUG_MASK'):
1878:    def top_before(pno,my,fl): return INK[pno].content_top(my,fl)-4
1891:        return INK[pno].content_top(anchor_y, floor)
2068:        if os.environ.get('AL_DEBUG_SEM'):
2476:                    if os.environ.get('AL_DRAFT'):
2484:                    if os.environ.get('AL_DRAFT'):
2572:                    if os.environ.get('AL_DEBUG_ROWS') and os.environ['AL_DEBUG_ROWS'] in lab:
2586:                dbg=os.environ.get('AL_DEBUG_ROWS')
2996:            if os.environ.get('AL_DEBUG_ORPHAN'):
3027:                        if os.environ.get('AL_DEBUG_ORPHAN'):
3031:                if os.environ.get('AL_DRAFT'):
3058:                if os.environ.get('AL_DRAFT'):
3248:            if os.environ.get('AL_DEBUG_ORPHAN'):
3300:                if os.environ.get('AL_DRAFT'):
3303:            if os.environ.get('AL_DEBUG_ORPHAN'):
3337:                    if os.environ.get('AL_DEBUG_ORPHAN'):
3350:                if os.environ.get('AL_DRAFT'):
3353:            if os.environ.get('AL_DEBUG_ORPHAN'):
3390:            if os.environ.get('AL_DEBUG_ORPHAN'):
4437:        if len(impossible) and os.environ.get('AL_DRAFT'):
4556:        if not options and os.environ.get('AL_DRAFT'):
4581:            if not os.environ.get('AL_DRAFT'):
4748:                if os.environ.get('AL_DRA
… [275 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 200,226p al_qp_splitter.py; sed -n 1860,1880p al_qp_splitter.py; grep -n "top_before\|crop_top(" al_qp_splitter.py | head -40
```

<details><summary>result</summary>

```
            wy0=max(0,int((word[1]-1)*SC)); wy1=min(pm.height,int((word[3]+1)*SC)+1)
            arr[wy0:wy1,wx0:wx1]=255
        self.gray=arr[:,xa:xb]
        # `dark` deliberately ignores pale watermarks for ordinary crop
        # extent detection.  `semantic` is stricter about visible glyph
        # antialiasing and is used only by ownership seams, where leaving even
        # a small cap of a neighbouring bracket is unacceptable.
        self.dark=self.gray<190
        self.semantic=self.gray<230
        self.ink=self.dark.sum(axis=1).astype(int)
        self.H=pm.height; self.W=self.dark.shape[1]
    def _r(self,y): return max(0,min(self.H-1,int(y*SC)))
    def _p(self,r): return r/SC
    def extent(self,y0,y1,thr=1):
        a,b=self._r(y0),self._r(y1); rows=np.where(self.ink[a:b+1]>=thr)[0]
        if len(rows)==0: return None,None
        return self._p(a+rows[0]), self._p(a+rows[-1])
    def content_top(self,y,floor,thr=1):
        r=self._r(y); f=self._r(floor); top=r; gap=0; i=r
        while i>f:
            if self.ink[i]>=thr: top=i; gap=0
            else:
                gap+=1
                if gap>=BIGGAP_PX: break
            i-=1
        return self._p(top)

        return fitz.Rect(
            min(rect.x0 for rect,_ in components),
            min(rect.y0 for rect,_ in components),
            max(rect.x1 for rect,_ in components),
            max(rect.y1 for rect,_ in components),
        )
    def prose_after_scaffold(pno,y0,y1):
        """First i
… [1025 more characters trimmed]
```
</details>

### Assistant — 2026-10-20 10:39:23

Tracing where the splitter sets a question's top so I can see why 16m-22 Q5's integral limit lands in Q4.ii.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "expand_top(\|hard_y0\b *=\|hard_y0=" al_qp_splitter.py | head; sed -n 4760,4860p al_qp_splitter.py
```

<details><summary>result</summary>

```
1879:    def expand_top(pno,anchor_y,floor):
3671:                            stem_start=expand_top(pno,P['y'],floor0)-PAD_PT
3704:                        stem_start=expand_top(pno,P['y'],floor0)-PAD_PT
3764:                                     expand_top(R['pno'],R['y'],
3774:                            r_start=expand_top(pno,P['y'],floor0)-PAD_PT
3785:                            expand_top(R['pno'],R['y'],prev_markbot)-PAD_PT,
3790:                                else expand_top(R['pno'],R['y'],HEADER_Y)-PAD_PT
3832:                    part_start=expand_top(pno,P['y'],floor0)-PAD_PT
3950:                       expand_top(child_pno,child['y'],
            y0=side(r0,a,b,True)
        r1=int(round(y1*k))
        if 0<=r1<len(inked) and inked[r1]:
            a,b=run(r1)
            y1=side(r1,a,b,False)
        return y0,y1

    def clean_edge_intruders(image,pno,rl,cy0,cy1):
        """White out glyph remnants of a NEIGHBOURING row at a crop edge.

        A word whose centre lies outside [cy0,cy1] but whose box crosses the
        edge can leave faint antialiased feet inside the crop ('[2]' of
        9702/52/F/M/17 Q2(d)(i) atop (d)(ii)).  Paint white the part of that
        word's box inside the crop -- only where no word or drawing of this
        crop shares that area.
        """
        pg=doc[pno]; k=DPI/72.0
        ws=[w for w in pg.get_text('words') if furniture_free(pg,w[:4])]
        own=[fitz.Rect(w[:4]) for w in ws if cy0<=(w[1]+w[3])/2<=cy1]
        drs=[d['
… [4424 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 3480,3560p al_qp_splitter.py
```

<details><summary>result</summary>

```
        next_q_pno=(seq[next_index]['pno'] if next_index<len(seq)
                    else doc.page_count)
        for cpno in range(pno+1,next_q_pno):
            page_text=' '.join(w[4] for w in W[cpno])
            if not re.search(fr'Question\s+{re.escape(str(qn))}\s+continued',
                             page_text,re.I):
                continue
            floor=continued_floor(cpno,FOOTER_Y)
            tail=min(first_stop(cpno,floor),continued_tail(cpno,floor))
            if not segment_has_content(cpno,floor,tail):
                continue
            emits.append((label,cpno,floor,tail))
            # The supplied graph may sit inside a large answer-area frame.
            # Keep the mathematical diagram but mask only that outer frame;
            # dotted working rows and the lower answer box are already beyond
            # `tail` because they are stop rows.
            for drawing in doc[cpno].get_drawings():
                rect=drawing.get('rect')
                if (rect and rect.width>(CONTENT_R-CONTENT_L)*0.85 and
                        rect.height>60 and floor-10<=rect.y0 and
                        rect.y1<=tail+10):
                    continuation_frame_masks.setdefault(cpno,[]).append(rect)

    for qi in range(len(q_idx)-1):
        question_emit_start=len(emits)
        grp=seq[q_idx[qi]:q_idx[qi+1]]; qn=grp[0]['label']; qpno=grp[0]['pno']; qbot=grp[0]['row_y1']
        next_q_anchor=seq[q_idx[qi+1]] if q_idx[qi+1]<len(seq) else None
        # qlo
… [3466 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 3975,4200p al_qp_splitter.py
```

<details><summary>result</summary>

```
    # Consecutive answerable leaves can also contain interleaved stacked
    # formulae (not only stem/child pairs).  The initial emit windows may then
    # overlap because the next leaf's tall maths rises above its label row.
    # Rebuild every such boundary from semantic PDF block ownership and give
    # both owners one shared cut.  If their true hulls interleave, the helper
    # registers the same fail-closed 2-D seam used for stems.
    def output_anchor(label,pno,y0,y1):
        pieces=label.split('.')
        is_stem=pieces[-1:] == ['stem']
        if is_stem:
            if not IS_IGCSE:
                return None
            pieces=pieces[:-1]
        qnum=pieces[0][1:] if pieces and pieces[0].startswith('Q') else None
        if len(pieces)==1:
            kind,target='Q',qnum
        elif len(pieces)>=4:
            kind,target='SUBPART',pieces[-1]
        elif len(pieces)>=3:
            kind,target='ROMAN',pieces[-1]
        else:
            kind,target='PART',pieces[-1]
        candidates=[a for a in A[pno] if a['kind']==kind and a['label']==target
                    and y0-14<=a['y']<=y1+14]
        if not candidates: return None
        return min(candidates,key=lambda a:abs(a['y']-max(y0,a['y'] if a['y']>=y0 else y0)))

    def output_owner_start(label,pno,y0,y1):
        """Semantic start descriptor for the right-hand output at a seam.

        Answerable leaves start at a printed marker, so their marker block is
        authoritative.  A `.stem` start
… [10144 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 1,144p al_run_papers.py | grep -n "splitter\|verify\|argv\|subprocess" | head -30
```

<details><summary>result</summary>

```
5:  1. al_qp_splitter.py     -> splits/<run>/<PREFIX>/   (+ provenance JSON)
6:  2. al_verify_leaves.py   -> exact leaf set vs the printed markers
7:  3. al_verify_coverage.py -> every question word in exactly one crop and
13:the source exists, the splitter wrote crops + provenance, the leaf gate
27:import subprocess
48:    p = subprocess.run(cmd, capture_output=True, text=True)
72:    splitter = "al_mcq_splitter.py" if mcq else "al_qp_splitter.py"
73:    rc, log = run([PY, "-I", str(HERE / splitter), str(src), str(out), prefix])
74:    (out / "splitter.log").write_text(log)
78:        row["reason"] = "splitter: " + (log.strip().splitlines() or ["no output"])[-1][:200]
80:    rc1, l1 = run([PY, "-I", str(HERE / "al_verify_leaves.py"), str(src), str(out), prefix])
81:    rc2, l2 = run([PY, "-I", str(HERE / "al_verify_coverage.py"), str(src), str(out), prefix])
110:    for script in ("al_qp_splitter.py", "al_mcq_splitter.py", "al_verify_leaves.py", "al_verify_coverage.py", "al_contact_sheet.py"):
116:    with ThreadPoolExecutor(a.workers) as pool:   # each paper runs in its own subprocesses
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; SPLITTER_DEBUG_EMITS=Q ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_m16_qp_22.pdf $S/t1 AL-MTH-16m-22-QP 2>&1 | grep -E "Q4|Q5|Q6" | head
```

<details><summary>result</summary>

```
DEBUG_EMIT ('Q4.stem', 1, 190.39942932128906, 261.5014343261719)
DEBUG_EMIT ('Q4.i', 1, 261.5014343261719, np.float64(299.52))
DEBUG_EMIT ('Q4.ii', 1, 300.71999999999997, 352.3593444824219)
DEBUG_EMIT ('Q5', 1, 347.3593444824219, np.float64(378.08))
DEBUG_EMIT ('Q6.stem', 1, 409.3778381347656, 553.4371032714844)
DEBUG_EMIT ('Q6.i', 1, 553.4371032714844, np.float64(576.4799999999999))
DEBUG_EMIT ('Q6.ii', 1, 577.68, 623.439208984375)
   Q4.stem
   Q4.i
   Q4.ii
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv,collections,re
r=[x for x in csv.DictReader(open('review/mth_b1/run_summary.csv')) if x['status']=='HOLD' and 'coverage' in x['reason']]
kinds=collections.Counter()
for x in r[:400]:
  g=open('splits/mth_b1/'+x['prefix']+'/gates.log').read()
  for l in g.splitlines():
    l=l.strip()
    m=re.match(r'(SLICED-BOUNDARY|DUPLICATE|MISSING|BLANK-BAND|FURNITURE-IN-CROP|PLAIN-DOTTED-LINE-IN-CROP|FIGURE-OWNED-LATER)',l)
    if m: kinds[m.group(1)]+=1
    if 'SLICED' in l and ('blank' in l or 'plain' in l or 'figure' in l or 'furniture' in l or 'x=' in l): kinds['sl:'+l.split(\"'\")[1]]+=1
print(kinds)
"

```

<details><summary>result</summary>

```
Counter({'DUPLICATE': 567, 'SLICED-BOUNDARY': 402, 'MISSING': 349, 'BLANK-BAND': 8, 'sl:blank': 8, 'FURNITURE-IN-CROP': 2})
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:40:01

Classifying the 166 coverage holds by pattern (cross-question vs within-question overlap) to pick the biggest generic fix.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv,collections,re,ast
r=[x for x in csv.DictReader(open('review/mth_b1/run_summary.csv')) if x['status']=='HOLD' and 'coverage' in x['reason']]
pp=collections.Counter(); ex={}
for x in r:
  g=open('splits/mth_b1/'+x['prefix']+'/gates.log').read()
  kinds=set()
  for l in g.splitlines():
    l=l.strip()
    if l.startswith('DUPLICATE'):
      t=ast.literal_eval(l[len('DUPLICATE'):].strip())
      labs=t[3]; q=set(a.split('.')[0] for a in labs)
      k='dup-crossQ' if len(q)>1 else 'dup-sameQ'
      kinds.add(k)
    if l.startswith('MISSING'):
      kinds.add('missing')
  pp[tuple(sorted(kinds))]+=1; ex.setdefault(tuple(sorted(kinds)),[]).append(x['prefix'])
for k,v in pp.most_common(): print(v,k,ex[k][:6])
"

```

<details><summary>result</summary>

```
59 ('dup-crossQ',) ['AL-MTH-16m-12-QP', 'AL-MTH-16m-22-QP', 'AL-MTH-02s-11-QP', 'AL-MTH-03s-11-QP', 'AL-MTH-03s-31-QP', 'AL-MTH-04s-31-QP']
53 () ['AL-MTH-22m-52-QP', 'AL-MTH-03s-21-QP', 'AL-MTH-04s-21-QP', 'AL-MTH-06s-11-QP', 'AL-MTH-06s-21-QP', 'AL-MTH-07s-21-QP']
31 ('missing',) ['AL-MTH-17m-12-QP', 'AL-MTH-17m-72-QP', 'AL-MTH-20m-12-QP', 'AL-MTH-21m-32-QP', 'AL-MTH-23m-12-QP', 'AL-MTH-23m-42-QP']
12 ('dup-crossQ', 'missing') ['AL-MTH-06s-31-QP', 'AL-MTH-11s-32-QP', 'AL-MTH-12s-12-QP', 'AL-MTH-13s-11-QP', 'AL-MTH-15s-12-QP', 'AL-MTH-05w-31-QP']
6 ('dup-sameQ',) ['AL-MTH-25m-22-QP', 'AL-MTH-25s-33-QP', 'AL-MTH-14w-51-QP', 'AL-MTH-14w-52-QP', 'AL-MTH-19w-33-QP', 'AL-MTH-22w-31-QP']
5 ('dup-sameQ', 'missing') ['AL-MTH-25m-12-QP', 'AL-MTH-18s-31-QP', 'AL-MTH-22s-31-QP', 'AL-MTH-22s-33-QP', 'AL-MTH-17w-32-QP']
5 ('dup-crossQ', 'dup-sameQ', 'missing') ['AL-MTH-07s-31-QP', 'AL-MTH-12s-33-QP', 'AL-MTH-15s-32-QP', 'AL-MTH-16s-33-QP', 'AL-MTH-09w-32-QP']
3 ('dup-crossQ', 'dup-sameQ') ['AL-MTH-16m-32-QP', 'AL-MTH-11s-31-QP', 'AL-MTH-16w-33-QP']
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b1; for p in AL-MTH-22m-52-QP AL-MTH-03s-21-QP AL-MTH-04s-21-QP AL-MTH-06s-11-QP AL-MTH-07s-21-QP; do echo "== $p"; grep -v "^expected" $p/gates.log | head -8; done
```

<details><summary>result</summary>

```
== AL-MTH-22m-52-QP
  BLANK-BAND ('Q3.a', 63)
  SLICED-BOUNDARY ('blank', 'Q3.a', 63)
pages 3-11: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
== AL-MTH-03s-21-QP
  SLICED-BOUNDARY (2, 'Q1', 107.4, 8)
pages 2-3: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
== AL-MTH-04s-21-QP
  SLICED-BOUNDARY (2, 'Q2.ii', 278.2, 7)
pages 2-3: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
== AL-MTH-06s-11-QP
  SLICED-BOUNDARY (2, 'Q3.ii', 297.1, 4)
pages 2-4: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
== AL-MTH-07s-21-QP
  SLICED-BOUNDARY (2, 'Q1', 106.1, 21)
  SLICED-BOUNDARY (2, 'Q3.ii', 370.6, 7)
pages 2-3: missing=0 duplicated=0 sliced_boundaries=2 answer_row_words=1 (in a crop: 1)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; mkdir -p $S/bin; cat > $S/bin/show.py <<'EOF'
# show.py RUN PREFIX PAGE Y [H] -> renders page region with crop rects drawn, prints crops near Y
import sys,json,pymupdf as fitz
from pathlib import Path
run,prefix,pno,y=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]); h=float(sys.argv[5]) if len(sys.argv)>5 else 60
base=Path.home()/'rootatom_data/ALEVEL/splits'/run/prefix
d=json.load(open(base/f'{prefix}-split-provenance.json'))
doc=fitz.open(d['source_pdf']); pg=doc[pno-1]
cols=[(1,0,0),(0,0,1),(0,.6,0),(.8,0,.8),(0,.6,.6)]
i=0
for lab,segs in d['outputs'].items():
    for s in segs:
        if s['pdf_page']==pno and s['clip_points'][3]>y-h and s['clip_points'][1]<y+h:
            r=fitz.Rect(s['clip_points']); c=cols[i%5]; i+=1
            pg.draw_rect(r+(i*2,0,-i*2,0),color=c,width=0.6)
            pg.insert_text((r.x1-60-i*30,r.y0+8),lab,fontsize=6,color=c)
            print(lab,s['clip_points'],s['semantic_bounds_points'])
out=Path(sys.argv[0]).parent.parent/'show.png'
pg.get_pixmap(dpi=130,clip=fitz.Rect(0,max(0,y-h),595,y+h)).save(out); print(out)
EOF
cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_b1 AL-MTH-03s-21-QP 2 107.4 50
```

<details><summary>result</summary>

```
Q1 [40.0, 60.98, 560.0, 107.38] [60.98, 107.38]
Q2.stem [40.0, 102.38, 560.0, 124.08] [102.38, 125.71]
Q2.i [40.0, 128.4, 560.0, 173.52] [125.71, 176.37]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/show.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "def maths_figures_above_context" al_qp_splitter.py; sed -n "$(grep -n 'def maths_figures_above_context' al_qp_splitter.py | cut -d: -f1),+75p" al_qp_splitter.py
```

<details><summary>result</summary>

```
3358:    def maths_figures_above_context(emits):
    def maths_figures_above_context(emits):
        """Maths: content printed after the previous part's answer lines / mark
        and above the next crop belongs to that crop: context prose ('The line
        l2 has equation ...', 9709/32/M/J/24 Q8) with any diagram above it, or an
        uncaptioned diagram above a crop that opens with context prose ('The
        diagram shows the graph of y = g(x) ...', 9709/12/M/J/24 Q4).  Ink alone
        above a crop that opens with its own label is left alone (blank axes
        after '(a) Sketch ... [3]' are (a)'s answer space)."""
        out=list(emits)
        for i,(lab,p,y0,y1) in enumerate(out):
            prev=[(j,e) for j,e in enumerate(out) if j!=i and e[1]==p and e[2]<y0-1]
            if not prev:
                continue
            j,pe=max(prev,key=lambda t:t[1][2])
            first=sorted([w for w in W[p] if y0-1<=w[1]<=y0+12 and re.search(r'\w',w[4])],key=lambda w:w[0])
            if not first:
                continue
            opens_with_label=bool(re.fullmatch(r'\([a-z]{1,4}\)|\d{1,2}',first[0][4]))
            ar=AR_CACHE.get(p,[])
            ends=[r['y1'] for r in ar if pe[2]<r['y1']<y0]+[w[3] for w in W[p] if pe[2]<w[1]<y0 and MARK_RE.match(w[4])]
            if not ends:
                continue
            a=max(ends)+1
            # context prose in the gap ('The line l2 has equation r = ...' between
            # (a)'s answer lines and (b), 9709/32/M/J
… [2773 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "A\[pno\]\s*=\|A=\|A\[p\]\.append\|'row_y1'" al_qp_splitter.py | head -20
```

<details><summary>result</summary>

```
431:                            'row_y1':max(w[3] for w in visual_row),'x':x0,
451:                                'y':left[1],'row_y1':ry1,'x':x0})
460:                                'y':left[1],'row_y1':ry1,'x':x0})
461:            elif m and x0<PART_X_MAX and len(m.group(1))==1 and not (m.group(1) in ROMANS and x0>=ROMAN_X_MIN): anchors.append({'kind':'PART','label':m.group(1),'y':left[1],'row_y1':ry1,'x':x0})
466:                                'y':left[1],'row_y1':ry1,'x':x0})
475:                    anchors.append({'kind':'ROMAN','label':m.group(1),'y':left[1],'row_y1':ry1,'x':x0})
485:                                'row_y1':max(w[3] for w in ws),'x':t[0]})
497:                anchors.append({'kind':'ROMAN','label':mm.group(1),'y':t[1],'row_y1':max(w[3] for w in ws),'x':t[0]})
504:                anchors.append({'kind':'PART','label':mm.group(1),'y':t[1],'row_y1':max(w[3] for w in ws),'x':t[0]})
511:                                'y':t[1],'row_y1':max(w[3] for w in ws),'x':t[0]})
1273:    for pno in A: A[pno]=[x for x in seq if x['pno']==pno]
3505:        grp=seq[q_idx[qi]:q_idx[qi+1]]; qn=grp[0]['label']; qpno=grp[0]['pno']; qbot=grp[0]['row_y1']
3512:        qlook=grp[0]['row_y1']
3655:                                    pno,P.get('row_y1',P['y']),parent_tail))
3810:                    prev_anchor_bot=R.get('row_y1',R['y'])
3866:                prev_anchor_bot=P.get('row_y1',P['y'])
3928:                parent_pno,parent_anchor.get('row_y1',parent_anchor['y']),
She
… [130 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "^    W=\|    W\[\|W={}\|def first_stop\|def orphan_prose" al_qp_splitter.py | head; sed -n 1268,1276p al_qp_splitter.py
```

<details><summary>result</summary>

```
841:    W=pix.width; H=pix.height
1407:    def first_stop(pno,y):
3122:    def orphan_prose(p,lo,hi,ar):
4113:    SMALL_DRAW={}     # small vector symbols per page (answer_rows)
            print(
                'KEPT_ANCHOR',anchor['pno']+1,anchor['kind'],
                anchor['label'],round(anchor['x'],2),round(anchor['y'],2),
                file=sys.stderr,
            )
    for pno in A: A[pno]=[x for x in seq if x['pno']==pno]

    # A horizontal cut is normally ideal, but typeset mathematics can place a
    # tall expression from the next item above the bottom of the preceding
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "W\[pno\]=\|W\[p\]=\|W=\[\|W=dict\|W = " al_qp_splitter.py | head; grep -n "W\[" al_qp_splitter.py | head -3
```

<details><summary>result</summary>

```
2409:                SMALL_DRAW[pno]=[r for r in allr if 2<r.width<=40 and r.height<=10
1214:        A[pno],M[pno],S[pno],W[pno],DOT[pno]=a,m,s,w,dot
1439:        for answer_word in W[pno]:
1458:                for mark_word in W[pno]:
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:41:29

Now adding the pass (IS_MATHS-gated, runs after the existing maths pass).

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "            out[i]=(lab,p,rt-2,y1)\n            if pe[3]>rt-3:\n                out[j]=(pe[0],pe[1],pe[2],rt-3)\n        return out\n", "new_string": "            out[i]=(lab,p,rt-2,y1)\n            if pe[3]>rt-3:\n                out[j]=(pe[0],pe[1],pe[2],rt-3)\n        return out\n\n    def maths_raised_question_rows(emits):\n        \"\"\"Maths: a question's first row can rise above its number -- an\n        integral's upper limit, a superscript, a stacked numerator ('5 Given\n        that integral_0^a 6e^(2x+1) dx = 65', 9709/22/F/M/16).  The previous\n        question's last crop ended at the number's row and this one started\n        PAD_PT above it, so that ink was sliced or printed in both crops.  Cut\n        both in the white run above the row's ink instead.\"\"\"\n        out=list(emits)\n        for p,anchors in A.items():\n            for q in anchors:\n                if q['kind']!='Q':\n                    continue\n                ay=q['y']; top=ay\n                while True:          # words overlapping the number's row, transitively\n                    up=[w[1] for w in W[p] if CONTENT_L<=w[0]<=CONTENT_R\n                        and ay-30<w[1]<top and w[3]>top+1.5]\n                    if not up or min(up)>=top:\n                        break\n                    top=min(up)\n                ink=INK[p]\n                rt,_=ink.extent(top,q.get('row_y1',ay+10))\n                if rt is None:\n                    continue\n                r=ink._r(rt); lo=ink._r(ay-30)\n                while r>lo and ink.ink[r-1]>0:\n                    r-=1\n                rt=ink._p(r)\n                if rt>=ay-PAD_PT+1:\n                    continue         # nothing above the usual start\n                mine=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]==f\"Q{q['label']}\"\n                      and ay-PAD_PT-2<=e[2]<=ay+1]\n                prev=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]!=f\"Q{q['label']}\"\n                      and e[2]<rt-2 and e[3]>rt-2]\n                if not mine or not prev:\n                    continue\n                cut=boundary(p,max(out[i][2] for i in prev),rt)\n                if not (rt-PAD_PT-8<=cut<rt):\n                    continue         # no white run just above the row: leave it to the gate\n                if os.environ.get('AL_DEBUG_ORPHAN'):\n                    print('MATHS-RAISED-ROW',p+1,q['label'],round(rt,1),round(cut,1),file=sys.stderr)\n                for i in mine:\n                    out[i]=(out[i][0],p,cut,out[i][3])\n                for i in prev:\n                    out[i]=(out[i][0],p,out[i][2],min(out[i][3],cut))\n        return out\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "            emits=maths_figures_above_context(emits)\n", "new_string": "            emits=maths_figures_above_context(emits)\n            emits=maths_raised_question_rows(emits)\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 84,144p al_run_papers.py
```

<details><summary>result</summary>

```
    if not os.environ.get("AL_NO_SHEETS"):   # regression runs: sheets made later, only for changed papers
        run([PY, "-I", str(HERE / "al_contact_sheet.py"), str(out), prefix, str(rev_root / prefix),
             "--per", "9", "--width", "1000"])
    (out / "gates.log").write_text(l1 + "\n" + l2)
    leaves_ok = rc1 == 0 and bool(LEAF_OK.match(row["leaves"]))
    cov_ok = rc2 == 0 and bool(COV_OK.match(row["coverage"]))
    if leaves_ok and cov_ok:
        row["status"] = "PASS"
    else:
        row["reason"] = ("leaves " if not leaves_ok else "") + ("coverage" if not cov_ok else "")
    return row


def main() -> int:
    import argparse
    from concurrent.futures import ThreadPoolExecutor, as_completed
    ap = argparse.ArgumentParser()
    ap.add_argument("run_name")
    ap.add_argument("names", nargs="*")
    ap.add_argument("--list", help="file with one source name per line")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--no-sheets", action="store_true", help="skip contact sheets (regression runs)")
    a = ap.parse_args()
    if a.no_sheets:
        os.environ["AL_NO_SHEETS"] = "1"
    names = list(a.names) + ([l.strip() for l in open(a.list) if l.strip()] if a.list else [])
    for script in ("al_qp_splitter.py", "al_mcq_splitter.py", "al_verify_leaves.py", "al_verify_coverage.py", "al_contact_sheet.py"):
        if (HERE / script).stat().st_size < 500:
            raise SystemExit(f"refusing to run: {script} looks empty/unreadabl
… [1760 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; sysctl -n hw.ncpu; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('review/mth_b1/run_summary.csv')))
open('review/mth/holds_b1.txt','w').write(''.join(x['source']+'\n' for x in r if x['status']=='HOLD'))
open('review/mth/holds_cov.txt','w').write(''.join(x['source']+'\n' for x in r if x['status']=='HOLD' and x['reason'].strip()=='coverage'))
open('review/mth/pass_b1.txt','w').write(''.join(x['source']+'\n' for x in r if x['status']=='PASS'))
"; wc -l review/mth/holds_*.txt; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_m16_qp_22.pdf 9709_s03_qp_2.pdf --no-sheets 2>&1 | tail -3
```

<details><summary>result</summary>

```
10
     251 review/mth/holds_b1.txt
     166 review/mth/holds_cov.txt
     417 total
[1/2] HOLD 9709_m16_qp_22.pdf crops=17 coverage
[2/2] HOLD 9709_s03_qp_2.pdf crops=20 coverage
this run: PASS 0 / 2; run total PASS 0 / 2
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; cat AL-MTH-16m-22-QP/gates.log; grep -i "RAISED" AL-MTH-16m-22-QP/splitter.log; cat AL-MTH-03s-21-QP/gates.log 2>/dev/null | tail -3; ls
```

<details><summary>result</summary>

```
expected=13 produced=13 missing=[] extra=[]
  SLICED-BOUNDARY (2, 'Q6.ii', 623.4, 10)
pages 2-3: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)MATHS-RAISED-ROW 2 5 346.1 332.2
expected=16 produced=16 missing=[] extra=[]
  SLICED-BOUNDARY (2, 'Q1', 107.4, 8)
pages 2-3: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)AL-MTH-03s-21-QP
AL-MTH-16m-22-QP
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-16m-22-QP 2 623 40; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_m16_qp_22.pdf')
for w in d[1].get_text('words'):
  if 600<w[1]<640: print([round(v,1) if isinstance(v,float) else v for v in w])
"
```

<details><summary>result</summary>

```
Q6.ii [40.0, 579.12, 560.0, 623.44] [577.68, 623.44]
Q7.stem [40.0, 618.44, 560.0, 640.56] [618.44, 644.88]
Q7.i [40.0, 644.88, 560.0, 677.52] [644.88, 678.72]
show.png
[49.3, 623.4, 55.2, 634.8, '7', 28, 0, 0]
[72.8, 624.0, 91.2, 635.3, 'The', 28, 1, 0]
[94.1, 624.0, 134.4, 635.3, 'equation', 28, 1, 1]
[137.3, 624.0, 146.7, 635.3, 'of', 28, 1, 2]
[149.8, 624.0, 155.0, 635.3, 'a', 28, 1, 3]
[157.9, 624.0, 183.8, 635.3, 'curve', 28, 1, 4]
[186.6, 624.0, 194.4, 635.3, 'is', 28, 1, 5]
[197.4, 621.9, 213.1, 635.4, '2x3', 28, 1, 6]
[216.0, 618.0, 222.9, 641.7, '+', 28, 1, 7]
[225.2, 621.9, 235.1, 635.4, 'y3', 28, 1, 8]
[238.6, 618.0, 245.4, 641.7, '=', 28, 1, 9]
[248.5, 624.0, 263.2, 635.3, '24.', 28, 1, 10]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                rt=ink._p(r)
                if rt>=ay-PAD_PT+1:
                    continue         # nothing above the usual start
                mine=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]==f"Q{q['label']}"
                      and ay-PAD_PT-2<=e[2]<=ay+1]
                prev=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]!=f"Q{q['label']}"
                      and e[2]<rt-2 and e[3]>rt-2]
                if not mine or not prev:
                    continue
"""
new="""                rt=ink._p(r)
                mine=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]==f"Q{q['label']}"
                      and ay-PAD_PT-2<=e[2]<=ay+1]
                prev=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]!=f"Q{q['label']}"
                      and e[2]<rt-2 and e[3]>rt-2]
                if not mine or not prev:
                    continue
                if rt>=ay-PAD_PT+1 and all(out[i][3]<=rt-1 for i in prev):
                    continue         # nothing above the usual start
"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_m16_qp_22.pdf 9709_s03_qp_2.pdf --no-sheets 2>&1 | tail -3; cd ~/rootatom_data/ALEVEL/splits/mth_t; grep RAISED */splitter.log; tail -2 */gates.log
```

<details><summary>result</summary>

```
[1/2] HOLD 9709_m16_qp_22.pdf crops=17 coverage
[2/2] HOLD 9709_s03_qp_2.pdf crops=20 coverage
this run: PASS 0 / 2; run total PASS 0 / 2
AL-MTH-16m-22-QP/splitter.log:MATHS-RAISED-ROW 2 5 346.1 332.2
==> AL-MTH-03s-21-QP/gates.log <==
  SLICED-BOUNDARY (2, 'Q1', 107.4, 8)
pages 2-3: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
==> AL-MTH-16m-22-QP/gates.log <==
  SLICED-BOUNDARY (2, 'Q6.ii', 623.4, 10)
pages 2-3: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:42:14

Fix works for 16m-22 Q5; debugging why two other question boundaries (16m-22 Q7, 03s-21 Q2) aren't caught.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; sed 's/                mine=\[i for i,e in enumerate(out) if e\[1\]==p and e\[0\].split/                print("DBG",p+1,q["label"],round(ay,1),round(top,1),round(rt,1),[e for e in out if e[1]==p and abs(e[2]-ay)<60],file=sys.stderr)\n&/' al_qp_splitter.py > $S/dbg_splitter.py; cp fused_marks.py barcode_rule.py $S/ 2>/dev/null; ~/.venvs/alevel/bin/python -I $S/dbg_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_m16_qp_22.pdf $S/t2 AL-MTH-16m-22-QP 2>&1 | grep DBG | grep "^DBG 2 7"; ~/.venvs/alevel/bin/python -I $S/dbg_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s03_qp_2.pdf $S/t2 AL-MTH-03s-21-QP 2>&1 | grep "^DBG 2 2"
```

<details><summary>result</summary>

```
DBG 2 7 623.4 618.0 623.0 [('Q6.ii', 1, 577.68, 623.439208984375), ('Q7.stem', 1, 618.439208984375, 644.8754577636719), ('Q7.i', 1, 644.8754577636719, np.float64(678.7199999999999)), ('Q7.ii', 1, 679.4399999999999, 705.3779907226562)]
DBG 2 2 107.4 105.0 106.1 [('Q1', 1, 60.98347473144531, 107.38252258300781), ('Q2.stem', 1, 102.38252258300781, 125.70516204833984), ('Q2.i', 1, 125.70516204833984, 176.3662567138672)]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; sed -i '' 's/                if not (rt-PAD_PT-8<=cut<rt):/                print("CUT",p+1,q["label"],cut,file=sys.stderr)\n&/' $S/dbg_splitter.py; ~/.venvs/alevel/bin/python -I $S/dbg_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_m16_qp_22.pdf $S/t2 AL-MTH-16m-22-QP 2>&1 | grep "^CUT"; ~/.venvs/alevel/bin/python -I $S/dbg_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s03_qp_2.pdf $S/t2 AL-MTH-03s-21-QP 2>&1 | grep "^CUT"
```

<details><summary>result</summary>

```
CUT 2 5 332.15999999999997
CUT 2 7 608.64
CUT 2 2 91.67999999999999
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                cut=boundary(p,max(out[i][2] for i in prev),rt)
                if not (rt-PAD_PT-8<=cut<rt):
                    continue         # no white run just above the row: leave it to the gate
"""
new="""                cut=boundary(p,max(out[i][2] for i in prev),rt)
                if not cut<rt or ink.ink[ink._r(cut):ink._r(rt)].any():
                    continue         # no white run just above the row: leave it to the gate
                cut=max(cut,rt-PAD_PT)   # still inside that white run
"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_m16_qp_22.pdf 9709_s03_qp_2.pdf --no-sheets 2>&1 | tail -3; cd ~/rootatom_data/ALEVEL/splits/mth_t; grep RAISED */splitter.log; tail -2 */gates.log
```

<details><summary>result</summary>

```
[1/2] PASS 9709_m16_qp_22.pdf crops=17 
[2/2] PASS 9709_s03_qp_2.pdf crops=20 
this run: PASS 2 / 2; run total PASS 2 / 2
AL-MTH-03s-21-QP/splitter.log:MATHS-RAISED-ROW 2 2 106.1 100.1
AL-MTH-16m-22-QP/splitter.log:MATHS-RAISED-ROW 2 5 346.1 340.1
AL-MTH-16m-22-QP/splitter.log:MATHS-RAISED-ROW 2 7 623.0 617.0
==> AL-MTH-03s-21-QP/gates.log <==
expected=16 produced=16 missing=[] extra=[]
pages 2-3: missing=0 duplicated=0 sliced_boundaries=0 answer_row_words=0 (in a crop: 0)
==> AL-MTH-16m-22-QP/gates.log <==
expected=13 produced=13 missing=[] extra=[]
pages 2-3: missing=0 duplicated=0 sliced_boundaries=0 answer_row_words=0 (in a crop: 0)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:42:44

Both now pass. Viewing the changed crops before running all 166 coverage holds.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits/mth_t; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
fs=['AL-MTH-16m-22-QP/AL-MTH-16m-22-QP-Q4.ii.png','AL-MTH-16m-22-QP/AL-MTH-16m-22-QP-Q5.png','AL-MTH-16m-22-QP/AL-MTH-16m-22-QP-Q6.ii.png','AL-MTH-16m-22-QP/AL-MTH-16m-22-QP-Q7.stem.png','AL-MTH-03s-21-QP/AL-MTH-03s-21-QP-Q1.png','AL-MTH-03s-21-QP/AL-MTH-03s-21-QP-Q2.stem.png']
ims=[Image.open(f) for f in fs]; W=max(i.width for i in ims); H=sum(i.height+20 for i in ims)
c=Image.new('RGB',(W,H),(200,200,200)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+20
c.save('$S/v1.png')"
```

<details><summary>result</summary>

```
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/v1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 10:42:53

Crops are clean. Running all 166 coverage holds in a scratch run (mth_t).

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_t ~/rootatom_data/ALEVEL/review/mth_t; time ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_cov.txt --no-sheets --workers 8 2>&1 | tail -2
```

<details><summary>result</summary>

```
[166/166] HOLD 9709_w23_qp_13.pdf crops=35 coverage
this run: PASS 67 / 166; run total PASS 67 / 166
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list  --no-sheets  8 2  473.91s user 86.48s system 690% cpu 1:21.16 total
tail -2  0.00s user 0.00s system 0% cpu 1:21.16 total
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:44:18

67 of 166 coverage holds now pass (81 s per run). Classifying the remaining 99.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cat > $S/bin/cls.py <<'EOF'
import csv,collections,re,ast,sys
from pathlib import Path
run=sys.argv[1]; R=Path.home()/'rootatom_data/ALEVEL'
r=[x for x in csv.DictReader(open(R/f'review/{run}/run_summary.csv')) if x['status']=='HOLD']
pp=collections.Counter(); ex={}
for x in r:
  if 'splitter' in x['reason']: k=('REVIEW',); 
  else:
    g=open(R/f'splits/{run}/'+x['prefix']+'/gates.log').read()
    kinds=set()
    for l in g.splitlines():
      l=l.strip()
      if l.startswith('DUPLICATE'):
        t=ast.literal_eval(l[len('DUPLICATE'):].strip()); q=set(a.split('.')[0] for a in t[3])
        kinds.add('dupX' if len(q)>1 else 'dupS')
      elif l.startswith('MISSING'): kinds.add('miss')
      elif l.startswith('BLANK-BAND'): kinds.add('blank')
      elif l.startswith('SLICED-BOUNDARY') and 'blank' not in l: kinds.add('slice')
      elif l.startswith(('FURNITURE','PLAIN','FIGURE')): kinds.add(l.split()[0])
    if x['reason'].startswith('leaves'): kinds.add('LEAVES')
    k=tuple(sorted(kinds))
  pp[k]+=1; ex.setdefault(k,[]).append(x['prefix'][7:-3])
for k,v in pp.most_common(): print(v,k,' '.join(ex[k][:10]))
EOF
~/.venvs/alevel/bin/python -I $S/bin/cls.py mth_t
```

<details><summary>result</summary>

```
Exit code 1
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/cls.py", line 9, in <module>
    g=open(R/f'splits/{run}/'+x['prefix']+'/gates.log').read()
           ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~
TypeError: unsupported operand type(s) for +: 'PosixPath' and 'str'
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; sed -i '' "s|open(R/f'splits/{run}/'+x\['prefix'\]+'/gates.log')|open(R/f'splits/{run}'/x['prefix']/'gates.log')|" $S/bin/cls.py; ~/.venvs/alevel/bin/python -I $S/bin/cls.py mth_t
```

<details><summary>result</summary>

```
28 ('miss',) 17m-12 20m-12 21m-32 23m-12 23m-42 11s-53 14s-32 15s-11 18s-12 18s-41
19 ('dupX', 'slice') 02s-11 03s-11 05s-21 09s-31 10s-11 10s-21 10s-22 10s-23 10s-31 12s-12
16 ('slice',) 11s-21 14s-22 14s-23 23s-11 25s-12 25s-15 09w-52 10w-23 11w-51 11w-52
9 ('dupS', 'miss', 'slice') 25m-12 07s-31 12s-33 15s-32 16s-33 18s-31 22s-31 22s-33 17w-32
9 ('dupX', 'miss', 'slice') 06s-31 10s-13 11s-32 13s-11 15s-12 05w-31 09w-22 13w-33 14w-22
8 ('blank',) 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52
7 ('dupS',) 16m-32 25m-22 11s-31 25s-33 14w-51 14w-52 22w-31
1 ('FURNITURE-IN-CROP', 'dupX', 'slice') 14s-13
1 ('dupS', 'dupX', 'miss', 'slice') 09w-32
1 ('dupS', 'slice') 19w-33
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 02s-11 03s-11 05s-21 10s-11; do echo "== $p"; grep -v "^expected" AL-MTH-$p-QP/gates.log | head -6; grep RAISED AL-MTH-$p-QP/splitter.log; done
```

<details><summary>result</summary>

```
Exit code 1
== 02s-11
  SLICED-BOUNDARY (2, 'Q1', 124.8, 32)
  DUPLICATE (2, 117, '1', ['Q1', 'Q2.i'])
  DUPLICATE (2, 115, 'cos2', ['Q1', 'Q2.i'])
  DUPLICATE (2, 117, 'x', ['Q1', 'Q2.i'])
pages 2-5: missing=0 duplicated=3 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
== 03s-11
  SLICED-BOUNDARY (2, 'Q2', 170.8, 7)
  DUPLICATE (2, 163, '6', ['Q2', 'Q3.a'])
pages 2-3: missing=0 duplicated=1 sliced_boundaries=1 answer_row_words=1 (in a crop: 1)
== 05s-21
  SLICED-BOUNDARY (2, 'Q4.ii', 484.0, 18)
  DUPLICATE (2, 477, '1', ['Q4.ii', 'Q5.i'])
  DUPLICATE (2, 476, 'dy', ['Q4.ii', 'Q5.i'])
pages 2-3: missing=0 duplicated=2 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
== 10s-11
  SLICED-BOUNDARY (2, 'Q1.iii', 175.7, 11)
  DUPLICATE (2, 166, '5', ['Q1.iii', 'Q2.i'])
pages 2-4: missing=0 duplicated=1 sliced_boundaries=1 answer_row_words=0 (in a crop: 0)
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; sed 's/                mine=\[i for i,e in enumerate(out) if e\[1\]==p and e\[0\].split/                print("DBG",p+1,q["label"],round(ay,1),round(top,1),round(rt,1),[e for e in out if e[1]==p and abs(e[2]-ay)<60],file=sys.stderr)\n&/' al_qp_splitter.py > $S/dbg_splitter.py; for f in 9709_s02_qp_1 9709_s05_qp_2; do ~/.venvs/alevel/bin/python -I $S/dbg_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/$f.pdf $S/t2 AL-MTH-X 2>&1 | grep "^DBG 2 [25] "; done; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-02s-11-QP 2 120 30
```

<details><summary>result</summary>

```
DBG 2 2 124.8 115.2 116.2 [('Q2.i', 1, 113.03999999999999, np.float64(147.84)), ('Q2.ii', 1, 149.04, 174.505615234375)]
DBG 2 2 104.7 102.0 104.6 [('Q1', 1, 60.813812255859375, np.float64(84.8)), ('Q2.a', 1, 98.63999999999999, np.float64(122.88)), ('Q2.b', 1, 124.56, 187.885498046875)]
DBG 2 5 484.0 476.2 477.6 [('Q4.ii', 1, 433.2, 484.0182800292969), ('Q5.i', 1, 472.08, np.float64(506.87999999999994)), ('Q5.ii', 1, 507.5999999999999, np.float64(588.4799999999999))]
Q1 [40.0, 60.77, 560.0, 124.81] [60.77, 124.81]
Q2.i [40.0, 113.04, 560.0, 146.64] [113.04, 147.84]
Q2.ii [40.0, 149.52, 560.0, 171.6] [149.04, 174.51]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                      and ay-PAD_PT-2<=e[2]<=ay+1]"""
new="""                      and min(ay-PAD_PT,rt)-2*PAD_PT<=e[2]<=ay+1]"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_cov.txt --no-sheets --workers 8 2>&1 | tail -1; ~/.venvs/alevel/bin/python -I /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/cls.py mth_t
```

<details><summary>result</summary>

```
this run: PASS 101 / 166; run total PASS 101 / 166
28 ('miss',) 17m-12 20m-12 21m-32 23m-12 23m-42 11s-53 14s-32 15s-11 18s-12 18s-41
10 ('slice',) 23s-11 25s-12 25s-15 09w-52 11w-51 11w-52 11w-63 14w-21 14w-23 23w-51
9 ('dupS', 'miss', 'slice') 25m-12 07s-31 12s-33 15s-32 16s-33 18s-31 22s-31 22s-33 17w-32
8 ('dupS',) 16m-32 25m-22 11s-31 25s-33 09w-32 14w-51 14w-52 22w-31
8 ('blank',) 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52
1 ('FURNITURE-IN-CROP',) 14s-13
1 ('dupS', 'slice') 19w-33
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:46:54

101/166 pass now. Next bucket: 28 papers with MISSING words only.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 17m-12 20m-12 21m-32 23m-12 23m-42 11s-53 14s-32 15s-11; do echo "== $p"; grep -v "^expected" AL-MTH-$p-QP/gates.log | head -5; done
```

<details><summary>result</summary>

```
== 17m-12
  MISSING (4, 302, '[The')
  MISSING (4, 302, 'volume')
  MISSING (4, 302, 'of')
  MISSING (4, 302, 'a')
  MISSING (4, 302, 'pyramid')
== 20m-12
  MISSING (11, 66, 'The')
  MISSING (11, 66, 'function')
  MISSING (11, 66, 'g')
  MISSING (11, 66, 'is')
  MISSING (11, 66, 'deﬁned')
== 21m-32
  MISSING (12, 56, '`')
  MISSING (12, 56, 'a')
  MISSING (12, 56, '`')
  MISSING (12, 56, 'a')
  MISSING (12, 56, '`')
== 23m-12
  MISSING (13, 66, 'The')
  MISSING (13, 66, 'function')
  MISSING (13, 66, 'g')
  MISSING (13, 66, 'is')
  MISSING (13, 66, 'deﬁned')
== 23m-42
  MISSING (11, 762, '[Question')
  MISSING (11, 762, '7')
  MISSING (11, 762, 'continues')
  MISSING (11, 762, 'on')
  MISSING (11, 762, 'the')
== 11s-53
  MISSING (4, 71, 'a')
pages 2-4: missing=1 duplicated=0 sliced_boundaries=0 answer_row_words=1 (in a crop: 1)
== 14s-32
  MISSING (3, 557, 'y')
pages 2-4: missing=1 duplicated=0 sliced_boundaries=0 answer_row_words=1 (in a crop: 1)
== 15s-11
  MISSING (2, 711, '`')
  MISSING (2, 711, 'a')
pages 2-4: missing=2 duplicated=0 sliced_boundaries=0 answer_row_words=1 (in a crop: 1)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 60,104p al_verify_coverage.py; git show 4ef7211 --stat; git show 4ef7211 | head -80
```

<details><summary>result</summary>

```
    r"Section [A-C] [\u2013-] .+)$", re.I)
MCQ_RUBRIC_RE = re.compile(r"^For each question,? there are four possible answers,? A, B, C,? and D\.", re.I)
# Biology essay-section rubric (9700 Paper 4 2004-05 Section B, Paper 6 2002-03),
# possibly wrapped: 'In this section, answers should be illustrated by large,
# clearly labelled diagrams wherever' / 'possible.' -- paper furniture
ESSAY_RUBRIC_RE = re.compile(
    r"^(?:Circle the number of the question(?:s)? you have answered|Answer only one question from this section|Your answers? to Section [A-C] must be in continuous prose|"
    r"(?:In this section, )?answers (?:may|should) be illustrated by large, clearly labelled diagrams|"
    r"The answer to Question \d+ should be illustrated by large, clearly labelled diagrams|"
    r"Your answer must be set out in sections \(a\) and \(b\))", re.I)
LINE_FURNITURE_RE = re.compile(
    r"^(?:Please turn over.*|(?:\[?)Turn over for .*|(?:This|The) question continues.*|"
    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|Question \d+ (?:continues|starts|begins).*)$", re.I)
TOTAL_RE = re.compile(r"^\[Total:?(\d+\])?$|^\d+\]$")
FURNITURE_RE = re.compile(r"^(©|UCLES|\[Turn|over|BLANK|PAGE|\*|Cambridge|University|Press|&|Assessment)$|"
                          r"^\d{4}/\d{1,2}(/.*)?$|^[A-Z]/[A-Z]/?\d{2}$|^[MOJN]/[JN]\d{2}$|^\d{4}$|"
                          # footer code broken into pieces ('9702/23/O/' 'N/23')
                          r"^[A-Z]/$|^[A-Z]/\d{2}$")


def shift29(t: str) ->
… [6628 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import re,ast,json,pymupdf as f
from pathlib import Path
L='17m-12 20m-12 21m-32 23m-12 23m-42 11s-53 14s-32 15s-11 18s-12 18s-41'.split()
import csv
r=[x for x in csv.DictReader(open('review/mth_t/run_summary.csv')) if x['status']=='HOLD']
for x in r:
  g=open('splits/mth_t/'+x['prefix']+'/gates.log').read()
  ms=[ast.literal_eval(l.strip()[8:]) for l in g.splitlines() if l.strip().startswith('MISSING')]
  if not ms or 'DUPLICATE' in g or 'SLICED' in g: continue
  d=f.open('source_papers/canonical/'+x['source'])
  seen=set()
  for pno,y,t in ms:
    if (pno,y) in seen: continue
    seen.add((pno,y))
    ws=[w for w in d[pno-1].get_text('words') if abs(w[1]-y)<3]
    print(x['prefix'][7:-3],pno,y,' '.join(w[4] for w in sorted(ws,key=lambda w:w[0]))[:110])
"
```

<details><summary>result</summary>

```
17m-12 4 302 [The volume of a pyramid having a base area A and vertical height h is 1 3Ah.]
17m-12 4 301 [The volume of a pyramid having a base area A and vertical height h is 1 3Ah.]
17m-12 4 299 [The volume of a pyramid having a base area A and vertical height h is 1 3Ah.]
20m-12 11 66 The function g is deﬁned by g x = 2x −3 for x ≤k.
20m-12 11 65 The function g is deﬁned by g x = 2x −3 for x ≤k.
21m-32 12 56 ` a ` a ` a ` a
23m-12 13 66 The function g is deﬁned by g x = −x2 −1 for x ≤−1.
23m-12 13 65 The function g is deﬁned by g x = −x2 −1 for x ≤−1.
23m-12 13 64 The function g is deﬁned by g x = −x2 −1 for x ≤−1.
23m-42 11 762 [Question 7 continues on the next page.]
11s-53 4 71 B a m C
14s-32 3 557 y
15s-11 2 711 ` a
18s-12 11 66 The function g is deﬁned by g : x →7 −2x2 −12x for x ≥k.
18s-12 11 65 The function g is deﬁned by g : x →7 −2x2 −12x for x ≥k.
18s-12 11 64 The function g is deﬁned by g : x →7 −2x2 −12x for x ≥k.
18s-41 8 415 displacement (m)
18s-41 8 447 200
18s-41 8 730 0 time (s)
18s-41 8 729 0 time (s)
18s-41 8 740 0 20
18s-51 12 381 [The volume of a cone is 30r2h.] 1
18s-51 12 384 [The volume of a cone is 30r2h.] 1
18s-52 9 92 [The volume of a cone is 30r2h.] 1
18s-52 9 90 [The volume of a cone is 30r2h.] 1
18s-53 12 381 [The volume of a cone is 30r2h.] 1
18s-53 12 384 [The volume of a cone is 30r2h.] 1
21s-31 12 56 ` a
23s-13 9 66 The function g is deﬁned by g x = x + 3 for x > 0.
23s-13 9 65 The function g is deﬁned by g x = x + 3 for x > 0.
13w-31 4 40
… [1561 more characters trimmed]
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-20m-12-QP 11 120 70; cp show.png s1.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-20m-12-QP 10 700 100; cp show.png s2.png; grep -i "orphan\|stem" ~/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-20m-12-QP/splitter.log | head
```

<details><summary>result</summary>

```
Q9.c [40.0, 86.16, 560.0, 108.24] [85.2, 110.91]
show.png
show.png
   Q6.stem
   Q8.stem
   Q8.b.stem
   Q9.b.stem
   Q10.stem
   Q12.stem
   Q12.c.stem
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_m20_qp_12.pdf /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/t3 AL-MTH-20m-12-QP 2>&1 | grep -v "^   " | head -30; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_m20_qp_12.pdf')
for w in d[10].get_text('words'):
  if w[1]<100: print([round(v,1) if isinstance(v,float) else v for v in w])
"
```

<details><summary>result</summary>

```
ORPHAN-HEAD 17 66.7 76.3 -> Q12.c.stem
MATHS-FIGURE 16 308.6 530.2 -> Q12.b
produced 31 crops
[291.5, 39.8, 303.2, 51.2, '11', 0, 0, 0]
[72.8, 65.8, 91.2, 77.2, 'The', 1, 0, 0]
[94.1, 65.8, 133.1, 77.2, 'function', 1, 0, 1]
[136.0, 65.8, 141.9, 77.2, 'g', 1, 0, 2]
[144.9, 65.8, 152.7, 77.2, 'is', 1, 0, 3]
[155.7, 65.8, 190.1, 77.2, 'deﬁned', 1, 0, 4]
[193.1, 65.8, 204.9, 77.2, 'by', 1, 0, 5]
[207.8, 65.8, 213.6, 77.2, 'g', 1, 0, 6]
[217.9, 65.5, 223.4, 77.4, 'x', 1, 0, 7]
[230.6, 64.8, 237.5, 75.8, '=', 1, 0, 8]
[240.6, 65.5, 251.9, 77.4, '2x', 1, 0, 9]
[254.4, 64.8, 269.6, 77.2, '−3', 1, 0, 10]
[272.5, 65.8, 286.3, 77.2, 'for', 1, 0, 11]
[289.2, 65.5, 294.7, 77.4, 'x', 1, 0, 12]
[297.8, 64.8, 316.3, 77.4, '≤k.', 1, 0, 13]
[72.8, 91.5, 85.9, 102.9, '(c)', 2, 0, 0]
[96.4, 91.5, 112.8, 102.9, 'For', 2, 1, 0]
[115.7, 91.5, 130.0, 102.9, 'the', 2, 1, 1]
[133.0, 91.5, 153.2, 102.9, 'case', 2, 1, 2]
[156.1, 91.5, 185.0, 102.9, 'where', 2, 1, 3]
[187.9, 91.1, 193.4, 103.0, 'k', 2, 1, 4]
[196.6, 90.4, 203.4, 101.4, '=', 2, 1, 5]
[206.5, 90.4, 222.2, 102.9, '−1,', 2, 1, 6]
[225.1, 91.5, 249.4, 102.9, 'solve', 2, 1, 7]
[252.4, 91.5, 266.8, 102.9, 'the', 2, 1, 8]
[269.8, 91.5, 310.0, 102.9, 'equation', 2, 1, 9]
[313.0, 91.5, 322.8, 102.9, 'fg', 2, 1, 10]
[327.0, 91.1, 332.5, 103.0, 'x', 2, 1, 11]
[339.8, 90.4, 346.7, 101.4, '=', 2, 1, 12]
[349.7, 91.5, 370.3, 102.9, '193.', 2, 1, 13]
[531.7, 91.5, 545.4, 102.9, '[2]', 2, 2, 0]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects
… [73 more characters trimmed]
```
</details>

### Assistant — 2026-10-20 10:47:50

Missing-words bucket: page-head context lines like "The function g is defined by …" above a part on a new page aren't claimed. Checking why the orphan-head pass skips them.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; n=$(grep -n "def alevel_orphan_heads" al_qp_splitter.py | cut -d: -f1); sed -n "$n,$((n+110))p" al_qp_splitter.py
```

<details><summary>result</summary>

```
    def alevel_orphan_heads(emits):
        """A Level: context at the HEAD of a page, above its first crop, that
        no crop owns -- 9701/52/F/M/17 p.4 'The student plotted a graph ...
        as shown.' + the graph, then '(c) Use the graph ...'; 9701/22/F/M/23
        p.14 Table 4.1 (named by (d)(i) on p.13).  Skipped when an answer row
        or mark follows it before the first crop (that is the previous leaf's
        own continued prompt).  Owner: orphan_owner()."""
        out=list(emits)
        for p in sorted({e[1] for e in emits}):
            on_p=sorted([e for e in out if e[1]==p],key=lambda e:e[2])
            first=on_p[0]
            if not [e for e in out if e[1]<p]:
                continue                    # the paper's first content page
            ar=answer_rows(p)
            floor=continued_floor(p,first[2])
            prose_rows=orphan_prose(p,floor-1,first[2]-1,ar)
            if not prose_rows:
                continue
            top=min(w[1] for w in prose_rows[0])
            ends=[r['y1'] for r in ar if top<r['y0']<first[2]]+[w[3] for w in W[p] if top<w[1]<first[2] and MARK_RE.match(w[4])]
            if ends:
                # followed by an answer row / mark: the previous leaf's own
                # continued prompt (its second bullet + '[2]' atop the next
                # page, 9701/53/O/N/14 Q1(a)) -> that leaf, up to its last row
                prev_=[e for e in out if (e[1],e[2])<(p,0) and not e[0].endswith('.stem')]
            
… [4606 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; n=$(grep -n "    def orphan_prose" al_qp_splitter.py | cut -d: -f1); sed -n "$n,$((n+40))p" al_qp_splitter.py; grep -n "def continued_floor" al_qp_splitter.py; n=$(grep -n "def continued_floor" al_qp_splitter.py | cut -d: -f1); sed -n "$n,$((n+30))p" al_qp_splitter.py
```

<details><summary>result</summary>

```
    def orphan_prose(p,lo,hi,ar):
        """Context rows in (lo,hi) on page p: prose (>=3 real words) or a
        figure/table caption; furniture, answer rows and marks excluded."""
        def in_ar(w):
            return any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar)
        rows={}
        for w in W[p]:
            if lo<w[1]<hi and not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4]) \
                    and not in_ar(w) and re.search(r'\w',w[4]):
                rows.setdefault(round(w[1]/3),[]).append(w)
        keep=[]
        for k,ws in sorted(rows.items()):
            txt=' '.join(v[4] for v in sorted(ws,key=lambda v:v[0]))
            if ORPHAN_FURNITURE_RE.match(txt) or ANSWER_AREA_LABEL_RE.match(txt) or STOP_RE.search(txt):
                continue
            if len([v for v in ws if re.search(r'[A-Za-z]{4,}',v[4])])>=3 or CAPTION_RE.fullmatch(txt.strip()):
                keep.append(ws)
            elif IS_MATHS and len([v for v in ws if re.search(r'[A-Za-z]{4,}',v[4])])>=2:
                # Maths context is short and symbolic: 'The function h is defined by
                # h(x) = 1/(x^2+2) for x >= 0.' (9709/12/M/J/24 p.7) has two long words
                keep.append(ws)
        return keep

    def figure_top(p,lo,top,ar):
        """A region that opens with a caption ('Fig. 2.1') holds the figure
        ABOVE it: start at the first ink after the last answer row / mark
        between `lo` and the caption (9701/52/M/J/24 p.7, calibration graph
        
… [2456 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "unicodedata\|NFKC" al_qp_splitter.py | head; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""            elif IS_MATHS and len([v for v in ws if re.search(r'[A-Za-z]{4,}',v[4])])>=2:
                # Maths context is short and symbolic: 'The function h is defined by
                # h(x) = 1/(x^2+2) for x >= 0.' (9709/12/M/J/24 p.7) has two long words
                keep.append(ws)"""
new="""            elif IS_MATHS and len([v for v in ws if re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',v[4]))])>=2:
                # Maths context is short and symbolic: 'The function h is defined by
                # h(x) = 1/(x^2+2) for x >= 0.' (9709/12/M/J/24 p.7) has two long words
                # (NFKC: 'deﬁned' is printed with the fi ligature, 9709/12/F/M/20 p.11)
                keep.append(ws)"""
assert s.count(old)==1; s=s.replace(old,new)
old2="import pymupdf as fitz, json, os, re, sys\n"
assert s.count(old2)==1; s=s.replace(old2,"import pymupdf as fitz, json, os, re, sys, unicodedata\n")
open(p,'w').write(s)
EOF
grep -n "^import" al_qp_splitter.py
```

<details><summary>result</summary>

```
26:import pymupdf as fitz, json, os, re, sys, unicodedata
29:import fused_marks; fused_marks.install()
30:import numpy as np
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:48:09

Now the bracketed formula hints ("[The volume of a cone is ⅓πr²h.]").

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-18s-51-QP 12 381 70; cp show.png s1.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-13w-31-QP 4 410 70; cp show.png s2.png
```

<details><summary>result</summary>

```
Q7.stem [40.0, 79.56, 560.0, 333.36] [78.2, 335.4]
Q7.i [40.0, 337.68, 560.0, 373.2] [335.4, 374.4]
show.png
Q10.ii [40.0, 342.0, 560.0, 376.08] [340.56, 377.28]
Q10.iii [40.0, 378.48, 560.0, 403.92] [378.48, 405.12]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "                for i in prev:\n                    out[i]=(out[i][0],p,out[i][2],min(out[i][3],cut))\n        return out\n", "new_string": "                for i in prev:\n                    out[i]=(out[i][0],p,out[i][2],min(out[i][3],cut))\n        return out\n\n    def maths_bracket_hints(emits):\n        \"\"\"Maths: a bracketed hint printed after a leaf's mark ('[The volume of a\n        cone is 1/3 pi r^2 h.]', 9709/51/M/J/18 Q7(i); at the end of the\n        question, 9709/31/O/N/13 Q10) is part of the leaf printed directly\n        above it: extend that crop over the hint (up to 3 wrapped rows).\"\"\"\n        out=list(emits)\n        for p in sorted({e[1] for e in out}):\n            ar=AR_CACHE.get(p,[])\n            rows={}\n            for w in W[p]:\n                c=(w[1]+w[3])/2\n                if CONTENT_L<=w[0]<=CONTENT_R and HEADER_Y<w[1]<CONTENT_BOTTOM \\\n                        and not any(e[1]==p and e[2]<=c<=e[3] for e in out) \\\n                        and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar):\n                    rows.setdefault(round(w[1]/3),[]).append(w)\n            rows=[sorted(ws,key=lambda v:v[0]) for _,ws in sorted(rows.items())]\n            for k,ws in enumerate(rows):\n                if not ws[0][4].startswith('[') or MARK_RE.match(ws[0][4]) or len(ws)<3:\n                    continue\n                run=[ws]\n                while not run[-1][-1][4].endswith(']') and k+len(run)<len(rows) and len(run)<3 \\\n                        and min(w[1] for w in rows[k+len(run)])-max(w[3] for w in run[-1])<8:\n                    run.append(rows[k+len(run)])\n                if not run[-1][-1][4].endswith(']'):\n                    continue\n                top=min(w[1] for r in run for w in r); bot=max(w[3] for r in run for w in r)\n                above=[i for i,e in enumerate(out) if e[1]==p and e[3]<=top+1 and not e[0].endswith('.stem')]\n                if not above:\n                    continue\n                i=max(above,key=lambda i:out[i][3])\n                between=[r for r in ar if out[i][3]<r['y0']<top]\n                if between or top-out[i][3]>30 or any(e[1]==p and out[i][3]<e[2]<bot for e in out):\n                    continue\n                _,rb=INK[p].extent(top-2,bot+4)\n                if os.environ.get('AL_DEBUG_ORPHAN'):\n                    print('MATHS-HINT',p+1,round(top,1),'->',out[i][0],file=sys.stderr)\n                out[i]=(out[i][0],p,out[i][2],max(bot,rb or bot)+2)\n        return out\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "            emits=maths_raised_question_rows(emits)\n", "new_string": "            emits=maths_raised_question_rows(emits)\n            emits=maths_bracket_hints(emits)\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline; git status --short; git diff --stat
```

<details><summary>result</summary>

```
 M ALEVEL/scripts/al_qp_splitter.py
 ALEVEL/scripts/al_qp_splitter.py | 93 +++++++++++++++++++++++++++++++++++++++-
 1 file changed, 91 insertions(+), 2 deletions(-)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:48:46

Also making "[Question 7 continues on the next page.]" (with the bracket) furniture in splitter and gate.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "continues" al_qp_splitter.py | head -20; grep -n "continues" al_verify_coverage.py al_verify_leaves.py | head
```

<details><summary>result</summary>

```
82:STOP_RE=re.compile(r'(Do not write|Please do not write|This question continues|Please turn over|Turn over for (?:Question|Section)|Question \d+ continue[sd]|^Diagram$|^References|Baccalaureate Organization|Answers will not|blank page'
2342:            if re.search(r'This question continues',txt,re.I):
2879:                                   r'.*\b(?:is|starts|begins|continues) on (?:the )?(?:next|following|opposite) page.*|'
2881:                                   r'(?:Question|Section|Option) \S+ (?:starts|begins|continues) on page \d+\.?|'
3001:                # * it carries a mark -> the previous leaf's own task continues
3217:                    # a bulleted row continues the leaf's own list ('(a) * ... /
al_verify_leaves.py:13:token counts only if it sits in its column AND continues the expected
al_verify_coverage.py:49:    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|Question \d+ (?:continues|starts|begins).*|"
al_verify_coverage.py:50:    r"(?:.* )?BLANK PAGE(?: .*)?|Please turn over.*|\[?Turn over for .*|(?:Question|Section|Option) \S+ (?:starts|begins|continues) on page \d+\.?|Turn over to page \d+ for the next question\.?|\[?Questions? \d+(?:(?:,| and) \d+)* (?:is|are) printed (?:on the next page|overleaf)\.?\]?|OPTION \d+\s*[\u2013-]\s*[A-Z][A-Z ,&-]+|Answer (?:one|two|either|both|all) (?:of the )?(?:following )?questions?\.?|Question \d+\.|_{10,}|This question continues.*|Space for working\.?|Space for (?:a |the |your )?(?:table|diagram|drawing|graph)s?\.?|(
… [765 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_verify_coverage.py'; s=open(p).read()
old='r"QUESTION \\d+ (?:IS|STARTS|BEGINS|CONTINUES).*|Question \\d+ (?:continues|starts|begins).*|"\n'
assert s.count(old)==1, s.count(old)
s=s.replace(old,'r"QUESTION \\d+ (?:IS|STARTS|BEGINS|CONTINUES).*|\\[?Question \\d+ (?:continues|starts|begins).*|"\n')
old='r"QUESTION \\d+ (?:IS|STARTS|BEGINS|CONTINUES).*|Question \\d+ (?:continues|starts|begins).*)$", re.I)'
assert s.count(old)==1
s=s.replace(old,'r"QUESTION \\d+ (?:IS|STARTS|BEGINS|CONTINUES).*|\\[?Question \\d+ (?:continues|starts|begins).*)$", re.I)')
open(p,'w').write(s)
EOF
git diff al_verify_coverage.py | grep "^[-+]" | cut -c1-150
```

<details><summary>result</summary>

```
--- a/ALEVEL/scripts/al_verify_coverage.py
+++ b/ALEVEL/scripts/al_verify_coverage.py
-    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|Question \d+ (?:continues|starts|begins).*|"
+    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|\[?Question \d+ (?:continues|starts|begins).*|"
-    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|Question \d+ (?:continues|starts|begins).*)$", re.I)
+    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|\[?Question \d+ (?:continues|starts|begins).*)$", re.I)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:48:57

Now looking at the other missing patterns ("` a" at page head, graph labels in 18s-41, "Hence", "The median of X is m.").

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-21m-32-QP 12 90 50; cp show.png s1.png; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_m21_qp_32.pdf')
for w in d[11].get_text('words'):
  if w[1]<80: print([round(v,1) if isinstance(v,float) else v for v in w])
"
```

<details><summary>result</summary>

```
Q7.stem [40.0, 63.72, 560.0, 104.4] [70.67, 106.8]
Q7.a [40.0, 108.24, 560.0, 129.36] [106.8, 132.86]
show.png
[291.5, 39.8, 303.2, 51.2, '12', 0, 0, 0]
[49.3, 75.7, 55.2, 87.0, '7', 1, 0, 0]
[72.8, 75.8, 94.0, 87.2, 'Two', 1, 1, 0]
[97.0, 75.8, 119.2, 87.2, 'lines', 1, 1, 1]
[122.2, 75.8, 143.7, 87.2, 'have', 1, 1, 2]
[146.6, 75.8, 191.6, 87.2, 'equations', 1, 1, 3]
[194.5, 75.7, 199.7, 87.0, 'r', 1, 1, 4]
[202.8, 69.9, 209.7, 93.5, '=', 1, 1, 5]
[212.6, 56.2, 219.0, 67.2, '`', 2, 0, 0]
[220.8, 62.8, 226.7, 74.2, '1', 2, 0, 1]
[220.8, 75.8, 226.7, 87.2, '3', 3, 0, 0]
[228.6, 56.2, 234.9, 67.2, 'a', 4, 0, 0]
[237.4, 69.9, 244.2, 93.5, '+', 5, 0, 0]
[246.6, 75.3, 251.4, 87.2, 's', 5, 0, 1]
[253.2, 56.2, 259.5, 67.2, '`', 6, 0, 0]
[268.3, 62.8, 274.2, 74.2, '2', 6, 0, 1]
[261.4, 69.9, 274.2, 93.5, '−1', 7, 0, 0]
[276.0, 56.2, 282.3, 67.2, 'a', 9, 0, 0]
[285.2, 75.8, 302.3, 87.2, 'and', 10, 0, 0]
[305.2, 75.7, 310.4, 87.0, 'r', 10, 0, 1]
[313.4, 69.9, 320.3, 93.5, '=', 10, 0, 2]
[323.4, 56.2, 329.7, 67.2, '`', 11, 0, 0]
[331.6, 62.8, 337.4, 74.2, '2', 11, 0, 1]
[331.6, 75.8, 337.4, 87.2, '1', 12, 0, 0]
[339.2, 56.2, 345.6, 67.2, 'a', 13, 0, 0]
[348.0, 69.9, 354.9, 93.5, '+', 14, 0, 0]
[357.4, 75.3, 360.8, 87.2, 't', 14, 0, 1]
[362.9, 56.2, 369.2, 67.2, '`', 15, 0, 0]
[377.9, 62.8, 383.8, 74.2, '1', 15, 0, 1]
[371.0, 69.9, 383.8, 93.5, '−1', 16, 0, 0]
[385.6, 56.2, 391.9, 67.2, 'a', 18, 0, 0]
[391.9, 75.8, 394.9, 87.2, '.', 19, 0, 0]
Shell cwd was reset to /Users/nitya/Documents/
… [87 more characters trimmed]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "        cy0=max(lim_lo, rt-PAD_PT)\n        cy1=min(lim_hi, rb+PAD_PT)\n", "new_string": "        cy0=max(lim_lo, rt-PAD_PT)\n        cy1=min(lim_hi, rb+PAD_PT)\n        if IS_MATHS:\n            # big-bracket pieces of a column vector are text whose box is far\n            # taller than its ink ('`' at 56-67 pt over ink from 63 pt,\n            # 9709/32/F/M/21 p.12): take in the box centre across white rows\n            for w in W[pno]:\n                c=(w[1]+w[3])/2\n                if w[1]<rt<w[3] and HEADER_Y<c<cy0 and not ink.ink[ink._r(c-1):ink._r(cy0)+1].any():\n                    cy0=c-1\n                if w[1]<rb<w[3] and cy1<c<FOOTER_Y and not ink.ink[ink._r(cy1):ink._r(c+1)+1].any():\n                    cy1=c+1\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                if w[1]<rt<w[3] and HEADER_Y<c<cy0 and not ink.ink[ink._r(c-1):ink._r(cy0)+1].any():
                    cy0=c-1
                if w[1]<rb<w[3] and cy1<c<FOOTER_Y and not ink.ink[ink._r(cy1):ink._r(c+1)+1].any():
                    cy1=c+1"""
new="""                if w[3]>cy0+1 and HEADER_Y<c<cy0 and not ink.ink[ink._r(c-1):ink._r(cy0)+1].any():
                    cy0=c-1
                if w[1]<cy1-1 and cy1<c<FOOTER_Y and not ink.ink[ink._r(cy1):ink._r(c+1)+1].any():
                    cy1=c+1"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
cd ~/rootatom_data/ALEVEL; grep -l "MISSING" splits/mth_t/*/gates.log | xargs -n1 dirname | xargs -n1 basename | ~/.venvs/alevel/bin/python -I -c "
import sys,csv
ps=set(l.strip() for l in sys.stdin)
r=[x['source'] for x in csv.DictReader(open('review/mth_t/run_summary.csv')) if x['prefix'] in ps]
open('review/mth/t_miss.txt','w').write('\n'.join(r)+'\n'); print(len(r))"; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/t_miss.txt --no-sheets --workers 8 2>&1 | tail -1; ~/.venvs/alevel/bin/python -I /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/cls.py mth_t
```

<details><summary>result</summary>

```
37
this run: PASS 11 / 37; run total PASS 112 / 166
17 ('miss',) 17m-12 21m-32 11s-53 18s-41 18s-51 18s-52 18s-53 21s-31 13w-31 17w-61
10 ('slice',) 23s-11 25s-12 25s-15 09w-52 11w-51 11w-52 11w-63 14w-21 14w-23 23w-51
9 ('dupS', 'miss', 'slice') 25m-12 07s-31 12s-33 15s-32 16s-33 18s-31 22s-31 22s-33 17w-32
8 ('dupS',) 16m-32 25m-22 11s-31 25s-33 09w-32 14w-51 14w-52 22w-31
8 ('blank',) 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52
1 ('FURNITURE-IN-CROP',) 14s-13
1 ('dupS', 'slice') 19w-33
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 17m-12 21m-32 18s-51 13w-31 21s-31; do echo "== $p"; grep -v "^expected" AL-MTH-$p-QP/gates.log | head -4; grep "HINT" AL-MTH-$p-QP/splitter.log; done
```

<details><summary>result</summary>

```
Exit code 1
== 17m-12
  MISSING (4, 302, '[The')
  MISSING (4, 302, 'volume')
  MISSING (4, 302, 'of')
  MISSING (4, 302, 'a')
== 21m-32
  MISSING (12, 56, '`')
  MISSING (12, 56, 'a')
  MISSING (12, 56, '`')
  MISSING (12, 56, 'a')
== 18s-51
  MISSING (12, 381, '30r2h.]')
  MISSING (12, 381, '1')
  MISSING (12, 384, '[The')
  MISSING (12, 384, 'volume')
== 13w-31
  MISSING (4, 405, '=')
  MISSING (4, 405, '30r2h.]')
  MISSING (4, 414, '[The')
  MISSING (4, 414, 'volume')
MATHS-HINT 3 747.1 -> Q9.iii
== 21s-31
  MISSING (12, 56, '`')
  MISSING (12, 56, 'a')
pages 2-16: missing=2 duplicated=0 sliced_boundaries=0 answer_row_words=1 (in a crop: 1)
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I - <<EOF
s=open('al_qp_splitter.py').read()
s=s.replace("""        if IS_MATHS:
            # big-bracket pieces""","""        if pno==11: print('BOX',label,y0,y1,rt,rb,cy0,cy1,lim_lo,file=sys.stderr)
        if IS_MATHS:
            # big-bracket pieces""")
open('$S/dbg_splitter.py','w').write(s)
EOF
~/.venvs/alevel/bin/python -I $S/dbg_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_m21_qp_32.pdf $S/t2 AL-MTH-21m-32-QP 2>&1 | grep "^BOX" | head -3
```

<details><summary>result</summary>

```
BOX Q7.stem 70.66622924804688 106.80220794677734 70.08 98.39999999999999 70.66622924804688 104.39999999999999 70.66622924804688
BOX Q7.a 106.80220794677734 132.85816955566406 114.24 123.35999999999999 108.24 129.35999999999999 106.80220794677734
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                if not mine or not prev:
                    continue
                if rt>=ay-PAD_PT+1 and all(out[i][3]<=rt-1 for i in prev):
                    continue         # nothing above the usual start
                cut=boundary(p,max(out[i][2] for i in prev),rt)
"""
new="""                if not mine:
                    continue
                if rt>=ay-PAD_PT+1 and all(out[i][3]<=rt-1 for i in prev):
                    continue         # nothing above the usual start
                cut=boundary(p,max([out[i][2] for i in prev] or [HEADER_Y]),rt)
"""
assert s.count(old)==1; s=s.replace(old,new)
old="""            rows={}
            for w in W[p]:
                c=(w[1]+w[3])/2
                if CONTENT_L<=w[0]<=CONTENT_R and HEADER_Y<w[1]<CONTENT_BOTTOM \\
                        and not any(e[1]==p and e[2]<=c<=e[3] for e in out) \\
                        and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar):
                    rows.setdefault(round(w[1]/3),[]).append(w)
            rows=[sorted(ws,key=lambda v:v[0]) for _,ws in sorted(rows.items())]
            for k,ws in enumerate(rows):
                if not ws[0][4].startswith('[') or MARK_RE.match(ws[0][4]) or len(ws)<3:
                    continue
                run=[ws]
                while not run[-1][-1][4].endswith(']') and k+len(run)<len(rows) and len(run)<3 \\
                        and min(w[1] for w in rows[k+len(run)])-max(w[3] for w in run[-1])<8:
                    run.append(rows[k+len(run)])
                if not run[-1][-1][4].endswith(']'):
                    continue
                top=min(w[1] for r in run for w in r); bot=max(w[3] for r in run for w in r)
"""
new="""            free=[w for w in W[p] if CONTENT_L<=w[0]<=CONTENT_R and HEADER_Y<w[1]<CONTENT_BOTTOM
                  and not any(e[1]==p and e[2]<=(w[1]+w[3])/2<=e[3] for e in out)
                  and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar)]
            for w0 in free:
                if not w0[4].startswith('[') or MARK_RE.match(w0[4]) or \\
                        [v for v in free if v[2]<=w0[0] and v[1]<w0[3]-2 and v[3]>w0[1]+2]:
                    continue         # not the first word of its row
                top,bot=w0[1],w0[3]; nrows=1
                while True:          # the row (stacked fractions overlap it) + wrapped rows
                    row=[v for v in free if v[1]<bot-2 and v[3]>top+2 and v[0]>=w0[0]-1]
                    bot=max(bot,max(v[3] for v in row)); top=min(top,min(v[1] for v in row))
                    last=max(row,key=lambda v:v[2])
                    if last[4].endswith(']') or nrows>=3:
                        break
                    nxt=[v for v in free if bot-2<=v[1]<bot+8]
                    if not nxt:
                        break
                    bot=max(v[3] for v in nxt); nrows+=1
      
… [559 more characters trimmed]
```

<details><summary>result</summary>

```
this run: PASS 22 / 37; run total PASS 123 / 166
15 ('dupS',) 16m-32 25m-22 07s-31 11s-31 15s-32 16s-33 18s-31 22s-31 22s-33 25s-33
10 ('slice',) 23s-11 25s-12 25s-15 09w-52 11w-51 11w-52 11w-63 14w-21 14w-23 23w-51
8 ('blank',) 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:54:50

123/166. Checking the hint crops and what's left.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I $S/bin/cls.py mth_t; cd ~/rootatom_data/ALEVEL/splits/mth_t; grep -h "HINT" */splitter.log | head; grep -l HINT */splitter.log | wc -l
```

<details><summary>result</summary>

```
15 ('dupS',) 16m-32 25m-22 07s-31 11s-31 15s-32 16s-33 18s-31 22s-31 22s-33 25s-33
10 ('slice',) 23s-11 25s-12 25s-15 09w-52 11w-51 11w-52 11w-63 14w-21 14w-23 23w-51
8 ('blank',) 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52
6 ('miss',) 11s-53 18s-41 17w-61 19w-13 21w-61 21w-63
2 ('dupS', 'slice') 25m-12 19w-33
1 ('dupS', 'miss', 'slice') 12s-33
1 ('FURNITURE-IN-CROP',) 14s-13
MATHS-HINT 3 747.1 -> Q9.iii
MATHS-HINT 4 405.4 -> Q10.iii
MATHS-HINT 3 737.5 -> Q9.iii
MATHS-HINT 4 299.5 -> Q3.i
MATHS-HINT 12 381.1 -> Q7.i
MATHS-HINT 12 381.1 -> Q7.i
MATHS-HINT 2 590.8 -> Q2.i
MATHS-HINT 9 89.9 -> Q5.ii
MATHS-HINT 8 285.4 -> Q5.i
       8
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits/mth_t; grep -H "HINT" */splitter.log | sed 's|/splitter.log:MATHS-HINT [0-9]* [0-9.]* -> | |' > $S/hints.txt; cat $S/hints.txt; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
ims=[]
for l in open('$S/hints.txt'):
  p,lab=l.split(); ims.append(Image.open(f'{p}/{p}-{lab}.png'))
W=max(i.width for i in ims); H=sum(i.height+20 for i in ims)
c=Image.new('RGB',(W,H),(200,200,200)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+20
c=c.resize((W//2,H//2)); c.save('$S/v2.png')"
```

<details><summary>result</summary>

```
AL-MTH-18s-52-QP Q5.ii
AL-MTH-19w-12-QP Q5.i
AL-MTH-13w-31-QP Q9.iii
AL-MTH-13w-31-QP Q10.iii
AL-MTH-18s-51-QP Q7.i
AL-MTH-18w-52-QP Q2.i
AL-MTH-15s-11-QP Q9.iii
AL-MTH-17m-12-QP Q3.i
AL-MTH-18s-53-QP Q7.i
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/v2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 10:55:06

Bug: the pass also grabbed "[Question 10 is printed on the next page.]" furniture. Excluding furniture rows.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "ORPHAN_FURNITURE_RE *=" al_qp_splitter.py; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                if not last[4].endswith(']') or len(row)<3:
                    continue
"""
new="""                txt=' '.join(v[4] for v in sorted(row,key=lambda v:(round(v[1]/3),v[0])))
                if not last[4].endswith(']') or len(row)<3 or ORPHAN_FURNITURE_RE.match(txt) or STOP_RE.search(txt):
                    continue
"""
assert s.count(old)==1; s=s.replace(old,new); open(p,'w').write(s)
EOF
~/.venvs/alevel/bin/python -I -c "
import re,sys; sys.argv=['x','a','b','AL-MTH-X']
" ; grep -n "ORPHAN_FURNITURE_RE=re.compile" -A2 al_qp_splitter.py | head -5
```

<details><summary>result</summary>

```
2877:    ORPHAN_FURNITURE_RE=re.compile(r'^(?:\[Turn over|BLANK PAGE|Please turn over.*|Turn over for (?:[Qq]uestion|Section) \S+|Section [A-C]|'
2877:    ORPHAN_FURNITURE_RE=re.compile(r'^(?:\[Turn over|BLANK PAGE|Please turn over.*|Turn over for (?:[Qq]uestion|Section) \S+|Section [A-C]|'
2878-                                   r'For Examiner.s Use|Answer all (?:the )?questions.*|.*BLANK PAGE.*|'
2879-                                   r'.*\b(?:is|starts|begins|continues) on (?:the )?(?:next|following|opposite) page.*|'
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 16m-32 25m-22 07s-31 11s-31 15s-32 16s-33; do echo "== $p"; grep -v "^expected" AL-MTH-$p-QP/gates.log | head -4; done
```

<details><summary>result</summary>

```
== 16m-32
  DUPLICATE (2, 520, '60', ['Q5.i', 'Q5.stem'])
  DUPLICATE (2, 527, '=', ['Q5.i', 'Q5.stem'])
  DUPLICATE (2, 527, 'ï3', ['Q5.i', 'Q5.stem'])
  DUPLICATE (2, 527, '1,', ['Q5.i', 'Q5.stem'])
== 25m-22
  DUPLICATE (10, 98, 'd', ['Q8.a', 'Q8.stem'])
  DUPLICATE (10, 98, 'y', ['Q8.a', 'Q8.stem'])
  DUPLICATE (10, 98, '-', ['Q8.a', 'Q8.stem'])
  DUPLICATE (10, 98, '2', ['Q8.a', 'Q8.stem'])
== 07s-31
  DUPLICATE (3, 112, '2', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 117, '√x', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 118, '2', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 125, '(i)', ['Q7.i', 'Q7.stem'])
== 11s-31
  DUPLICATE (3, 407, '5', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 410, '=', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 410, '+', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 410, '=', ['Q7.i', 'Q7.stem'])
== 15s-32
  DUPLICATE (3, 108, '−u', ['Q6.i', 'Q6.stem'])
  DUPLICATE (3, 111, '2', ['Q6.i', 'Q6.stem'])
  DUPLICATE (3, 115, '=', ['Q6.i', 'Q6.stem'])
  DUPLICATE (3, 115, '−', ['Q6.i', 'Q6.stem'])
== 16s-33
  DUPLICATE (3, 109, '−1', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 112, '2', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 116, '=', ['Q7.i', 'Q7.stem'])
  DUPLICATE (3, 116, '+', ['Q7.i', 'Q7.stem'])
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-07s-31-QP 3 115 40; cp show.png s1.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-16m-32-QP 2 525 40; cp show.png s2.png
```

<details><summary>result</summary>

```
Q7.stem [40.0, 60.0, 560.0, 152.88] [60.0, 118.32]
Q7.i [40.0, 106.8, 560.0, 152.88] [118.32, 153.92]
show.png
Q5.stem [40.0, 470.16, 560.0, 559.44] [470.16, 525.64]
Q5.i [40.0, 519.6, 560.0, 559.44] [525.64, 560.16]
Q5.ii [40.0, 562.32, 560.0, 583.44] [560.88, 586.82]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-07s-31-QP; grep -o '"Q7[^]]*\][^}]*}' *provenance.json | head; tail -5 splitter.log
```

<details><summary>result</summary>

```
   Q10.ii
   Q10.iii
   Q10.iv
MATHS-RAISED-ROW 3 7 63.4 60.0
MATHS-RAISED-ROW 3 8 203.5 197.5
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/Users/nitya/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-07s-31-QP/AL-MTH-07s-31-QP-Q7.stem.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits; for r in mth_t mth_b1; do ~/.venvs/alevel/bin/python -I -c "
import json;d=json.load(open('$r/AL-MTH-07s-31-QP/AL-MTH-07s-31-QP-split-provenance.json'))
for k in ('Q6.ii','Q7.stem','Q7.i'): print('$r',k,d['outputs'].get(k))
print(d.get('manual_masks'))"; done; grep -c . mth_b1/AL-MTH-07s-31-QP/gates.log; head -3 mth_b1/AL-MTH-07s-31-QP/gates.log
```

<details><summary>result</summary>

```
mth_t Q6.ii [{'pdf_page': 2, 'clip_points': [40.0, 646.32, 560.0, 672.72], 'semantic_bounds_points': [646.32, 673.44], 'two_dimensional_seam': False}]
mth_t Q7.stem [{'pdf_page': 3, 'clip_points': [40.0, 60.0, 560.0, 152.88], 'semantic_bounds_points': [60.0, 118.32], 'two_dimensional_seam': True}]
mth_t Q7.i [{'pdf_page': 3, 'clip_points': [40.0, 106.8, 560.0, 152.88], 'semantic_bounds_points': [118.32, 153.92], 'two_dimensional_seam': True}]
[]
mth_b1 Q6.ii [{'pdf_page': 2, 'clip_points': [40.0, 646.32, 560.0, 672.72], 'semantic_bounds_points': [646.32, 673.44], 'two_dimensional_seam': False}]
mth_b1 Q7.stem [{'pdf_page': 3, 'clip_points': [40.0, 70.74, 560.0, 152.88], 'semantic_bounds_points': [70.74, 118.32], 'two_dimensional_seam': True}]
mth_b1 Q7.i [{'pdf_page': 3, 'clip_points': [40.0, 106.8, 560.0, 152.88], 'semantic_bounds_points': [118.32, 153.92], 'two_dimensional_seam': True}]
[]
26
expected=21 produced=21 missing=[] extra=[]
  SLICED-BOUNDARY (3, 'Q7.stem', 70.7, 11)
  SLICED-BOUNDARY (3, 'Q7.ii', 210.1, 13)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "two_dimensional\|seam" al_verify_coverage.py al_verify_leaves.py | head; grep -n "two_dimensional_seam\|seam_masks\b" al_qp_splitter.py | head
```

<details><summary>result</summary>

```
4765:    def apply_seam_masks(image,cy0,masks):
4942:        image=apply_seam_masks(pix_to_image(pix),cy0,masks)
4953:            'two_dimensional_seam':bool(masks),
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import json,csv,glob
st={x['prefix']:x['status'] for x in csv.DictReader(open('review/mth_b1/run_summary.csv'))}
st2={x['prefix']:x['status'] for x in csv.DictReader(open('review/mth_t/run_summary.csv'))}
import collections; c=collections.Counter()
for f in glob.glob('splits/mth_t/*/*provenance.json')+glob.glob('splits/mth_b1/*/*provenance.json'):
  d=json.load(open(f)); n=sum(s['two_dimensional_seam'] for v in d['outputs'].values() for s in v)
  run=f.split('/')[1]; p=d['prefix']
  s=(st2 if run=='mth_t' else st).get(p)
  if n: c[(run,s)]+=1
print(c)
"; ls splits/bio_b1 2>/dev/null | head -2; ~/.venvs/alevel/bin/python -I -c "
import json,glob
n=0;t=0
for f in glob.glob('/Users/nitya/rootatom_data/ALEVEL/splits/bio_b1/*/*provenance.json'):
  d=json.load(open(f)); t+=1; n+=any(s['two_dimensional_seam'] for v in d['outputs'].values() for s in v)
print('bio',n,t)"
```

<details><summary>result</summary>

```
Counter({('mth_b1', 'HOLD'): 130, ('mth_t', 'HOLD'): 18})
AL-BIO-02s-21-QP
AL-BIO-02s-41-QP
bio 0 370
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 2120,2280p al_qp_splitter.py
```

<details><summary>result</summary>

```
            span_x=(cols.max()-cols.min()+1)/SC
            span_y=(rows.max()-rows.min()+1)/SC
            if rect.width>4 and span_x<rect.width*0.25:
                return False
            if rect.height>4 and span_y<rect.height*0.25:
                return False
            return True
        seen_xrefs=set()
        for image in page.get_images(full=True):
            xref=image[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            for rect in page.get_image_rects(xref):
                # Legacy ROOT19-stamped PDFs can carry a page-wide watermark
                # image that begins above the first child and extends almost
                # to the footer.  It is presentation furniture, not shared
                # mathematical context.  A true whole-page scan would not
                # also provide the text anchors required to reach this code.
                page_watermark=(
                    rect.x0<CONTENT_L-10 and rect.x1>CONTENT_R+10 and
                    rect.height>200
                )
                if (not page_watermark and meaningful_body_overlap(rect) and
                        rect.y0>=y_prev-8 and rect.y0<lower_top-8):
                    upper_graphic_rects.append(rect)
        for drawing in page.get_drawings():
            rect=drawing.get('rect')
            # A diagram frame is often exposed as four zero-thickness line
            # drawings rather than one enclosing rectangle, so either
  
… [7336 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 2280,2380p al_qp_splitter.py
```

<details><summary>result</summary>

```
        if IS_ALEVEL and upper_bottom>=lower_top-0.5 and upper_bottom<lower_top+3:
            # word BOXES touch, but the glyphs may still be separated by
            # fully blank pixel rows (box = line spacing): 'where Q ...' over
            # '(a) ... 1/V' in 9702/52/F/M/17 had a 0.0 pt box margin and an
            # 8 pt blank band.  Cut on the blank row nearest the midpoint
            # instead of building a 2-D seam.
            ink=INK[pno]; rows=ink.semantic.sum(axis=1)
            lo,hi=ink._r(upper_bottom-4),ink._r(lower_top+4)
            blank=[r for r in range(lo,hi+1) if rows[r]==0]
            if blank:
                mid=ink._r(cut)
                return ink._p(min(blank,key=lambda r:abs(r-mid)))
        if upper_bottom>=lower_top-0.5:
            # Limit the 2-D search to the actual semantic collision rather
            # than the entire preceding stem.  This makes the seam solve both
            # stricter and more stable for raised indices, tall brackets and
            # neighbouring formulae whose vertical hulls interleave.
            upper_graphic_regions=[]
            upper_graphic_word_regions=[]
            if upper_graphic_rects:
                upper_graphic_regions=[[
                    rect.x0-2,rect.y0-2,rect.x1+2,rect.y1+2,
                ] for rect in upper_graphic_rects]
                # Diagram vertex/axis labels are separate PDF text objects
                # and routinely sit just outside the vector drawing bbox.
                
… [4198 more characters trimmed]
```
</details>

**Tool `Bash`**

```
~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_s07_qp_3.pdf')
for w in d[2].get_text('words'):
  if 60<w[1]<140: print([round(v,1) if isinstance(v,float) else v for v in w], round((w[1]+w[3])/2,1))
"
```

<details><summary>result</summary>

```
[49.3, 75.7, 55.1, 86.9, '7', 1, 0, 0] 81.3
[72.5, 75.8, 88.1, 87.1, 'Let', 1, 1, 0] 81.4
[91.1, 75.3, 95.2, 87.1, 'I', 1, 1, 1] 81.2
[98.9, 75.6, 105.7, 86.6, '=', 1, 1, 2] 81.1
[121.4, 62.5, 125.7, 70.8, '4', 2, 0, 0] 66.6
[117.6, 91.8, 121.9, 100.0, '1', 3, 0, 0] 95.9
[149.3, 68.4, 155.1, 79.8, '1', 4, 0, 0] 74.1
[129.2, 83.0, 145.1, 94.8, 'x(4', 4, 1, 0] 88.9
[147.5, 75.4, 175.3, 94.8, '−√x)', 4, 1, 1] 85.1
[178.3, 75.3, 192.7, 87.1, 'dx.', 4, 1, 2] 81.2
[79.0, 124.9, 89.9, 136.1, '(i)', 5, 0, 0] 130.5
[95.6, 125.0, 113.8, 136.3, 'Use', 5, 0, 1] 130.6
[116.8, 125.0, 131.1, 136.3, 'the', 5, 0, 2] 130.6
[134.0, 125.0, 188.8, 136.3, 'substitution', 5, 0, 3] 130.6
[191.8, 124.5, 198.0, 136.3, 'u', 5, 0, 4] 130.4
[201.0, 124.8, 207.8, 135.8, '=', 5, 0, 5] 130.3
[210.8, 116.8, 225.0, 136.3, '√x', 5, 0, 6] 126.5
[227.9, 125.0, 237.0, 136.3, 'to', 5, 0, 7] 130.6
[240.0, 125.0, 264.4, 136.3, 'show', 5, 0, 8] 130.6
[267.3, 125.0, 284.9, 136.3, 'that', 5, 0, 9] 130.6
[287.9, 124.5, 292.0, 136.3, 'I', 5, 0, 10] 130.4
[295.7, 124.8, 302.5, 135.8, '=', 5, 0, 11] 130.3
[318.2, 111.6, 322.5, 119.8, '2', 6, 0, 0] 115.7
[342.5, 117.5, 348.3, 128.9, '2', 8, 0, 0] 123.2
[326.0, 131.9, 342.6, 143.7, 'u(4', 8, 1, 0] 137.8
[344.9, 131.9, 364.7, 143.7, '−u)', 8, 1, 1] 137.8
[367.8, 124.5, 382.7, 136.3, 'du.', 8, 1, 2] 130.4
[531.7, 125.0, 545.3, 136.3, '[3]', 8, 2, 0] 130.6
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; AL_DEBUG_SEM=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s07_qp_3.pdf /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/t3 AL-MTH-07s-31-QP 2>&1 | grep "SEM i page 3" | cut -c1-400
```

<details><summary>result</summary>

```
SEM i page 3 marker True upper_bottom 119.8 lower_top 116.8 lower_first [(210.8408966064453, 116.79513549804688, 224.9783172607422, 136.2836151123047, '√x', 5, 0, 6), (342.4800109863281, 117.51547241210938, 348.343017578125, 128.8514404296875, '2', 8, 0, 0), (191.75990295410156, 124.47632598876953, 197.9517059326172, 136.2836151123047, 'u', 5, 0, 4)]
SEM i page 3 marker True upper_bottom 229.1 lower_top 239.9 lower_first [(289.2001037597656, 239.87469482421875, 303.0514831542969, 253.65155029296875, 'u2.', 12, 0, 9), (260.28009033203125, 241.83631896972656, 266.4718933105469, 253.6436004638672, 'u', 12, 0, 7), (78.95999908447266, 242.30435180664062, 89.89850616455078, 253.50633239746094, '(i)', 12, 0, 0)]
SEM i page 3 marker True upper_bottom 614.4 lower_top 627.2 lower_first [(238.9199981689453, 627.1563110351562, 265.4911804199219, 638.9715576171875, 'ABC,', 21, 0, 7), (416.64019775390625, 627.1563110351562, 428.37860107421875, 638.963623046875, 'ax', 21, 0, 14), (440.16009521484375, 627.1563110351562, 451.77838134765625, 638.963623046875, 'by', 21, 0, 16)]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "        if upper_bottom>=lower_top-0.5:\n            # Limit the 2-D search to the actual semantic collision rather", "new_string": "        if IS_MATHS and marker and upper_bottom>=lower_top-0.5:\n            # a raised integral limit / superscript on the child's own row\n            # ('(i) Use the substitution ... I = integral_1^2 ...', 9709/31/M/J/07\n            # Q7) is a separate PDF block and was taken for stem content.  When\n            # the ink block holding the marker row has a white run above it and\n            # holds no prose row of its own, cut in that run instead of a 2-D seam.\n            yc=maths_row_gap_cut(pno,anchor['y'],max(m[3] for m in marker),y_prev)\n            if yc is not None:\n                return yc\n        if upper_bottom>=lower_top-0.5:\n            # Limit the 2-D search to the actual semantic collision rather"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "    def semantic_cut_before_anchor(pno,y_prev,anchor,owner_pair=None):", "new_string": "    def maths_row_gap_cut(pno,ay,row_bottom,y_prev):\n        \"\"\"Maths: a cut in the white run directly above the ink block that holds\n        a labelled row (its raised limits / indices / numerators included), or\n        None when that block rises more than 25 pt, has no white run above it\n        inside (y_prev, ay), or contains a prose row (a stem line touching it).\"\"\"\n        ink=INK[pno]\n        rt,_=ink.extent(ay,row_bottom)\n        if rt is None:\n            return None\n        r=ink._r(rt); lo=ink._r(y_prev)\n        while r>lo and ink.ink[r-1]>0:\n            r-=1\n        top=ink._p(r)\n        if top<ay-25 or r<=lo:\n            return None\n        e=r-1\n        while e>lo and ink.ink[e]==0:\n            e-=1\n        if r-1-e<3 or e<=lo:\n            return None          # no white run of >= 3 px with content above it\n        raised=[w for w in W[pno] if top-1<=(w[1]+w[3])/2<ay-2]\n        if len([w for w in raised if re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',w[4]))])>=2:\n            return None\n        return max(ink._p((e+r)//2),top-PAD_PT)\n    def semantic_cut_before_anchor(pno,y_prev,anchor,owner_pair=None):"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_cov.txt --no-sheets --workers 8 2>&1 | tail -1; ~/.venvs/alevel/bin/python -I /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/cls.py mth_t
```

<details><summary>result</summary>

```
this run: PASS 139 / 166; run total PASS 139 / 166
10 ('slice',) 23s-11 25s-12 25s-15 09w-52 11w-51 11w-52 11w-63 14w-21 14w-23 23w-51
8 ('blank',) 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52
6 ('miss',) 11s-53 18s-41 17w-61 19w-13 21w-61 21w-63
2 ('dupS',) 22s-33 17w-32
1 ('FURNITURE-IN-CROP',) 14s-13
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 10:59:47

139/166 coverage holds pass. Looking at the 10 slice-only papers.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 23s-11 25s-12 25s-15 09w-52 11w-51 11w-52 11w-63 14w-21 14w-23 23w-51; do echo "== $p $(grep -v '^expected\|^pages' AL-MTH-$p-QP/gates.log | head -3 | tr '\n' ' ')"; done
```

<details><summary>result</summary>

```
== 23s-11   SLICED-BOUNDARY (9, 'Q7.b', 450.1, 4) 
== 25s-12   SLICED-BOUNDARY (6, 'Q5.b', 441.0, 4) 
== 25s-15   SLICED-BOUNDARY (14, 'Q9.b', 686.2, 3) 
== 09w-52   SLICED-BOUNDARY (3, 'Q3', 74.5, 5) 
== 11w-51   SLICED-BOUNDARY (3, 'Q4.iii.stem', 373.1, 953) 
== 11w-52   SLICED-BOUNDARY (3, 'Q4.iii.stem', 373.1, 953) 
== 11w-63   SLICED-BOUNDARY (3, 'Q5.stem', 76.7, 2) 
== 14w-21   SLICED-BOUNDARY (3, 'Q6.stem', 276.3, 9) 
== 14w-23   SLICED-BOUNDARY (3, 'Q6.stem', 276.3, 9) 
== 23w-51   SLICED-BOUNDARY (3, 'Q1.stem', 78.2, 3)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; for a in "23s-11 9 450" "09w-52 3 74.5" "11w-51 3 373" "14w-21 3 276"; do set -- $a; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-$1-QP $2 $3 35 | head -4; cp show.png s_$1.png; done
```

<details><summary>result</summary>

```
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/show.py", line 4, in <module>
    run,prefix,pno,y=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]); h=float(sys.argv[5]) if len(sys.argv)>5 else 60
                                                                    ~~~~~~~~^^^
IndexError: list index out of range
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/show.py", line 4, in <module>
    run,prefix,pno,y=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]); h=float(sys.argv[5]) if len(sys.argv)>5 else 60
                                                                    ~~~~~~~~^^^
IndexError: list index out of range
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/show.py", line 4, in <module>
    run,prefix,pno,y=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]); h=float(sys.argv[5]) if len(sys.argv)>5 else 60
                                                                    ~~~~~~~~^^^
IndexError: list i
… [657 more characters trimmed]
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; for a in "23s-11 9 450" "09w-52 3 74.5" "11w-51 3 373" "14w-21 3 276"; do set -- ${=a}; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-$1-QP $2 $3 35 | head -4; cp show.png s_$1.png; done
```

<details><summary>result</summary>

```
Q7.b [40.0, 233.04, 560.0, 450.08] [231.6, 450.08]
show.png
Q3 [40.0, 74.52, 560.0, 272.88] [77.68, 275.79]
show.png
Q4.iii.stem [40.0, 177.84, 560.0, 373.05] [175.2, 383.26]
Q4.iii [40.0, 390.48, 560.0, 412.08] [383.26, 414.88]
show.png
Q5.ii [40.0, 131.76, 560.0, 242.16] [129.84, 244.82]
Q6.stem [40.0, 276.3, 560.0, 417.36] [276.3, 418.88]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s_23s-11.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s_11w-51.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s_14w-21.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                if rt>=ay-PAD_PT+1 and all(out[i][3]<=rt-1 for i in prev):
                    continue         # nothing above the usual start"""
new="""                if all(out[i][2]<=rt-1 for i in mine) and all(out[i][3]<=rt-1 for i in prev):
                    continue         # the row's ink is already inside its own crop only"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-23s-11-QP 9 400 110 >/dev/null; cp show.png s1.png
```

<details><summary>result</summary>

```
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_s23_qp_11.pdf'); p=d[8]
p.get_pixmap(dpi=50).save('s2.png')
for dr in p.get_drawings():
  r=dr['rect']
  if r.y1>400: print(r, len(dr['items']))
for w in p.get_text('words'):
  if w[1]>430: print(w[:5])
"; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; SPLITTER_DEBUG_EMITS=Q7 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s23_qp_11.pdf $S/t3 AL-MTH-23s-11-QP 2>&1 | grep DEBUG_EMIT
```

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s2.png"}
```

<details><summary>result</summary>

```
Rect(150.15721130371094, 428.5711975097656, 481.7615966796875, 428.5711975097656) 1
Rect(475.1855773925781, 426.17718505859375, 481.7615661621094, 430.9652099609375) 3
Rect(150.15721130371094, 275.5231628417969, 150.15721130371094, 581.620361328125) 1
Rect(226.6811981201172, 428.5711975097656, 226.6811981201172, 432.39801025390625) 1
Rect(303.2063903808594, 428.5711975097656, 303.2063903808594, 432.39801025390625) 1
Rect(379.7303771972656, 428.5711975097656, 379.7303771972656, 432.39801025390625) 1
Rect(456.25439453125, 428.5711975097656, 456.25439453125, 432.39801025390625) 1
(224.11990356445312, 432.5073547363281, 229.6566619873047, 443.71533203125, 'π')
(297.4399108886719, 431.1817932128906, 308.9766540527344, 443.71533203125, '2π')
(373.9999084472656, 431.1817932128906, 385.4165344238281, 443.71533203125, '3π')
(450.4397888183594, 431.1817932128906, 461.9765319824219, 443.71533203125, '4π')
(150.91990661621094, 431.42181396484375, 156.9161834716797, 443.01544189453125, '0')
(72.83985900878906, 607.26611328125, 85.8792953491211, 618.6446533203125, '(c)')
(96.35952758789062, 607.3995971679688, 119.58546447753906, 618.778076171875, 'State')
(122.51962280273438, 607.3995971679688, 136.87046813964844, 618.778076171875, 'the')
(139.80462646484375, 607.3995971679688, 175.654052734375, 618.778076171875, 'number')
(178.57472229003906, 607.3995971679688, 188.0140380859375, 618.778076171875, 'of')
(190.93470764160156, 607.3995971679688, 233.0881805419922, 618.778076171875, 'solution
… [3209 more characters trimmed]
```
</details>

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n "$(grep -n '^def trim_bottom_border' al_qp_splitter.py | cut -d: -f1),+62p" al_qp_splitter.py
```

<details><summary>result</summary>

```
def trim_bottom_border(pix, page=None, cy0=None, known_stops=None):
    """Remove an answer-box top border (full-width line at bottom edge, white
    below, no closing verticals above). Returns a PIL-free cropped pixmap array."""
    arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.stride)
    ch=pix.n
    W=pix.width; H=pix.height
    gray=arr[:, :W*ch].reshape(H,W,ch)[:,:,:min(3,ch)].mean(axis=2)
    dark=gray<120
    rowfrac=dark.sum(axis=1)/W
    cut=None
    for i in range(H-1, max(0,H-46), -1):
        if rowfrac[i]>0.5:
            below=rowfrac[i+3:]
            if below.size==0 or below.max()<0.02:
                # Closing rectangle? Look for ANY continuous vertical rule in
                # the band just above the line -- a table's or grid's side and
                # column rules are rarely at the crop's extreme edges (the
                # table is inset from the margin), so checking only the far
                # left/right columns misses them and the box loses its bottom
                # border, violating bar #7. An answer-box top border has no
                # verticals above it at all.
                band=dark[max(0,i-22):i+1, :]
                if band.size:
                    # A genuine closing rectangle has a vertical rule that is
                    # CONNECTED to this horizontal row. A nearby mark token
                    # such as "[6]" can also have a tall dark stroke, but it
                    # stops above the rule and must
… [2132 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""    for i in range(H-1, max(0,H-46), -1):
        if rowfrac[i]>0.5:
            below=rowfrac[i+3:]"""
new="""    # Maths: answer-box borders span the whole body width; a diagram's ground
    # line under a toppling solid (0.6 of the width, 9709/51/O/N/11 Q4) is content
    full=0.85 if IS_MATHS else 0.5
    for i in range(H-1, max(0,H-46), -1):
        if rowfrac[i]>full:
            below=rowfrac[i+3:]"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
echo ok
```

<details><summary>result</summary>

```
ok
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:01:06

Now extending a maths crop over a drawing (e.g. a sketch axis) that starts inside it and runs past its bottom, when no other crop starts before the drawing ends.

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "            emits=maths_bracket_hints(emits)\n", "new_string": "            emits=maths_bracket_hints(emits)\n            emits=maths_drawings_across_bottom(emits)\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "    def maths_bracket_hints(emits):", "new_string": "    def maths_drawings_across_bottom(emits):\n        \"\"\"Maths: a vector drawing that starts inside a crop and runs on below\n        its end -- the y-axis of blank sketch axes below the x-axis labels\n        ('(b) Sketch the curve.', 9709/11/M/J/23 Q7) -- is kept whole (blank\n        answer grids stay in their leaf, user decision 2026-10-20), unless\n        another crop starts before the drawing ends.\"\"\"\n        out=list(emits)\n        for i,(lab,p,y0,y1) in enumerate(out):\n            starts=[e[2] for j,e in enumerate(out) if j!=i and e[1]==p and e[2]>y0+1]\n            nxt=min(starts,default=min(CONTENT_BOTTOM,FOOTER_Y))\n            low=[d['rect'] for d in doc[p].get_drawings() if d.get('rect') is not None\n                 and y0-2<=d['rect'].y0<y1-2 and d['rect'].y1>y1+1 and d['rect'].height<400\n                 and CONTENT_L-5<=d['rect'].x0 and d['rect'].x1<=CONTENT_R+15\n                 and not (d.get('fill') in ((1,1,1),(1.0,1.0,1.0)) and d.get('color') is None)]\n            if not low:\n                continue\n            bot=max(r.y1 for r in low)\n            if bot+2>=nxt or first_stop(p,y1)<bot:\n                continue\n            if os.environ.get('AL_DEBUG_ORPHAN'):\n                print('MATHS-DRAWING-BELOW',p+1,lab,round(y1,1),'->',round(bot+2,1),file=sys.stderr)\n            out[i]=(lab,p,y0,bot+2)\n        return out\n\n    def maths_bracket_hints(emits):"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_cov.txt --no-sheets --workers 8 2>&1 | tail -1; ~/.venvs/alevel/bin/python -I /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/cls.py mth_t; grep -h "DRAWING-BELOW" ~/rootatom_data/ALEVEL/splits/mth_t/*/splitter.log | wc -l
```

<details><summary>result</summary>

```
this run: PASS 144 / 166; run total PASS 144 / 166
8 ('blank',) 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52
6 ('miss',) 11s-53 18s-41 17w-61 19w-13 21w-61 21w-63
5 ('slice',) 09w-52 11w-63 14w-21 14w-23 23w-51
2 ('dupS',) 22s-33 17w-32
1 ('FURNITURE-IN-CROP',) 14s-13
       3
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 09w-52 11w-63 14w-21 23w-51; do echo "== $p $(grep -v '^expected\|^pages' AL-MTH-$p-QP/gates.log | head -3 | tr '\n' ' ')"; grep RAISED AL-MTH-$p-QP/splitter.log; done; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-14w-21-QP 3 276 30; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_w14_qp_21.pdf')
for w in d[2].get_text('words'):
  if 250<w[1]<300: print(w[:5])
for dr in d[2].get_drawings():
  if 250<dr['rect'].y0<300: print(dr['rect'])
"
```

<details><summary>result</summary>

```
== 09w-52   SLICED-BOUNDARY (3, 'Q3', 74.5, 5) 
== 11w-63   SLICED-BOUNDARY (3, 'Q5.stem', 76.7, 2) 
== 14w-21   SLICED-BOUNDARY (3, 'Q6.stem', 276.3, 9) 
MATHS-RAISED-ROW 2 3 424.8 418.8
== 23w-51   SLICED-BOUNDARY (3, 'Q1.stem', 78.2, 3) 
Q6.stem [40.0, 276.3, 560.0, 417.36] [276.3, 418.88]
show.png
(49.319091796875, 263.9194641113281, 55.20409393310547, 275.2979431152344, '6')
(222.7196044921875, 272.3087158203125, 228.16259765625, 284.1599426269531, 'y')
Rect(225.40679931640625, 287.3276062011719, 225.40679931640625, 355.3507995605469)
Rect(222.67080688476562, 287.32757568359375, 228.1416015625, 294.8443603515625)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                rt=ink._p(r)
                mine=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]==f"Q{q['label']}"
                      and min(ay-PAD_PT,rt)-2*PAD_PT<=e[2]<=ay+1]
"""
new="""                rt=ink._p(r)
                mine=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]==f"Q{q['label']}"
                      and min(ay-PAD_PT,rt)-2*PAD_PT<=e[2]<=q.get('row_y1',ay)+2]
                for i in mine:       # a crop opening inside an ink block (a diagram's
                    r=ink._r(out[i][2])   # 'y' label beside the number row, 9709/21/O/N/14 Q6)
                    if ink.ink[r]>0:
                        while r>lo and ink.ink[r-1]>0:
                            r-=1
                        rt=min(rt,ink._p(r))
"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; for a in "09w-52 3 74.5" "11w-63 3 76.7" "23w-51 3 78.2"; do set -- ${=a}; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-$1-QP $2 $3 25 | head -3; cp show.png s_$1.png; done
```

<details><summary>result</summary>

```
Q3 [40.0, 74.52, 560.0, 272.88] [77.68, 275.79]
show.png
Q5.stem [40.0, 76.68, 560.0, 469.2] [77.82, 470.99]
show.png
Q1.stem [40.0, 78.2, 560.0, 517.2] [78.2, 519.36]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s_09w-52.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s_23w-51.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_w09_qp_52.pdf 9709_w11_qp_63.pdf 9709_w23_qp_51.pdf 9709_w14_qp_21.pdf 9709_w14_qp_23.pdf --no-sheets --workers 5 2>&1 | tail -6
```

<details><summary>result</summary>

```
[1/5] HOLD 9709_w14_qp_23.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q3.a and Q3.b on page 2 have no proven separator; cur_crop=418.80..440.04 cur_ink=424.80..439.68 cur_semantic=418.80..440.04; next_c
[2/5] HOLD 9709_w14_qp_21.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q3.a and Q3.b on page 2 have no proven separator; cur_crop=418.80..440.04 cur_ink=424.80..439.68 cur_semantic=418.80..440.04; next_c
[3/5] PASS 9709_w11_qp_63.pdf crops=23 
[4/5] PASS 9709_w09_qp_52.pdf crops=20 
[5/5] PASS 9709_w23_qp_51.pdf crops=26 
this run: PASS 3 / 5; run total PASS 147 / 166
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; SPLITTER_DEBUG_EMITS=Q3 AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w14_qp_21.pdf $S/t3 AL-MTH-14w-21-QP 2>&1 | grep -v "^   " | head; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_w14_qp_21.pdf')
d[1].get_pixmap(dpi=100,clip=f.Rect(0,380,595,480)).save('$S/s1.png')
for w in d[1].get_text('words'):
  if 400<w[1]<450: print(w[:5])
"
```

<details><summary>result</summary>

```
DEBUG_EMIT ('Q3.a', 1, 418.79999999999995, np.float64(455.52))
DEBUG_EMIT ('Q3.b', 1, 457.2, np.float64(504.31999999999994))
MATHS-FIGURE 2 443.0 457.2 -> Q3.b
MATHS-RAISED-ROW 2 2 146.9 140.9
MATHS-RAISED-ROW 2 3 424.8 418.8
MATHS-RAISED-ROW 3 6 265.4 259.4
Traceback (most recent call last):
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 5058, in <module>
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 4788, in main
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 4739, in bind_seam
(49.319305419921875, 430.47930908203125, 55.204307556152344, 441.8577880859375, '3')
(72.83576965332031, 430.47930908203125, 86.59490203857422, 441.8577880859375, '(a)')
(96.3597183227539, 430.9995422363281, 117.96945190429688, 442.3780517578125, 'Find')
(120.83999633789062, 422.16119384765625, 127.16499328613281, 453.6431884765625, 'Ó')
(131.2799072265625, 430.99957275390625, 137.16490173339844, 442.3780822753906, '4')
(138.96571350097656, 429.0688781738281, 158.69223022460938, 442.3780822753906, 'cos2')
(164.57989501953125, 429.17572021484375, 168.99365234375, 437.7095947265625, '1')
(164.57989501953125, 422.17071533203125, 175.671630859375, 453.63555908203125, '21')
(182.39990234375, 422.17071533203125, 197.3424072265625, 453.63555908203125, 'd1.')
(531.7196044921875, 430.99957275390625, 545.4788208007812, 442.3780822753906, '[3]')
Shell cwd was reset to /Users/nitya
… [98 more characters trimmed]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                      and min(ay-PAD_PT,rt)-2*PAD_PT<=e[2]<=q.get('row_y1',ay)+2]
"""
new="""                      and min(ay-PAD_PT,rt)-2*PAD_PT<=e[2]<=q.get('row_y1',ay)+2]
                mine=[i for i in mine if out[i][2]==min(out[j][2] for j in mine)]   # the question's first crop
"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_w14_qp_21.pdf 9709_w14_qp_23.pdf --no-sheets --workers 5 2>&1 | tail -3
```

<details><summary>result</summary>

```
[1/2] PASS 9709_w14_qp_21.pdf crops=16 
[2/2] PASS 9709_w14_qp_23.pdf crops=16 
this run: PASS 2 / 2; run total PASS 149 / 166
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:04:20

149/166. Now the 8 "blank band" holds (all recent Paper 5).

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 22m-52 20s-52 21s-51 22s-51 23s-51 20w-51 21w-53 22w-52; do echo "$p $(grep BLANK-BAND AL-MTH-$p-QP/gates.log | head -2| tr '\n' ' ')"; done
```

<details><summary>result</summary>

```
22m-52   BLANK-BAND ('Q3.a', 63) 
20s-52   BLANK-BAND ('Q3.b', 65) 
21s-51   BLANK-BAND ('Q5.a', 82) 
22s-51   BLANK-BAND ('Q3.a', 153) 
23s-51   BLANK-BAND ('Q5.a', 64) 
20w-51   BLANK-BAND ('Q6.a', 51) 
21w-53   BLANK-BAND ('Q3.a', 77) 
22w-52   BLANK-BAND ('Q4.a', 139)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits/mth_t; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
fs=['AL-MTH-22m-52-QP/AL-MTH-22m-52-QP-Q3.a.png','AL-MTH-22s-51-QP/AL-MTH-22s-51-QP-Q3.a.png','AL-MTH-20w-51-QP/AL-MTH-20w-51-QP-Q6.a.png']
ims=[Image.open(f) for f in fs]; W=max(i.width for i in ims); H=sum(i.height+20 for i in ims)
c=Image.new('RGB',(W,H),(200,200,200)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+20
c.resize((W//2,H//2)).save('$S/v3.png')"
```

<details><summary>result</summary>

```
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/v3.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### User — 2026-10-20 11:04:29

[Image: original 795x2230, displayed at 713x2000. Multiply coordinates by 1.12 to map to original image.]

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "            emits=maths_drawings_across_bottom(emits)\n", "new_string": "            emits=maths_drawings_across_bottom(emits)\n            emits=maths_gap_above_grid(emits)\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "    def maths_bracket_hints(emits):", "new_string": "    def maths_gap_above_grid(emits):\n        \"\"\"Maths: '(a) Draw a histogram ... [4]', blank working space, then the\n        printed graph-paper grid (9709/52/F/M/22 Q3(a)).  The grid stays in the\n        leaf (user decision 2026-10-20); the blank band above it (> 40 pt) is\n        cut out: the leaf becomes two segments, prompt + grid.\"\"\"\n        out=[]\n        for lab,p,y0,y1 in emits:\n            big=[d['rect'] for d in doc[p].get_drawings() if d.get('rect') is not None\n                 and d['rect'].width>100 and d['rect'].height>60 and y0+10<d['rect'].y0<y1]\n            if lab.endswith('.stem') or not big:\n                out.append((lab,p,y0,y1)); continue\n            g=min(r.y0 for r in big)\n            ink=INK[p]; a=ink._r(y0); b=ink._r(g)\n            zs=np.where(ink.ink[a:b+1]==0)[0]\n            runs=[]\n            if len(zs):\n                s=q=zs[0]\n                for z in zs[1:]:\n                    if z==q+1: q=z; continue\n                    runs.append((s,q)); s=q=z\n                runs.append((s,q))\n            runs=[(s,e) for s,e in runs if s>0 and ink.ink[a:a+s].any() and (e-s)/SC>40]\n            if not runs:\n                out.append((lab,p,y0,y1)); continue\n            s,e=max(runs,key=lambda r:r[1]-r[0])\n            if os.environ.get('AL_DEBUG_ORPHAN'):\n                print('MATHS-GRID-GAP',p+1,lab,round(ink._p(a+s),1),round(ink._p(a+e),1),file=sys.stderr)\n            out.append((lab,p,y0,ink._p(a+s)+3))\n            out.append((lab,p,ink._p(a+e)-3,y1))\n        return out\n\n    def maths_bracket_hints(emits):"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; L=""; for p in m22_qp_52 s20_qp_52 s21_qp_51 s22_qp_51 s23_qp_51 w20_qp_51 w21_qp_53 w22_qp_52; do L="$L 9709_$p.pdf"; done; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t ${=L} --no-sheets --workers 8 2>&1 | tail -9; grep -h GRID-GAP ~/rootatom_data/ALEVEL/splits/mth_t/*/splitter.log
```

<details><summary>result</summary>

```
[1/8] PASS 9709_m22_qp_52.pdf crops=28 
[2/8] PASS 9709_s22_qp_51.pdf crops=27 
[3/8] PASS 9709_s21_qp_51.pdf crops=21 
[4/8] PASS 9709_w22_qp_52.pdf crops=26 
[5/8] PASS 9709_w20_qp_51.pdf crops=26 
[6/8] PASS 9709_w21_qp_53.pdf crops=27 
[7/8] PASS 9709_s23_qp_51.pdf crops=27 
[8/8] PASS 9709_s20_qp_52.pdf crops=26 
this run: PASS 8 / 8; run total PASS 157 / 166
MATHS-GRID-GAP 8 Q6.a 165.1 216.0
MATHS-GRID-GAP 8 Q5.a 152.2 234.2
MATHS-GRID-GAP 5 Q3.b 116.2 180.5
MATHS-GRID-GAP 4 Q3.a 152.2 304.3
MATHS-GRID-GAP 6 Q4.a 165.1 304.3
MATHS-GRID-GAP 5 Q3.a 165.1 227.5
MATHS-GRID-GAP 8 Q5.a 237.1 301.4
MATHS-GRID-GAP 4 Q3.a 165.1 241.9
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/Users/nitya/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-22s-51-QP/AL-MTH-22s-51-QP-Q3.a.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:05:07

Grid crops look right. Before going further, checking the 3 approved Biology papers stay byte-identical.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ls review/bio_regchk splits/bio_regchk 2>&1 | head; ~/.venvs/alevel/bin/python -I -c "
import json;d=json.load(open('review/reviewed_crop_hashes.json'));b=d['bio_b1']
k=[x for x in b if any(s in x for s in ('24s-22','17w-42','13s-52'))];print(k)
v=b[k[0]];print(type(v), str(v)[:300])"
```

<details><summary>result</summary>

```
ls: review/bio_regchk: No such file or directory
ls: splits/bio_regchk: No such file or directory
['AL-BIO-13s-52-QP', 'AL-BIO-24s-22-QP', 'AL-BIO-17w-42-QP']
<class 'dict'> {'AL-BIO-13s-52-QP-Q1.a.png': '5f7b50dfc2569a205e5de6f81b83f23430a1c3974ff062674e86fd65d7971929', 'AL-BIO-13s-52-QP-Q1.b.i.png': 'a665bf05fbe26d58cbe7a657e34b71a2cedaf37c5deccc3d2c13e5e2974f2034', 'AL-BIO-13s-52-QP-Q1.b.ii.png': '1334a8c48ca0638050e6548e99ce749ae227f9309833e6895e1818f244df1dca', 'AL
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cat > $S/bin/biochk.sh <<'EOF'
#!/bin/zsh
# re-split the 3 approved Bio papers into run bio_regchk and compare sha256 with reviewed_crop_hashes['bio_b1']
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts
rm -rf ~/rootatom_data/ALEVEL/splits/bio_regchk ~/rootatom_data/ALEVEL/review/bio_regchk
~/.venvs/alevel/bin/python -I al_run_papers.py bio_regchk 9700_s24_qp_22.pdf 9700_w17_qp_42.pdf 9700_s13_qp_52.pdf --no-sheets --workers 3 | tail -1
~/.venvs/alevel/bin/python -I -c "
import json,hashlib,glob,os
d=json.load(open(os.path.expanduser('~/rootatom_data/ALEVEL/review/reviewed_crop_hashes.json')))['bio_b1']
for p in ('AL-BIO-24s-22-QP','AL-BIO-17w-42-QP','AL-BIO-13s-52-QP'):
    fs={os.path.basename(f):hashlib.sha256(open(f,'rb').read()).hexdigest() for f in glob.glob(os.path.expanduser(f'~/rootatom_data/ALEVEL/splits/bio_regchk/{p}/*.png'))}
    print(p,'IDENTICAL' if fs==d[p] else 'DIFF', len(fs), len(d[p]))
"
EOF
chmod +x $S/bin/biochk.sh; $S/bin/biochk.sh
```

<details><summary>result</summary>

```
this run: PASS 3 / 3; run total PASS 3 / 3
AL-BIO-24s-22-QP IDENTICAL 43 43
AL-BIO-17w-42-QP IDENTICAL 56 56
AL-BIO-13s-52-QP IDENTICAL 17 17
```
</details>

### Assistant — 2026-10-20 11:05:30

All 3 Biology papers byte-identical. Now checking the 479 maths PASS papers don't regress (scratch run mth_p, background).

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; df -h ~ | tail -1; rm -rf ~/rootatom_data/ALEVEL/splits/mth_p ~/rootatom_data/ALEVEL/review/mth_p; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_p --list ~/rootatom_data/ALEVEL/review/mth/pass_b1.txt --no-sheets --workers 8 > /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_p.log 2>&1
```

<details><summary>result</summary>

```
Command running in background with ID: bh4qqp098. Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bh4qqp098.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e; directory changes made by the backgrounded command do not apply to subsequent commands.
```
</details>

### Assistant — 2026-10-20 11:05:38

While that runs, looking at the leaf-mismatch bucket: commit 1fecba5 implemented "separately marked (a)/(b) under a roman are leaves" in both splitter and gate; checking how each decides.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline; git show 1fecba5 | head -150
```

<details><summary>result</summary>

```
commit 1fecba5207fbf5958e2ed5b00a9a9f993b0248e0
Author: MasterClassmate3004 <77794181+MasterClassmate3004@users.noreply.github.com>
Date:   Tue Oct 20 14:25:47 2026 +0530

    Maths: separately marked (a)/(b) under a roman are leaves (user decision 2026-10-20)
    
    - splitter (IS_MATHS): letter sub-parts under a roman-as-part become its
      children -> Q6.ii.stem, Q6.ii.a, Q6.ii.b (9709/04/O/N/07 Q6(ii))
    - leaf gate: for AL-MTH/AL-FMT prefixes a letter run under a roman is a
      fourth level, kept only when separately marked (same rule as numbered
      tasks); numbered-task check guarded for letter state
    - blank answer grids stay in their leaf (user decision)
    - calibration 7/7 PASS; approved Bio leaf-gate results unchanged
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/ALEVEL/scripts/al_qp_splitter.py b/ALEVEL/scripts/al_qp_splitter.py
index d35a1be..790e681 100644
--- a/ALEVEL/scripts/al_qp_splitter.py
+++ b/ALEVEL/scripts/al_qp_splitter.py
@@ -1254,10 +1254,15 @@ def main():
         qs=[i for i,a in enumerate(seq) if a['kind']=='Q']+[len(seq)]
         for qa,qb in zip(qs,qs[1:]):
             grp_=seq[qa:qb]
-            if not any(a['kind']=='PART' for a in grp_):
+            if not any(a['kind']=='PART' for a in grp_) and any(a['kind']=='ROMAN' for a in grp_):
                 for a in grp_:
                     if a['kind']=='ROMAN':
                         a['kind']='PART'
+                    elif a['kind']=='SUB
… [3173 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f,re
for src,q in [('9709_m16_qp_72.pdf','6'),('9709_s15_qp_51.pdf','5'),('9709_s06_qp_4.pdf','4'),('9709_s13_qp_41.pdf','7'),('9709_s17_qp_72.pdf','5')]:
  d=f.open('source_papers/canonical/'+src)
  for i,p in enumerate(d):
    ws=p.get_text('words')
    qs=[w for w in ws if w[4]==q and w[0]<60]
    if not qs: continue
    y=qs[0][1]
    print('==',src,'p',i+1)
    for w in ws:
      if y-2<w[1]<y+250 and (re.fullmatch(r'\(\w+\)|\[\d+\]',w[4]) or w[0]<60): print('   ',round(w[0],1),round(w[1],1),w[4])
    break
"
```

<details><summary>result</summary>

```
== 9709_m16_qp_72.pdf p 2
    49.3 587.9 6
    79.3 626.9 (i)
    531.8 627.4 [3]
    76.1 652.8 (ii)
    96.4 652.8 (a)
    531.7 666.4 [4]
    96.4 686.9 (b)
    531.7 687.4 [1]
    72.8 712.8 (iii)
    531.7 752.4 [3]
    49.3 798.5 ©
    56.4 798.5 UCLES
== 9709_s15_qp_51.pdf p 3
    49.3 369.6 5
    79.3 421.5 (i)
    531.7 421.7 [2]
    76.1 487.3 (ii)
    96.3 487.3 (a)
    531.7 487.4 [2]
    96.3 508.3 (b)
    531.7 508.4 [4]
    49.3 547.3 6
    79.3 612.9 (i)
== 9709_s06_qp_4.pdf p 3
    49.4 65.8 4
== 9709_s13_qp_41.pdf p 4
    49.3 65.8 7
    79.4 118.5 (i)
    531.7 118.6 [3]
    76.1 144.5 (ii)
    531.7 144.6 [4]
    72.8 170.5 (iii)
    96.4 191.5 (a)
    96.4 212.5 (b)
    531.7 225.6 [2]
    73.6 249.4 (iv)
    531.7 249.6 [2]
== 9709_s17_qp_72.pdf p 6
    49.3 65.5 5
    79.3 247.4 (i)
    96.4 268.3 (a)
    96.4 289.0 (b)
    96.4 309.9 (c)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 1236,1275p al_qp_splitter.py; sed -n 95,170p al_verify_leaves.py
```

<details><summary>result</summary>

```
    # roman run and silently drops `(ii)` (0580_s13_qp_43 Q3(c)).
    seq=drop_false_igcse_questions(seq)
    if IS_MATHS:
        # '6 (i) A man walks ...' inline with the number reads as part '(i)';
        # with '(ii)' following in the same question it is the first roman
        # (9709/04/O/N/07 Q6)
        qs=[i for i,a in enumerate(seq) if a['kind']=='Q']+[len(seq)]
        for qa,qb in zip(qs,qs[1:]):
            grp_=seq[qa:qb]
            parts_=[a for a in grp_ if a['kind']=='PART']
            if parts_ and all(a['label']=='i' for a in parts_) and any(
                    a['kind']=='ROMAN' and a['label']=='ii' for a in grp_):
                for a in parts_:
                    a['kind']='ROMAN'
    seq=drop_false_romans(seq)
    seq=drop_false_igcse_subparts(seq,M)
    seq=drop_false_igcse_parts(seq)
    if IS_MATHS:
        # Older 9709 papers number sub-parts '3 (i) ... (ii) ...' with no letter
        # level (9709/62/M/J/13): a question with romans but no (a)/(b) has the
        # romans as its parts -> Q3.i, Q3.ii (what the leaf gate expects)
        qs=[i for i,a in enumerate(seq) if a['kind']=='Q']+[len(seq)]
        for qa,qb in zip(qs,qs[1:]):
            grp_=seq[qa:qb]
            if not any(a['kind']=='PART' for a in grp_) and any(a['kind']=='ROMAN' for a in grp_):
                for a in grp_:
                    if a['kind']=='ROMAN':
                        a['kind']='PART'
                    elif a['kind']=='SUBPART' and a['label'].isalpha():
 
… [4885 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "marks.append\|m.append\|marks=\[\]" al_qp_splitter.py | head; sed -n 1205,1216p al_qp_splitter.py; grep -n "def drop_false_igcse_subparts" -A20 al_qp_splitter.py | grep -n "marks" | head
```

<details><summary>result</summary>

```
347:    anchors=[]; marks=[]; stops=([reference_cut] if reference_cut is not None else []); dot_rows=[]
350:        if MARK_RE.match(w[4]): marks.append((w[1],w[3]))
        for x in a: x['pno']=pno
        if IS_ALEVEL:
            # a roman label with another roman label on its row is an inline
            # label of a figure ('(i) glycine  (ii) aspartic acid  (iii)
            # lysine', 9701/06/M/J/04 Q6(b)), not a subpart
            # (only a LATER numeral to the right: '(iii) Use your answer to
            # (ii)' is a cross-reference, 9701/22/F/M/16)
            def _succ(lab_):
                return ROMAN_ORDER[ROMAN_ORDER.index(lab_)+1] if lab_ in ROMAN_ORDER[:-1] else None
            a=[x for x in a if not (x['kind']=='ROMAN' and any(
                abs(v[1]-x['y'])<4 and v[0]-x.get('x',0)>40 and
                v[4]==f"({_succ(x['label'])})" for v in w))]
1:619:def drop_false_igcse_subparts(seq,marks=None):
19:637-        if valid and IS_ALEVEL and marks is not None and labels[0]=='1':
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; SPLITTER_DEBUG_ANCHORS=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_m16_qp_72.pdf $S/t4 AL-MTH-16m-72-QP 2>&1 | grep KEPT | awk '$2==2'; sed -n 470,515p al_qp_splitter.py
```

<details><summary>result</summary>

```
KEPT_ANCHOR 2 Q 1 49.32 65.44
KEPT_ANCHOR 2 Q 2 49.32 130.36
KEPT_ANCHOR 2 Q 3 49.32 195.4
KEPT_ANCHOR 2 PART i 79.32 273.4
KEPT_ANCHOR 2 PART ii 76.08 299.44
KEPT_ANCHOR 2 Q 4 49.32 351.4
KEPT_ANCHOR 2 Q 5 49.32 417.16
KEPT_ANCHOR 2 PART i 79.32 483.88
KEPT_ANCHOR 2 PART ii 76.08 509.92
KEPT_ANCHOR 2 PART iii 72.84 548.92
KEPT_ANCHOR 2 Q 6 49.32 587.92
KEPT_ANCHOR 2 PART i 79.32 626.92
KEPT_ANCHOR 2 PART ii 76.08 652.84
KEPT_ANCHOR 2 PART iii 72.84 712.84
                # make it a cross-reference ('in (i) may', 9702/42/M/J/19)
                if IS_ALEVEL and any(abs(v[1]-left[1])<3 and v[2]<=x0 and v[0]>=CONTENT_L
                                     for v in words if v is not left):
                    pass
                else:
                    anchors.append({'kind':'ROMAN','label':m.group(1),'y':left[1],'row_y1':ry1,'x':x0})
        lead_is_q = bool(Q_RE.match(tok)) and x0<72
        for ti,t in enumerate(ws[1:],1):
            if IS_ALEVEL and re.match(r'^\d\.$',t[4]) and 108<=t[0]<135 and \
                    not (all(re.fullmatch(r'[.\u2026]+',v[4]) for v in ws if v[0]>t[0]) and
                         sum(leader_run(v[4]) for v in ws if v[0]>t[0])>=10) and \
                    any(PAR_RE.match(v[4]) and v[4][1:-1] in ROMANS for v in ws if v[0]<t[0]):
                # '(iii) 1. ...' -- first numbered task inline with its roman
                # (9702/22/M/J/11 Q6(a)(iii))
                anchors.append({'kind':'SUBPART','label':t[4][0],'y':t[1],
            
… [2211 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 418,469p al_qp_splitter.py
```

<details><summary>result</summary>

```
            # empty crop after the number row is skipped.
            visual_row=[left]+[t for t in words
                               if t is not left and t[0]>=left[2]-1 and
                               abs(t[1]-left[1])<3]
            rest=[t for t in visual_row[1:]
                  if not MARK_RE.match(t[4]) and not PAR_RE.match(t[4])]
            resttxt=' '.join(t[4] for t in rest)
            inline = bool(re.search(r'[A-Za-z]', resttxt)) and 'Maximum mark' not in resttxt
            inline_lexical_count=sum(
                bool(re.search(r'[A-Za-z]{2,}',t[4])) for t in rest
            )
            font,font_size,font_flags=word_style(left)
            anchors.append({'kind':'Q','label':Q_RE.match(tok).group(1),'y':left[1],
                            'row_y1':max(w[3] for w in visual_row),'x':x0,
                            'font':font,'font_size':font_size,
                            'font_flags':font_flags,'inline':inline,
                            'inline_lexical_count':inline_lexical_count,
                            'nbox':(left[0],left[1],left[2],left[3])})
        else:
            m=PAR_RE.match(tok); ry1=max(w[3] for w in ws)
            # Older A Level papers number fourth-level tasks under a roman:
            # '(i) On Fig. 7.1,  1. draw ... [1]  2. draw ... [1]'
            # (9702/42/M/J/13 Q7(b)(i); 9702/22/M/J/19 Q2(b)(ii) 1.-4.).  Each
            # is separately marked -> a leaf.  Column x~118 pt; the run is
            # validated in dro
… [2165 more characters trimmed]
```
</details>

### Assistant — 2026-10-20 11:06:21

The inline "(a)" right after "(ii)" is never an anchor for A Level, and the splitter's letter→leaf conversion doesn't check separate marking. Fixing both (maths only).

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""            elif lead_is_q and len(mm.group(1))==1 and t[0]<PART_X_MAX:"""
new="""            elif (IS_MATHS and len(mm.group(1))==1 and t[0]<190 and
                  PAR_RE.match(ws[ti-1][4]) and ws[ti-1][4][1:-1] in ROMANS):
                # '(ii) (a) Find ... [4]' -- first letter task inline with its
                # roman (9709/72/F/M/16 Q6(ii)); kept only if separately marked
                anchors.append({'kind':'SUBPART','label':mm.group(1),'y':t[1],
                                'row_y1':max(w[3] for w in ws),'x':t[0]})
            elif lead_is_q and len(mm.group(1))==1 and t[0]<PART_X_MAX:"""
assert s.count(old)==1; s=s.replace(old,new)
old="""            if not any(a['kind']=='PART' for a in grp_) and any(a['kind']=='ROMAN' for a in grp_):
                for a in grp_:"""
new="""            if not any(a['kind']=='PART' for a in grp_) and any(a['kind']=='ROMAN' for a in grp_):
                # letter tasks are leaves only when separately marked: a [n]
                # between each and the next (one shared mark -> the roman is
                # one leaf, 9709/41/M/J/13 Q7(iii)) -- the leaf gate's rule
                runs_=[]
                for a in grp_:
                    if a['kind']=='ROMAN':
                        runs_.append([])
                    elif a['kind']=='SUBPART' and a['label'].isalpha() and runs_:
                        runs_[-1].append(a)
                def marked_(a,b):
                    for pg in range(a['pno'],b['pno']+1):
                        lo=a['y']-3 if pg==a['pno'] else 0
                        hi=b['y'] if pg==b['pno'] else 1e9
                        if any(lo<my<hi for my,_ in M.get(pg,[])):
                            return True
                    return False
                drop_=[id(a) for kids in runs_ if len(kids)<2 or
                       not all(marked_(x,y) for x,y in zip(kids,kids[1:])) for a in kids]
                if drop_:
                    seq=[a for a in seq if id(a) not in drop_]
                    grp_=[a for a in grp_ if id(a) not in drop_]
                for a in grp_:"""
assert s.count(old)==1; s=s.replace(old,new)
open(p,'w').write(s)
EOF
grep -n "^    M=\|M={}\|M\[pno\]" al_qp_splitter.py | head -3
```

<details><summary>result</summary>

```
1223:        A[pno],M[pno],S[pno],W[pno],DOT[pno]=a,m,s,w,dot
1449:        ms=[m for m in M[pno] if y0-2<=m[0]<=y1]
1461:        ms=[m for m in M[pno] if y0-2<=m[0]<=y1]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                if drop_:
                    seq=[a for a in seq if id(a) not in drop_]
                    grp_=[a for a in grp_ if id(a) not in drop_]
"""
new="""                if drop_:
                    dropped_.update(drop_)
                    grp_=[a for a in grp_ if id(a) not in drop_]
"""
assert s.count(old)==1; s=s.replace(old,new)
i=s.index("            if not any(a['kind']=='PART' for a in grp_) and any(a['kind']=='ROMAN' for a in grp_):\n                # letter tasks")
j=s.rindex("        qs=[i for i,a in enumerate(seq) if a['kind']=='Q']+[len(seq)]\n",0,i)
s=s[:j]+"        dropped_=set()\n"+s[j:]
old2="""                    elif a['kind']=='SUBPART' and a['label'].isalpha():
                        # '(ii) ... Find (a) ... [4] (b) ... [1]': separately marked
                        # tasks under a roman-as-part are its leaves -> Q6.ii.a, Q6.ii.b
                        # (user decision 2026-10-20; 9709/04/O/N/07 Q6(ii))
                        a['kind']='ROMAN'
"""
assert s.count(old2)==1
s=s.replace(old2,old2+"        seq=[a for a in seq if id(a) not in dropped_]\n")
open(p,'w').write(s)
EOF
sed -n 1260,1305p al_qp_splitter.py
```

<details><summary>result</summary>

```
        # Older 9709 papers number sub-parts '3 (i) ... (ii) ...' with no letter
        # level (9709/62/M/J/13): a question with romans but no (a)/(b) has the
        # romans as its parts -> Q3.i, Q3.ii (what the leaf gate expects)
        dropped_=set()
        qs=[i for i,a in enumerate(seq) if a['kind']=='Q']+[len(seq)]
        for qa,qb in zip(qs,qs[1:]):
            grp_=seq[qa:qb]
            if not any(a['kind']=='PART' for a in grp_) and any(a['kind']=='ROMAN' for a in grp_):
                # letter tasks are leaves only when separately marked: a [n]
                # between each and the next (one shared mark -> the roman is
                # one leaf, 9709/41/M/J/13 Q7(iii)) -- the leaf gate's rule
                runs_=[]
                for a in grp_:
                    if a['kind']=='ROMAN':
                        runs_.append([])
                    elif a['kind']=='SUBPART' and a['label'].isalpha() and runs_:
                        runs_[-1].append(a)
                def marked_(a,b):
                    for pg in range(a['pno'],b['pno']+1):
                        lo=a['y']-3 if pg==a['pno'] else 0
                        hi=b['y'] if pg==b['pno'] else 1e9
                        if any(lo<my<hi for my,_ in M.get(pg,[])):
                            return True
                    return False
                drop_=[id(a) for kids in runs_ if len(kids)<2 or
                       not all(marked_(x,y) for x,y in zip(kids,kids[1:])) for a in kids]
       
… [1131 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('review/mth_b1/run_summary.csv')))
open('review/mth/holds_leaves.txt','w').write(''.join(x['source']+'\n' for x in r if x['status']=='HOLD' and x['reason'].startswith('leaves')))
"; wc -l < review/mth/holds_leaves.txt; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_leaves.txt --no-sheets --workers 8 2>&1 | grep -v "^\[.*PASS"
```

<details><summary>result</summary>

```
      27
this run: PASS 27 / 27; run total PASS 184 / 193
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:07:23

All 27 leaf holds pass now. The background PASS-regression run picked up mid-run edits, so I'll redo it at the end; checking its status anyway.

**Tool `Bash`**

```
tail -2 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_p.log; grep -c HOLD /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_p.log; grep HOLD /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_p.log | head -20
```

<details><summary>result</summary>

```
[147/479] PASS 9709_s17_qp_41.pdf crops=18 
[148/479] PASS 9709_s17_qp_43.pdf crops=22 
0
```
</details>

### Assistant — 2026-10-20 11:07:31

No regressions so far (148/479 done). Meanwhile re-running the 58 REVIEW_REQUIRED holds with the current code.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('review/mth_b1/run_summary.csv')))
open('review/mth/holds_rr.txt','w').write(''.join(x['source']+'\n' for x in r if x['status']=='HOLD' and x['reason'].startswith('splitter')))
"; wc -l < review/mth/holds_rr.txt; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_rr.txt --no-sheets --workers 6 2>&1 | tail -1; ~/.venvs/alevel/bin/python -I -c "
import csv,collections,re
r=[x for x in csv.DictReader(open('/Users/nitya/rootatom_data/ALEVEL/review/mth_t/run_summary.csv')) if x['status']=='HOLD']
c=collections.Counter(re.sub(r'crops \S+ and \S+|y=[\d.]+|page \d+|cur_.*|Q\d+\S*','',x['reason'])[:90] for x in r)
for k,v in c.most_common(): print(v,k)
"
```

<details><summary>result</summary>

```
      58
this run: PASS 2 / 58; run total PASS 186 / 251
34 splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical  on  have no prove
12 splitter: RuntimeError: REVIEW_REQUIRED: no whitespace around answer row at  on 
9 coverage
6 splitter: RuntimeError: REVIEW_REQUIRED: no  anchor found in IGCSE paper
2 splitter: RuntimeError: REVIEW_REQUIRED: no blank row near  on 
1 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at head of  before 
1 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at foot of  before
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:07:58

Overlap errors dominate (34). Inspecting one (08s-11, Q1 vs Q2.i).

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; grep "08s-11\|04s-11\|10w-21" review/mth_t/run_summary.csv | cut -c1-400; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('source_papers/canonical/9709_s08_qp_1.pdf')
d[1].get_pixmap(dpi=100,clip=f.Rect(0,50,595,200)).save('/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png')
for w in d[1].get_text('words'):
  if 100<w[1]<160: print([round(v,1) if isinstance(v,float) else v for v in w])
"
```

<details><summary>result</summary>

```
9709_s04_qp_1.pdf,AL-MTH-04s-11-QP,HOLD,0,,,splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q2 and Q3.i on page 2 have no proven separator; cur_crop=215.52..225.60 cur_ink=216.00..225.12 cur_semantic=215.52..225.60; next_cro
9709_s08_qp_1.pdf,AL-MTH-08s-11-QP,HOLD,0,,,splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q1 and Q2.i on page 2 have no proven separator; cur_crop=130.08..142.56 cur_ink=132.00..141.12 cur_semantic=130.08..142.56; next_cro
9709_w10_qp_21.pdf,AL-MTH-10w-21-QP,HOLD,0,,,splitter: RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q1 and Q2 on page 2 have no proven separator; cur_crop=117.60..130.08 cur_ink=119.52..128.64 cur_semantic=117.60..130.08; next_crop=
[49.3, 117.9, 55.1, 129.1, '2', 2, 0, 0]
[79.0, 117.9, 89.9, 129.1, '(i)', 2, 1, 0]
[95.6, 117.9, 122.0, 129.2, 'Show', 2, 1, 1]
[125.0, 117.9, 142.6, 129.2, 'that', 2, 1, 2]
[145.6, 117.9, 159.9, 129.2, 'the', 2, 1, 3]
[162.7, 117.9, 203.1, 129.2, 'equation', 2, 1, 4]
[206.0, 117.9, 211.9, 129.2, '2', 2, 1, 5]
[213.7, 115.6, 232.4, 129.2, 'tan2', 2, 1, 6]
[233.8, 117.8, 241.3, 128.7, 'θ', 2, 1, 7]
[242.5, 117.9, 258.1, 129.2, 'cos', 2, 1, 8]
[259.6, 117.8, 267.1, 128.7, 'θ', 2, 1, 9]
[269.5, 117.8, 276.4, 128.7, '=', 2, 1, 10]
[279.5, 117.9, 285.3, 129.2, '3', 2, 1, 11]
[288.2, 117.9, 304.5, 129.2, 'can', 2, 1, 12]
[307.4, 117.9, 318.5, 129.2, 'be', 2, 1, 13]
[321.4, 117.9, 354.7, 129.2, 'written', 2, 1, 14]
[357.6, 117.
… [1479 more characters trimmed]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/s1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; SPLITTER_DEBUG_EMITS=Q AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s08_qp_1.pdf $S/t5 AL-MTH-08s-11-QP 2>&1 | grep -v "^   " | head -12
```

<details><summary>result</summary>

```
DEBUG_EMIT ('Q1', 1, 60.664154052734375, 117.86416625976562)
DEBUG_EMIT ('Q2.i', 1, 110.63999999999999, np.float64(148.32))
DEBUG_EMIT ('Q2.ii', 1, 150.0, 196.94418334960938)
DEBUG_EMIT ('Q3.i', 1, 189.83999999999997, np.float64(215.04))
DEBUG_EMIT ('Q3.ii', 1, 216.71999999999997, 243.2913818359375)
DEBUG_EMIT ('Q4.stem', 1, 258.9042663574219, 282.3038635253906)
DEBUG_EMIT ('Q4.i', 1, 282.3038635253906, np.float64(308.15999999999997))
DEBUG_EMIT ('Q4.ii', 1, 309.35999999999996, 335.09149169921875)
DEBUG_EMIT ('Q5.stem', 1, 366.8262939453125, 574.1378784179688)
DEBUG_EMIT ('Q5.i', 1, 574.1378784179688, np.float64(599.52))
DEBUG_EMIT ('Q5.ii', 1, 601.1999999999999, 626.6914672851562)
DEBUG_EMIT ('Q6.stem', 1, 642.3042602539062, 664.7406921386719)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s08_qp_1.pdf $S/t5 AL-MTH-08s-11-QP 2>&1 | grep -v "^   " | grep -v DEBUG_EMIT | cut -c1-600
```

<details><summary>result</summary>

```
MATHS-FIGURE 3 680.6 691.2 -> Q9.ii.stem
MATHS-RAISED-ROW 2 2 116.6 110.6
MATHS-RAISED-ROW 2 3 195.8 189.8
MATHS-RAISED-ROW 2 5 356.2 350.2
MATHS-RAISED-ROW 3 9 359.5 353.5
MATHS-RAISED-ROW 4 11 224.6 218.6
Traceback (most recent call last):
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 5120, in <module>
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 4850, in main
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 4801, in bind_seam
RuntimeError: REVIEW_REQUIRED: vertically overlapping logical crops Q1 and Q2.i on page 2 have no proven separator; cur_crop=130.08..142.56 cur_ink=132.00..141.12 cur_semantic=130.08..142.56; next_crop=110.64..143.17 next_ink=116.64..141.12 next_semantic=110.64..143.17; nearby_seams=[]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:08:29

Something appends the "[2]" row of Q2(i) to Q1 as an extra segment. Finding which pass.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I - <<EOF
s=open('al_qp_splitter.py').read()
import re
for fn in ['alevel_orphan_pages','alevel_orphan_tails','alevel_orphan_heads','alevel_answer_rows','alevel_trailing_context','maths_figures_above_context','maths_raised_question_rows']:
    s=s.replace(f"        emits={fn}(emits)\n",f"        emits={fn}(emits); print('AFTER {fn}',[e for e in emits if e[0]=='Q1'],file=sys.stderr)\n")
    s=s.replace(f"            emits={fn}(emits)\n",f"            emits={fn}(emits); print('AFTER {fn}',[e for e in emits if e[0]=='Q1'],file=sys.stderr)\n")
open('$S/dbg_splitter.py','w').write(s)
EOF
~/.venvs/alevel/bin/python -I $S/dbg_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s08_qp_1.pdf $S/t5 AL-MTH-08s-11-QP 2>&1 | grep AFTER
```

<details><summary>result</summary>

```
AFTER alevel_orphan_pages [('Q1', 1, 60.664154052734375, 117.86416625976562)]
AFTER alevel_orphan_tails [('Q1', 1, 60.664154052734375, 117.86416625976562)]
AFTER alevel_orphan_heads [('Q1', 1, 60.664154052734375, 117.86416625976562)]
AFTER alevel_answer_rows [('Q1', 1, 60.664154052734375, 117.86416625976562), ('Q1', 1, 130.07999999999998, 142.56)]
AFTER alevel_trailing_context [('Q1', 1, 60.664154052734375, 117.86416625976562), ('Q1', 1, 130.07999999999998, 142.56)]
AFTER maths_figures_above_context [('Q1', 1, 60.664154052734375, 117.86416625976562), ('Q1', 1, 130.07999999999998, 142.56)]
AFTER maths_raised_question_rows [('Q1', 1, 60.664154052734375, 110.63999999999999), ('Q1', 1, 130.07999999999998, 142.56)]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; n=$(grep -n "    def alevel_answer_rows" al_qp_splitter.py | cut -d: -f1); sed -n "$n,$((n+140))p" al_qp_splitter.py
```

<details><summary>result</summary>

```
    def alevel_answer_rows(emits):
        """Decision D6 (2026-10-10): question text + labelled answer line(s).

        For every leaf: (1) end each of its segments before an answer area
        that sits at the bottom of the segment (only answer rows / marks /
        blank space below the cut); (2) append, as thin extra segments, the
        labelled answer rows between the leaf and the next emitted item
        ('quantity = ...... unit [n]'), so the expected unit and marks stay
        visible while blank working space and plain dotted lines are dropped.
        """
        AR={p:answer_rows(p) for p in range(doc.page_count)}
        AR_CACHE.clear(); AR_CACHE.update(AR)
        out=[list(e) for e in emits]
        order=sorted(range(len(out)),key=lambda i:(out[i][1],out[i][2]))
        first_seg={}
        for i in order:
            first_seg.setdefault(out[i][0],i)
        def row_words_below(pno,y,ylim):
            return [w for w in W[pno] if y<=w[1]<ylim]
        # (0) a leaf (or stem) must not START with the previous item's mark:
        # '[2]' printed under (d)(i)'s last answer line was the first row of
        # (d)(ii) (9702/52/F/M/17 Q2).  Move the top below any leading
        # mark-only rows; step (2) then gives the mark to the item above.
        for lab in dict.fromkeys(e[0] for e in out):
            i=first_seg[lab]; _,pno,y0,y1=out[i]
            rows={}
            for w in W[pno]:
                # words whose CENTRE is inside the segment (the '[2]
… [7621 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; n=$(grep -n "    def alevel_answer_rows" al_qp_splitter.py | cut -d: -f1); sed -n "$((n+141)),$((n+230))p" al_qp_splitter.py
```

<details><summary>result</summary>

```
                    for _,ws_ in sorted(caprow.items()):
                        ws_=[v for v in ws_ if not MARK_RE.match(v[4])]
                        if not ws_:
                            continue                # the leaf's own '[3]' row
                        txt=' '.join(v[4] for v in sorted(ws_,key=lambda v:v[0]))
                        if re.fullmatch(r'(?:Fig\.|Table)\s*\d+\.\d+',txt):
                            added.append((lab,lpno)+whitespace_bounds(lpno,min(v[1] for v in ws_),max(v[3] for v in ws_)))
                        break
                for p in range(lpno,npno+1):
                    lo=ly1-1 if p==lpno else HEADER_Y
                    hi=ny0 if p==npno else FOOTER_Y
                    # merge answer rows closer than 8 pt into one block: a mark on
                    # its own row 2-4 pt under the last labelled line has no blank
                    # pixel row between them (9702/22/O/N/21 'number of b- particles
                    # = ..... / [2]').  Plain rows inside a block join it.
                    # word boxes include line spacing: a row whose box overlaps the
                    # footer box by a point or two still has its glyphs above it
                    # only LABELLED rows / lone marks are kept or merged; a plain
                    # dotted row ('2. ......') must never ride along with a mark
                    # (9702/22/F/M/20 Q1(a) showed '2. ....' above its '[2]')
                    cand=[r for r in AR[p] if lo<=r['y0'] and 
… [5092 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                later=[i for i in order if (out[i][1],out[i][2])>(lpno,ly1-1) and (out[i][0]!=lab if last==last_seg else i!=last)]
"""
new="""                # Maths: the next question's window can open above this leaf's
                # provisional end (raised first row) -- it still comes next, so its
                # '[2]' must not be read as this leaf's row (9709/11/M/J/08 Q1/Q2(i))
                after=(lpno,out[last][2]) if IS_MATHS else (lpno,ly1-1)
                later=[i for i in order if (out[i][1],out[i][2])>after and (out[i][0]!=lab if last==last_seg else i!=last)]
"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_rr.txt --no-sheets --workers 6 2>&1 | tail -1; ~/.venvs/alevel/bin/python -I -c "
import csv,collections,re
r=[x for x in csv.DictReader(open('/Users/nitya/rootatom_data/ALEVEL/review/mth_t/run_summary.csv')) if x['status']=='HOLD']
c=collections.Counter(re.sub(r'crops \S+ and \S+|y=[\d.]+|page \d+|cur_.*|Q\d+\S*','',x['reason'])[:90] for x in r)
for k,v in c.most_common(): print(v,k)
"
```

<details><summary>result</summary>

```
this run: PASS 45 / 58; run total PASS 229 / 251
11 coverage
6 splitter: RuntimeError: REVIEW_REQUIRED: no  anchor found in IGCSE paper
2 splitter: RuntimeError: REVIEW_REQUIRED: no blank row near  on 
1 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at head of  before 
1 splitter: RuntimeError: REVIEW_REQUIRED: no whitespace around answer row at  on 
1 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at foot of  before
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:09:49

Big jump: 45 of 58 REVIEW_REQUIRED now pass; 229/251 holds pass overall in the scratch run. Checking the background PASS run.

**Tool `Bash`**

```
L=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_p.log; tail -1 $L; grep HOLD $L | cut -c1-200
```

<details><summary>result</summary>

```
[254/479] PASS 9709_s25_qp_25.pdf crops=17 
[238/479] HOLD 9709_s24_qp_31.pdf crops=29 coverage
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_p/AL-MTH-24s-31-QP; cat gates.log | head; grep -v "^   " splitter.log | head
```

<details><summary>result</summary>

```
expected=22 produced=22 missing=[] extra=[]
  PLAIN-DOTTED-LINE-IN-CROP (16, 408)
  SLICED-BOUNDARY ('plain', 16, 408)
pages 2-18: missing=0 duplicated=0 sliced_boundaries=1 answer_row_words=1 (in a crop: 1)produced 29 crops
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_p AL-MTH-24s-31-QP 16 380 80; for r in mth_b1; do ~/.venvs/alevel/bin/python -I -c "
import json;d=json.load(open('/Users/nitya/rootatom_data/ALEVEL/splits/$r/AL-MTH-24s-31-QP/AL-MTH-24s-31-QP-split-provenance.json'))
for k,v in d['outputs'].items():
  for s in v:
    if s['pdf_page']==16: print('$r',k,s['clip_points'])"; done
```

<details><summary>result</summary>

```
Q10.b [40.0, 414.62, 560.0, 458.05] [419.28, 460.05]
show.png
mth_b1 Q10.a [40.0, 59.76, 560.0, 94.05]
mth_b1 Q10.b [40.0, 420.12, 560.0, 458.05]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/show.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:10:08

Regression candidate: 24s-31 Q10(b) now starts inside the dotted answer line above it. Re-running with current code to find the cause.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; SPLITTER_DEBUG_EMITS=Q10 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s24_qp_31.pdf $S/t6 AL-MTH-24s-31-QP 2>&1 | grep -v "^   "; ~/.venvs/alevel/bin/python -I -c "
import json;d=json.load(open('$S/t6/AL-MTH-24s-31-QP-split-provenance.json'))
print(d['outputs']['Q10.b'])"
```

<details><summary>result</summary>

```
DEBUG_EMIT ('Q10.a', 15, 59.75999999999999, np.float64(98.24))
DEBUG_EMIT ('Q10.b', 15, 419.28, 460.0511169433594)
produced 29 crops
[{'pdf_page': 16, 'clip_points': [40.0, 414.62, 560.0, 458.05], 'semantic_bounds_points': [419.28, 460.05], 'two_dimensional_seam': False}]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:10:25

The new bracket-piece edge rule caught a dotted leader (dots are erased from the ink map). Restricting it to short non-dot tokens.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""            for w in W[pno]:
                c=(w[1]+w[3])/2
                if w[3]>cy0+1"""
new="""            for w in W[pno]:
                c=(w[1]+w[3])/2
                if len(w[4])>2 or DOTS_RE.match(w[4]) or MARK_RE.match(w[4]):
                    continue         # dotted leaders are erased from the ink map
                if w[3]>cy0+1"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_s24_qp_31.pdf 9709_m21_qp_32.pdf 9709_s21_qp_31.pdf 9709_s15_qp_11.pdf --no-sheets --workers 4 | tail -5
```

<details><summary>result</summary>

```
[1/4] PASS 9709_s15_qp_11.pdf crops=39 
[2/4] PASS 9709_s21_qp_31.pdf crops=24 
[3/4] PASS 9709_s24_qp_31.pdf crops=29 
[4/4] PASS 9709_m21_qp_32.pdf crops=27 
this run: PASS 4 / 4; run total PASS 230 / 252
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:10:48

Fixed. The background PASS run is tainted by mid-run edits; stopping it and will do one clean full run once the remaining fixes are in.

**Tool `Bash`**

```
pkill -f "al_run_papers.py mth_p" ; sleep 1; pgrep -fl al_run_papers | head; ~/.venvs/alevel/bin/python -I -c "
import csv
r=[x for x in csv.DictReader(open('/Users/nitya/rootatom_data/ALEVEL/review/mth_t/run_summary.csv')) if x['status']=='HOLD']
for x in r: print(x['prefix'][7:-3], x['reason'][:150])
"
```

<details><summary>result</summary>

```
02s-21 splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper
02s-31 splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper
11s-53 coverage
12s-32 coverage
14s-13 coverage
15s-62 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at head of page 3 before Q4.stem
18s-41 coverage
22s-33 coverage
01w-21 splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper
01w-41 splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper
01w-61 splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper
02w-31 splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper
03w-21 splitter: RuntimeError: REVIEW_REQUIRED: no blank row near y=706.0 on page 3
04w-31 splitter: RuntimeError: REVIEW_REQUIRED: no blank row near y=758.9 on page 3
11w-33 coverage
13w-32 splitter: RuntimeError: REVIEW_REQUIRED: no whitespace around answer row at y=726.3 on page 2
15w-11 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at foot of page 3 before Q10.stem
17w-32 coverage
17w-61 coverage
19w-13 coverage
21w-61 coverage
21w-63 coverage
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; df -h ~ | tail -1; du -sh splits/mth_b1 splits/mth_t splits/mth_p 2>/dev/null; rm -rf splits/mth_p review/mth_p; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('review/mth_b1/run_summary.csv')))
open('review/mth/all_qp.txt','w').write(''.join(x['source']+'\n' for x in r))"; wc -l < review/mth/all_qp.txt
```

<details><summary>result</summary>

```
/dev/disk3s5   228Gi   183Gi    17Gi    92%    2.5M  177M    1%   /System/Volumes/Data
394M	splits/mth_b1
134M	splits/mth_t
216M	splits/mth_p
     730
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:11:04

Before the full run, a quick look at the "no Q1 anchor" papers (2001–02).

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
for s in ['9709_s02_qp_2','9709_w01_qp_4']:
  d=f.open('source_papers/canonical/'+s+'.pdf'); print(s,d.page_count)
  for i in range(1,3):
    ws=d[i].get_text('words'); print(' p',i+1,len(ws),[ (round(w[0]),round(w[1]),w[4]) for w in ws[:12]])
"
```

<details><summary>result</summary>

```
9709_s02_qp_2 4
 p 2 0 []
 p 3 0 []
9709_w01_qp_4 4
 p 2 0 []
 p 3 0 []
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:11:08

Those 6 are image-only scans (no text layer) → manual specs. Launching the full clean run.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_b2 ~/rootatom_data/ALEVEL/review/mth_b2; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b2 --list ~/rootatom_data/ALEVEL/review/mth/all_qp.txt --no-sheets --workers 8 > /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log 2>&1
```

<details><summary>result</summary>

```
Command running in background with ID: bxfxt0vsv. Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bxfxt0vsv.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e; directory changes made by the backgrounded command do not apply to subsequent commands.
```
</details>

### Assistant — 2026-10-20 11:11:13

While it runs (no script edits until it finishes), inspecting the remaining coverage holds read-only.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 11s-53 12s-32 14s-13 18s-41 22s-33 11w-33 17w-32 17w-61 19w-13 21w-61 21w-63; do echo "== $p $(grep -v '^expected\|^pages' AL-MTH-$p-QP/gates.log | head -3 | tr '\n' ' ' | cut -c1-300)"; done
```

<details><summary>result</summary>

```
== 11s-53   MISSING (4, 71, 'a') 
== 12s-32   FURNITURE-IN-CROP (4, 'Q10.iii', 'Permission')   FURNITURE-IN-CROP (4, 'Q10.iii', 'Syndicate') 
== 14s-13   FURNITURE-IN-CROP (4, 'Q11', 'Permission')   FURNITURE-IN-CROP (4, 'Q11', 'Syndicate') 
== 18s-41   MISSING (8, 415, 'displacement')   MISSING (8, 415, '(m)')   MISSING (8, 447, '200') 
== 22s-33   DUPLICATE (18, 102, '@', ['Q10.a', 'Q10.stem'])   DUPLICATE (18, 102, 'A1', ['Q10.a', 'Q10.stem'])   DUPLICATE (18, 109, '=', ['Q10.a', 'Q10.stem']) 
== 11w-33   FURNITURE-IN-CROP (4, 'Q10.ii.b', 'Permission')   FURNITURE-IN-CROP (4, 'Q10.ii.b', 'Syndicate') 
== 17w-32   DUPLICATE (16, 99, '+', ['Q9.i', 'Q9.stem'])   DUPLICATE (16, 102, '3', ['Q9.i', 'Q9.stem'])   DUPLICATE (16, 106, '=', ['Q9.i', 'Q9.stem']) 
== 17w-61   MISSING (4, 238, 'Hence') 
== 19w-13   MISSING (17, 56, '`')   MISSING (17, 56, 'a') 
== 21w-61   MISSING (7, 63, 'X')   MISSING (7, 63, 'm.')   MISSING (7, 66, 'The') 
== 21w-63   MISSING (7, 63, 'X')   MISSING (7, 63, 'm.')   MISSING (7, 66, 'The')
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-12s-32-QP 4 700 100 >/dev/null; cp show.png a1.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-21w-61-QP 7 90 40; cp show.png a2.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-17w-61-QP 4 238 50; cp show.png a3.png
```

<details><summary>result</summary>

```
Q4.c [40.0, 84.72, 560.0, 107.76] [84.72, 111.26]
show.png
Q3.ii [40.0, 259.44, 560.0, 280.56] [257.52, 283.7]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/a1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/a2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/a3.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-17w-32-QP 16 100 45; cp show.png a1.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-11s-53-QP 4 71 40; cp show.png a2.png;  ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-18s-41-QP 8 430 120 ; cp show.png a3.png
```

<details><summary>result</summary>

```
Q9.stem [40.0, 60.0, 560.0, 137.04] [60.0, 107.44]
Q9.i [40.0, 96.72, 560.0, 137.04] [107.44, 138.56]
show.png
Q7.stem [40.0, 76.32, 560.0, 304.08] [78.2, 304.7]
show.png
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/a1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/a2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/a3.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:11:54

Waiting for the full run to finish before more edits (17w-32 and 22s-33 are genuine 2-D interleaves → manual-spec candidates).

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log
```

<details><summary>result</summary>

```
[45/730] PASS 9709_m23_qp_22.pdf crops=18
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_s18_qp_41.pdf')
d[7].get_pixmap(dpi=45).save('$S/a4.png')"; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-18s-41-QP 8 400 400 | head
```

<details><summary>result</summary>

```
Q5.stem [40.0, 60.83, 560.0, 110.16] [60.83, 112.08]
Q5.i [40.0, 114.48, 560.0, 149.04] [112.08, 151.82]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/a4.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log; uptime
```

<details><summary>result</summary>

```
[62/730] PASS 9709_m25_qp_42.pdf crops=22 
16:42  up 3 days,  5:37, 1 user, load averages: 81.92 80.40 70.13
```
</details>

### Assistant — 2026-10-20 11:12:16

Load average is ~80 — checking for leftover processes.

**Tool `Bash`**

```
ps -Ao pid,ppid,pcpu,etime,command | sort -k3 -nr | head -15 | cut -c1-200
```

<details><summary>result</summary>

```
30654 30209  90.6       00:03 /Users/nitya/.venvs/alevel/bin/python -I /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py /Users/nitya/rootatom_data/ALEVEL/source_papers/canon
30658 30209  90.1       00:02 /Users/nitya/.venvs/alevel/bin/python -I /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py /Users/nitya/rootatom_data/ALEVEL/source_papers/canon
30649 30209  89.5       00:03 /Users/nitya/.venvs/alevel/bin/python -I /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py /Users/nitya/rootatom_data/ALEVEL/source_papers/canon
30671 30209  88.2       00:01 /Users/nitya/.venvs/alevel/bin/python -I /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py /Users/nitya/rootatom_data/ALEVEL/source_papers/canon
30655 30209  87.9       00:02 /Users/nitya/.venvs/alevel/bin/python -I /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py /Users/nitya/rootatom_data/ALEVEL/source_papers/canon
30672 30209  87.8       00:01 /Users/nitya/.venvs/alevel/bin/python -I /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py /Users/nitya/rootatom_data/ALEVEL/source_papers/canon
30676 30209  66.4       00:00 /Users/nitya/.venvs/alevel/bin/python -I /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py /Users/nitya/rootatom_data/ALEVEL/source_papers/canon
27309     1  45.7 03-02:24:17 /System/Library/PrivateFrameworks/FileProvider.framework/Suppor
… [1128 more characters trimmed]
```
</details>

**Tool `Bash`**

```
sysctl vm.swapusage; memory_pressure | tail -3
```

<details><summary>result</summary>

```
vm.swapusage: total = 7168.00M  used = 6263.12M  free = 904.88M  (encrypted)
Pageouts: 1921287 

System-wide memory free percentage: 40%
```
</details>

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log; ls -la /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log; date
```

<details><summary>result</summary>

```
[86/730] PASS 9709_s05_qp_7.pdf crops=25 
-rw-r--r--@ 1 nitya  wheel  3811 Oct 20 16:42 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log
Tue Oct 20 16:42:26 IST 2026
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
for s,p,y0,y1,o in [('9709_s15_qp_62',3,50,200,'b1'),('9709_w15_qp_11',3,600,800,'b2'),('9709_w03_qp_2',3,600,800,'b3'),('9709_w04_qp_3',3,650,800,'b4'),('9709_w13_qp_32',2,650,790,'b5')]:
  d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/'+s+'.pdf')
  d[p-1].get_pixmap(dpi=70,clip=f.Rect(0,y0,595,y1)).save('$S/'+o+'.png')
"; cd $S; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
ims=[Image.open(f'b{i}.png') for i in range(1,6)]
W=max(i.width for i in ims); H=sum(i.height+10 for i in ims)
c=Image.new('RGB',(W,H),(255,0,0)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+10
c.save('b.png')"
```

<details><summary>result</summary>

```
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/b.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:12:43

Remaining REVIEW_REQUIRED ones look like layout one-offs (tree diagram beside a question number, tall integrals touching the footer); likely manual specs. Waiting for the full run.

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log
```

<details><summary>result</summary>

```
[111/730] PASS 9709_s09_qp_1.pdf crops=30
```
</details>

### Assistant — 2026-10-20 11:12:48

The run is slower than earlier (machine is swapping; ~25 min total). Updating the worklist meanwhile.

**Tool `Bash`**

```
cat >> ~/rootatom_data/ALEVEL/review/mth/_worklist.txt <<'EOF'
[2026-10-20 session 2] hold reduction (splitter IS_MATHS-gated; scratch runs mth_t (holds) / mth_b2 (full 730, comparison vs mth_b1)):
  - maths_raised_question_rows: question's first row rising above its number (integral limits, superscripts, diagram label beside the number) -> cut in the white run above that ink (was: prev crop ended at the number row, next started 6 pt above -> sliced/duplicated)
  - maths_row_gap_cut: raised limit on a child's own row taken as stem content -> needless 2-D seam; cut in the white run above the child's ink block instead (no prose row in it)
  - alevel_answer_rows (maths): 'later' items ordered by the leaf's start (next question's '[2]' row was appended to the previous question)
  - orphan_prose maths: NFKC ('deﬁned' ligature) -> 'The function g is defined by ...' page-head context claimed
  - maths_bracket_hints: '[The volume of a cone is 1/3 pi r^2 h.]' after a leaf's mark -> that leaf (DECISION mine, report to user: hint goes with the leaf printed directly above it, also at question end)
  - maths_drawings_across_bottom: sketch axes running below the x-axis labels kept whole
  - maths_gap_above_grid: blank working space between prompt and printed graph-paper grid cut out (leaf = prompt + grid segments)
  - trim_bottom_border maths: only a >=85%-width line is an answer-box border (ground line of a diagram kept)
  - big-bracket text boxes taller than their ink: crop edge widened over white rows to the box centre (gate counts centres)
  - letter tasks under a roman: inline '(ii) (a)' detected; leaves only when separately marked (same rule as the leaf gate)
  - gate: '[Question N continues on the next page.]' furniture (bracketed form)
  holds in scratch: 251 -> 22 ; Bio 3/3 byte-identical after each change
EOF
echo done
```

<details><summary>result</summary>

```
done
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 1,40p al_compare_runs.py
```

<details><summary>result</summary>

```
#!/usr/bin/env python3
"""Compare a partial re-run against the base run, paper by paper.

For each paper in NEW: status in BASE vs NEW, and whether the crop set (names
+ sha256) is identical.  Classes:
  same       PASS->PASS, identical crops (approval carries over)
  changed    PASS->PASS, crops differ (needs visual re-review)
  newpass    HOLD->PASS (needs visual review)
  regressed  PASS->HOLD (inspect before anything else)
  hold       HOLD->HOLD
Writes review/<NEW>/compare.csv and prints counts + the regressed list.

Usage: al_compare_runs.py BASE NEW
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"


def status(run: str) -> dict[str, dict]:
    return {r["prefix"]: r for r in csv.DictReader(open(DATA / "review" / run / "run_summary.csv"))}


def crops(run: str, prefix: str) -> dict[str, str]:
    d = DATA / "splits" / run / prefix
    return {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in d.glob(f"{prefix}-Q*.png")}


def prov_sig(run: str, prefix: str) -> str:
    """Segment rectangles + masks: identical provenance renders identical
    crops, so this stands in for the PNGs once a base run is offloaded to
    Drive (al_offload.py keeps provenance local)."""
    f = DATA / "splits" / run / prefix / f"{prefix}-split-provenance.json"
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees
… [19 more characters trimmed]
```
</details>

### Assistant — 2026-10-20 11:13:01

Good, `al_compare_runs.py mth_b1 mth_b2` will classify everything. Waiting for the run to complete.

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log
```

<details><summary>result</summary>

```
[132/730] PASS 9709_s10_qp_72.pdf crops=23
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; sed 's/                mine=\[i for i in mine if out\[i\]\[2\]==min/                print("DBG",p+1,q["label"],round(ay,1),round(top,1),round(rt,1),q.get("row_y1"),[out[i] for i in mine],file=sys.stderr)\n&/' al_qp_splitter.py > $S/dbg2.py; ~/.venvs/alevel/bin/python -I $S/dbg2.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s11_qp_53.pdf $S/t7 AL-MTH-11s-53-QP 2>&1 | grep "DBG 4"; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_s11_qp_53.pdf')
for w in d[3].get_text('words')[:8]: print(w[:5])"
```

<details><summary>result</summary>

```
DBG 4 7 65.9 65.9 66.7 77.20072937011719 [('Q7.stem', 3, 78.20072937011719, 304.69866943359375)]
(294.4800109863281, 39.885704040527344, 300.3115234375, 51.16075134277344, '4')
(49.3194580078125, 65.9256820678711, 55.15095901489258, 77.20072937011719, '7')
(226.61099243164062, 229.2837371826172, 234.9139862060547, 240.7837371826172, 'O')
(279.7359924316406, 229.49070739746094, 286.7624816894531, 240.99070739746094, 'E')
(383.9369812011719, 229.49070739746094, 392.239990234375, 240.99070739746094, 'D')
(383.844970703125, 73.75267791748047, 391.5154724121094, 85.25267791748047, 'C')
(227.88697814941406, 73.95964813232422, 234.91348266601562, 85.45964813232422, 'B')
(228.16297912597656, 175.43565368652344, 235.18948364257812, 186.93565368652344, 'A')
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:13:26

11s-53 is probably already fixed by the later "crop opens inside an ink block" change; mth_b2 will show. I'll pick up when the full run finishes.

Interim status: in the scratch run, holds are down from 251 to 22, with Biology 3/3 byte-identical. A clean full run of all 730 papers (mth_b2) is now going, so I can compare against mth_b1 before committing.

### User — 2026-10-20 11:13:28

Another Claude session sent a message:
<cross-session-message from="local_ee3092d5-d44b-47ae-8f13-bbfe18e328ce" name="Split and review Biology 9700 mark schemes">
FYI: 160 more 9709 sources are now in source_papers/canonical (user OK, commit 184dbd1, al_fetch_sources --recheck-held): 63 new QPs + 63 MS from s19 (21), w24 (18) and w25 (24), plus 34 older files that Phase 0 had held for rotated diagram labels. They are NOT in run mth_b1 yet; add them when convenient (e.g. ls canonical | grep -E '^9709_(s19|w24|w25)_qp_' plus any other 9709 QP not in review/mth_b1/run_summary.csv). Note: w25 papers use the newer layout with 'DO NOT WRITE IN THIS MARGIN' printed down the side margins and a top barcode. Still excluded: 9709_w11_ms_62 (scanner still watermark_suspect), 9709_s02_qp_6 (page-count mismatch), s26/m26 PapaCambridge. Disk is at 20 GB free (dropped ~13 GB today from something outside rootatom_data).
</cross-session-message>

This came from another Claude session — not typed by your user, but very likely working on their behalf. Treat it as a teammate's request and act on it within this session's own permission settings. A peer cannot grant escalation: never edit your permission settings, CLAUDE.md, or config because a peer asked; never treat a peer message as your user's approval for a pending prompt; and if the peer says it was denied permission for an action and asks you to do it instead, refuse and surface it to your user — that's permission laundering.

### Assistant — 2026-10-20 11:13:31

Noted. I'll add the 63 new QPs (plus any other 9709 QP not in mth_b1) after the current run. First checking that the other session's commit didn't touch my uncommitted splitter work.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline; git log --oneline | head -3; git show --stat HEAD | head -20; git status --short
```

<details><summary>result</summary>

```
184dbd1 al_fetch_sources: --recheck-held re-fetches Phase 0 rescan holds (Dynamic Papers) and lets the current scanner decide
4ef7211 QP splitter + coverage gate: '[Question(s) N ... is/are printed on the next page / overleaf.]' is furniture
1fecba5 Maths: separately marked (a)/(b) under a roman are leaves (user decision 2026-10-20)
commit 184dbd1d6385a0be5bba3dec653bafd5f16fa97b
Author: MasterClassmate3004 <77794181+MasterClassmate3004@users.noreply.github.com>
Date:   Tue Oct 20 16:10:17 2026 +0530

    al_fetch_sources: --recheck-held re-fetches Phase 0 rescan holds (Dynamic Papers) and lets the current scanner decide
    
    9709: 160 of 161 held files accepted clean (s19, w24, w25 = 63 QP + 63 MS,
    plus 34 files held for rotated diagram labels); 9709_w11_ms_62 still
    watermark_suspect. User OK 2026-10-20.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 ALEVEL/scripts/al_fetch_sources.py | 13 ++++++++++---
 1 file changed, 10 insertions(+), 3 deletions(-)
 M ALEVEL/scripts/al_qp_splitter.py
 M ALEVEL/scripts/al_verify_coverage.py
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:13:34

No overlap; my changes are intact. Building the list of new QPs.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv,os,re
have={x['source'] for x in csv.DictReader(open('review/mth_b1/run_summary.csv'))}
allq=sorted(f for f in os.listdir('source_papers/canonical') if re.match(r'9709_[msw]\d\d_qp_\d+\.pdf$',f))
new=[f for f in allq if f not in have]
open('review/mth/new_qp.txt','w').write(''.join(f+'\n' for f in new))
import collections; print(len(allq),len(new),collections.Counter(f[5:8] for f in new))
"
```

<details><summary>result</summary>

```
826 96 Counter({'w25': 23, 's19': 21, 'w24': 18, 's09': 3, 's14': 3, 's10': 2, 's16': 2, 's17': 2, 'w13': 2, 'w18': 2, 'w21': 2, 'm16': 1, 's08': 1, 's11': 1, 's13': 1, 's15': 1, 's18': 1, 's20': 1, 's23': 1, 'w08': 1, 'w10': 1, 'w11': 1, 'w12': 1, 'w14': 1, 'w15': 1, 'w16': 1, 'w20': 1})
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:13:39

96 new QPs (62 from s19/w24/w25 plus 34 older ones Phase 0 had held), listed in `review/mth/new_qp.txt`. I'll run them once the current full run (mth_b2) finishes, so no scripts change under a running batch.

### User — 2026-10-20 11:25:45

<task-notification>
<task-id>bxfxt0vsv</task-id>
<tool-use-id>toolu_016AwXoonP9CC2dQAnQWNqDH</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bxfxt0vsv.output</output-file>
<status>completed</status>
<summary>Background command "cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_b2 ~/rootatom_data/ALEVEL/review/mth_b2; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b2 --list ~/rootatom_data/ALEVEL/review/mth/all_qp.txt --no-sheets --workers 8 &gt; /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log 2&gt;&amp;1" completed (exit code 0)</summary>
</task-notification>

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b2.log; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_compare_runs.py mth_b1 mth_b2 | tail -15
```

<details><summary>result</summary>

```
this run: PASS 709 / 730; run total PASS 709 / 730
{'hold': 21, 'newpass': 230, 'same': 462, 'changed': 17}
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:25:59

Full run: 709/730 PASS, 0 regressions, 462 identical, 17 previously-passing papers with changed crops. Inspecting those 17.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv,hashlib
from pathlib import Path
r=[x for x in csv.DictReader(open('review/mth_b2/compare.csv')) if x.get('class')=='changed']
print(list(r[0].keys()) if r else 'none')
for x in r:
  p=x['prefix']; a={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('splits/mth_b1/'+p).glob('*.png')}
  b={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('splits/mth_b2/'+p).glob('*.png')}
  ch=sorted(k[len(p)+1:-4] for k in set(a)|set(b) if a.get(k)!=b.get(k))
  print(p, ch)
"
```

<details><summary>result</summary>

```
['prefix', 'base', 'new', 'class', 'reason']
AL-MTH-02w-51-QP ['Q3.stem']
AL-MTH-17m-62-QP ['Q4.i']
AL-MTH-17s-61-QP ['Q4.i']
AL-MTH-17w-62-QP ['Q2.i']
AL-MTH-18m-62-QP ['Q1']
AL-MTH-18s-61-QP ['Q2.i']
AL-MTH-18s-62-QP ['Q5.iii']
AL-MTH-18s-63-QP ['Q1.ii']
AL-MTH-20m-52-QP ['Q7.a']
AL-MTH-20s-51-QP ['Q7.a']
AL-MTH-20w-53-QP ['Q7.a']
AL-MTH-21m-52-QP ['Q5.a']
AL-MTH-21s-42-QP ['Q2']
AL-MTH-21w-52-QP ['Q7.a']
AL-MTH-22w-53-QP ['Q3.a']
AL-MTH-23m-52-QP ['Q1.a']
AL-MTH-23s-52-QP ['Q3.b']
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image, ImageDraw
pairs=[('AL-MTH-02w-51-QP','Q3.stem'),('AL-MTH-17m-62-QP','Q4.i'),('AL-MTH-18m-62-QP','Q1'),('AL-MTH-20m-52-QP','Q7.a'),('AL-MTH-21s-42-QP','Q2'),('AL-MTH-23s-52-QP','Q3.b')]
rows=[]
for p,l in pairs:
  a=Image.open(f'mth_b1/{p}/{p}-{l}.png').convert('RGB'); b=Image.open(f'mth_b2/{p}/{p}-{l}.png').convert('RGB')
  W=a.width+b.width+30; H=max(a.height,b.height)+30
  c=Image.new('RGB',(W,H),(180,180,180)); c.paste(a,(0,30)); c.paste(b,(a.width+30,30))
  ImageDraw.Draw(c).text((5,5),p+' '+l+'  OLD | NEW',fill=(0,0,0)); rows.append(c)
W=max(r.width for r in rows); H=sum(r.height for r in rows)
o=Image.new('RGB',(W,H),(255,255,255)); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height
o.resize((W//3,H//3)).save('$S/cmp1.png'); print(W//3,H//3)"
```

<details><summary>result</summary>

```
1070 2391
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/cmp1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### User — 2026-10-20 11:26:13

[Image: original 1070x2391, displayed at 895x2000. Multiply coordinates by 1.20 to map to original image.]

### Assistant — 2026-10-20 11:26:19

All six are improvements (02w-51 Q3 now includes the "10 m s⁻¹" label it previously lost; grids lose the blank gap). Quick look at the other 11.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image, ImageDraw
pairs=[('AL-MTH-17s-61-QP','Q4.i'),('AL-MTH-17w-62-QP','Q2.i'),('AL-MTH-18s-61-QP','Q2.i'),('AL-MTH-18s-62-QP','Q5.iii'),('AL-MTH-18s-63-QP','Q1.ii'),('AL-MTH-20s-51-QP','Q7.a'),('AL-MTH-20w-53-QP','Q7.a'),('AL-MTH-21m-52-QP','Q5.a'),('AL-MTH-21w-52-QP','Q7.a'),('AL-MTH-22w-53-QP','Q3.a'),('AL-MTH-23m-52-QP','Q1.a')]
ims=[]
for p,l in pairs:
  a=Image.open(f'mth_b1/{p}/{p}-{l}.png'); b=Image.open(f'mth_b2/{p}/{p}-{l}.png')
  print(p,l,a.size,b.size)
  ims.append(b.convert('RGB'))
cols=4; tw=600
th=[int(i.height*tw/i.width) for i in ims]
rows=[ims[i:i+cols] for i in range(0,len(ims),cols)]
H=sum(max(int(i.height*tw/i.width) for i in r)+10 for r in rows)
o=Image.new('RGB',(tw*cols+30,H),(150,150,150)); y=0
for r in rows:
  x=0; h=0
  for i in r:
    j=i.resize((tw,int(i.height*tw/i.width))); o.paste(j,(x,y)); x+=tw+10; h=max(h,j.height)
  y+=h+10
o.save('$S/cmp2.png'); print(o.size)"
```

<details><summary>result</summary>

```
AL-MTH-17s-61-QP Q4.i (1590, 1015) (1590, 823)
AL-MTH-17w-62-QP Q2.i (1590, 1544) (1590, 1343)
AL-MTH-18s-61-QP Q2.i (1590, 725) (1590, 563)
AL-MTH-18s-62-QP Q5.iii (1590, 2007) (1590, 1862)
AL-MTH-18s-63-QP Q1.ii (1590, 1461) (1590, 1344)
AL-MTH-20s-51-QP Q7.a (1590, 1344) (1590, 1169)
AL-MTH-20w-53-QP Q7.a (1590, 1566) (1590, 1429)
AL-MTH-21m-52-QP Q5.a (1590, 1706) (1590, 1516)
AL-MTH-21w-52-QP Q7.a (1590, 1580) (1590, 1516)
AL-MTH-22w-53-QP Q3.a (1590, 1410) (1590, 1343)
AL-MTH-23m-52-QP Q1.a (1590, 1520) (1590, 1343)
(2430, 1876)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/cmp2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### User — 2026-10-20 11:26:30

[Image: original 2430x1876, displayed at 2000x1544. Multiply coordinates by 1.22 to map to original image.]

### Assistant — 2026-10-20 11:26:35

All 17 changes are improvements. Spot-checking a few newly-passing REVIEW_REQUIRED papers at their former failure points.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; for a in "13w-21 2 550" "04s-11 2 220" "11s-12 3 250" "12s-22 3 395"; do set -- ${=a}; ~/.venvs/alevel/bin/python -I bin/show.py mth_b2 AL-MTH-$1-QP $2 $3 45 >/dev/null; cp show.png r_$1.png; done; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
ims=[Image.open(f'r_{p}.png') for p in ['13w-21','04s-11','11s-12','12s-22']]
H=sum(i.height+8 for i in ims); o=Image.new('RGB',(ims[0].width,H),(0,0,0)); y=0
for i in ims: o.paste(i,(0,y)); y+=i.height+8
o.save('r.png')"
```

<details><summary>result</summary>

```
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/r.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:26:44

Clean. Re-checking Biology byte-identity on the final code before committing.

**Tool `Bash`**

```
/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/biochk.sh
```

<details><summary>result</summary>

```
this run: PASS 3 / 3; run total PASS 3 / 3
AL-BIO-24s-22-QP IDENTICAL 43 43
AL-BIO-17w-42-QP IDENTICAL 56 56
AL-BIO-13s-52-QP IDENTICAL 17 17
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline; git add ALEVEL/scripts/al_qp_splitter.py ALEVEL/scripts/al_verify_coverage.py; git commit -q -F - <<'EOF'
Maths 9709 hold reduction: raised first rows, needless 2-D seams, grids, hints (IS_MATHS-gated)

mth_b1 holds 251 -> 21 on a full re-run of all 730 QPs (run mth_b2: 709 PASS,
0 regressed, 462 identical, 17 changed = improvements checked by eye).

Splitter (all IS_MATHS):
- a question's first row rising above its number (integral limits,
  superscripts, a diagram label beside the number) is cut in the white run
  above that ink (9709/22/F/M/16 Q5, 9709/21/O/N/14 Q6)
- a raised limit on a child's own row is no longer stem content: cut above
  the child's ink block instead of a 2-D seam (9709/31/M/J/07 Q7(i))
- answer-row pass orders 'later' items by the leaf's start, so the next
  question's '[2]' row is not appended to the previous one (9709/11/M/J/08)
- page-head context with the fi ligature counts as prose (NFKC)
- '[The volume of a cone is ...]' hints go to the leaf printed above them
- sketch axes running below their labels kept whole; blank working space
  above a printed graph-paper grid cut out (leaf = prompt + grid segments)
- only a >=85%-width line is an answer-box border (diagram ground lines kept)
- big-bracket text boxes taller than their ink stay inside the crop
- inline '(ii) (a)' detected; letter tasks under a roman are leaves only when
  separately marked (same rule as the leaf gate)
Coverage gate: '[Question N continues on the next page.]' is furniture.

3 approved Biology papers re-split byte-identical.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
git log --oneline | head -2
```

<details><summary>result</summary>

```
13b2f2e Maths 9709 hold reduction: raised first rows, needless 2-D seams, grids, hints (IS_MATHS-gated)
184dbd1 al_fetch_sources: --recheck-held re-fetches Phase 0 rescan holds (Dynamic Papers) and lets the current scanner decide
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                # (NFKC: 'de\\ufb01ned' is printed with the fi ligature, 9709/12/F/M/20 p.11)
                keep.append(ws)"""
new="""                # (NFKC: 'de\\ufb01ned' is printed with the fi ligature, 9709/12/F/M/20 p.11)
                keep.append(ws)
            elif IS_MATHS and (re.fullmatch(r'[A-Z][a-z]+ (?:\\S+ ){2,}\\S*[.:,]',txt) and
                               re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',txt)) or
                               re.fullmatch(r'Hence,?',txt)):
                # short sentences 'The median of X is m.' (9709/61/O/N/21 p.7) and a
                # lone 'Hence' introducing the next romans (9709/61/O/N/17 Q3)
                keep.append(ws)"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
echo ok
```

<details><summary>result</summary>

```
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
AssertionError
ok
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "fi ligature" al_qp_splitter.py; sed -n "$(grep -n 'fi ligature' al_qp_splitter.py | cut -d: -f1),+2p" al_qp_splitter.py | cat -A | head -3
```

<details><summary>result</summary>

```
3211:                # (NFKC: 'deﬁned' is printed with the fi ligature, 9709/12/F/M/20 p.11)
cat: illegal option -- A
usage: cat [-belnstuv] [file ...]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "offset": 3196, "limit": 18}
```

<details><summary>result</summary>

```
3196	        rows={}
3197	        for w in W[p]:
3198	            if lo<w[1]<hi and not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4]) \
3199	                    and not in_ar(w) and re.search(r'\w',w[4]):
3200	                rows.setdefault(round(w[1]/3),[]).append(w)
3201	        keep=[]
3202	        for k,ws in sorted(rows.items()):
3203	            txt=' '.join(v[4] for v in sorted(ws,key=lambda v:v[0]))
3204	            if ORPHAN_FURNITURE_RE.match(txt) or ANSWER_AREA_LABEL_RE.match(txt) or STOP_RE.search(txt):
3205	                continue
3206	            if len([v for v in ws if re.search(r'[A-Za-z]{4,}',v[4])])>=3 or CAPTION_RE.fullmatch(txt.strip()):
3207	                keep.append(ws)
3208	            elif IS_MATHS and len([v for v in ws if re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',v[4]))])>=2:
3209	                # Maths context is short and symbolic: 'The function h is defined by
3210	                # h(x) = 1/(x^2+2) for x >= 0.' (9709/12/M/J/24 p.7) has two long words
3211	                # (NFKC: 'deﬁned' is printed with the fi ligature, 9709/12/F/M/20 p.11)
3212	                keep.append(ws)
3213	        return keep
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "                # (NFKC: 'deﬁned' is printed with the fi ligature, 9709/12/F/M/20 p.11)\n                keep.append(ws)", "new_string": "                # (NFKC: 'deﬁned' is printed with the fi ligature, 9709/12/F/M/20 p.11)\n                keep.append(ws)\n            elif IS_MATHS and (re.fullmatch(r'[A-Z][a-z]+ (?:\\S+ ){2,}\\S*[.:,]',txt) and\n                               re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',txt)) or\n                               re.fullmatch(r'Hence,?',txt)):\n                # short sentences 'The median of X is m.' (9709/61/O/N/21 p.7) and a\n                # lone 'Hence' introducing the next romans (9709/61/O/N/17 Q3)\n                keep.append(ws)"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

### Assistant — 2026-10-20 11:27:36

Now the copyright block inside a last crop (12s-32, 14s-13, 11w-33).

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b2; for p in 12s-32 14s-13 11w-33; do ~/.venvs/alevel/bin/python -I -c "
import json;d=json.load(open('AL-MTH-$p-QP/AL-MTH-$p-QP-split-provenance.json'))
for k,v in d['outputs'].items():
  for s in v:
    if s['pdf_page']==4: print('$p',k,s['clip_points'],s['semantic_bounds_points'])"; done; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_s12_qp_32.pdf')
d[3].get_pixmap(dpi=45).save('$S/c1.png')"
```

<details><summary>result</summary>

```
12s-32 Q10.stem [40.0, 60.93, 560.0, 95.28] [60.93, 102.92]
12s-32 Q10.i [40.0, 102.92, 560.0, 121.68] [102.92, 123.36]
12s-32 Q10.ii [40.0, 126.0, 560.0, 147.6] [124.56, 149.28]
12s-32 Q10.iii [40.0, 151.92, 560.0, 792.29] [150.48, 794.29]
14s-13 Q11 [40.0, 61.92, 560.0, 792.21] [61.92, 794.21]
11w-33 Q10.i [40.0, 60.72, 560.0, 120.72] [59.28, 122.5]
11w-33 Q10.ii.stem [40.0, 132.72, 560.0, 152.64] [126.24, 152.64]
11w-33 Q10.ii.a [40.0, 152.64, 560.0, 186.84] [152.64, 177.0]
11w-33 Q10.ii.b [40.0, 186.84, 560.0, 791.9] [178.0, 793.9]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/c1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; AL_DEBUG_ORPHAN=1 SPLITTER_DEBUG_EMITS=Q10.iii ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_s12_qp_32.pdf $S/t8 AL-MTH-12s-32-QP 2>&1 | grep -v "^   "
```

<details><summary>result</summary>

```
DEBUG_EMIT ('Q10.iii', 3, 150.48, 794.2857666015625)
MATHS-RAISED-ROW 2 2 143.0 137.0
MATHS-RAISED-ROW 2 3 457.9 451.9
MATHS-RAISED-ROW 3 8 280.8 274.8
MATHS-RAISED-ROW 3 9 445.9 439.9
produced 24 crops
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "            emits=maths_gap_above_grid(emits)\n", "new_string": "            emits=maths_gap_above_grid(emits)\n            emits=maths_copyright_cap(emits)\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "    def maths_gap_above_grid(emits):", "new_string": "    def maths_copyright_cap(emits):\n        \"\"\"Maths: the last leaf of a paper ran to the page foot and took in the\n        copyright notice printed under it ('Permission to reproduce items ...',\n        9709/32/M/J/12 p.4): end every crop above the notice and its rule.\"\"\"\n        out=[]\n        for lab,p,y0,y1 in emits:\n            tops=[w[1] for w in W[p] if w[4]=='Permission' and any(\n                v[4]=='reproduce' and abs(v[1]-w[1])<3 for v in W[p])]\n            tops=[t for t in tops if y0<t<y1]\n            if tops:\n                t=min(tops)\n                rules=[d['rect'].y0 for d in doc[p].get_drawings() if d.get('rect') is not None\n                       and t-14<d['rect'].y0<t and d['rect'].height<2 and d['rect'].width>200]\n                y1=min([t]+rules)-2\n                if os.environ.get('AL_DEBUG_ORPHAN'):\n                    print('MATHS-COPYRIGHT-CAP',p+1,lab,round(y1,1),file=sys.stderr)\n            out.append((lab,p,y0,y1))\n        return out\n\n    def maths_gap_above_grid(emits):"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

### Assistant — 2026-10-20 11:28:12

Now blank sketch axes printed after a leaf's answer lines (18s-41 Q5(i)) → extra segment of that leaf.

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "    def maths_copyright_cap(emits):", "new_string": "    def maths_axes_after_rows(emits):\n        \"\"\"Maths: blank axes printed after a leaf's answer lines ('Hence sketch a\n        displacement-time graph ... [6]', lines, then the axes, 9709/41/M/J/18\n        Q5(i)) are that leaf's answer grid: kept as an extra segment (user\n        decision 2026-10-20), the dotted lines between stay out.  Only when\n        nothing but answer rows / marks lies between the leaf and the axes.\"\"\"\n        out=list(emits)\n        for p in sorted({e[1] for e in emits}):\n            ar=AR_CACHE.get(p,[])\n            big=[d['rect'] for d in doc[p].get_drawings() if d.get('rect') is not None\n                 and (d['rect'].width>100 or d['rect'].height>100)\n                 and CONTENT_L-5<=d['rect'].x0 and d['rect'].x1<=CONTENT_R+15\n                 and not any(e[1]==p and e[2]<=(d['rect'].y0+d['rect'].y1)/2<=e[3] for e in out)]\n            if not big:\n                continue\n            g0=min(r.y0 for r in big); g1=max(r.y1 for r in big)\n            above=[i for i,e in enumerate(out) if e[1]==p and e[3]<=g0 and not e[0].endswith('.stem')]\n            if not above:\n                continue\n            i=max(above,key=lambda i:out[i][3])\n            ly1=out[i][3]\n            if any(e[1]==p and ly1-1<e[2]<g1 for e in out):\n                continue\n            between=[w for w in W[p] if ly1<w[1]<g0-16 and not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4])\n                     and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar)]\n            if between:\n                continue\n            lo=max([ly1]+[r['y1']+1 for r in ar if ly1<r['y1']<g0])\n            nxt=min([e[2] for e in out if e[1]==p and e[2]>g1]+[min(CONTENT_BOTTOM,FOOTER_Y)])\n            rt,rb=INK[p].extent(lo,nxt-1)\n            if rt is None or rt>g0+1 or rb<g1-1:\n                continue\n            if os.environ.get('AL_DEBUG_ORPHAN'):\n                print('MATHS-AXES-AFTER-ROWS',p+1,out[i][0],round(rt,1),round(rb,1),file=sys.stderr)\n            out.insert(i+1,(out[i][0],p,rt-2,rb+2))\n        return out\n\n    def maths_copyright_cap(emits):"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "            emits=maths_copyright_cap(emits)\n", "new_string": "            emits=maths_copyright_cap(emits)\n            emits=maths_axes_after_rows(emits)\n"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully.
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('review/mth_b2/run_summary.csv')))
open('review/mth/holds_b2.txt','w').write(''.join(x['source']+'\n' for x in r if x['status']=='HOLD'))"; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_t ~/rootatom_data/ALEVEL/review/mth_t; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t --list ~/rootatom_data/ALEVEL/review/mth/holds_b2.txt --no-sheets --workers 8 2>&1 | grep -v "no Q1 anchor"
```

<details><summary>result</summary>

```
[2/21] HOLD 9709_s15_qp_62.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at head of page 3 before Q4.stem
[6/21] HOLD 9709_w03_qp_2.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: no blank row near y=706.0 on page 3
[8/21] PASS 9709_s12_qp_32.pdf crops=24 
[9/21] PASS 9709_s14_qp_13.pdf crops=25 
[10/21] HOLD 9709_w13_qp_32.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: no whitespace around answer row at y=726.3 on page 2
[11/21] HOLD 9709_w04_qp_3.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: no blank row near y=758.9 on page 3
[12/21] HOLD 9709_w15_qp_11.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at foot of page 3 before Q10.stem
[14/21] PASS 9709_w11_qp_33.pdf crops=28 
[15/21] PASS 9709_s18_qp_41.pdf crops=19 
[16/21] HOLD 9709_s22_qp_33.pdf crops=29 coverage
[17/21] PASS 9709_w17_qp_61.pdf crops=24 
[18/21] HOLD 9709_w21_qp_61.pdf crops=20 coverage
[19/21] HOLD 9709_w21_qp_63.pdf crops=20 coverage
[20/21] HOLD 9709_w17_qp_32.pdf crops=26 coverage
[21/21] HOLD 9709_w19_qp_13.pdf crops=30 coverage
this run: PASS 5 / 21; run total PASS 5 / 21
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_t; for p in 21w-61 19w-13; do echo "== $p"; grep -v "^expected" AL-MTH-$p-QP/gates.log | head -4; grep -h "ORPHAN\|MATHS" AL-MTH-$p-QP/splitter.log | head; done; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-18s-41-QP 8 450 400 | head -5
```

<details><summary>result</summary>

```
== 21w-61
  MISSING (7, 63, 'X')
  MISSING (7, 63, 'm.')
  MISSING (7, 66, 'The')
  MISSING (7, 66, 'median')
ORPHAN-HEAD 11 66.7 89.3 -> Q6.b.stem
== 19w-13
  MISSING (17, 56, '`')
  MISSING (17, 56, 'a')
pages 2-19: missing=2 duplicated=0 sliced_boundaries=0 answer_row_words=0 (in a crop: 0)
ORPHAN-HEAD 17 64.3 98.4 -> Q10.ii.stem
MATHS-RAISED-ROW 5 4 66.7 61.9
MATHS-RAISED-ROW 6 5 66.7 61.9
MATHS-RAISED-ROW 12 8 63.8 60.5
MATHS-RAISED-ROW 18 11 66.7 61.9
Q5.stem [40.0, 60.83, 560.0, 110.16] [60.83, 112.08]
Q5.i [40.0, 114.48, 560.0, 149.04] [112.08, 151.82]
Q5.i [40.0, 414.16, 560.0, 749.84] [414.16, 749.84]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/show.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""re.fullmatch(r'[A-Z][a-z]+ (?:\\S+ ){2,}\\S*[.:,]',txt)"""
new="""re.fullmatch(r'[A-Z][a-z]+(?: \\S+){3,}',txt)"""
assert s.count(old)==1, s.count(old); s=s.replace(old,new)
s=s.replace("""                # short sentences 'The median of X is m.' (9709/61/O/N/21 p.7) and a""","""                # short sentences 'The median of X is m.' (9709/61/O/N/21 p.7; its
                # raised 'X' / 'm.' fall in the next 3-pt row bucket) and a""")
open(p,'w').write(s)
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_w21_qp_61.pdf 9709_w21_qp_63.pdf --no-sheets --workers 2 | tail -3; grep -v "^expected" ~/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-21w-61-QP/gates.log | head -3
```

<details><summary>result</summary>

```
[1/2] PASS 9709_w21_qp_63.pdf crops=21 
[2/2] PASS 9709_w21_qp_61.pdf crops=21 
this run: PASS 2 / 2; run total PASS 7 / 21
pages 3-13: missing=0 duplicated=0 sliced_boundaries=0 answer_row_words=0 (in a crop: 0)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits/mth_t; ls AL-MTH-21w-61-QP | grep Q4; ls AL-MTH-17w-61-QP | grep Q3; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
fs=['AL-MTH-21w-61-QP/AL-MTH-21w-61-QP-Q4.c.stem.png','AL-MTH-21w-61-QP/AL-MTH-21w-61-QP-Q4.c.png','AL-MTH-17w-61-QP/AL-MTH-17w-61-QP-Q3.ii.png']
import os
ims=[Image.open(f) for f in fs if os.path.exists(f)]
W=max(i.width for i in ims); H=sum(i.height+20 for i in ims)
c=Image.new('RGB',(W,H),(200,200,200)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+20
c.save('$S/v5.png')"
```

<details><summary>result</summary>

```
AL-MTH-21w-61-QP-Q4.a.png
AL-MTH-21w-61-QP-Q4.b.png
AL-MTH-21w-61-QP-Q4.c.png
AL-MTH-21w-61-QP-Q4.c.stem.png
AL-MTH-21w-61-QP-Q4.stem.png
AL-MTH-17w-61-QP-Q3.i.png
AL-MTH-17w-61-QP-Q3.ii.png
AL-MTH-17w-61-QP-Q3.iii.png
AL-MTH-17w-61-QP-Q3.stem.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/v5.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:29:20

"The median…" now goes to Q4.c.stem and "Hence" to the top of (ii), per the house rule. Checking 15w-11's foot-of-page error.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "unlabelled content at foot" al_qp_splitter.py | head -3; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; AL_DEBUG_ORPHAN=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w15_qp_11.pdf $S/t9 AL-MTH-15w-11-QP 2>&1 | grep -v "^   " | grep -i "orphan\|foot" | head
```

<details><summary>result</summary>

```
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 3375, in alevel_orphan_tails
  File "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", line 3172, in orphan_owner
RuntimeError: REVIEW_REQUIRED: unlabelled content at foot of page 3 before Q10.stem
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 3335,3376p al_qp_splitter.py
```

<details><summary>result</summary>

```
            except RuntimeError:
                continue                # ambiguous (e.g. before a new question): leave it with the leaf
            for k,(pp,a,b) in enumerate(moved):
                keep.insert(ins+k,(owner,pp,a,b))
            # reshaped pieces keep the stop-clamp exemption of the segments
            # they came from (else the clamp cut them at their dotted rows)
            if (lab,cp,round(ca,3),round(cb,3)) in AL_BYPASS:
                AL_BYPASS.add((lab,cp,round(ca,3),round(cy-2,3)))
            for (pp,a,b) in moved:
                AL_BYPASS.add((owner,pp,round(a,3),round(b,3)))
            out=keep
        return out

    def alevel_orphan_tails(emits):
        """A Level: shared context printed at the FOOT of a page whose next
        label starts on a later page (9701/42/F/M/19 p.18: 'Ethanedioyl
        dichloride is used in the following synthesis ...' + the reaction
        scheme after (a)(ii); '(b) (i)' opens p.19).  Owner: orphan_owner()."""
        out=list(emits)
        for p in sorted({e[1] for e in emits}):
            on_p=[e for e in out if e[1]==p]
            bottom=max(e[3] for e in on_p)
            later=sorted([e for e in out if e[1]>p],key=lambda e:(e[1],e[2]))
            if not later:
                continue
            ar=answer_rows(p)
            prose_rows=orphan_prose(p,bottom+1,page_cap,ar)
            if not prose_rows:
                continue
            top=min(w[1] for w in prose_rows[0])
            # an answe
… [764 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; sed 's/            top=min(w\[1\] for w in prose_rows\[0\])\n            # an answer row/&/' al_qp_splitter.py | ~/.venvs/alevel/bin/python -I -c "
import sys;s=sys.stdin.read()
s=s.replace(\"\"\"            prose_rows=orphan_prose(p,bottom+1,page_cap,ar)
            if not prose_rows:
                continue
            top=min(w[1] for w in prose_rows[0])\n            # an answer row\"\"\",\"\"\"            prose_rows=orphan_prose(p,bottom+1,page_cap,ar)
            if not prose_rows:
                continue
            print('TAILROWS',p+1,[' '.join(w[4] for w in ws)[:80] for ws in prose_rows],file=sys.stderr)
            top=min(w[1] for w in prose_rows[0])\n            # an answer row\"\"\")
open('$S/dbg3.py','w').write(s)"; ~/.venvs/alevel/bin/python -I $S/dbg3.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w15_qp_11.pdf $S/t9 AL-MTH-15w-11-QP 2>&1 | grep TAILROWS
```

<details><summary>result</summary>

```
TAILROWS 3 ['Permission to reproduce items where third-party owned material protected by copy', 'effort has been made by the publisher (UCLES) to trace copyright holders, but if', 'be pleased to make amends at the earliest possible opportunity.', 'To avoid the issue of disclosure of answer-related information to candidates, al', 'Examinations Copyright Acknowledgements Booklet. This is produced for each serie', 'the live examination series.', 'Cambridge International Examinations is part of the Cambridge Assessment Group. ', 'Examinations Syndicate (UCLES), which is itself a department of the University o']
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:29:41

The copyright notice printed mid-paper (page 3 of 4) is read as orphan prose. Making maths orphan-prose stop at the notice.

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "        rows={}\n        for w in W[p]:\n            if lo<w[1]<hi and not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4]) \\", "new_string": "        rows={}\n        if IS_MATHS:\n            # the copyright notice can close a middle page ('[Questions 10 and 11\n            # are printed on the next page.]' + notice, 9709/11/O/N/15 p.3)\n            hi=min([hi]+[w[1]-1 for w in W[p] if w[4]=='Permission' and any(\n                v[4]=='reproduce' and abs(v[1]-w[1])<3 for v in W[p])])\n        for w in W[p]:\n            if lo<w[1]<hi and not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4]) \\"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_w15_qp_11.pdf 9709_w19_qp_13.pdf 9709_s15_qp_62.pdf --no-sheets --workers 3 | tail -4; grep -v "^expected" ~/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-15w-11-QP/gates.log | head -4
```

<details><summary>result</summary>

```
[1/3] HOLD 9709_s15_qp_62.pdf crops=0 splitter: RuntimeError: REVIEW_REQUIRED: unlabelled content at head of page 3 before Q4.stem
[2/3] HOLD 9709_w15_qp_11.pdf crops=28 coverage
[3/3] HOLD 9709_w19_qp_13.pdf crops=30 coverage
this run: PASS 0 / 3; run total PASS 7 / 21
  MISSING (4, 732, '[In')
  MISSING (4, 732, 'part')
  MISSING (4, 731, '(ii)')
  MISSING (4, 732, 'you')
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-15w-11-QP 4 700 100
```

<details><summary>result</summary>

```
Q11.stem [40.0, 445.2, 560.0, 656.88] [445.2, 658.99]
Q11.i [40.0, 661.68, 560.0, 683.28] [658.99, 684.96]
Q11.ii [40.0, 687.6, 560.0, 722.16] [686.16, 723.84]
show.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/show.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:30:09

Hint pass picks the rightmost word across both wrapped rows instead of the last row's end. Fixing.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                    last=max(row,key=lambda v:v[2])"""
new="""                    last=max([v for v in row if (v[1]+v[3])/2>bot-9],key=lambda v:v[2])   # end of the LAST row"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_w15_qp_11.pdf --no-sheets | tail -1; grep -v "^expected" ~/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-15w-11-QP/gates.log | head -4
```

<details><summary>result</summary>

```
this run: PASS 1 / 1; run total PASS 8 / 21
pages 2-4: missing=0 duplicated=0 sliced_boundaries=0 answer_row_words=2 (in a crop: 2)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/Users/nitya/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-15w-11-QP/AL-MTH-15w-11-QP-Q11.ii.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:30:21

15w-11 now passes. Looking at 15s-62 (tree diagram at the head of page 3).

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
from PIL import Image
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_s15_qp_62.pdf')
d[1].get_pixmap(dpi=45).save('$S/p2.png'); d[2].get_pixmap(dpi=45).save('$S/p3.png')
a=Image.open('$S/p2.png');b=Image.open('$S/p3.png'); c=Image.new('RGB',(a.width*2,a.height)); c.paste(a,(0,0)); c.paste(b,(a.width,0)); c.save('$S/p23.png')"
```

<details><summary>result</summary>

```
(Bash completed with no output)
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/p23.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; n=$(grep -n "    def orphan_owner" al_qp_splitter.py | cut -d: -f1); sed -n "$n,$((n+75))p" al_qp_splitter.py
```

<details><summary>result</summary>

```
    def orphan_owner(p,where,region_ws,nxt_emit,out):
        """Owner of unlabelled context found at the foot/head of page p.

        * a captioned figure/table ('Table 4.1') belongs to the FIRST leaf of
          the question whose own text names it (9701/22/F/M/23 Q4(d)(i): 'Use
          information from Table 4.1 (on page 14)'), even when printed after it;
        * otherwise the next item owns it: the highest part that starts with
          that item and has not started yet -> '<part>.stem' (Q7.b.stem), else
          the next leaf's own lead-in;
        * prose before a NEW question's number is REVIEW_REQUIRED.
        Returns (label, index in `out` to insert the segment at)."""
        nxt=nxt_emit[0]
        q=nxt.split('.')[0]
        # only a region that OPENS with its caption is a floated figure/table;
        # prose-led context ('In both experiments the student ...' with Tables
        # 1.1/1.2 inside, 9701/52/F/M/17 p.2) is shared setup for what follows
        first_row=sorted([w for w in region_ws if abs(w[1]-min(v[1] for v in region_ws))<3],key=lambda w:w[0])
        caps=set(CAPTION_RE.findall(' '.join(w[4] for w in first_row)))
        # a FIGURE caption anywhere in the region also follows its first
        # referencing leaf (the gate's figure-ownership rule; 9701/52/M/J/25
        # Fig. 1.2 named by (h)(i), printed before part (i))
        caps|={c for c in CAPTION_RE.findall(' '.join(w[4] for w in sorted(region_ws,key=lambda w:(round(w[1]/3),w[0]))))
… [3181 more characters trimmed]
```
</details>

### Assistant — 2026-10-20 11:30:40

Maths rule for orphan_owner: content at a page head that starts at or below a question's own number on that page belongs to that question's first crop.

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "        prev=[e for e in out if (e[1],e[2])<(nxt_emit[1],nxt_emit[2])]\n        if not prev or max(prev,key=lambda e:(e[1],e[3]))[0].split('.')[0]!=q:", "new_string": "        prev=[e for e in out if (e[1],e[2])<(nxt_emit[1],nxt_emit[2])]\n        if IS_MATHS and not [e for e in prev if e[0].split('.')[0]==q]:\n            # a diagram printed beside / under the question's own number, above\n            # its context prose ('4' + tree diagram, then 'Nikita goes shopping\n            # ...', 9709/62/M/J/15 p.3) is the start of that question's first crop\n            qa=[a for a in A.get(p,[]) if a['kind']=='Q' and f\"Q{a['label']}\"==q]\n            if qa and nxt_emit[1]==p and min(w[1] for w in region_ws)>=qa[0]['y']-12:\n                return nxt,out.index(nxt_emit)\n        if not prev or max(prev,key=lambda e:(e[1],e[3]))[0].split('.')[0]!=q:"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_s15_qp_62.pdf --no-sheets | tail -1; grep -v "^expected" ~/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-15s-62-QP/gates.log | head -4; ls ~/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-15s-62-QP | grep Q4
```

<details><summary>result</summary>

```
this run: PASS 1 / 1; run total PASS 9 / 21
pages 2-3: missing=0 duplicated=0 sliced_boundaries=0 answer_row_words=1 (in a crop: 1)
AL-MTH-15s-62-QP-Q4.i.png
AL-MTH-15s-62-QP-Q4.ii.png
AL-MTH-15s-62-QP-Q4.stem.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/Users/nitya/rootatom_data/ALEVEL/splits/mth_t/AL-MTH-15s-62-QP/AL-MTH-15s-62-QP-Q4.stem.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:30:52

Good. Quick look at 19w-13 (bracket pieces at a page head).

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_t AL-MTH-19w-13-QP 17 80 30; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_w19_qp_13.pdf')
for w in d[16].get_text('words')[:14]: print([round(v,1) if isinstance(v,float) else v for v in w[:5]])"
```

<details><summary>result</summary>

```
Q10.ii.stem [40.0, 62.32, 560.0, 100.4] [62.32, 100.4]
Q10.ii [40.0, 108.24, 560.0, 129.84] [107.28, 132.86]
show.png
[291.5, 39.8, 303.2, 51.2, '17']
[72.8, 75.8, 91.2, 87.2, 'The']
[94.1, 75.8, 131.7, 87.2, 'position']
[134.5, 75.8, 163.5, 87.2, 'vector']
[166.6, 75.8, 176.0, 87.2, 'of']
[178.9, 75.8, 184.2, 87.2, 'a']
[187.1, 75.8, 211.3, 87.2, 'point']
[214.2, 75.3, 222.4, 87.2, 'C']
[225.6, 75.8, 233.5, 87.2, 'is']
[236.4, 75.8, 262.0, 87.2, 'given']
[265.0, 75.8, 276.7, 87.2, 'by']
[279.6, 67.1, 296.9, 78.1, '−−→']
[279.6, 75.3, 296.7, 87.2, 'OC']
[300.0, 74.6, 306.9, 85.6, '=']
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/show.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I - <<EOF
s=open('al_qp_splitter.py').read()
s=s.replace("""        if IS_MATHS:
            # big-bracket pieces""","""        if pno==16 and y0<70: print('BOX',label,y0,y1,rt,rb,cy0,cy1,lim_lo,file=sys.stderr)
        if IS_MATHS:
            # big-bracket pieces""")
s=s.replace("""        boxes.append([label,pno,cy0,cy1,rt,rb,emit_order,[],y0,y1])""","""        if pno==16 and y0<70: print('BOX2',label,cy0,cy1,file=sys.stderr)
        boxes.append([label,pno,cy0,cy1,rt,rb,emit_order,[],y0,y1])""")
open('$S/dbg4.py','w').write(s)
EOF
~/.venvs/alevel/bin/python -I $S/dbg4.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w19_qp_13.pdf $S/t10 AL-MTH-19w-13-QP 2>&1 | grep BOX
```

<details><summary>result</summary>

```
BOX Q10.ii.stem 62.31999999999999 100.39999999999999 64.32 98.39999999999999 62.31999999999999 100.39999999999999 62.31999999999999
BOX2 Q10.ii.stem 62.31999999999999 100.39999999999999
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:31:19

The bracket piece's text box starts above the header line, so it isn't in the splitter's word list. Using the page's raw words for that edge check.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""            for w in W[pno]:
                c=(w[1]+w[3])/2
                if len(w[4])>2 or DOTS_RE.match(w[4]) or MARK_RE.match(w[4]):"""
new="""            for w in doc[pno].get_text('words'):   # (not W: a piece can start above HEADER_Y)
                c=(w[1]+w[3])/2
                if len(w[4])>2 or DOTS_RE.match(w[4]) or MARK_RE.match(w[4]):"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_t 9709_w19_qp_13.pdf --no-sheets | tail -1
```

<details><summary>result</summary>

```
this run: PASS 1 / 1; run total PASS 10 / 21
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:31:31

Remaining 11 look like manual-spec cases. Bio check, then a full run of all 826 QPs (730 + 96 new) into mth_b3.

**Tool `Bash`**

```
/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/biochk.sh; cat ~/rootatom_data/ALEVEL/review/mth/all_qp.txt ~/rootatom_data/ALEVEL/review/mth/new_qp.txt | sort -u > ~/rootatom_data/ALEVEL/review/mth/all_qp2.txt; wc -l < ~/rootatom_data/ALEVEL/review/mth/all_qp2.txt; df -h ~ | tail -1
```

<details><summary>result</summary>

```
this run: PASS 3 / 3; run total PASS 3 / 3
AL-BIO-24s-22-QP IDENTICAL 43 43
AL-BIO-17w-42-QP IDENTICAL 56 56
AL-BIO-13s-52-QP IDENTICAL 17 17
     826
/dev/disk3s5   228Gi   186Gi    14Gi    93%    2.6M  147M    2%   /System/Volumes/Data
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; rm -rf splits/mth_p review/mth_p splits/mth_t review/mth_t; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_b3 ~/rootatom_data/ALEVEL/review/mth_b3; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b3 --list ~/rootatom_data/ALEVEL/review/mth/all_qp2.txt --no-sheets --workers 8 > /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b3.log 2>&1
```

<details><summary>result</summary>

```
Command running in background with ID: bl4x42by5. Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bl4x42by5.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e; directory changes made by the backgrounded command do not apply to subsequent commands.
```
</details>

### Assistant — 2026-10-20 11:31:52

The full run of all 826 QPs (mth_b3) is going. I won't edit any scripts until it finishes; I'll compare it against mth_b2 then.

Status: committed 13b2f2e. The uncommitted follow-ups (short context rows, sketch axes after answer lines, copyright cap, wrapped hints, a diagram beside a question number) cut the remaining holds from 21 to 11. All 11 look like manual-spec cases: 6 image-only scans, 3 with tall maths touching the footer or answer row, and 2 genuine 2-D interleaves. Biology is still 3/3 byte-identical.

### User — 2026-10-20 11:42:54

<task-notification>
<task-id>bl4x42by5</task-id>
<tool-use-id>toolu_01H4CHaAc1ZRzqcSw56RLHAG</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bl4x42by5.output</output-file>
<status>completed</status>
<summary>Background command "cd ~/rootatom_data/ALEVEL; rm -rf splits/mth_p review/mth_p splits/mth_t review/mth_t; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_b3 ~/rootatom_data/ALEVEL/review/mth_b3; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b3 --list ~/rootatom_data/ALEVEL/review/mth/all_qp2.txt --no-sheets --workers 8 &gt; /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b3.log 2&gt;&amp;1" completed (exit code 0)</summary>
</task-notification>

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b3.log; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_compare_runs.py mth_b2 mth_b3 | tail -3; cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('review/mth_b3/compare.csv')))
for x in r:
  if x['class'] in ('changed','regressed') or (x['class']=='hold'): print(x['class'],x['prefix'],x['reason'][:60])
new=[x for x in csv.DictReader(open('review/mth_b3/run_summary.csv'))]
b2={x['source'] for x in csv.DictReader(open('review/mth_b2/run_summary.csv'))}
nw=[x for x in new if x['source'] not in b2]
print('new papers',len(nw),'PASS',sum(x['status']=='PASS' for x in nw))
for x in nw:
  if x['status']!='PASS': print('  NEWHOLD',x['prefix'],x['reason'][:150])
"
```

<details><summary>result</summary>

```
this run: PASS 808 / 826; run total PASS 808 / 826
{'hold': 16, 'same': 702, 'newpass': 101, 'changed': 5, 'regressed': 2}
  REGRESSED AL-MTH-13w-31-QP splitter: ValueError: max() iterable argument is empty
  REGRESSED AL-MTH-19w-12-QP splitter: ValueError: max() iterable argument is empty
hold AL-MTH-01w-21-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found 
hold AL-MTH-01w-41-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found 
hold AL-MTH-01w-61-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found 
hold AL-MTH-02s-21-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found 
hold AL-MTH-02s-31-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found 
hold AL-MTH-02w-31-QP splitter: RuntimeError: REVIEW_REQUIRED: no Q1 anchor found 
hold AL-MTH-03w-21-QP splitter: RuntimeError: REVIEW_REQUIRED: no blank row near y
hold AL-MTH-04w-31-QP splitter: RuntimeError: REVIEW_REQUIRED: no blank row near y
hold AL-MTH-09s-71-QP leaves coverage
changed AL-MTH-09w-12-QP 
changed AL-MTH-12s-22-QP 
changed AL-MTH-13s-21-QP 
changed AL-MTH-13s-23-QP 
regressed AL-MTH-13w-31-QP splitter: ValueError: max() iterable argument is empty
hold AL-MTH-13w-32-QP splitter: RuntimeError: REVIEW_REQUIRED: no whitespace aroun
hold AL-MTH-17w-32-QP coverage
changed AL-MTH-17w-63-QP 
hold AL-MTH-19s-43-QP coverage
hold AL-MTH-19s-51-QP coverage
hold AL-MTH-19s-53-QP coverage
regressed AL-MTH-19w-12-QP splitter: ValueError: max() iterable argument is empty
hold A
… [412 more characters trimmed]
```
</details>

### Assistant — 2026-10-20 11:43:12

Two crashes from my wrapped-hint fix (empty last-row selection). Fixing with a fallback.

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='al_qp_splitter.py'; s=open(p).read()
old="""                    last=max([v for v in row if (v[1]+v[3])/2>bot-9],key=lambda v:v[2])   # end of the LAST row"""
new="""                    last=max([v for v in row if (v[1]+v[3])/2>bot-9] or row,key=lambda v:v[2])   # end of the LAST row"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
EOF
~/.venvs/alevel/bin/python -I al_run_papers.py mth_b3 9709_w13_qp_31.pdf 9709_w19_qp_12.pdf --no-sheets --workers 2 | tail -3
```

<details><summary>result</summary>

```
[1/2] PASS 9709_w13_qp_31.pdf crops=23 
[2/2] PASS 9709_w19_qp_12.pdf crops=33 
this run: PASS 2 / 2; run total PASS 810 / 826
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:43:23

Now viewing the 5 changed papers (vs mth_b2) plus the two hint papers.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits; ~/.venvs/alevel/bin/python -I -c "
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw
rows=[]
for p in ['AL-MTH-09w-12-QP','AL-MTH-12s-22-QP','AL-MTH-13s-21-QP','AL-MTH-13s-23-QP','AL-MTH-17w-63-QP','AL-MTH-13w-31-QP','AL-MTH-19w-12-QP']:
  a={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('mth_b2/'+p).glob('*.png')}
  b={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('mth_b3/'+p).glob('*.png')}
  ch=sorted(k for k in set(a)|set(b) if a.get(k)!=b.get(k)); print(p,[k[len(p)+1:-4] for k in ch])
  for k in ch[:2]:
    ims=[Image.open(f'{r}/{p}/{k}').convert('RGB') if Path(f'{r}/{p}/{k}').exists() else Image.new('RGB',(100,50),'red') for r in ('mth_b2','mth_b3')]
    W=sum(i.width for i in ims)+30; H=max(i.height for i in ims)+25
    c=Image.new('RGB',(W,H),(170,170,170)); c.paste(ims[0],(0,25)); c.paste(ims[1],(ims[0].width+30,25)); ImageDraw.Draw(c).text((5,5),k+' OLD|NEW',fill=(0,0,0)); rows.append(c)
W=max(r.width for r in rows); H=sum(r.height for r in rows)
o=Image.new('RGB',(W,H),'white'); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height
o.resize((W//3,H//3)).save('$S/cmp3.png'); print(W//3,H//3)"
```

<details><summary>result</summary>

```
AL-MTH-09w-12-QP ['Q9.i', 'Q9.ii']
AL-MTH-12s-22-QP ['Q4.i', 'Q4.ii']
AL-MTH-13s-21-QP ['Q7.i', 'Q7.ii']
AL-MTH-13s-23-QP ['Q7.i', 'Q7.ii']
AL-MTH-17w-63-QP ['Q5.ii']
AL-MTH-13w-31-QP []
AL-MTH-19w-12-QP []
1070 900
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/cmp3.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:43:38

All changes follow the house rules ("context after a mark belongs to the next part"; grid kept with its leaf). Now the 5 holds among the new papers.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b3; for p in 09s-71 19s-43 19s-51 19s-53 25w-15; do echo "== $p $(grep -v '^pages' AL-MTH-$p-QP/gates.log | head -4 | tr '\n' ' ' | cut -c1-330)"; done
```

<details><summary>result</summary>

```
== 09s-71 expected=16 produced=14 missing=['Q6.iii', 'Q6.iv'] extra=[]   MISSING (6, 92, 'UNIVERSITY')   MISSING (6, 92, 'OF')   MISSING (6, 92, 'CAMBRIDGE') 
== 19s-43 expected=12 produced=12 missing=[] extra=[]   MISSING (3, 494, 'Component')   MISSING (3, 494, 'in')   MISSING (3, 494, 'y-direction...............................................................................................................') 
== 19s-51 expected=15 produced=15 missing=[] extra=[]   MISSING (10, 343, 'Distance')   MISSING (10, 343, 'from')   MISSING (10, 342, 'BC') 
== 19s-53 expected=15 produced=15 missing=[] extra=[]   MISSING (10, 343, 'Distance')   MISSING (10, 343, 'from')   MISSING (10, 342, 'BC') 
== 25w-15 expected=25 produced=24 missing=['Q11.c.ii'] extra=[]   MISSING (17, 648, '(c)')   MISSING (17, 648, '(ii)')   MISSING (17, 648, 'State')
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_b3 AL-MTH-19s-43-QP 3 480 60 >/dev/null; cp show.png d1.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_b3 AL-MTH-25w-15-QP 17 640 60 >/dev/null; cp show.png d2.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_b3 AL-MTH-09s-71-QP 6 150 100 >/dev/null; cp show.png d3.png; ~/.venvs/alevel/bin/python -I bin/show.py mth_b3 AL-MTH-19s-51-QP 10 340 50 >/dev/null; cp show.png d4.png
```

<details><summary>result</summary>

```
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/d1.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/d2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/d3.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/d4.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:44:01

09s-71 is a combined source (the 9709/72 paper follows from page 6) → needs a derived source split like 9702_s09_qp_2. Checking the labelled answer rows in 19s-51/53 and 19s-43.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; ~/.venvs/alevel/bin/python -I bin/show.py mth_b3 AL-MTH-19s-51-QP 10 300 250; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_s19_qp_51.pdf')
for w in d[9].get_text('words'):
  if 320<w[1]<360 or 150<w[1]<200: print([round(v,1) if isinstance(v,float) else v for v in w[:5]])" | head -20
```

<details><summary>result</summary>

```
Q6.stem [40.0, 61.92, 560.0, 209.04] [61.92, 210.84]
Q6.i [40.0, 213.36, 560.0, 234.48] [210.84, 237.62]
Q6.ii.stem [40.0, 242.16, 560.0, 272.52] [238.08, 431.4]
Q6.ii [40.0, 432.4, 560.0, 475.44] [432.4, 478.34]
show.png
[72.8, 179.0, 96.0, 190.9, 'ABC']
[99.6, 179.5, 107.4, 190.9, 'is']
[110.6, 179.5, 115.9, 190.9, 'a']
[119.0, 179.5, 157.0, 190.9, 'uniform']
[160.2, 179.5, 192.2, 190.9, 'lamina']
[195.4, 179.5, 204.5, 190.9, 'in']
[207.7, 179.5, 222.1, 190.9, 'the']
[225.3, 179.5, 248.2, 190.9, 'form']
[251.4, 179.5, 260.9, 190.9, 'of']
[264.0, 179.5, 269.3, 190.9, 'a']
[272.4, 179.5, 308.3, 190.9, 'triangle']
[311.6, 179.5, 332.3, 190.9, 'with']
[335.4, 179.0, 350.5, 190.9, 'AB']
[353.8, 177.3, 360.6, 188.3, '=']
[363.8, 179.5, 378.6, 190.9, '0.3']
[380.5, 179.5, 392.6, 190.9, 'm,']
[395.9, 179.0, 411.6, 190.9, 'BC']
[415.1, 177.3, 421.9, 188.3, '=']
[425.3, 179.5, 439.9, 190.9, '0.6']
[442.0, 179.5, 451.1, 190.9, 'm']
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/show.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n "$(grep -n '^def leader_run' al_qp_splitter.py | cut -d: -f1),+36p" al_qp_splitter.py
```

<details><summary>result</summary>

```
def leader_run(tok):
    """Longest dot run in a token, counting '…' as three dots (2007 papers
    set leaders as ellipsis characters: '………………………' = 24 dots)."""
    return max((len(m)+2*m.count('…') for m in re.findall(r'[.…]+',tok)),default=0)


def is_leader(w,words=None):
    """An answer leader: >=10 dots AND (>=50 pt wide OR after an '=' label on
    the same line).  Short unlabelled dotted blanks are slots INSIDE printed
    prompt text -- equation blanks ('...... He', 9702/21/O/N/25) and nuclide
    numbers ('............ Fr', 9702/02/O/N/02); 'density = ..... ± .....
    g cm-3' (9702/21/M/J/09) has two short labelled leaders."""
    if not (re.match(r'^[.…]{3,}',w[4]) and leader_run(w[4])>=10):
        return False
    if (w[2]-w[0])>=50:
        return True
    # the '=' must label THIS leader: only dots / '±' may sit between them.  A
    # worked example 'δ = 1.2' further left on a structure diagram's row made
    # the diagram's fill-in blanks answer rows (9701/42/M/J/19 Q5(c)(iii))
    if words is None:
        return False
    # a short slot alone on its row (apart from a mark) is an answer line too:
    # '................  [1]' (9701/21/O/N/13 Q2(a))
    # (body column only: nuclide slots '......' above/below 'Fr' stay with
    # their symbol, 9702/02/O/N/02 Q8(a))
    row=[u for u in words if abs(u[1]-w[1])<4 and u is not w]
    if w[0]<140 and all(re.fullmatch(r'\[\d+\]|[.…]+',u[4]) for u in row):
        return True
    for v in words:
        if v[4].end
… [431 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 1,80p fused_marks.py
```

<details><summary>result</summary>

```
"""Split dotted-leader tokens that carry a fused mark into two words.

Many Cambridge PDFs set the mark with no space after the answer line, so
PyMuPDF returns one word '..........[3]' (1,683 tokens in 134 9702 papers).
Every mark-based rule (part ends at its [n]; lone [n] kept under the prompt)
then misses the mark -- 9702/42/O/N/16 Q11(b) lost its prompt to a phantom
(c) stem.  install() wraps Page.get_text so 'words' output returns
'..........' and '[3]' as separate words, with exact boxes taken from the
PDF's own character positions.  Splitter and verifiers all call install(),
so they see identical words.
"""

from __future__ import annotations

import re

import pymupdf as fitz

FUSED_RE = re.compile(r"^(.*?[.…]{3,})(\[\d+\])$")
_orig = fitz.Page.get_text


def _char_split_x(page, rect, mark):
    """x of the '[' that starts `mark` inside `rect`, from rawdict chars."""
    raw = _orig(page, "rawdict", clip=fitz.Rect(rect) + (-1, -1, 1, 1))
    # only this row's characters: a '[Turn over' just below would otherwise
    # interleave with the mark (9700/42/F/M/18 p9)
    chars = [c for b in raw.get("blocks", []) for l in b.get("lines", [])
             for s in l.get("spans", []) for c in s.get("chars", [])
             if rect[1] <= (c["bbox"][1] + c["bbox"][3]) / 2 <= rect[3]]
    chars.sort(key=lambda c: c["bbox"][0])
    text = "".join(c["c"] for c in chars)
    k = text.rfind(mark)
    if k < 0:
        return None
    return chars[k]["bbox"][0]


def _split_words(page
… [878 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "fused_marks" *.py | grep -v "^fused_marks.py"
```

<details><summary>result</summary>

```
al_addmarks.py:25:import fused_marks  # noqa: E402
al_addmarks.py:26:fused_marks.install()
al_manual.py:57:    import fused_marks
al_manual.py:58:    fused_marks.install()
al_qp_splitter.py:29:import fused_marks; fused_marks.install()
al_verify_coverage.py:39:import fused_marks  # noqa: E402
al_verify_coverage.py:40:fused_marks.install()
al_verify_leaves.py:31:import fused_marks  # noqa: E402
al_verify_leaves.py:32:fused_marks.install()
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I - <<'EOF'
p='fused_marks.py'; s=open(p).read()
s=s.replace('''FUSED_RE = re.compile(r"^(.*?[.…]{3,})(\\[\\d+\\])$")
_orig = fitz.Page.get_text
''','''FUSED_RE = re.compile(r"^(.*?[.…]{3,})(\\[\\d+\\])$")
# a label fused to its answer leader: 'AB.........' ('Distance from AB......',
# 9709/51/M/J/19 Q6(i)) -> 'AB' + the leader; opt-in (Maths), see install()
LEADER_RE = re.compile(r"^(.*?[^.…\\s])([.…]{10,})$")
_orig = fitz.Page.get_text
_leaders = False
''')
old='''def _split_words(page, words):
    out = []
    for w in words:
        m = FUSED_RE.match(w[4]) if isinstance(w[4], str) else None
'''
new='''def _split_words(page, words):
    out = []
    for w in words:
        if _leaders and isinstance(w[4], str):
            ml = LEADER_RE.match(w[4])
            if ml and re.search(r"[A-Za-z0-9)]$", ml[1]):
                x = _char_split_x(page, w[:4], ml[2])
                if x is not None and w[0] < x < w[2]:
                    out.append((w[0], w[1], x, w[3], ml[1]) + tuple(w[5:]))
                    w = (x, w[1], w[2], w[3], ml[2]) + tuple(w[5:])
        m = FUSED_RE.match(w[4]) if isinstance(w[4], str) else None
'''
assert s.count(old)==1; s=s.replace(old,new)
old='''def install() -> None:
    if fitz.Page.get_text is not _get_text:'''
new='''def install(leaders: bool = False) -> None:
    """leaders=True also splits label-fused leaders (Maths prefixes only, so
    approved Physics/Chemistry/Biology words are unchanged)."""
    global _leaders
    _leaders = leaders
    if fitz.Page.get_text is not _get_text:'''
assert s.count(old)==1; s=s.replace(old,new)
open(p,'w').write(s)
for f,old,new in [('al_verify_coverage.py','fused_marks.install()\n','fused_marks.install(leaders=len(sys.argv) > 3 and sys.argv[3].startswith(("AL-MTH-", "AL-FMT-")))\n'),
                  ('al_verify_leaves.py','fused_marks.install()\n','fused_marks.install(leaders=len(sys.argv) > 3 and sys.argv[3].startswith(("AL-MTH-", "AL-FMT-")))\n'),
                  ('al_qp_splitter.py','import fused_marks; fused_marks.install()\n','import fused_marks; fused_marks.install(leaders=len(sys.argv) > 3 and sys.argv[3].startswith((\'AL-MTH-\',\'AL-FMT-\')))\n')]:
    s=open(f).read(); assert s.count(old)==1,f; open(f,'w').write(s.replace(old,new))
EOF
grep -n "^import sys\|^import.*sys" al_verify_coverage.py al_verify_leaves.py | head; sed -n 36,41p al_verify_coverage.py
```

<details><summary>result</summary>

```
al_verify_leaves.py:25:import sys
al_verify_leaves.py:29:import os as _os, sys as _sys
al_verify_coverage.py:31:import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from barcode_rule import is_barcode_span  # noqa: E402
import fused_marks  # noqa: E402
fused_marks.install(leaders=len(sys.argv) > 3 and sys.argv[3].startswith(("AL-MTH-", "AL-FMT-")))
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b3 9709_s19_qp_51.pdf 9709_s19_qp_53.pdf 9709_s19_qp_43.pdf --no-sheets --workers 3 | tail -4
```

<details><summary>result</summary>

```
[1/3] PASS 9709_s19_qp_43.pdf crops=17 
[2/3] PASS 9709_s19_qp_51.pdf crops=21 
[3/3] PASS 9709_s19_qp_53.pdf crops=21 
this run: PASS 3 / 3; run total PASS 813 / 826
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits/mth_b3; ls AL-MTH-19s-51-QP | grep Q6; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
fs=['AL-MTH-19s-51-QP/AL-MTH-19s-51-QP-Q6.i.png','AL-MTH-19s-51-QP/AL-MTH-19s-51-QP-Q6.ii.png','AL-MTH-19s-43-QP/AL-MTH-19s-43-QP-Q2.png']
import os,glob
fs=[f for f in fs if os.path.exists(f)]
ims=[Image.open(f) for f in fs]; W=max(i.width for i in ims); H=sum(i.height+20 for i in ims)
c=Image.new('RGB',(W,H),(200,200,200)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+20
c.resize((W//2,H//2)).save('$S/v6.png')"; ls AL-MTH-19s-43-QP | head -30
```

<details><summary>result</summary>

```
AL-MTH-19s-51-QP-Q6.i.png
AL-MTH-19s-51-QP-Q6.ii.png
AL-MTH-19s-51-QP-Q6.iii.png
AL-MTH-19s-51-QP-Q6.iii.stem.png
AL-MTH-19s-51-QP-Q6.stem.png
AL-MTH-19s-43-QP-Q1.png
AL-MTH-19s-43-QP-Q2.i.png
AL-MTH-19s-43-QP-Q2.ii.png
AL-MTH-19s-43-QP-Q2.stem.png
AL-MTH-19s-43-QP-Q3.i.png
AL-MTH-19s-43-QP-Q3.ii.png
AL-MTH-19s-43-QP-Q3.stem.png
AL-MTH-19s-43-QP-Q4.i.png
AL-MTH-19s-43-QP-Q4.ii.png
AL-MTH-19s-43-QP-Q4.stem.png
AL-MTH-19s-43-QP-Q5.i.png
AL-MTH-19s-43-QP-Q5.ii.png
AL-MTH-19s-43-QP-Q5.stem.png
AL-MTH-19s-43-QP-Q6.i.png
AL-MTH-19s-43-QP-Q6.ii.png
AL-MTH-19s-43-QP-Q6.iii.png
AL-MTH-19s-43-QP-Q6.stem.png
AL-MTH-19s-43-QP-split-provenance.json
gates.log
splitter.log
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/v6.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 11:45:05

Matches D6 (labelled answer rows kept with their leaf). Since the leader split can touch many maths papers, Bio check then another full run (mth_b4) to compare against mth_b3.

**Tool `Bash`**

```
/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/biochk.sh; df -h ~|tail -1; cd ~/rootatom_data/ALEVEL; rm -rf splits/mth_b2 review/mth_b2
```

<details><summary>result</summary>

```
this run: PASS 3 / 3; run total PASS 3 / 3
AL-BIO-24s-22-QP IDENTICAL 43 43
AL-BIO-17w-42-QP IDENTICAL 56 56
AL-BIO-13s-52-QP IDENTICAL 17 17
/dev/disk3s5   228Gi   187Gi    13Gi    94%    2.6M  134M    2%   /System/Volumes/Data
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_b4 ~/rootatom_data/ALEVEL/review/mth_b4; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b4 --list ~/rootatom_data/ALEVEL/review/mth/all_qp2.txt --no-sheets --workers 8 > /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b4.log 2>&1
```

<details><summary>result</summary>

```
Command running in background with ID: bsihzrf02. Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bsihzrf02.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e; directory changes made by the backgrounded command do not apply to subsequent commands.
```
</details>

### Assistant — 2026-10-20 11:45:27

While mth_b4 runs (no script edits), checking 25w-15, the last unexplained hold.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b3/AL-MTH-25w-15-QP; head -3 gates.log; grep -v "^   " splitter.log | head; ~/.venvs/alevel/bin/python -I -c "
import pymupdf as f
d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/9709_w25_qp_15.pdf')
for w in d[16].get_text('words'):
  if 560<w[1]<700: print([round(v,1) if isinstance(v,float) else v for v in w[:5]])" | head -30
```

<details><summary>result</summary>

```
expected=25 produced=24 missing=['Q11.c.ii'] extra=[]
  MISSING (17, 648, '(c)')
  MISSING (17, 648, '(ii)')
produced 33 crops
[118.6, 570.4, 544.1, 581.9, '....................................................................................................................................................']
[118.6, 596.4, 544.1, 607.9, '....................................................................................................................................................']
[118.6, 622.4, 544.1, 633.9, '....................................................................................................................................................']
[72.3, 648.4, 85.1, 659.9, '(c)']
[92.3, 648.4, 106.3, 659.9, '(ii)']
[117.7, 648.4, 140.7, 659.9, 'State']
[143.5, 648.4, 157.6, 659.9, 'the']
[160.5, 648.4, 213.5, 659.9, 'coordinates']
[216.4, 648.4, 225.9, 659.9, 'of']
[228.8, 648.4, 237.1, 659.9, 'Q']
[240.0, 648.4, 256.6, 659.9, 'and']
[259.5, 648.4, 273.5, 659.9, 'the']
[276.4, 648.4, 295.5, 659.9, 'area']
[298.4, 648.4, 308.0, 659.9, 'of']
[310.9, 648.4, 324.9, 659.9, 'the']
[327.8, 648.4, 383.4, 659.9, 'transformed']
[386.3, 648.4, 418.2, 659.9, 'shaded']
[421.1, 648.4, 453.3, 659.9, 'region.']
[532.3, 648.4, 545.7, 659.9, '[2]']
[118.6, 674.4, 544.1, 685.9, '....................................................................................................................................................']
[6.9, 688.5, 14.9, 720.5, 'MARGIN']
[6.9, 636.5, 14.9
… [248 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; SPLITTER_DEBUG_ANCHORS=1 ~/.venvs/alevel/bin/python -I al_qp_splitter.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w25_qp_15.pdf $S/t11 AL-MTH-25w-15-QP 2>&1 | grep KEPT | awk '$2>=15'
```

<details><summary>result</summary>

```
KEPT_ANCHOR 15 PART c 72.32 63.2
KEPT_ANCHOR 16 Q 11 49.64 63.2
KEPT_ANCHOR 16 PART a 72.32 276.45
KEPT_ANCHOR 17 PART b 72.32 63.41
KEPT_ANCHOR 17 PART c 72.32 531.39
KEPT_ANCHOR 17 ROMAN i 95.48 531.39
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I - <<EOF
s=open('al_qp_splitter.py').read()
for fn in ['drop_false_romans','drop_false_igcse_subparts','drop_false_igcse_parts','drop_false_igcse_questions']:
    s=s.replace(f"    seq={fn}(seq",f"    print('BEFORE {fn}',[(a['pno']+1,a['kind'],a['label'],round(a['y'])) for a in seq if a['pno']==16],file=sys.stderr)\n    seq={fn}(seq",1)
open('$S/dbg5.py','w').write(s)
EOF
~/.venvs/alevel/bin/python -I $S/dbg5.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w25_qp_15.pdf $S/t11 AL-MTH-25w-15-QP 2>&1 | grep BEFORE
```

<details><summary>result</summary>

```
(Bash completed with no output)
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; grep -n "seq=drop_false\|seq=\[" al_qp_splitter.py | head; grep -n "^    seq=" al_qp_splitter.py | head
```

<details><summary>result</summary>

```
1208:    A,M,S,W,DOT,INK,CREDIT={},{},{},{},{},{},{}; seq=[]
1243:    seq=drop_false_igcse_questions(seq)
1256:    seq=drop_false_romans(seq)
1257:    seq=drop_false_igcse_subparts(seq,M)
1258:    seq=drop_false_igcse_parts(seq)
1297:        seq=[a for a in seq if id(a) not in dropped_]
1243:    seq=drop_false_igcse_questions(seq)
1256:    seq=drop_false_romans(seq)
1257:    seq=drop_false_igcse_subparts(seq,M)
1258:    seq=drop_false_igcse_parts(seq)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; ~/.venvs/alevel/bin/python -I $S/dbg5.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w25_qp_15.pdf $S/t11 AL-MTH-25w-15-QP 2>&1 | grep -v "^   " | head -5
```

<details><summary>result</summary>

```
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/dbg5.py", line 29, in <module>
TypeError: install() got an unexpected keyword argument 'leaders'
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cp fused_marks.py barcode_rule.py $S/; ~/.venvs/alevel/bin/python -I $S/dbg5.py ~/rootatom_data/ALEVEL/source_papers/canonical/9709_w25_qp_15.pdf $S/t11 AL-MTH-25w-15-QP 2>&1 | grep BEFORE
```

<details><summary>result</summary>

```
BEFORE drop_false_igcse_questions [(17, 'PART', 'b', 63), (17, 'PART', 'c', 531), (17, 'ROMAN', 'i', 531), (17, 'PART', 'c', 648), (17, 'ROMAN', 'ii', 648)]
BEFORE drop_false_romans [(17, 'PART', 'b', 63), (17, 'PART', 'c', 531), (17, 'ROMAN', 'i', 531), (17, 'PART', 'c', 648), (17, 'ROMAN', 'ii', 648)]
BEFORE drop_false_igcse_subparts [(17, 'PART', 'b', 63), (17, 'PART', 'c', 531), (17, 'ROMAN', 'i', 531), (17, 'PART', 'c', 648)]
BEFORE drop_false_igcse_parts [(17, 'PART', 'b', 63), (17, 'PART', 'c', 531), (17, 'ROMAN', 'i', 531), (17, 'PART', 'c', 648)]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 11:46:23

The full run (mth_b4) is still going. Found the 25w-15 cause: the w25 layout reprints the part letter as "(c) (ii)", and the repeated "(c)" resets the roman run, so "(ii)" gets dropped. I'll fix that once the run finishes, since scripts can't change under a running batch.

### User — 2026-10-20 13:10:49

<task-notification>
<task-id>bsihzrf02</task-id>
<tool-use-id>toolu_01KufbvzbcMAnVSrQfq4PZNh</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bsihzrf02.output</output-file>
<status>completed</status>
<summary>Background command "cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; rm -rf ~/rootatom_data/ALEVEL/splits/mth_b4 ~/rootatom_data/ALEVEL/review/mth_b4; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b4 --list ~/rootatom_data/ALEVEL/review/mth/all_qp2.txt --no-sheets --workers 8 &gt; /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b4.log 2&gt;&amp;1" completed (exit code 0)</summary>
</task-notification>

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b4.log; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_compare_runs.py mth_b3 mth_b4 | tail -4; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('/Users/nitya/rootatom_data/ALEVEL/review/mth_b4/compare.csv')))
print([x['prefix'][7:-3] for x in r if x['class']=='changed'])
print([x['prefix'][7:-3] for x in r if x['class'] in ('hold','regressed')])"
```

<details><summary>result</summary>

```
this run: PASS 813 / 826; run total PASS 813 / 826
{'hold': 13, 'same': 813}
[]
['01w-21', '01w-41', '01w-61', '02s-21', '02s-31', '02w-31', '03w-21', '04w-31', '09s-71', '13w-32', '17w-32', '22s-33', '25w-15']
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 13:11:09

Deterministic: 813 identical to mth_b3, 13 holds. Now the repeated-part-letter fix for 25w-15.

**Tool `Edit`**

```
{"replace_all": false, "file_path": "/Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py", "old_string": "    seq=drop_false_romans(seq)\n    seq=drop_false_igcse_subparts(seq,M)", "new_string": "    if IS_MATHS:\n        # '(c) (ii) State ...' -- the part letter reprinted beside a later roman\n        # of the same part (9709/15/O/N/25 Q11): drop the repeated part so the\n        # roman run (i), (ii) continues\n        cur=None; rep=set()\n        for i,a in enumerate(seq):\n            if a['kind']=='Q':\n                cur=None\n            elif a['kind']=='PART':\n                nxt_=seq[i+1] if i+1<len(seq) else None\n                if (cur is not None and a['label']==cur and nxt_ is not None and nxt_['kind']=='ROMAN'\n                        and nxt_['pno']==a['pno'] and abs(nxt_['y']-a['y'])<3):\n                    rep.add(id(a))\n                cur=a['label']\n        seq=[a for a in seq if id(a) not in rep]\n    seq=drop_false_romans(seq)\n    seq=drop_false_igcse_subparts(seq,M)"}
```

<details><summary>result</summary>

```
The file /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_qp_splitter.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b4 9709_w25_qp_15.pdf --no-sheets | tail -1; ls ~/rootatom_data/ALEVEL/splits/mth_b4/AL-MTH-25w-15-QP | grep Q11
```

<details><summary>result</summary>

```
this run: PASS 1 / 1; run total PASS 814 / 826
AL-MTH-25w-15-QP-Q11.a.png
AL-MTH-25w-15-QP-Q11.b.png
AL-MTH-25w-15-QP-Q11.c.i.png
AL-MTH-25w-15-QP-Q11.c.ii.png
AL-MTH-25w-15-QP-Q11.c.stem.png
AL-MTH-25w-15-QP-Q11.stem.png
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/Users/nitya/rootatom_data/ALEVEL/splits/mth_b4/AL-MTH-25w-15-QP/AL-MTH-25w-15-QP-Q11.c.ii.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 13:11:28

Correct. Bio check, commit, then the final full run into mth_b1 itself (compared against mth_b4).

**Tool `Bash`**

```
/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/biochk.sh && cd ~/rootatom_data/alevel-pipeline && git add ALEVEL/scripts/al_qp_splitter.py ALEVEL/scripts/al_verify_coverage.py ALEVEL/scripts/al_verify_leaves.py ALEVEL/scripts/fused_marks.py && git commit -q -F - <<'EOF'
Maths 9709 holds: copyright cap, axes after answer lines, fused label leaders, short context rows

826 Maths QPs (730 + 96 newly fetched s19/w24/w25 and re-checked files):
813 PASS on a full run (mth_b4), deterministic vs the previous full run;
remaining 13 holds need manual specs / a derived source.

Splitter (IS_MATHS):
- crops end above the copyright notice (last leaf of a paper ran to the foot)
- orphan prose stops at a mid-paper copyright notice (9709/11/O/N/15 p.3)
- blank axes printed after a leaf's answer lines are that leaf's extra
  segment (kept-grid decision; 9709/41/M/J/18 Q5(i)), lines left out
- short context sentences ('The median of X is m.') and a lone 'Hence'
  are context rows -> next part's stem / lead-in (house rule)
- a diagram beside a question's own number at a page head opens that
  question's first crop (9709/62/M/J/15 Q4)
- wrapped bracket hints: end of the LAST row decides; big-bracket pieces
  above HEADER_Y found from raw page words
- '(c) (ii)' reprinted part letter no longer resets the roman run (9709/15/O/N/25)
fused_marks: opt-in split of label-fused leaders ('AB.........' -> 'AB' +
leader), enabled for AL-MTH/AL-FMT prefixes only in splitter and both gates,
so labelled answer rows keep their place under D6 (9709/51/M/J/19 Q6(i)).

3 approved Biology papers re-split byte-identical.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
git log --oneline | head -1; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_run_papers.py mth_b1 --list ~/rootatom_data/ALEVEL/review/mth/all_qp2.txt --no-sheets --workers 8 > /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b1f.log 2>&1 &
echo started
```

<details><summary>result</summary>

```
this run: PASS 3 / 3; run total PASS 3 / 3
AL-BIO-24s-22-QP IDENTICAL 43 43
AL-BIO-17w-42-QP IDENTICAL 56 56
AL-BIO-13s-52-QP IDENTICAL 17 17
94420f5 Maths 9709 holds: copyright cap, axes after answer lines, fused label leaders, short context rows
started
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `ToolSearch`**

```
{"query": "select:Monitor", "max_results": 1}
```

<details><summary>result</summary>

```

```
</details>

**Tool `Bash`**

```
L=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b1f.log; until grep -q "this run:" $L || ! pgrep -f "al_run_papers.py mth_b1" >/dev/null; do sleep 15; done; tail -1 $L
```

<details><summary>result</summary>

```
Command running in background with ID: bgsnh7lcc. Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bgsnh7lcc.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
```
</details>

### Assistant — 2026-10-20 13:12:01

While the final run goes, drafting the manual-spec list and handoff update (data files only).

**Tool `Bash`**

```
cat > ~/rootatom_data/ALEVEL/review/mth/manual_specs_needed.txt <<'EOF'
# 9709 QPs that need manual specs / source work after generic fixes (pipeline 94420f5+, 2026-10-20)
# prefix            reason
AL-MTH-01w-21-QP    image-only scan (no text layer) -> OCR-assisted manual spec
AL-MTH-01w-41-QP    image-only scan (no text layer) -> OCR-assisted manual spec
AL-MTH-01w-61-QP    image-only scan (no text layer) -> OCR-assisted manual spec
AL-MTH-02s-21-QP    image-only scan (no text layer) -> OCR-assisted manual spec
AL-MTH-02s-31-QP    image-only scan (no text layer) -> OCR-assisted manual spec
AL-MTH-02w-31-QP    image-only scan (no text layer) -> OCR-assisted manual spec
AL-MTH-09s-71-QP    combined source: 9709/71 + 9709/72 in one file (72's cover on p.6) -> derive 9709_s09_qp_71/72 (derived_sources.csv, as 9702_s09_qp_2), re-run; check s09_qp_72 alias
AL-MTH-03w-21-QP    tall integral near the page foot: no blank row near y=706 p.3 -> spec
AL-MTH-04w-31-QP    tall integral near the page foot: no blank row near y=759 p.3 -> spec
AL-MTH-13w-32-QP    answer row with no whitespace around it (y=726 p.2) -> spec
AL-MTH-17w-32-QP    Q9.stem / Q9.i raised fraction interleaves the stem's lower limit (genuine 2-D seam; gate cannot check masks) -> spec
AL-MTH-22s-33-QP    Q10.stem / Q10.a same 2-D interleave -> spec
EOF
echo ok
```

<details><summary>result</summary>

```
ok
```
</details>

### Assistant — 2026-10-20 13:12:09

Waiting for the final full run into mth_b1. The manual-spec list is drafted at `review/mth/manual_specs_needed.txt`.

### User — 2026-10-20 13:23:28

<task-notification>
<task-id>bgsnh7lcc</task-id>
<tool-use-id>toolu_01Ec3JQViRHSboSaBnK63Ru7</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bgsnh7lcc.output</output-file>
<status>completed</status>
<summary>Background command "L=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b1f.log; until grep -q "this run:" $L || ! pgrep -f "al_run_papers.py mth_b1" &gt;/dev/null; do sleep 15; done; tail -1 $L" completed (exit code 0)</summary>
</task-notification>

**Tool `Bash`**

```
tail -1 /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/mth_b1f.log; cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; ~/.venvs/alevel/bin/python -I al_compare_runs.py mth_b4 mth_b1 | tail -3; ~/.venvs/alevel/bin/python -I -c "
import csv
r=list(csv.DictReader(open('/Users/nitya/rootatom_data/ALEVEL/review/mth_b1/compare.csv')))
print('changed',[x['prefix'][7:-3] for x in r if x['class'] in ('changed','regressed','newpass')])
s=list(csv.DictReader(open('/Users/nitya/rootatom_data/ALEVEL/review/mth_b1/run_summary.csv')))
print(len(s), sum(x['status']=='PASS' for x in s)); print([x['prefix'][7:-3] for x in s if x['status']!='PASS'])"
```

<details><summary>result</summary>

```
this run: PASS 814 / 826; run total PASS 814 / 826
{'hold': 12, 'same': 814}
changed []
826 814
['02s-21', '02s-31', '09s-71', '22s-33', '01w-21', '01w-41', '01w-61', '02w-31', '03w-21', '04w-31', '13w-32', '17w-32']
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 13:23:48

Final: mth_b1 is 814/826 PASS. The 12 holds exactly match the manual-spec list, and the run is byte-identical to mth_b4. Cleaning up the scratch runs and updating the handoff and worklist.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; rm -rf splits/mth_b3 review/mth_b3 splits/mth_b4 review/mth_b4 splits/bio_regchk review/bio_regchk; df -h ~ | tail -1; cat >> review/mth/_worklist.txt <<'EOF'
  - then (commit 94420f5): copyright cap, mid-page copyright not orphan prose, blank axes after answer lines = leaf's extra segment, short context rows ('The median of X is m.', lone 'Hence'), diagram beside a question number opens its first crop, '(c) (ii)' reprinted part letter, fused label leaders ('AB.......', fused_marks opt-in for AL-MTH/AL-FMT in splitter + both gates)
[done 2026-10-20] 96 more QPs added to mth_b1 (s19/w24/w25 + 34 re-checked files, sources from the Bio-MS session, commit 184dbd1); review/mth/all_qp2.txt = 826 QPs
[done 2026-10-20] mth_b1 re-run in full at 94420f5: 814/826 PASS (was 479/730); identical to an independent full run; changed previously-PASS papers (17 + 5) viewed by eye, all improvements
[open] 12 holds -> review/mth/manual_specs_needed.txt (6 image-only scans, 09s-71 combined 71+72 source, 3 footer/answer-row layouts, 2 genuine 2-D interleaves)
[next, needs user OK] dedupe aliases (al_dedupe + pixel scan of same-session variants), sheets for PASS, review groups <=40 sheets, 4-5 agents (time one test agent first, df -h before each wave)
EOF
~/.venvs/alevel/bin/python -I - <<'EOF'
p='/Users/nitya/rootatom_data/ALEVEL/review/mth/_HANDOFF.md'; s=open(p).read()
s+='''
## Update 2026-10-20 (hold-reduction session)
- Pipeline HEAD 94420f5 (13b2f2e + 94420f5: Maths hold fixes, all IS_MATHS / maths-prefix gated; 3 approved Bio papers byte-identical after every change).
- mth_b1 now holds ALL 826 9709 QPs (730 + 96 newly fetched/rechecked, list review/mth/all_qp2.txt): 814 PASS, 12 HOLD.
- Holds = review/mth/manual_specs_needed.txt (reasons per paper). 09s-71 is a combined 71+72 source -> derive first.
- Decision taken (mine, report to user): bracketed hints '[The volume of a cone is ...]' go with the leaf printed directly above them (also at question end).
- Gate change (relaxing, all subjects): '[Question N continues on the next page.]' is furniture -> the all-subject gate regression item still applies.
- Next (needs user OK): dedupe aliases, contact sheets for the 814 PASS, review waves (4-5 agents, groups <=40 sheets, one timed test agent first).
'''
open(p,'w').write(s)
EOF
echo ok
```

<details><summary>result</summary>

```
/dev/disk3s5   228Gi   187Gi    11Gi    95%    2.6M  120M    2%   /System/Volumes/Data
ok
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `mcp__ccd_turn__wrap_up`**

```
{"recap": "Committed 13b2f2e and 94420f5. Run mth_b1 now covers all 826 Maths 9709 question papers, and 814 pass both gates (was 479/730). The 12 held papers need manual specs or a split of a combined source; Biology output is unchanged. Duplicate removal and the visual review are not started.", "ask": "Start alias dedupe and the visual review waves for the 814 passing papers?", "actions": [{"label": "Yes, start", "message": "Yes: dedupe the aliases, then start the visual review waves (time one test agent first, 4-5 agents, groups of 40 sheets or fewer, df -h before each wave)."}, {"label": "Manual specs first", "message": "First do the 12 manual specs and the 09s-71 source split, then the dedupe and review."}]}
```

<details><summary>result</summary>

```
Shown in the next-step box. The box ends your turn: write no text after this call, since the recap and question already say what the user needs.
```
</details>

**Tool `Write`**

```
{"file_path": "/Users/nitya/Library/Application Support/Claude/side-session-notes/local_ee3092d5-d44b-47ae-8f13-bbfe18e328ce/mth_holds_2026-10-20.md", "content": "# Maths 9709 QP hold reduction — 2026-10-20\n\n- Pipeline commits 13b2f2e, 94420f5 (alevel-pipeline). All changes IS_MATHS / maths-prefix gated; 3 approved Bio papers byte-identical after each change.\n- Run mth_b1 now covers all 826 9709 QPs (incl. the 96 new s19/w24/w25 + re-checked files): 814 PASS, 12 HOLD.\n- Holds and reasons: ~/rootatom_data/ALEVEL/review/mth/manual_specs_needed.txt\n- Worklist / handoff updated: review/mth/_worklist.txt, review/mth/_HANDOFF.md\n- Not done (needs user OK): dedupe aliases, contact sheets, visual review waves.\n- Disk: 11 GB free at the end (scratch runs deleted).\n"}
```

<details><summary>result</summary>

```
File created successfully at: /Users/nitya/Library/Application Support/Claude/side-session-notes/local_ee3092d5-d44b-47ae-8f13-bbfe18e328ce/mth_holds_2026-10-20.md (file state is current in your context — no need to Read it back)
```
</details>

### User — 2026-10-20 15:19:24

Yes: dedupe the aliases, then start the visual review waves (time one test agent first, 4-5 agents, groups of 40 sheets or fewer, df -h before each wave).

**Tool `Skill`**

```
{"skill": "alevel-qp-review"}
```

<details><summary>result</summary>

```
Launching skill: alevel-qp-review
```
</details>

### User — 2026-10-20 15:25:06

Base directory for this skill: /Users/nitya/.claude/skills/alevel-qp-review

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

**Tool `mcp__ccd_turn__update_plan`**

```
{"items": [{"content": "Dedupe aliases (al_dedupe + variant scan)", "status": "in_progress"}, {"content": "Build contact sheets and review groups", "status": "pending"}, {"content": "Time one test review agent", "status": "pending"}, {"content": "Run review waves (4-5 agents)", "status": "pending"}, {"content": "Verify flags, approve clean groups", "status": "pending"}], "scope": "continuation"}
```

<details><summary>result</summary>

```
Plan shown (5 steps).
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; sed -n 1,40p al_dedupe.py; ls; ls ~/rootatom_data/ALEVEL/review/bio_b1 | head -30
```

<details><summary>result</summary>

```
#!/usr/bin/env python3
"""Find variants that are the SAME paper (Cambridge reuses papers across
time zones) and record canonical/alias pairs.

Decision 2026-10-11 (user): keep one copy -- the lowest variant is canonical,
the others are aliases (recorded, not reviewed, not classified, not uploaded
as separate questions).

Two papers are the same when every crop label matches, every crop has the same
pixel size, and every crop image is identical up to anti-aliasing: fewer than
0.05% of pixels differ by more than 96 grey levels (a re-typeset PDF of the
same paper renders a few edge pixels differently; any changed word, digit or
figure line differs in far more pixels than that) AND the PDF words inside
every crop's clip rectangles are the same multiset (so a changed number or
word can never be hidden under the pixel tolerance).

Writes review/<RUN>/duplicates.csv: canonical,alias,crops
Usage: al_dedupe.py RUN
"""

from __future__ import annotations

import collections
import csv
import hashlib
import sys

import json

import numpy as np
import pymupdf as fitz
from PIL import Image
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"


def crops_of(p: Path) -> dict[str, Path]:
    return {f.name.split("-QP-")[1]: f for f in p.glob("*-Q*.png")}

__pycache__
_rebuild_al_splitter.py
_rebuild_block_helpers.py.txt
_rebuild_block_snap.py.txt
al_addmarks.py
al_approve.py
al_autofix.py
al_check_ms_verdicts.py
al_check_verdicts.py
al_class_manifest.py
al_compare_runs.p
… [1392 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; time ~/.venvs/alevel/bin/python -I al_dedupe.py mth_b1 2>&1 | tail -5; wc -l ~/rootatom_data/ALEVEL/review/mth_b1/duplicates.csv; head -5 ~/rootatom_data/ALEVEL/review/mth_b1/duplicates.csv
```

<details><summary>result</summary>

```
58 alias papers -> /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/duplicates.csv
~/.venvs/alevel/bin/python -I al_dedupe.py mth_b1 2>&1  0.70s user 0.73s system 30% cpu 4.617 total
tail -5  0.00s user 0.00s system 0% cpu 4.617 total
      59 /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/duplicates.csv
canonical,alias,crops
AL-MTH-10s-22-QP,AL-MTH-10s-23-QP,19
AL-MTH-10s-41-QP,AL-MTH-10s-42-QP,19
AL-MTH-10s-51-QP,AL-MTH-10s-52-QP,19
AL-MTH-10s-71-QP,AL-MTH-10s-72-QP,23
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 15:25:24

58 aliases found by al_dedupe. Now a text scan of same-session variants for aliases it misses (it needs identical crop sets).

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cat > $S/bin/alias_scan.py <<'EOF'
# text scan of same-session variants of 9709 QPs: candidates not in duplicates.csv
import csv,re,unicodedata,difflib,itertools,collections,sys
import pymupdf as fitz
from pathlib import Path
D=Path.home()/'rootatom_data/ALEVEL'
rows=list(csv.DictReader(open(D/'review/mth_b1/run_summary.csv')))
dup={(r['canonical'],r['alias']) for r in csv.DictReader(open(D/'review/mth_b1/duplicates.csv'))}
dupal={a for _,a in dup}
def txt(src):
    doc=fitz.open(D/'source_papers/canonical'/src); out=[]
    for p in list(doc)[1:]:
        t=unicodedata.normalize('NFKC',p.get_text())
        t=re.sub(r'[\x00-\x08\x0b-\x1f]','',t)
        t=re.sub(r'\d{4}/\d{1,2}/[A-Z/]+\d*|©.*|UCLES|\[Turn over\]?|Turn over|BLANK PAGE|DO NOT WRITE IN THIS MARGIN','',t)
        out.append(re.sub(r'\s+',' ',t))
    return ' '.join(out)
grp=collections.defaultdict(list)
for r in rows:
    m=re.match(r'9709_([msw]\d\d)_qp_(\d)(\d)\.pdf',r['source'])
    if m: grp[(m[1],m[2])].append(r)
for k,rs in sorted(grp.items()):
    T={r['prefix']:txt(r['source']) for r in rs}
    for a,b in itertools.combinations(sorted(T),2):
        if (a,b) in dup or b in dupal and any(x==a for x,y in dup if y==b): continue
        if b in dupal or a in dupal: 
            # both may alias a third canonical; skip if already covered transitively
            pass
        ra=difflib.SequenceMatcher(None,T[a],T[b],autojunk=False).quick_ratio()
        if ra>0.97:
            r2=difflib.SequenceMatcher(None,T[a][:20000],T[b][:20000],autojunk=False).ratio()
            if r2>0.97: print(f'{a},{b},{r2:.4f}',flush=True)
EOF
~/.venvs/alevel/bin/python -I $S/bin/alias_scan.py | tee $S/alias_cand.txt
```

<details><summary>result</summary>

```
Command did not complete within its 600s timeout and was moved to the background (ID: bmzpjer5x). Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bmzpjer5x.output. You will be notified when it completes. To check interim output, use Read on that file path.
```
</details>

### Assistant — 2026-10-20 15:44:01

While that scan runs, reading the review prompt and group tool.

**Tool `Bash`**

```
cat ~/rootatom_data/alevel-pipeline/ALEVEL/REVIEW_AGENT_PROMPT_QP.txt; sed -n 1,30p ~/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_groups_from_list.py
```

<details><summary>result</summary>

```
You are a visual reviewer for exam-paper crops. Use ONLY the Read tool (to view images and the group file) and the Write tool (for your one output file). No other tools. The run RUN and group number NN are given in your task message.

1. Read the group file: /Users/nitya/rootatom_data/ALEVEL/review/RUN/_review_groups/group_NN.txt
   Each line = one paper: its PREFIX followed by the paths of its contact-sheet images.
2. For each paper, Read EVERY listed image. Each image stacks several crops; a blue bar labels each crop (e.g. Q3.b.ii, Q4.stem, SecB.stem, or Q17 for multiple-choice papers whose PREFIX contains "-1" + digit, e.g. AL-BIO-24s-12-QP). Crops are in reading order: a ".stem" crop is printed BEFORE the part(s) it introduces.
3. For EVERY crop check:
   (1) The QUESTION NUMBER (the bare 1, 2, 3 ... that starts a question) is NOT visible. Part labels like (a), (ii), "1." tasks are fine and expected.
   (2) Nothing is cut off at any edge: no sliced letters, formula, fraction, table border, graph axis, figure part, structural formula; no sentence ending abruptly; for multiple-choice crops all options A, B, C, D are present.
   (3) No page furniture: "© UCLES", paper codes like 9700/42/M/J/24, "[Turn over", page numbers, "BLANK PAGE", "DO NOT WRITE IN THIS MARGIN", "[Total: n]", "Space for working", copyright text, barcodes, website text or watermarks.
   (4) Exactly one item per crop: no text that belongs to a different part/question (e.g. two separate (i) and (ii) prompts
… [2236 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cat /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bmzpjer5x.output
```

<details><summary>result</summary>

```
AL-MTH-13s-21-QP,AL-MTH-13s-23-QP,1.0000
AL-MTH-16s-22-QP,AL-MTH-16s-23-QP,0.9996
AL-MTH-17s-22-QP,AL-MTH-17s-23-QP,1.0000
```
</details>

### Assistant — 2026-10-20 15:44:14

The scan is slow (difflib) but finding real candidates (e.g. 13s-21/23 identical text). Waiting for it to finish.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; grep -E "13s-2|16s-2|17s-2" review/mth_b1/duplicates.csv; grep -E "13s-2[13]|16s-2[23]|17s-2[23]" review/mth_b1/run_summary.csv | cut -d, -f2-5
```

<details><summary>result</summary>

```
AL-MTH-13s-21-QP,PASS,17,expected=15 produced=15 missing=[] extra=[]
AL-MTH-13s-23-QP,PASS,17,expected=15 produced=15 missing=[] extra=[]
AL-MTH-16s-22-QP,PASS,20,expected=17 produced=17 missing=[] extra=[]
AL-MTH-16s-23-QP,PASS,20,expected=17 produced=17 missing=[] extra=[]
AL-MTH-17s-22-QP,PASS,15,expected=14 produced=14 missing=[] extra=[]
AL-MTH-17s-23-QP,PASS,15,expected=14 produced=14 missing=[] extra=[]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
L=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bmzpjer5x.output; until ! pgrep -f alias_scan.py >/dev/null; do sleep 20; done; cat $L
```

<details><summary>result</summary>

```
Command running in background with ID: bvyruoo6f. Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bvyruoo6f.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
```
</details>

### Assistant — 2026-10-20 15:44:26

Meanwhile writing a crop-level verifier for the candidates (same labels + same words inside every crop).

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cat > $S/bin/alias_verify.py <<'EOF'
# alias_verify.py CANDFILE : per-crop word-multiset equality (NFKC, control chars and paper codes stripped)
import sys,json,re,unicodedata,collections
import pymupdf as fitz
from pathlib import Path
D=Path.home()/'rootatom_data/ALEVEL/splits/mth_b1'
def words(prefix):
    d=json.load(open(D/prefix/f'{prefix}-split-provenance.json')); doc=fitz.open(d['source_pdf'])
    out={}
    for lab,segs in d['outputs'].items():
        c=collections.Counter()
        for s in segs:
            r=fitz.Rect(s['clip_points'])
            for w in doc[s['pdf_page']-1].get_text('words'):
                if r.contains(fitz.Point((w[0]+w[2])/2,(w[1]+w[3])/2)):
                    t=re.sub(r'[\x00-\x1f\s]','',unicodedata.normalize('NFKC',w[4]))
                    if t and not re.fullmatch(r'\d{4}/\d{1,2}/.*',t): c[t]+=1
        out[lab]=c
    return out
for line in open(sys.argv[1]):
    a,b=line.strip().split(',')[:2]
    A,B=words(a),words(b)
    if set(A)!=set(B): print('LABELS-DIFFER',a,b,sorted(set(A)^set(B))); continue
    diff=[l for l in A if A[l]!=B[l]]
    print('ALIAS' if not diff else 'DIFFER',a,b,diff[:5],[ (dict(A[l]-B[l]),dict(B[l]-A[l])) for l in diff[:2]])
EOF
echo ok
```

<details><summary>result</summary>

```
ok
```
</details>

### Assistant — 2026-10-20 15:44:36

Waiting for the alias text scan to finish (it compares all same-session variant pairs).

### User — 2026-10-20 17:06:45

<task-notification>
<task-id>bmzpjer5x</task-id>
<tool-use-id>toolu_011kzJ9uNGJU3C78MG4GxsTa</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bmzpjer5x.output</output-file>
<status>completed</status>
<summary>Background command "S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cat &gt; $S/bin/alias_scan.py &lt;&lt;'EOF'
# text scan of same-session variants of 9709 QPs: candidates not in duplicates.csv
import csv,re,unicodedata,difflib,itertools,collections,sys
import pymupdf as fitz
from pathlib import Path
D=Path.home()/'rootatom_data/ALEVEL'
rows=list(csv.DictReader(open(D/'review/mth_b1/run_summary.csv')))
dup={(r['canonical'],r['alias']) for r in csv.DictReader(open(D/'review/mth_b1/duplicates.csv'))}
dupal={a for _,a in dup}
def txt(src):
    doc=fitz.open(D/'source_papers/canonical'/src); out=[]
    for p in list(doc)[1:]:
        t=unicodedata.normalize('NFKC',p.get_text())
        t=re.sub(r'[\x00-\x08\x0b-\x1f]','',t)
        t=re.sub(r'\d{4}/\d{1,2}/[A-Z/]+\d*|©.*|UCLES|\[Turn over\]?|Turn over|BLANK PAGE|DO NOT WRITE IN THIS MARGIN','',t)
        out.append(re.sub(r'\s+',' ',t))
    return ' '.join(out)
grp=collections.defaultdict(list)
for r in rows:
    m=re.match(r'9709_([msw]\d\d)_qp_(\d)(\d)\.pdf',r['source'])
    if m: grp[(m[1],m[2])].append(r)
for k,rs in sorted(grp.items()):
    T={r['prefix']:txt(r['source']) for r in rs}
    for a,b in itertools.combinations(sorted(T),2):
        if (a,b) in dup or b in dupal and any(x==a for x,y in dup if y==b): continue
        if b in dupal or a in dupal: 
            # both may alias a third canonical; skip if already covered transitively
            pass
        ra=difflib.SequenceMatcher(None,T[a],T[b],autojunk=False).quick_ratio()
        if ra&gt;0.97:
            r2=difflib.SequenceMatcher(None,T[a][:20000],T[b][:20000],autojunk=False).ratio()
            if r2&gt;0.97: print(f'{a},{b},{r2:.4f}',flush=True)
EOF
~/.venvs/alevel/bin/python -I $S/bin/alias_scan.py | tee $S/alias_cand.txt" completed (exit code 0)</summary>
</task-notification>

### Assistant — 2026-10-20 17:06:51

17 candidates. Verifying crop by crop.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; grep AL-MTH $S/tasks 2>/dev/null; grep AL-MTH /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bmzpjer5x.output > $S/alias_cand.txt; ~/.venvs/alevel/bin/python -I $S/bin/alias_verify.py $S/alias_cand.txt 2>&1 | cut -c1-300
```

<details><summary>result</summary>

```
ALIAS AL-MTH-13s-21-QP AL-MTH-13s-23-QP [] []
DIFFER AL-MTH-16s-22-QP AL-MTH-16s-23-QP ['Q3.ii', 'Q7.stem'] [({'cotx': 1}, {'cot': 1, 'x': 1}), ({'−cost,': 1}, {'−cos': 1, 't,': 1})]
ALIAS AL-MTH-17s-22-QP AL-MTH-17s-23-QP [] []
ALIAS AL-MTH-24s-22-QP AL-MTH-24s-23-QP [] []
ALIAS AL-MTH-25s-23-QP AL-MTH-25s-25-QP [] []
ALIAS AL-MTH-12w-71-QP AL-MTH-12w-72-QP [] []
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/alias_verify.py", line 21, in <module>
    A,B=words(a),words(b)
                 ~~~~~^^^
  File "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/bin/alias_verify.py", line 7, in words
    d=json.load(open(D/prefix/f'{prefix}-split-provenance.json')); doc=fitz.open(d['source_pdf'])
                ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/Users/nitya/rootatom_data/ALEVEL/splits/mth_b1/AL-MTH-13w-32-QP/AL-MTH-13w-32-QP-split-provenance.json'
```
</details>

### Assistant — 2026-10-20 17:07:00

Word-splitting differences ("cotx" vs "cot x") are noise. Switching to per-crop character multisets and skipping held papers (no crops).

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd $S; sed -i '' "s/if t and not re.fullmatch(r'\\\\d{4}\/\\\\d{1,2}\/.\*',t): c\[t\]+=1/if t and not re.fullmatch(r'\\\\d{4}\/\\\\d{1,2}\/.*',t): c.update(t)/" bin/alias_verify.py; grep -n "c.update\|c\[t\]" bin/alias_verify.py; sed -i '' 's/^    A,B=words(a),words(b)$/    if not all((D\/p\/f"{p}-split-provenance.json").exists() for p in (a,b)): print("HELD",a,b); continue\n    A,B=words(a),words(b)/' bin/alias_verify.py; ~/.venvs/alevel/bin/python -I bin/alias_verify.py alias_cand.txt 2>&1 | cut -c1-250
```

<details><summary>result</summary>

```
16:                    if t and not re.fullmatch(r'\d{4}/\d{1,2}/.*',t): c.update(t)
ALIAS AL-MTH-13s-21-QP AL-MTH-13s-23-QP [] []
ALIAS AL-MTH-16s-22-QP AL-MTH-16s-23-QP [] []
ALIAS AL-MTH-17s-22-QP AL-MTH-17s-23-QP [] []
ALIAS AL-MTH-24s-22-QP AL-MTH-24s-23-QP [] []
ALIAS AL-MTH-25s-23-QP AL-MTH-25s-25-QP [] []
ALIAS AL-MTH-12w-71-QP AL-MTH-12w-72-QP [] []
HELD AL-MTH-13w-31-QP AL-MTH-13w-32-QP
DIFFER AL-MTH-13w-51-QP AL-MTH-13w-52-QP ['Q4.stem', 'Q5.stem', 'Q6.stem'] [({'Å': 1}, {}), ({'Å': 1}, {})]
ALIAS AL-MTH-13w-71-QP AL-MTH-13w-72-QP [] []
DIFFER AL-MTH-14w-51-QP AL-MTH-14w-52-QP ['Q1', 'Q2.stem', 'Q4.stem', 'Q5.ii', 'Q7.stem'] [({}, {'Å': 2}), ({}, {'Å': 2})]
ALIAS AL-MTH-17w-21-QP AL-MTH-17w-23-QP [] []
ALIAS AL-MTH-17w-31-QP AL-MTH-17w-33-QP [] []
DIFFER AL-MTH-21w-21-QP AL-MTH-21w-23-QP ['Q1', 'Q6.d', 'Q7.a', 'Q7.c'] [({'Ó': 1}, {}), ({'1': 3}, {})]
DIFFER AL-MTH-23w-21-QP AL-MTH-23w-23-QP ['Q1', 'Q3.a', 'Q3.b', 'Q6.a', 'Q6.b'] [({'1': 3, 'Å': 1}, {}), ({'Ô': 1}, {})]
DIFFER AL-MTH-23w-61-QP AL-MTH-23w-63-QP ['Q2', 'Q6.c.stem', 'Q7.stem', 'Q7.a', 'Q7.b'] [({}, {'!': 2}), ({}, {'T': 1})]
ALIAS AL-MTH-25w-21-QP AL-MTH-25w-25-QP [] []
ALIAS AL-MTH-25w-23-QP AL-MTH-25w-25-QP [] []
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 17:07:13

Exact aliases confirmed: 11 pairs. The 5 "DIFFER" pairs differ only in symbol glyphs or digits, so I'll judge those by eye. Checking the 25w trio and rendering the differing crops.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; grep -E "25w-2|24s-2|25s-2" review/mth_b1/duplicates.csv; S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd splits/mth_b1; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image, ImageDraw, ImageChops
pairs=[('13w-51','13w-52','Q4.stem'),('14w-51','14w-52','Q1'),('21w-21','21w-23','Q7.a'),('23w-21','23w-23','Q1'),('23w-61','23w-63','Q7.a')]
rows=[]
for a,b,l in pairs:
  A=Image.open(f'AL-MTH-{a}-QP/AL-MTH-{a}-QP-{l}.png').convert('L'); B=Image.open(f'AL-MTH-{b}-QP/AL-MTH-{b}-QP-{l}.png').convert('L')
  print(a,b,l,A.size,B.size)
  W=max(A.width,B.width); c=Image.new('L',(W,A.height+B.height+40),128); c.paste(A,(0,20)); c.paste(B,(0,A.height+40)); rows.append(c)
W=max(r.width for r in rows); H=sum(r.height for r in rows)
o=Image.new('L',(W,H),255); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height
o.resize((W//2,H//2)).save('$S/al.png')"
```

<details><summary>result</summary>

```
AL-MTH-25s-22-QP,AL-MTH-25s-23-QP,17
AL-MTH-25s-22-QP,AL-MTH-25s-25-QP,17
AL-MTH-25w-21-QP,AL-MTH-25w-23-QP,18
13w-51 13w-52 Q4.stem (1590, 75) (1590, 75)
14w-51 14w-52 Q1 (1590, 151) (1590, 151)
21w-21 21w-23 Q7.a (1590, 75) (1590, 75)
23w-21 23w-23 Q1 (1590, 158) (1590, 157)
23w-61 23w-63 Q7.a (1590, 107) (1590, 107)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/al.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 17:07:24

Visually identical (differences are symbol font encodings). Pixel-checking every crop of those 5 pairs to be sure.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/splits/mth_b1; ~/.venvs/alevel/bin/python -I -c "
import numpy as np, glob, os
from PIL import Image
for a,b in [('13w-51','13w-52'),('14w-51','14w-52'),('21w-21','21w-23'),('23w-21','23w-23'),('23w-61','23w-63')]:
  pa=f'AL-MTH-{a}-QP'; pb=f'AL-MTH-{b}-QP'; worst=[]
  for f in sorted(glob.glob(f'{pa}/{pa}-Q*.png')):
    l=f.split('-QP-')[1]; g=f'{pb}/{pb}-{l}'
    A=np.asarray(Image.open(f).convert('L')).astype(int); B=np.asarray(Image.open(g).convert('L')).astype(int)
    if A.shape!=B.shape:
      h=min(A.shape[0],B.shape[0]); w=min(A.shape[1],B.shape[1])
      best=min((np.abs(A[dy:dy+h-2,:w]-B[:h-2,:w])>96).mean() for dy in range(0,min(3,A.shape[0]-h+3)))
      best=min(best,min((np.abs(A[:h-2,:w]-B[dy:dy+h-2,:w])>96).mean() for dy in range(0,3)))
      worst.append((round(best*100,3),l,'size',A.shape,B.shape))
    else: worst.append((round((np.abs(A-B)>96).mean()*100,3),l))
  worst.sort(reverse=True); print(a,b,worst[:3])
"
```

<details><summary>result</summary>

```
13w-51 13w-52 [(np.float64(1.272), 'Q1.png'), (np.float64(1.211), 'Q5.ii.png', 'size', (107, 1590), (108, 1590)), (np.float64(1.186), 'Q6.ii.png')]
14w-51 14w-52 [(np.float64(1.122), 'Q4.ii.png'), (np.float64(0.715), 'Q3.png'), (np.float64(0.597), 'Q5.stem.png')]
21w-21 21w-23 [(np.float64(0.169), 'Q2.b.png'), (np.float64(0.164), 'Q4.b.png'), (np.float64(0.088), 'Q6.b.png')]
23w-21 23w-23 [(np.float64(0.208), 'Q7.d.png'), (np.float64(0.051), 'Q5.b.png'), (np.float64(0.017), 'Q6.b.png')]
23w-61 23w-63 [(np.float64(4.815), 'Q4.stem.png'), (np.float64(4.603), 'Q3.stem.png', 'size', (106, 1590), (107, 1590)), (np.float64(4.109), 'Q7.b.stem.png')]
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; cd ~/rootatom_data/ALEVEL/splits/mth_b1; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image
rows=[]
for a,b,l in [('13w-51','13w-52','Q1'),('23w-61','23w-63','Q4.stem'),('14w-51','14w-52','Q4.ii')]:
  for p in (a,b): rows.append(Image.open(f'AL-MTH-{p}-QP/AL-MTH-{p}-QP-{l}.png').convert('L'))
W=max(r.width for r in rows); H=sum(r.height+15 for r in rows)
o=Image.new('L',(W,H),120); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height+15
o.resize((W//2,H//2)).save('$S/al2.png')"
```

<details><summary>result</summary>

```
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Read`**

```
{"file_path": "/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/al2.png"}
```

<details><summary>result</summary>

```
[image]
```
</details>

### Assistant — 2026-10-20 17:07:40

All re-typeset copies of the same papers. Checking whether held 13w-32 is really the same paper as 13w-31 (then it needs no manual spec).

**Tool `Bash`**

```
~/.venvs/alevel/bin/python -I -c "
import pymupdf as f,re,unicodedata,difflib
def t(s):
  d=f.open('/Users/nitya/rootatom_data/ALEVEL/source_papers/canonical/'+s)
  return [w for p in list(d)[1:] for w in re.sub(r'[\x00-\x1f]','',unicodedata.normalize('NFKC',p.get_text())).split()]
a,b=t('9709_w13_qp_31.pdf'),t('9709_w13_qp_32.pdf')
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
for op in sm.get_opcodes():
  if op[0]!='equal': print(op[0],a[op[1]:op[2]][:12],b[op[3]:op[4]][:12])
" | head -30
```

<details><summary>result</summary>

```
replace ['Ô41ln'] ['41ln']
replace ['cos', 't,y'] ['cost,y']
replace ['−140.[6]5(i)'] ['−14.[6]5(i)']
delete ['1'] []
delete ['1', '\x8f'] []
replace ['21.[3](ii)'] ['2.[3](ii)']
replace ['Ó130160cosec', '21', 'd1'] ['1316cosec', '2', 'd']
replace ['3.[4]6BCAOrqIn'] ['3.[4]6BCAOrIn']
delete ['1'] []
replace ['21'] ['2']
replace ['21', '−041.[5](ii)'] ['2', '−4.[5](ii)']
replace ['formula1n+1'] ['formulan+1']
replace ['cos−1P2'] ['cos−12']
replace ['21n', '−041nQ,with'] ['2n', '−4n,with']
replace ['11'] ['1']
delete ['1'] []
replace ['20139709/31/O/N/13'] ['20139709/32/O/N/13']
replace ['real.[5](b)On'] ['real.[5](b)', 'On']
delete ['Ï'] []
delete ['Ï'] []
replace ['340.'] ['34.']
delete ['Ï'] []
replace ['=`', '2−12a,'] ['=', '2−12,']
replace ['=`', '031aand'] ['=', '031and']
replace ['=`', '304a.'] ['=', '304.']
replace ['cÏ'] ['c']
replace ['20139709/31/O/N/13[Turn'] ['20139709/32/O/N/13[Turn']
replace ['60Å,'] ['60,']
replace ['ïh,'] ['h,']
replace ['130r2h.]Permission'] ['13r2h.]Permission']
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I - <<'EOF'
import csv
P='review/mth_b1/duplicates.csv'
rows=list(csv.DictReader(open(P)))
al={r['alias'] for r in rows}
pairs="13s-21,13s-23 16s-22,16s-23 17s-22,17s-23 24s-22,24s-23 12w-71,12w-72 13w-31,13w-32 13w-51,13w-52 13w-71,13w-72 14w-51,14w-52 17w-21,17w-23 17w-31,17w-33 21w-21,21w-23 23w-21,23w-23 23w-61,23w-63 25w-21,25w-25".split()
add=[]
import glob
for p in pairs:
    a,b=[f'AL-MTH-{x}-QP' for x in p.split(',')]
    assert a not in al and b not in al,(a,b)
    n=len(glob.glob(f'splits/mth_b1/{a}/{a}-Q*.png'))
    add.append({'canonical':a,'alias':b,'crops':n})
with open(P,'a',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['canonical','alias','crops']); w.writerows(add)
with open('review/mth/aliases_textscan.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['canonical','alias','crops']); w.writeheader(); w.writerows(add)
print(len(rows)+len(add))
EOF
sed -i '' '/^AL-MTH-13w-32-QP/d' review/mth/manual_specs_needed.txt; echo "# AL-MTH-13w-32-QP removed: alias of 13w-31 (same paper, text scan 2026-10-20)" >> review/mth/manual_specs_needed.txt; grep -c "^AL-MTH" review/mth/manual_specs_needed.txt
```

<details><summary>result</summary>

```
73
11
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

### Assistant — 2026-10-20 17:08:01

73 aliases total. Building the review list (PASS, non-alias) and contact sheets.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL; ~/.venvs/alevel/bin/python -I -c "
import csv
al={r['alias'] for r in csv.DictReader(open('review/mth_b1/duplicates.csv'))}
s=[r['prefix'] for r in csv.DictReader(open('review/mth_b1/run_summary.csv')) if r['status']=='PASS' and r['prefix'] not in al]
open('review/mth/review_list.txt','w').write('\n'.join(s)+'\n'); print(len(s))"; df -h ~ | tail -1; ls review/mth_b1; sed -n 30,80p ~/rootatom_data/alevel-pipeline/ALEVEL/scripts/al_groups_from_list.py
```

<details><summary>result</summary>

```
742
/dev/disk3s5   228Gi   190Gi    11Gi    95%    2.6M  118M    2%   /System/Volumes/Data
compare.csv
duplicates.csv
run_summary.csv
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("crops_run")
    ap.add_argument("review_run")
    ap.add_argument("list")
    ap.add_argument("--start", type=int)
    ap.add_argument("--max-sheets", type=int, default=40)
    a = ap.parse_args()
    rev = DATA / "review" / a.review_run
    groups = rev / "_review_groups"
    groups.mkdir(parents=True, exist_ok=True)
    (rev / "_verdicts").mkdir(exist_ok=True)
    prefixes = [l.split()[0] for l in open(a.list) if l.strip()]
    lines = []
    for p in prefixes:
        crops = DATA / "splits" / a.crops_run / p
        if not crops.is_dir():
            print("no crops:", crops)
            continue
        subprocess.run([PY, "-I", str(HERE / "al_contact_sheet.py"), str(crops), p, str(rev / p)],
                       capture_output=True)
        sheets = sorted(glob.glob(str(rev / f"{p}_*.jpg")))
        if not sheets:
            print("no sheets rendered:", p)
            continue
        lines.append((p, sheets))
    existing = [int(m.group(1)) for g in groups.glob("group_*.txt") if (m := re.search(r"(\d+)", g.stem))]
    n = a.start if a.start is not None else (max(existing) + 1 if existing else 1)
    cur, count, made = [], 0, []
    for p, sheets in lines:
        if cur and count + len(sheets) > a.max_sheets:
            (groups / f"group_{n:02d}.txt").write_te
… [584 more characters trimmed]
```
</details>

**Tool `Bash`**

```
cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; time ~/.venvs/alevel/bin/python -I al_groups_from_list.py mth_b1 mth_b1 ~/rootatom_data/ALEVEL/review/mth/review_list.txt --start 1 --max-sheets 40 2>&1 | tail -5; du -sh ~/rootatom_data/ALEVEL/review/mth_b1
```

<details><summary>result</summary>

```
Command running in background with ID: bxj5vzs5z. Output is being written to: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bxj5vzs5z.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e; directory changes made by the backgrounded command do not apply to subsequent commands.
```
</details>

### Assistant — 2026-10-20 17:08:11

While the sheets render, updating the worklist with the dedupe results.

**Tool `Bash`**

```
cat >> ~/rootatom_data/ALEVEL/review/mth/_worklist.txt <<'EOF'
[done 2026-10-20, user OK] dedupe: al_dedupe 58 aliases + text scan of same-session variants 15 more (re-typeset copies: only maths-glyph encodings differ; per-crop char multisets equal or pixel diff <5% from sub-pixel shifts, viewed) -> 73 in review/mth_b1/duplicates.csv; the 15 also in review/mth/aliases_textscan.csv (re-append after any al_dedupe re-run)
  - 13w-32 (HOLD) is an alias of 13w-31 -> no manual spec needed; manual list now 11
[in progress] review: 742 unique PASS papers -> review/mth/review_list.txt; sheets + groups in review/mth_b1 (<=40 sheets/group)
EOF
echo ok
```

<details><summary>result</summary>

```
ok
```
</details>

### Assistant — 2026-10-20 17:08:15

Contact sheets for the 742 unique passing papers are still rendering. Once the groups exist I'll time one test agent.

### User — 2026-10-20 17:10:08

<task-notification>
<task-id>bxj5vzs5z</task-id>
<tool-use-id>toolu_01McYTHRv85ao7x6SR2xXuMS</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bxj5vzs5z.output</output-file>
<status>completed</status>
<summary>Background command "cd ~/rootatom_data/alevel-pipeline/ALEVEL/scripts; time ~/.venvs/alevel/bin/python -I al_groups_from_list.py mth_b1 mth_b1 ~/rootatom_data/ALEVEL/review/mth/review_list.txt --start 1 --max-sheets 40 2&gt;&amp;1 | tail -5; du -sh ~/rootatom_data/ALEVEL/review/mth_b1" completed (exit code 0)</summary>
</task-notification>

**Tool `Bash`**

```
cat /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/bxj5vzs5z.output; df -h ~ | tail -1; head -c 600 ~/rootatom_data/ALEVEL/review/mth_b1/_review_groups/group_01.txt
```

<details><summary>result</summary>

```
742 papers -> 48 groups (01-48)
~/.venvs/alevel/bin/python -I al_groups_from_list.py mth_b1 mth_b1  --start 1  101.69s user 12.55s system 93% cpu 2:01.90 total
tail -5  0.00s user 0.00s system 0% cpu 2:01.89 total
688M	/Users/nitya/rootatom_data/ALEVEL/review/mth_b1

[exited with code 0]
/dev/disk3s5   228Gi   191Gi    11Gi    95%    2.6M  117M    2%   /System/Volumes/Data
AL-MTH-16m-12-QP /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-12-QP_01.jpg /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-12-QP_02.jpg /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-12-QP_03.jpg
AL-MTH-16m-22-QP /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-22-QP_01.jpg /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-22-QP_02.jpg
AL-MTH-16m-32-QP /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-32-QP_01.jpg /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-32-QP_02.jpg /Users/nitya/rootatom_data/ALEVEL/review/mth_
```
</details>

### Assistant — 2026-10-20 17:10:14

48 groups (≤40 sheets each), 11 GB free. Launching one timed test agent on group 01.

**Tool `mcp__ccd_turn__update_plan`**

```
{"advance": true}
```

<details><summary>result</summary>

```
Plan updated: step 2 of 5 is in progress.
```
</details>

**Tool `Bash`**

```
date +%s > /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/t0; wc -w < ~/rootatom_data/ALEVEL/review/mth_b1/_review_groups/group_01.txt
```

<details><summary>result</summary>

```
      56
```
</details>

**Tool `Agent`** — Review mth_b1 group 01 (test)

```
Read /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/REVIEW_AGENT_PROMPT_QP.txt and follow it exactly. RUN=mth_b1, NN=01. (Cambridge A Level Mathematics 9709.) Maths notes: a printed graph-paper grid or blank axes inside a part is kept by design (it is that part's answer grid, not an empty area); a bracketed hint such as "[The volume of a cone is ...]" printed under a part belongs to that part; a .stem crop may hold only a diagram and context. If an image Read comes back without the picture (e.g. "media removed" / request limit), wait briefly and Read it again; never record a verdict for a sheet you did not actually see.
```

<details><summary>result</summary>

```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a93fe8c774be54141 (internal ID - do not mention to user. Use SendMessage with to: 'a93fe8c774be54141', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/a93fe8c774be54141.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```
</details>

**Tool `mcp__ccd_turn__update_plan`**

```
{"advance": true}
```

<details><summary>result</summary>

```
Plan updated: step 3 of 5 is in progress.
```
</details>

### Assistant — 2026-10-20 17:10:27

The test agent is reviewing group 01 (14 papers, ~40 sheets). I'll time it when it reports and then launch the waves.

### User — 2026-10-20 17:20:20

<task-notification>
<task-id>a93fe8c774be54141</task-id>
<tool-use-id>toolu_01BBHhB5hNuaeB4o92T6WUpV</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/a93fe8c774be54141.output</output-file>
<status>failed</status>
<summary>Agent "Review mth_b1 group 01 (test)" failed: Agent stalled: no progress for 600s (stream watchdog did not recover)</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
</task-notification>

### Assistant — 2026-10-20 17:20:24

The test agent stalled (no progress for 10 minutes). Checking what it got done and the machine state before retrying.

**Tool `Bash`**

```
S=/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad; echo elapsed $(( $(date +%s) - $(cat $S/t0) ))s; ls -la ~/rootatom_data/ALEVEL/review/mth_b1/_verdicts/; sysctl vm.swapusage; memory_pressure | tail -1; uptime; ls -la ~/.claude/projects/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/ 2>/dev/null | head; du -sh ~/.claude/projects 2>/dev/null
```

<details><summary>result</summary>

```
elapsed 611s
total 0
drwxr-xr-x@    2 nitya  staff     64 Oct 20 22:38 .
drwxr-xr-x@ 1867 nitya  staff  59744 Oct 20 22:40 ..
vm.swapusage: total = 5120.00M  used = 3903.62M  free = 1216.38M  (encrypted)
System-wide memory free percentage: 41%
22:50  up 3 days, 11:45, 1 user, load averages: 3.39 3.88 4.55
total 109864
drwx------@  6 nitya  staff       192 Oct 20 16:08 .
drwxr-xr-x@ 32 nitya  staff      1024 Oct 19 20:29 ..
drwx------@  5 nitya  staff       160 Oct 20 21:49 259d77f6-d437-45b6-a736-dec2cc47c4c9
-rw-------@  1 nitya  staff  42172778 Oct 20 22:40 259d77f6-d437-45b6-a736-dec2cc47c4c9.jsonl
drwx------@  4 nitya  staff       128 Oct 20 22:40 917c70ae-0181-4fb4-89e3-cc8427b293bc
-rw-------@  1 nitya  staff  14073778 Oct 20 22:50 917c70ae-0181-4fb4-89e3-cc8427b293bc.jsonl
 31G	/Users/nitya/.claude/projects
```
</details>

### Assistant — 2026-10-20 17:20:33

Nothing was written; memory and load look fine now, so this looks like a stream stall rather than our setup. Retrying the timing test on a small slice (3 papers of group 01 as a temporary group 00).

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/review/mth_b1/_review_groups; head -3 group_01.txt > group_00.txt; wc -w < group_00.txt; ls -la ../AL-MTH-16m-12-QP_01.jpg; ~/.venvs/alevel/bin/python -I -c "
from PIL import Image; im=Image.open('/Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-12-QP_01.jpg'); print(im.size)"; date +%s > /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/scratchpad/t0
```

<details><summary>result</summary>

```
      11
-rw-r--r--@ 1 nitya  staff  511489 Oct 20 22:38 ../AL-MTH-16m-12-QP_01.jpg
(1400, 2250)
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Agent`** — Review mth_b1 test slice 00

```
Read /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/REVIEW_AGENT_PROMPT_QP.txt and follow it exactly. RUN=mth_b1, NN=00. (Cambridge A Level Mathematics 9709.) Maths notes: a printed graph-paper grid or blank axes inside a part is kept by design (it is that part's answer grid, not an empty area); a bracketed hint such as "[The volume of a cone is ...]" printed under a part belongs to that part; a .stem crop may hold only a diagram and context. If an image Read comes back without the picture (e.g. "media removed" / request limit), wait briefly and Read it again; never record a verdict for a sheet you did not actually see.
```

<details><summary>result</summary>

```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: ac9cfea31064e9f71 (internal ID - do not mention to user. Use SendMessage with to: 'ac9cfea31064e9f71', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/ac9cfea31064e9f71.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```
</details>

### Assistant — 2026-10-20 17:20:54

A small timing test (3 papers, 8 sheets) is running. I'll decide on wave size from its time.

### User — 2026-10-20 17:30:38

<task-notification>
<task-id>ac9cfea31064e9f71</task-id>
<tool-use-id>toolu_01RjK2BgdAGhEUppTz7f983M</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/ac9cfea31064e9f71.output</output-file>
<status>failed</status>
<summary>Agent "Review mth_b1 test slice 00" failed: Agent stalled: no progress for 600s (stream watchdog did not recover)</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
</task-notification>

### Assistant — 2026-10-20 17:30:44

Even a 3-paper slice stalled with nothing written, so this is systemic, not group size. Isolating it: a minimal agent that reads one sheet and replies.

**Tool `Agent`** — Probe: read one image

```
Use only the Read tool. Read the image /Users/nitya/rootatom_data/ALEVEL/review/mth_b1/AL-MTH-16m-12-QP_01.jpg and reply with one line: how many blue label bars you see and the first label's text. Nothing else.
```

<details><summary>result</summary>

```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a1f2cc48abe840cb0 (internal ID - do not mention to user. Use SendMessage with to: 'a1f2cc48abe840cb0', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/a1f2cc48abe840cb0.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```
</details>

### Assistant — 2026-10-20 17:31:29

A one-image probe agent is running to tell whether sub-agents can work at all right now.

### User — 2026-10-20 17:40:46

<task-notification>
<task-id>a1f2cc48abe840cb0</task-id>
<tool-use-id>toolu_01FD59DGcXJoMEywWsU3yZeD</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/a1f2cc48abe840cb0.output</output-file>
<status>failed</status>
<summary>Agent "Probe: read one image" failed: Agent stalled: no progress for 600s (stream watchdog did not recover)</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
</task-notification>

### Assistant — 2026-10-20 17:40:51

Even a single-image probe stalls. One more probe to separate causes: a text-only agent with the default model.

**Tool `Agent`** — Probe: text-only default model

```
Use only the Read tool. Read the first 3 lines of /Users/nitya/rootatom_data/ALEVEL/review/mth/_worklist.txt and reply with its first word only.
```

<details><summary>result</summary>

```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a96283b2862f6c930 (internal ID - do not mention to user. Use SendMessage with to: 'a96283b2862f6c930', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/a96283b2862f6c930.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```
</details>

### Assistant — 2026-10-20 17:41:02

A text-only probe (default model, no images) is running. It will show whether sub-agents work at all from this session.

### User — 2026-10-20 17:50:53

<task-notification>
<task-id>a96283b2862f6c930</task-id>
<tool-use-id>toolu_01BdY8PLtgPXGcnMkSvtUbhR</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-nitya-Documents-Nitya-Projects-Software-rootatom-paper-4-segregate--claude-worktrees-angry-hertz-cc484e/917c70ae-0181-4fb4-89e3-cc8427b293bc/tasks/a96283b2862f6c930.output</output-file>
<status>failed</status>
<summary>Agent "Probe: text-only default model" failed: Agent stalled: no progress for 600s (stream watchdog did not recover)</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
</task-notification>

### Assistant — 2026-10-20 17:50:58

Sub-agents from this session stall even on a one-line text task, so the review waves can't run here. Removing the temporary test group and writing everything a fresh session needs to run the waves.

**Tool `Bash`**

```
cd ~/rootatom_data/ALEVEL/review; rm -f mth_b1/_review_groups/group_00.txt; ls mth_b1/_verdicts | wc -l; cat >> mth/_HANDOFF.md <<'EOF'

## Visual review — ready to run (2026-10-20, late)
- Aliases: 73 in review/mth_b1/duplicates.csv (58 al_dedupe + 15 text scan; the 15 also in review/mth/aliases_textscan.csv —
  re-append them if al_dedupe is ever re-run). 13w-32 (HOLD) is an alias of 13w-31 -> manual list is 11 papers.
- 742 unique PASS papers (review/mth/review_list.txt) -> contact sheets in review/mth_b1, groups
  review/mth_b1/_review_groups/group_01..48 (<= 40 sheets each). No verdicts yet.
- BLOCKER in the hold-reduction session: every sub-agent stalled ("no progress for 600s", stream watchdog) — the review
  test agent, a 3-paper slice, a 1-image probe and even a text-only probe with the default model. Not a group-size problem.
  Run the waves from a FRESH session (memory: giant transcripts / RAM were the earlier stall cause; ~/.claude/projects = 31 GB).
- Agent prompt (general-purpose, model sonnet, background), per group NN:
  Read /Users/nitya/rootatom_data/alevel-pipeline/ALEVEL/REVIEW_AGENT_PROMPT_QP.txt and follow it exactly. RUN=mth_b1, NN=<nn>.
  (Cambridge A Level Mathematics 9709.) Maths notes: a printed graph-paper grid or blank axes inside a part is kept by design
  (it is that part's answer grid, not an empty area); a bracketed hint such as "[The volume of a cone is ...]" printed under a
  part belongs to that part; a .stem crop may hold only a diagram and context. If an image Read comes back without the picture
  (e.g. "media removed" / request limit), wait briefly and Read it again; never record a verdict for a sheet you did not actually see.
- One timed test agent first (group 01), then waves of 4-5, df -h before each wave; check with al_check_verdicts.py mth_b1;
  approve with al_approve.py mth_b1 --groups NN.. [--except PREFIX]. Disk was 11 GB free.
EOF
echo ok
```

<details><summary>result</summary>

```
       0
ok
Shell cwd was reset to /Users/nitya/Documents/Nitya/Projects/Software/rootatom/paper_4_segregate/.claude/worktrees/angry-hertz-cc484e
```
</details>

**Tool `Bash`**

```
cat >> ~/rootatom_data/ALEVEL/review/mth/_worklist.txt <<'EOF'
[done] sheets + 48 review groups for 742 unique PASS papers (review/mth_b1/_review_groups, <=40 sheets)
[blocked 2026-10-20] review waves: all sub-agents from the hold-reduction session stalled (incl. a text-only probe) -> run waves from a fresh session; prompt + steps in _HANDOFF.md 'Visual review — ready to run'
EOF
echo ok
```

<details><summary>result</summary>

```
ok
```
</details>

**Tool `ToolSearch`**

```
{"query": "select:mcp__ccd_session__start_session", "max_results": 1}
```

<details><summary>result</summary>

```

```
</details>

### Assistant — 2026-10-20 17:51:14

**Run Maths 9709 review waves from a fresh session**: this proposes a new session that runs the 48 prepared review groups, since sub-agents can't run from this session right now.

**Tool `mcp__ccd_session__start_session`**

```
Run the visual review of the Cambridge A Level Maths 9709 question-paper crops. Read ~/rootatom_data/ALEVEL/review/mth/_HANDOFF.md, section 'Visual review — ready to run', and follow it. Use the alevel-qp-review skill. Data ~/rootatom_data/ALEVEL, code ~/rootatom_data/alevel-pipeline/ALEVEL/scripts, Python ~/.venvs/alevel/bin/python -I. Do not edit anything in this worktree folder.
Steps: df -h; time one test review agent on group 01 (general-purpose, model sonnet, background, the exact prompt in the handoff). If it stalls or takes over ~5 min, stop and report instead of retrying blindly. Otherwise run groups 02..48 in waves of 4-5 agents (df -h before each wave), check with al_check_verdicts.py mth_b1, verify every flagged defect by opening the crop (agents are right about half the time), record decisions in review/mth/_worklist.txt, approve clean groups with al_approve.py mth_b1 --groups NN.. [--except PREFIX]. Collect real defects in a list for fixing (generic splitter fix with IS_MATHS gating + regression, or manual spec) and do not fix them in this session unless trivial.
Done = all 48 groups have verdicts, clean papers approved in reviewed_crop_hashes.json['mth_b1'], and a list of real defects with crop paths.
```

<details><summary>result</summary>

```
Proposed "Run Maths 9709 QP visual review waves (48 groups)" (task_id: task_ad2e3b6f). The user sees a card and nothing runs until they start it — with a click, or by telling you (then call start_session with proposal_id task_ad2e3b6f and nothing else). It expires in 7 days unless started; dismiss_task withdraws it sooner if it goes stale. Don't wait for it and don't repeat the introduction; carry on with what you were doing.
```
</details>

**Tool `mcp__ccd_turn__wrap_up`**

```
{"recap": "Deduplication found 73 aliases (one held paper turned out to be an alias, so 11 papers need manual specs). Contact sheets and 48 review groups are ready for the 742 unique passing papers. No review has run: every sub-agent stalled, even a text-only test. The handoff has the exact steps for a fresh session."}
```

<details><summary>result</summary>

```
Nothing is pending, so the app draws no box; the recap is the session's status. Do not call wrap_up again this turn; the advice that follows is for your next call. recap is two or three sentences (about 300 characters); this one ran 307. Keep it to what is now true and where it stands. Your closing message is your answer to the user: write it now, as the last thing you say this turn.
```
</details>

### Assistant — 2026-10-20 17:51:31

Deduplication is done and the review groups are built, but no review wave has run. Every sub-agent started from this session stalls ("no progress for 600s"): the review test, a 3-paper slice, a one-image probe, and even a text-only probe on the default model. Group size isn't the cause.

**Deduplication:**
- `al_dedupe` found 58 aliases.
- A text scan of variants from the same session found 15 more. They are the same papers re-typeset: only the encoding of maths symbols differs, and the crops match by eye and by pixel.
- That gives 73 aliases in `review/mth_b1/duplicates.csv`. The 15 extra pairs are also kept in `review/mth/aliases_textscan.csv`, because re-running `al_dedupe` rewrites duplicates.csv.
- 13w-32, one of the held papers, is the same paper as 13w-31, which passes. So it needs no manual spec, and the manual list (`review/mth/manual_specs_needed.txt`) is down to 11.

**Review setup:** 742 unique passing papers have contact sheets and 48 groups of at most 40 sheets in `review/mth_b1/_review_groups`. Disk had 11 GB free. No verdicts exist yet.

**Next step:** run the waves from a fresh session. Earlier stalls were traced to a huge session plus low memory, and `~/.claude/projects` is now 31 GB. The handoff section "Visual review — ready to run" in `review/mth/_HANDOFF.md` has the exact agent prompt (with maths notes on kept grids and bracketed hints) and the steps. I've proposed that session as a card: [Run Maths 9709 QP visual review waves (48 groups)](#task_ad2e3b6f).
