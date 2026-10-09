# Candidate completion verification

Date: 2026-10-09 (Asia/Shanghai). Temporary work remains under
`/private/tmp/preset-petclinic-validation-20261009/completion`.
This supplements the [initial field run](petclinic-v1.1.0.md) and
[refresh/install follow-up](petclinic-refresh-install.md).

## Observed checks

| Area | Actual result | Boundary |
| --- | --- | --- |
| Schema migration | Historical 14-section schema 1.0 Petclinic artifact migrated to six generated schema 2.0 sections; manual bytes retained | Current source fixture rechecked; historical generated facts were not accepted as current evidence |
| Explicit replacement | Unowned disposable target replaced with `--replace-existing`; original content deliberately discarded | Explicit test authorization; no automatic backups; path/change guards retained |
| Hooks | 26 isolated phase checks; ten actual read-only hook actions; native true/false condition evaluation and priority-order execution | Active-agent rule decisions, not 26 full independent LLM runs |
| Fresh Codex discovery | New `codex exec --ephemeral --ignore-user-config` session discovered and read installed project skill | Read-only discovery; earlier current-agent field run establishes actual workflow execution |
| Optional graph | Actual in-memory full index, scoped symbol/trace/coverage queries, source verification, and graph-enhanced context refresh | Source-only projection; fast mode skipped samples; static evidence only |
| Python 3.11 | 23 base checks passed | Local macOS equivalent of CI matrix, not GitHub Actions |
| Python 3.13 + pinned 0.10.8 | All 25 checks passed, including strict MCP handshake, no skips | Private short runtime directory avoids active-user-backend conflicts |
| Local release asset | Clean ZIP actually built, installed, six items resolved and uninstall verified | Hosted v1.1.0 asset is not yet published |

### Migration correction

The historical schema 1.0 marker interior contains `## 14. Project Overrides`.
The earlier schema 2.0 template put its generated section 6 heading inside the
same preserved region, making faithful migration structurally inconsistent.
The section 6 heading now belongs to the generated region before the start
marker. All old marker-interior bytes, including legacy headings, remain opaque
manual content; generated-heading validation excludes that interior.
[Migration and replacement outcomes](artifacts/completion/migration-replacement.json),
[old schema artifact](artifacts/completion/migration-before.md),
[migrated artifact](artifacts/completion/migration-after.md), and
[replacement artifact](artifacts/completion/replace-after.md) retain the evidence.

### Hook phase matrix

Both before/after phases covered absent event, disabled, true, false, null,
empty, unsupported expression, default optional without authorization,
authorized optional, actual mandatory action failure, unavailable command,
recursive unsafe command and invalid YAML. [The matrix](artifacts/completion/hook-matrix.json)
records decisions, actual subprocess exits and retained target bytes.
The active agent selected the actions from the inspected prompt; fixture and
measurement code did not implement the whole generator.

[The native Spec Kit executor](artifacts/completion/condition-executor.json)
returned true/false for supported synthetic environment expressions. Its unknown
expression fallback is false; the preset intentionally treats unsupported
expressions as pending. No fabricated native evaluator support is claimed.
Priority checks executed the agent-selected ascending order with stable ties and
invalid priority defaulting to ten. The earlier actual lifecycle run retains
before-success/after-failure evidence. Permission-denied reads and every possible
configuration encoding are not claimed covered by this finite matrix.

### Client and graph evidence

[Fresh Codex events](artifacts/completion/codex-discovery.json) show a successful
read of the native discovered skill and its final schema/lock/graph description.
The initial sandbox blocked the CLI app-server; the approved read-only retry
succeeded. This follows [official Codex skill evaluation guidance](https://developers.openai.com/blog/eval-skills).
The user subsequently limited actual client coverage to one client. Claude's
attempt returned a configured gateway 503; no alternative client support result
is claimed and no model/configuration was changed.

The graph indexed a source-only Petclinic copy, without submitting configuration
or security-excluded files. Fast mode excluded samples; full mode included the
Java sources. Queries found the binder and validator-test constructor references;
current source verified `setValidator(new PetValidator())`. Cited paths had
matching coverage hashes, a best-effort signal rather than completeness proof.
[Graph result](artifacts/completion/graph-result.json) and
[actual refreshed context](artifacts/completion/graph-enhanced-codebase.md)
disclose the source projection and limits. No graph persistence artifact was
requested. Runtime reachability and all routes were not inferred from counts.

### CI and publication boundary

[Python 3.11 log](artifacts/completion/ci311-final.log.txt): 23 passed, two backend
checks deselected. [Python 3.13 log](artifacts/completion/ci313-final.log.txt):
25 passed, no skips. Strict backend testing initially exposed a version conflict
with the live 0.11.0 server and a long socket path. Tests now create their own
short private runtime without stopping the user's server. All final checks passed.
Remote GitHub Actions results will be recorded separately against the submitted
validation commit; local matrix results are not presented as hosted CI results.

The remote v1.1.0 ref was checked and returned 404. Catalog changes therefore
remain a reviewable dependent update, not an assertion of an available release.
The catalog download URL now points to a **clean release ZIP asset**, because
source archives include historical logs that can interfere with host scanners.
The new tag-triggered release workflow builds/tests, publishes, downloads and
compares that asset, then verifies install/resolve/remove. This workflow has not
published anything during local validation. Its hosted download result requires
an actual release and cannot be manufactured from the local ZIP.

The external-writer race remains an explicit safety boundary, not a test that
will eventually prove universal protection: cooperating invocations are locked,
observed edits block commit, and non-cooperating last-instant edits can still race.
[Artifact hashes](artifacts/completion/artifact-sha256.json) identify retained evidence.
