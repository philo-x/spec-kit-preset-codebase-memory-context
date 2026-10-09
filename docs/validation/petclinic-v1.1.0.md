# Spring Petclinic field validation — v1.1.0 candidate

This is the initial run. The subsequent [refresh/install follow-up](petclinic-refresh-install.md)
records the revised safety protocol, a successful refresh and clean installation;
the original blocked outcomes below are retained as historical evidence.

Date: 2026-10-09 (Asia/Shanghai). This record supplements the
[candidate automated checks](v1.1.0.md); it does not announce a release.

## Subject and execution boundary

The human authorized use of a local temporary directory and
[Spring Petclinic](https://github.com/spring-projects/spring-petclinic).
The source was cloned at `500158f732419217507c7656904b8e6aa1bcc0d6`.
The working directory is `/private/tmp/preset-petclinic-validation-20261009/petclinic`;
scenario copies, build logs and isolated Maven caches are in its parent directory.
Environment: macOS arm64, Python 3.14.7, specify-cli 1.1.2, JDK 21.0.1,
project Maven wrapper 3.9.16. The source declares Java 17 and Spring Boot 4.1.0.

The active Codex agent read the installed command skills and executed their
instructions using file and terminal tools. This is an actual agent field run,
not a Python implementation of the generator. It does not test automatic skill
discovery in a fresh native client session or an independent `codex exec` run.
No graph/MCP code exploration was used in the field run: direct source evidence
was sufficient. Backend-enhanced generation remains untested here.

The installed preset commands matched the working-tree source; all five command
and output-template hashes are in [preset-source-digests.json](artifacts/petclinic-v1.1.0/preset-source-digests.json).
Initialization used Spec Kit's real CLI `init --here --force --integration codex
--script py --preset <local-preset> --ignore-agent-tools --non-interactive` in the
temporary repository, through its Click runner. See
[initialization.txt](artifacts/petclinic-v1.1.0/initialization.txt).
No remote writes, publication or changes to a user's application repository
were performed.

## Generator and protection scenarios

The agent inspected repository metadata, Maven/Gradle manifests, CI, application
source, selected tests and schema. Credentials in application configuration were
redacted at inspection. It derived actual reuse anchors, scoped flows,
conventions, validation commands and uncertainty rather than inventing a graph.
The schema 2.0 [generated codebase.md](artifacts/petclinic-v1.1.0/codebase.md)
contains six sections, evidence qualifiers, command working directories and
execution status. Its SHA-256 is
`55fe7ccc87f1c095f7be47ddba138f2e3f71003c08d9b260587003dbc7a47ed6`.

Generation did not change any of the 132 original tracked source files, whose
hashes were captured in [source-baseline.json](artifacts/petclinic-v1.1.0/source-baseline.json).
It did not execute a build or test. The absent target was created with a
same-directory fsynced candidate and atomic no-clobber `os.link`; the temporary
candidate was removed. Build results below happened later during implementation.

Scenario preparation was external instrumentation, followed by active-agent
execution of the installed instructions. Hash/mtime measurements verify file
outcomes; they do not independently prove every possible agent behavior.
[Field outcomes](artifacts/petclinic-v1.1.0/field-results.json),
[preflight baselines](artifacts/petclinic-v1.1.0/scenario-baselines.json) and
[observations](artifacts/petclinic-v1.1.0/scenario-observations.json) retain the evidence.

| Scenario | Observed result |
| --- | --- |
| Absent target | Created; application source unchanged |
| Unchanged source with manual overrides | Unchanged; file bytes and mtime retained, including 332 bytes of CRLF/UTF-8 override text |
| Unowned target | Halted; original retained |
| Missing override end marker | Halted; original retained |
| Target symlink | Halted using lstat; linked target was not read |
| Synthetic credential in override | Halted; original retained; fixture value is excluded from published evidence |
| Real content change after preflight | Halted; concurrent writer's content retained |
| Another writer creates absent target | Actual FileExistsError from atomic no-clobber creation; writer's file retained |
| Mandatory read-only before hook | Emitted execution instruction, read installed hook skill, executed action with exit 0; Unchanged |
| Failing read-only after hook | Executed action with exit 1; file remained Unchanged, lifecycle incomplete |
| Unsupported mandatory condition | Halted/pending; not treated as false or successful skip |
| Recursive generator hook | Halted; original retained |
| Changed README with existing target | Halted because guarded atomic replacement was unavailable; original retained |

Excluded synthetic `.env.validation` files were prepared but never read by the
agent. This observation is not an OS-level proof of universal secret exclusion.
Hook actions really ran; there was no native extension hook runner available,
so the agent executed the installed read-only hook instructions itself.

### Refresh portability finding

The prompt requires atomic replacement guarded by the preflight identity and
content, and explicitly rejects check-then-rename as insufficient. Available
general filesystem operations do not provide that compare-and-swap primitive.
The active agent therefore refused to replace the existing target after source
changed. This respects the safety rule but prevents successful refresh in this
environment. A maintainer needs to resolve this usability issue before claiming
portable refresh support. This run does not establish a `Refreshed` outcome,
changed-body override preservation, schema 1.0 migration, explicit replacement,
or a general guarantee against all races. No safety requirement was weakened.

## Downstream command workflow

The agent read the installed `speckit-plan`, `speckit-tasks`, `speckit-analyze`
and `speckit-implement` skills, and ran their real Python prerequisites/setup
scripts. A disposable feature branch `001-pet-birthdate` and local constitution
were created. The small feature rejects a future date in the existing shared
`PetValidator`, preserving controller routes, persistence and required fields.

Plan consumed the context, then checked reuse and command anchors against current
source. Tasks specified tests before implementation and six ordered work items.
Analyze checked requirements, task coverage and consistency without editing the
feature files: four requirements covered, no blocking findings. The agent used
existing `PetValidatorTests`, `MapBindingResult`, `LocalDate` conventions and the
existing `typeMismatch.birthDate` code; no service layer or test harness was added.
The native implement setup also appended missing Java/editor/OS ignore patterns,
with an exception retaining wrapper jars.

### Installation interference discovered by the build

The first real Maven attempt failed before tests: the local-directory preset
installation had copied its development `.venv` into `.specify/presets/`.
Petclinic's root-wide nohttp scan reported 790 violations, all inside that copied
virtual environment. This is installation/build interference, not a red test.
Only the copied temporary installation's `.venv` was moved outside the Petclinic
root; the source preset environment and application build configuration were
left intact. The original command was then retried with checks enabled.
Directory-install users should use a clean preset distribution; the local ZIP
installation tests do not by themselves demonstrate behavior of a hosted release.

### Actual regression result

The rerun before production changes executed nine validator tests: one failure,
zero errors/skips, exit 1. The failing assertion was precisely
`rejectsFutureBirthDateWithExistingErrorCode`. The agent then added only the
non-null future-date branch and `LocalDate` import to the existing validator.

The final selected validator/controller run executed **23 tests, zero failures,
zero errors, zero skips**, exit 0, with Maven's existing lifecycle checks enabled.
This is focused testing, not full `verify`, native-image or database-matrix coverage.
See [test results](artifacts/petclinic-v1.1.0/test-results.json),
[red log excerpt](artifacts/petclinic-v1.1.0/red-test2.log.tail.txt),
[green log excerpt](artifacts/petclinic-v1.1.0/green-test.log.tail.txt) and
[implementation validation](artifacts/petclinic-v1.1.0/feature/validation.md).

All six feature tasks were completed. The [feature documents](artifacts/petclinic-v1.1.0/feature/plan.md),
[tasks](artifacts/petclinic-v1.1.0/feature/tasks.md),
[recorded analysis](artifacts/petclinic-v1.1.0/analysis.md),
[application patch](artifacts/petclinic-v1.1.0/application.patch) and
[final original-file changes](artifacts/petclinic-v1.1.0/final-source-changes.json)
make the result reviewable. `git diff --check` passed in the application clone.
The generated context remains the pre-feature snapshot: it does not assert that
the later validator change was already present. Source checks in the consumers
were necessary to establish current behavior. The copied Petclinic material
retains its [Apache 2.0 license](artifacts/petclinic-v1.1.0/SPRING_PETCLINIC_LICENSE.txt).

## Remaining scope

This run covers one active agent, one repository and one Python-script integration.
It does not prove Claude/Copilot/Gemini execution, Bash/PowerShell execution,
fresh-session command routing, optional/disabled/false-condition hook semantics,
backend-enhanced generation, hosted release installation, catalog publication,
or all Petclinic behavior. Read-only analyze findings were recorded by the
validation harness afterward, not written by the analyze command itself.

## Evidence checks in the preset repository

After adding this report, four relevant preset contract checks passed (manifest
and documentation, candidate catalog, generator prompt, output template).
Relative links in the edited documentation resolve, and `git diff --check`
passed. Artifact digests are recorded in
[artifact-sha256.json](artifacts/petclinic-v1.1.0/artifact-sha256.json).
The broader earlier 23-pass/1-skip automated result retains its original scope.
