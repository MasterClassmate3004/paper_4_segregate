---
name: alevel-storage
description: Storage and disk management for the ROOTATOM A Level pipeline — offloading finished question-paper and mark-scheme PNG sets to Google Drive with verified read-back, restoring them, offloading source PDFs, the disk guard, and freeing local space safely. Use whenever someone says "offload Biology to Drive", "pull the Physics crops back", "disk is full", "free some space", "the Drive zip is empty / 0 bytes", "Google Drive isn't syncing", or before deleting any local images or sources.
---

# Storage: Google Drive offload and disk

Code `~/rootatom_data/alevel-pipeline/ALEVEL/scripts/`, Python `~/.venvs/alevel/bin/python -I`.
Drive mount: `~/Library/CloudStorage/GoogleDrive-<account>/My Drive/ROOTATOM_ALEVEL/` (Google Drive for desktop, **Stream** mode).

## Offload / restore images
```
al_offload.py push RUN [--only PREFIX ...] [--keep]     # zip PNGs per paper -> Drive splits/RUN/PREFIX.zip, read back, ledger, delete local PNGs
al_offload.py pull RUN PREFIX ...                        # restore PNGs, hash-checked against the ledger
```
- Ledger: `~/rootatom_data/ALEVEL/review/offload_ledger.csv` (`run,prefix,drive_path,zip_sha256,files,bytes,members_sha256,date`).
- Provenance JSON, logs, `answers.csv` stay local (small; any image can be regenerated from source + code).
- Offload only **approved** sets (QP run, manual crops, MS runs). Use `--only` lists built from the approved set.
- **Local read-back is not enough in Stream mode:** a zip written into the mount is only safe once Drive has uploaded it — wait for
  the `com.google.drivefs.item-id` extended attribute on every zip (`xattr -l FILE`), then do a cloud read-back, **then** delete
  locally (or push with `--keep` first, verify, then delete).
- Before deleting anything **on Drive**, read the zips back from the cloud and get the user's OK. Superseded zips go to Drive trash
  with ledger rows updated.
- Classification and other readers can read single members on demand: `zipfile.ZipFile(path).read(member)`.

## Source PDFs on Drive
Physics sources: `sources/9702_canonical.zip` (941 MB, 1,006 files; `review/sources_offload_ledger.csv`). Extract to a scratch folder
under `~/rootatom_data/ALEVEL/classification/` for reading; copy single files into `source_papers/canonical/` only temporarily for a
re-render/regression and remove them afterwards.

## When Drive misbehaves
Symptoms: files read as 0 bytes (`shasum` = e3b0c442... = empty input), `ls` of the Drive folder hangs, the stat size differs from the
ledger. History: 2026-10-17 → 10-20 Drive for desktop failed to start (macOS File Provider: `CANNOT_START_CORE` /
`FILE_PROVIDER_ACTIVATION_FAILED`); quitting and relaunching Drive (10-20) and a real reboot (10-21) fixed it. Fix order: relaunch Drive,
then a real Mac reboot (confirm with `sysctl kern.boottime`), then sign in again. **Never delete local copies while Drive is in this state.**
Cloud check without downloading: `al_cloud_verify.py` compares each zip with Drive's server md5 + size, then (with `--delete`) removes the
local PNGs after re-checking them against the zip members. Drive may leave a `GoogleDrive-<account> (<date>)` folder with items it could
not upload — compare with the cloud before deleting it.

Shared folder: `My Drive/ROOTATOM_ALEVEL` (https://drive.google.com/drive/folders/10o-FCTblCWGhnb1bN1sIWivPgQQCie9d) — keep every
uploaded split and source under it (`splits/<run>/`, `sources/`), nothing elsewhere.

## Disk
- `al_space.py` — report; runners stop below `AL_MIN_FREE_GB` (default 4). Keep > 8 GB free before agent waves.
- Regenerable and safe to delete after approval: contact sheets `review/<run>/*.jpg`, regression scratch runs (`splits/*_reg*`,
  `review/*_reg*`), frozen code copies no longer needed.
- Never delete: `source_papers/canonical/`, specs (`manual/`, `manual_specs/`), `reviewed_crop_hashes.json`, ledgers, provenance.
- Big consumers outside the pipeline: iCloud CloudKit cache (grows by GBs on its own; Desktop & Documents sync is on),
  `~/.claude/projects` (sub-agent logs, 300–570 MB per review agent — the user deletes finished `subagents/` folders; Claude may not
  delete transcripts), Claude Cowork VM image (`~/Library/Application Support/Claude/vm_bundles`, 12 GB, re-downloads on use),
  pip/Xcode caches. Ask before deleting anything outside the pipeline.
