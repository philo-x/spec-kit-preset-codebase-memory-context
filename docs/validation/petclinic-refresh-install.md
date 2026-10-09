# Petclinic refresh and clean-install follow-up

> Writing-procedure update (2026-10-09): the lock/atomic-write procedure recorded
> here is historical. The current command uses normal agent file editing with
> a write-time content comparison and output verification. See
> [refresh simplification](refresh-simplification.md); prior field results and CI
> identities describe their recorded command versions, not this revision.

Date: 2026-10-09. This follows the [initial Petclinic run](petclinic-v1.1.0.md)
at commit `500158f732419217507c7656904b8e6aa1bcc0d6` in
`/private/tmp/preset-petclinic-validation-20261009/petclinic`.
The active Codex agent executed the revised installed generator instructions
with filesystem tools, without graph access. No independent client session or
native automatic command routing is claimed.

## Changes and safety boundary

The old instruction required compare-and-swap atomic replacement, which the
available filesystem could not provide. The revised generator acquires an
exclusive `.specify/.codebase-memory.lock` directory before reading the target
or executing hooks, snapshots target identity and bytes, and holds the lock
through after-hooks. It writes/fsyncs an exclusive same-directory candidate,
rechecks the snapshot immediately before atomic replacement, and releases only
its own lock. An existing lock is busy; interrupted locks are not stolen.
Creation still uses atomic no-clobber publication.

This is a deliberate change of guarantee, not an implementation of universal
compare-and-swap. The lock serializes cooperating generator invocations and
snapshot checks detect observed external changes. An editor ignoring the lock
can still race the final check/rename; known ongoing external edits require a
quiet window. Unsupported filesystem primitives still block writing.
No tests claim to eliminate that residual race.

## Actual refresh

External fixture setup inserted a Chinese note with CRLF bytes into the main
Petclinic override section before invoking the generator. The agent acquired
the lock, inspected the changed validator and current test definitions, and
checked source hashes against its evidence. It corrected the stale future-date
validation description and working-tree metadata. Source and target snapshot
checks preceded `os.replace`; the lock and candidate were cleaned up.
The generator did not run tests or modify application files.

- **Refreshed**: body updated; exact override bytes preserved.
- **Unchanged** subsequent invocation: file bytes and mtime retained.
- **Busy** second lock acquisition while the first held it: halted, first lock
  left intact. This exercises actual lock contention, not two independent LLMs.
- **External edit after locked preflight** in a disposable scenario: an actual
  fixture writer appended content; the agent detected the mismatch, halted,
  retained the writer's bytes, and released its owned lock. This does not test
  the undetectable last-instant race described above.

Review [before](artifacts/petclinic-refresh-install/preflight-codebase.md),
[after](artifacts/petclinic-refresh-install/refreshed-codebase.md),
[refresh result](artifacts/petclinic-refresh-install/refresh-result.json),
[no-op result](artifacts/petclinic-refresh-install/unchanged-result.json),
[lock contention](artifacts/petclinic-refresh-install/lock-contention.json) and
[external edit](artifacts/petclinic-refresh-install/external-edit-result.json).
The installed [command snapshot](artifacts/petclinic-refresh-install/generator-command.md)
identifies the tested prompt. Fixture preparation and measurement code are
instrumentation; synthesis, decisions and file operations were performed by
the active agent, not a simulated generator implementation.

## Clean installation and build

Spec Kit 1.1.2's `install_from_directory` uses `shutil.copytree` and ignores
`.gitignore`. The preset cannot change that upstream behavior. Instead,
`tools/package_preset.py` builds a release-file allowlist into a clean directory
and deterministic ZIP. It excludes environments, Git metadata, caches, build
output and historical evidence logs. Omitted evidence links in packaged docs
point to the source repository. The generator needs no runtime Python helper;
the builder is optional development/distribution tooling using the standard library.

The active run built that distribution and used Spec Kit's real
`PresetManager.install_from_directory(..., force=True)` to replace the temporary
installation. Context and feature documents survived. Installed command bytes
matched the current source, and the installed tree had no development noise.
Both clean-directory and generated-ZIP installs are additionally covered by
actual API installation tests; a hosted release remains untested.

The existing Maven command, with checks enabled and the isolated cache, then ran:

```sh
MAVEN_USER_HOME=/private/tmp/preset-petclinic-validation-20261009/maven-home ./mvnw -o -B -Dmaven.repo.local=/private/tmp/preset-petclinic-validation-20261009/maven-repository -Dtest=PetValidatorTests,PetControllerTests test
```

The sandbox attempt reported **0 nohttp violations**, then failed because Mockito
could not attach its agent to the JVM. The approved offline rerun in the same
execution environment as the earlier regression passed: **23 tests, 0 failures,
0 errors, 0 skips; exit 0**. No copied environment was moved manually after this
clean installation; no build configuration or check was disabled.
See [installation inventory and tests](artifacts/petclinic-refresh-install/installation-and-tests.json)
and [final Maven excerpt](artifacts/petclinic-refresh-install/clean-install-maven.tail.txt).

## Preset checks and remaining scope

Backend-free suite: **23 passed, 2 deselected** (20.78s). It includes actual clean
install/resolve tests, command rendering/uninstall across the existing matrix,
and packaging tests with deliberately noisy input, deterministic archives,
existing-output refusal and symlink-input rejection. After broadening excluded
path-component filtering, the five targeted packaging/install/prompt/documentation
checks passed again (0.65s); relative links and `git diff --check` passed.
These tests do not execute an LLM. The optional backend contracts were not rerun because this change does
not affect them. The earlier MCP handshake limitation remains.

Schema 1.0 migration, explicit replacement, hook-condition matrices, graph
augmentation, other clients' execution and hosted release/catalog checks remain
outside this follow-up. Atomic rename behavior is observed locally, not proven
for every filesystem or platform. No commit, push or release was made.
[Artifact digests](artifacts/petclinic-refresh-install/artifact-sha256.json)
identify the retained evidence. The initial report remains unchanged in outcome;
its old blocked refresh result does not describe the revised command.
