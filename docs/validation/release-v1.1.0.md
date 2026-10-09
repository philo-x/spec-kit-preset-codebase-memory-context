# v1.1.0 publication and hosted installation verification

Date: 2026-10-09. The maintainer authorized publication and official catalog
submission. The tested release commit is
`52b67e61b0ecdac0aec7c17acb0852e0355f31c1`; main was fast-forwarded from
`343ae8dfee4219dc825ec1e1fd493d3365e4ba5a`, then annotated tag `v1.1.0` was
created and pushed without force. Later documentation commits do not move the
tag or replace the published asset.

## CI and release

- [Final candidate CI](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/actions/runs/37911781212): all three jobs passed, Python 3.11/3.13 base checks and pinned 0.10.8 backend contracts.
- [Tag CI](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/actions/runs/37912023848): passed.
- [Release workflow](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/actions/runs/37912023865): passed, including published-asset download, byte comparison and real archive install/resolve/remove.
- [Published v1.1.0](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/releases/tag/v1.1.0): clean ZIP asset, 82,319 bytes.

SHA-256: `530869fc13fe55d6841e392f83ebfc89e4dd78a5d92aef06f8b76fe1d021de43`.
The public downloaded ZIP matched a clean distribution built locally from the
exact tagged checkout byte for byte. The README at the tag contains the same
release download URL used by the catalog submission.

## Actual local hosted-URL installation

A fresh disposable project was initialized with Spec Kit 1.1.2, Codex skills
integration and Python scripts. The actual CLI then executed:

```sh
specify preset add --from https://github.com/philo-x/spec-kit-preset-codebase-memory-context/releases/download/v1.1.0/codebase-memory-context.zip
specify preset info codebase-memory-context
specify preset resolve speckit.codebase-memory
specify preset resolve codebase-context-template
specify preset resolve speckit.plan
specify preset resolve speckit.tasks
specify preset resolve speckit.analyze
specify preset resolve speckit.implement
specify preset remove codebase-memory-context
```

All nine invocations exited 0. All five command source files matched the archive;
Codex skills existed with rendered script/command placeholders. Installed files
contained no development environments, Git metadata, caches or historical
artifacts. Removal deleted the generator skill, restored the four core commands,
and retained a disposable `.specify/memory/codebase.md` preservation sentinel.
This checks publication and CLI registration, not another full LLM workflow.

See the [hosted result](artifacts/release-v1.1.0/hosted-result.json),
[publication metadata](artifacts/release-v1.1.0/publication.json),
[install log](artifacts/release-v1.1.0/preset-add-0.log),
[remove log](artifacts/release-v1.1.0/preset-remove-8.log), and
[artifact hashes](artifacts/release-v1.1.0/artifact-sha256.json).

## Official catalog submission

[Preset Submission #4892](https://github.com/github/spec-kit/issues/4892) was
created using the official issue form for the existing entry's update to 1.1.0.
It includes the pinned release URL, tag README, command/template inventory,
release hash and validation evidence. At verification it was open with the
`triage-must-have` label. No direct catalog PR was submitted.

Upstream `CONTRIBUTING.md` requires this issue flow for new entries, updates and
repairs; maintainers apply `preset-submission` in triage, automation validates
and creates the catalog PR, and maintainers review/merge. The earlier fork branch
and hand-edited patch are historical preparation, not the submission route.
The official catalog is not claimed updated until the upstream change merges.
