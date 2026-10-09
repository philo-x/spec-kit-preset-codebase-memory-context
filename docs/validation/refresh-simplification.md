# Refresh writing procedure simplification

Date: 2026-10-09. This supersedes the lock/atomic-write requirements recorded
in earlier field reports. Those artifacts remain unchanged as historical evidence.

## Current behavior

The command reads existing target bytes before analysis, preserves manual
Overrides and upgrades owned schema 1.0 documents to 2.0. Immediately before
writing, it compares existing content or confirms continued absence. Observed
changes halt the update, including explicit replacement. It uses ordinary agent
file editing and rereads the output for verification; an identical candidate
is left unchanged. No lock, stale-lock recovery, fsync, hard link, atomic rename,
or filesystem compare-and-swap capability is required.

This is a prompt preset, not a filesystem transaction implementation. The check
can detect already-visible edits but cannot guarantee simultaneous-edit safety.
The upstream Spec Kit 1.1.2 constitution command likewise specifies an ordinary
overwrite, without a lock or atomic-publication protocol. This generator retains
its additional manual-preservation and write-time content checks.

## Focused active-agent verification

The active agent inspected the existing Petclinic `PetValidator.validate`
implementation, which rejects future dates with `typeMismatch.birthDate`.
A disposable copy of the previously generated context was prepared with a stale
validation sentence and a Chinese CRLF manual note. The agent assembled the
source-backed correction, checked the target bytes, wrote with an ordinary
`Path.write_bytes` call and reread the result. All six generated headings and
exact manual bytes survived. The identical-output check performed no write.

A separate fixture write then changed the target after the recorded read.
The agent observed the mismatch and did not overwrite it. No lock was created.
This is a focused editing exercise, not a repeat of the entire generation,
schema migration, hook matrix, native discovery, graph indexing or downstream
workflow. Fixture setup and assertions are measurement code, not a generator
implementation or independent LLM end-to-end test.

Review the [result](artifacts/refresh-simplification/result.json),
[before](artifacts/refresh-simplification/before.md),
[refreshed](artifacts/refresh-simplification/refreshed.md),
[retained external edit](artifacts/refresh-simplification/external-edit.md) and
[artifact hashes](artifacts/refresh-simplification/artifact-sha256.json).

## Revision validation

`pytest -q -m "not backend"`: **24 passed, 2 deselected** (21.36 seconds).
`git diff --check` passed. The two unchanged graph backend contracts were not
rerun for this writing-procedure adjustment.

The backend-free suite covers prompt contracts, exact upstream consumer
baselines, real installation/render/removal, distribution packaging and artifact
hashes. Prior remote CI and field records identify the earlier command revision;
they must not be described as results for this simplification. Optional graph
backend contracts are unchanged. No release or catalog publication is performed
as part of this adjustment.
