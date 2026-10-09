# Verified Codebase Context

Verified Codebase Context is a Spec Kit preset for established repositories. It
generates an evidence-qualified repository context at
`.specify/memory/codebase.md` and makes the core `plan`, `tasks`, `analyze`, and
`implement` workflows consume that context when it exists.

The preset provides one standalone generator command,
`speckit.codebase-memory`, one versioned output template, and four complete core
command replacements aligned with the **Spec Kit v1.1.2** baseline. The
generator uses standard repository reading and code search as its baseline, with
optional structural enhancement from code graph backends such as
[codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp). Material
claims require direct repository evidence and coverage checks before context is
written.

## Requirements

- Spec Kit 1.1.2 or newer.
- A Git repository. The generator uses the canonical Git root as its safety and
  analysis boundary.
- Standard filesystem read and search capabilities. Optional: a code graph
  backend (such as `codebase-memory-mcp 0.10.8` or newer) for accelerated
  symbol and call-chain discovery.

The preset does not install or update analysis tools or graph backends. It does
not modify project ignore files (`.gitignore`, `.dockerignore`, etc.). It does
not require PyYAML or a project-specific helper runtime: the generator reads its
installed, preset-owned output template directly.

## Installation

Install the v1.1.0 release archive from a Spec Kit project:

```bash
specify preset add --from https://github.com/philo-x/spec-kit-preset-codebase-memory-context/archive/refs/tags/v1.1.0.zip
```

For local development:

```bash
specify preset add --dev /path/to/spec-kit-preset-codebase-memory-context
```

Verify the generator, output template, and consumer commands:

```bash
specify preset resolve speckit.codebase-memory
specify preset resolve codebase-context-template
specify preset resolve speckit.plan
specify preset resolve speckit.tasks
specify preset resolve speckit.analyze
specify preset resolve speckit.implement
```

## Field Validation

The v1.0.0 release was exercised end to end against two real repositories: a
Spec Kit checkout for the generic profile and Spring Petclinic for the Spring
Boot Maven profile. Details are in the [v1.0.0 field-validation report](docs/validation/v1.0.0.md).

The [v1.0.1 MCP and workflow report](docs/validation/v1.0.1.md) verified a real
stdio MCP handshake, tool discovery, and a downstream smoke test.

The [v1.1.0 validation report](docs/validation/v1.1.0.md) validates the
tool-neutral execution path without graph backends, read-only Project Setup
Verification boundaries, custom lifecycle hooks (`before_codebase_memory` and
`after_codebase_memory`), and downstream command consumption aligned with Spec
Kit v1.1.2.

CI splits base validation (without any graph backend installed) from optional
backend contract validation.

Remove the preset with:

```bash
specify preset remove codebase-memory-context
```

## Usage

Run `speckit.codebase-memory` through the active coding agent after installing
the preset. Invoke it again whenever architecture, dependencies, deployment, or
repository conventions change materially.

The command:

- performs read-only Project Setup Verification to ensure path, symlink, and
  sensitive credential boundaries are respected before any reading or indexing;
- executes pre-execution hooks (`before_codebase_memory`) with re-entrancy
  guards;
- uses available repository reading and search capabilities as a tool-neutral
  baseline, incorporating graph tools as optional enhancements when available;
- identifies project technology stacks via manifest detection;
- separates lightweight architectural baseline discovery from deep probing,
  investigating persistence, pipelines, auth, and integrations only when
  actually applicable;
- traces representative business flows (capped at five) prioritizing
  modification boundaries;
- audits evidence coverage and reports explicit boundaries and limitations;
- synthesizes context in memory, strictly preserving the human-maintained
  Project Overrides section on refresh;
- writes safely and atomically to `.specify/memory/codebase.md`; and
- executes post-execution hooks (`after_codebase_memory`) and reports lifecycle
  completion status.

The generator records repository-declared build, test, quality, run, and
deployment commands but does not execute them. It does not modify application
source, build files, configuration, tests, ignore files, deployment artifacts,
or any file other than `.specify/memory/codebase.md`.

## When to Use It

Use this preset when:

- Spec Kit is being adopted in an established or unfamiliar repository;
- planning repeatedly rediscovers modules, entry points, persistence patterns,
  security boundaries, or validation commands;
- later workflow stages need a shared architecture baseline with explicit
  uncertainty and source evidence; or
- downstream commands need concrete code anchors and reusable mechanisms
  without performing ad-hoc repository scans each time.

## When Not to Use It

Do not use this preset when:

- the repository is so small or short-lived that maintaining generated context
  would cost more than rediscovery;
- runtime behavior, production traffic, or dynamic configuration must be proven
  rather than statically inferred; or
- another preset already replaces the same core commands and the two full
  replacement sets have not been reconciled.

## Context Contract

Generated files carry this ownership marker in frontmatter:

```yaml
generator: "speckit.codebase-memory"
```

The generator refreshes an owned file only when its schema and Project
Overrides markers are valid. It preserves every byte between:

```markdown
<!-- PROJECT OVERRIDES START -->
<!-- PROJECT OVERRIDES END -->
```

An existing unowned file is not overwritten by default. Move trusted manual
content into a Project Overrides section, then invoke the command with
`--replace-existing` only when a full replacement is intended. There is no
automatic adopt mode because old generated and human-authored statements cannot
be distinguished safely.

The context file is optional for the four consumer workflows. If it is absent,
each consumer follows the corresponding core workflow without codebase-context
augmentation.

## Workflow Effects

| Command | Added behavior |
|---|---|
| `speckit.codebase-memory` | Generates or refreshes evidence-qualified repository context using tool-neutral discovery, read-only preflight checks, and lifecycle hooks. |
| `speckit.plan` | Uses existing architecture and conventions to fill Technical Context, focus discovery, shape data models and contracts, while validating critical paths against source. |
| `speckit.tasks` | Uses module and persistence conventions to anchor Setup and Foundational tasks in the existing codebase with concrete code anchors. |
| `speckit.analyze` | Optionally checks plan and task references against repository context and corroborates findings with current source. |
| `speckit.implement` | Loads coding conventions and repository-specific validation commands before executing tasks, verifying commands against current build/CI config. |

## Compatibility and Maintenance

The four consumer commands use `strategy: replace`. They preserve the Spec Kit
1.1.2 command structure, script selection, native command references, and hook
surfaces, but they do not inherit future core command changes automatically.
Review and resynchronize them before each preset release that raises the
supported Spec Kit baseline.

Static graph evidence cannot prove runtime execution, production frequency,
active profiles, successful transactions, or external-service availability.
The generated context is an evidence-qualified engineering aid, not a runtime
observability report or security certification.

## License

MIT. See [LICENSE](LICENSE).
