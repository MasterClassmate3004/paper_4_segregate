---
name: alevel-sources
description: Phase 0 of the ROOTATOM A Level pipeline — obtaining clean Cambridge past-paper PDFs (question papers and mark schemes for 9702/9701/9700/9709/9231) with zero third-party watermarks, under canonical names, ready for splitting. Use whenever someone needs to fetch or re-fetch a subject's sources, finds a missing/corrupt/unreadable source PDF, sees a watermark or website stamp in a paper, has an A3-sized paper, a combined multi-paper PDF, a mark scheme that belongs to a different paper, or asks where the A Level source files come from — e.g. "fetch the 9709 papers", "this mark scheme is the wrong paper", "the PDF is blank", "there's a dynamicpapers stamp in the crop".
---

# A Level sources (Phase 0)

## Rules
- **Ask the user before any download** — show archive, file list/count and total size. Downloads go into a fresh folder and are
  only opened by our scripts with `python -I`; nothing downloaded is executed.
- **Zero third-party watermarks.** Preferred source: Dynamic Papers (user's choice; one "www.dynamicpapers.com" text line in the
  header band, removed by the stripper). PapaCambridge only via the exact overlay stripper (A-PDF ribbon, XtremePapers diagonal,
  StudentBounty links). 2026 PapaCambridge files with a tiled "PapaCambridge PDF pipeline" watermark or licence/trace-ID notice
  stay out. Dynamic Papers has no 9231 → PapaCambridge for Further Maths.
- Canonical names: `<code>_<s|w|m><yy>_<qp|ms>_<vv>.pdf` in `~/rootatom_data/ALEVEL/source_papers/canonical/`.
  Pre-2010 single-digit components (e.g. `qp_4`) map to the first variant (`41`).

## Tools (`~/rootatom_data/alevel-pipeline/ALEVEL/scripts/`, run with `~/.venvs/alevel/bin/python -I`)
| Script | Use |
|---|---|
| `al_fetch_sources.py SUBJECT [--workers 6] [--exclude _s26_,_m26_] [--read-errors F1,F2] [--recheck-held]` | Rebuild one subject's canonical set from the Phase 0 originals (ledger URL + raw sha256) and run the same stripper + scanner. `--read-errors`: files Phase 0 could not open. `--recheck-held`: re-fetch Phase 0 holds and let the current scanner decide. |
| `strip_overlay_watermarks.py IN.pdf OUT.pdf` | Remove third-party overlays exactly (object-level, not pixels). |
| `check_source_watermarks.py` | Phase 0 gate: text + image scan for third-party strings/overlays. Must be clean after stripping. |
| `al_normalise_a4.py FILE.pdf ...` | A3 pages → A4 in place; original kept in `canonical_original/`, recorded in `derived_sources.csv`. |

Ledgers/manifests: `source_papers/download_ledger.csv`, `canonical_manifest.csv`, `derived_sources.csv`,
`alevel-pipeline/ALEVEL/source_papers_phase0_{ledger,manifest}.csv`.

## Typical situations
- **Missing / unreadable file** → `al_fetch_sources.py SUBJ --read-errors NAME`. If Phase 0 never had it, propose a second
  archive to the user.
- **Combined source** (two components in one PDF, e.g. `9702_s09_qp_2` = 21+22, `9709_s09_qp_7` = 71+72): derive the separate
  files first, record them in `derived_sources.csv`.
- **MS belongs to another paper** (e.g. Biology 08w-21): find a correct copy (user OK for another archive), strip, rescan, place in
  `canonical/`, move the wrong file to `canonical_original/`, update `derived_sources.csv` + manifest.
- **Old mark schemes**: combined all-component booklets and 2002 MCQ keys in examiner reports (`raw_ms_search/*_er.pdf`) —
  `al_run_ms.py` already searches booklets; see `alevel-mark-schemes`.
- **Scanned (no text layer) papers**: accepted only where agreed (2002 Physics MS were done by OCR); otherwise deferred.
- **Sources offloaded to Drive** (Physics: `sources/9702_canonical.zip`, ledger `review/sources_offload_ledger.csv`): extract into a
  scratch folder under `~/rootatom_data/ALEVEL/classification/` for read-only work; to re-render or re-split, copy only the needed
  files into `canonical/` temporarily and remove them afterwards. Needs a working Drive (see `alevel-storage`).

## Done when
Every in-scope QP and MS for the subject is in `canonical/`, scanner-clean, with gaps listed explicitly and signed off by the user.
