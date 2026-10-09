# Candidate completion verification

> Writing-procedure update (2026-10-09): the lock/atomic-write procedure recorded
> here is historical. The current command uses normal agent file editing with
> a write-time content comparison and output verification. See
> [refresh simplification](refresh-simplification.md); prior field results and CI
> identities describe their recorded command versions, not this revision.

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
Actual [GitHub Actions run 37905447930](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/actions/runs/37905447930)
completed successfully at `e5d702af8a34165ba9c8ccb722b555c91fb302b7`.
All three jobs passed: backend-free Python 3.11, backend-free Python 3.13, and
pinned-backend contracts. [Hosted CI evidence](artifacts/completion/github-ci.json)
records exact commit and job URLs. The commit adds a hash check and Git attributes
preserving CRLF evidence across checkouts. Subsequent documentation records this
result; local results above retain their earlier 25-test scope.

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

## Reviewable branches and release decision

The preset changes were pushed to
[codex/validation-completion](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/tree/codex/validation-completion).
The GitHub connector denied write/PR operations with 403; existing Git credentials
successfully pushed only the isolated validation branch. No PR was created, main
was not changed, and no version tag was published.

The exact [catalog patch](../catalog-update.v1.1.0.patch) was regenerated with
standard context against a fresh upstream checkout and verified. It preserves
the creation date, updates version/requirements/description/download URL and the
existing docs row, and leaves ordering intact. Its prepared fork branch is
`community/codebase-context-1.1.0` in `philo-x/spec-kit`; this must not merge into
the official catalog before the clean release asset exists. The initial automatic
review rejected the push as an apparent upstream-target mismatch. Explicit remote
configuration and repository ownership were checked before retrying the fork-only
operation. This did not bypass a rejected official-upstream write.

Publishing v1.1.0 and merging the candidate require the maintainer's release
confirmation. Hosted package download evidence and upstream catalog acceptance
remain dependent on that actual publication; they are not represented as passed.
