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

- Spec Kit 1.1.2 or newer. The tested command baseline is exactly 1.1.2;
  later versions require compatibility review because these commands replace core files.
- A Git repository. The generator uses the canonical Git root as its safety and
  analysis boundary.
- Standard filesystem read and search capabilities. Optional: a code graph
  backend for accelerated
  symbol and call-chain discovery. The optional backend contract job pins
  `codebase-memory-mcp==0.10.8`; it does not establish support for every newer backend.

The generator does not install or update analysis tools or graph backends and
does not modify project ignore files. The upstream `implement` workflow still
creates or verifies ignore files during implementation. No additional Python
helper or PyYAML installation is required by the generator prompt; Spec Kit
itself and the development tests have their own Python dependencies.

## Installation

For development, build a clean distribution from the current checkout and
install it locally:

```bash
# Run in the preset checkout; use a fresh output directory on subsequent builds.
python3 tools/package_preset.py --output-dir dist
# Run in the target project; replace this with the absolute generated path.
specify preset add --dev /path/to/spec-kit-preset-codebase-memory-context/dist/codebase-memory-context
```

The builder also creates `dist/codebase-memory-context.zip` for archive distribution.
Spec Kit 1.1.2's directory installer copies the entire source directory; it does
not honor `.gitignore`. Do not point it at a development checkout containing
`.venv`, `.git`, caches or build output. The clean directory includes release
commands/templates and documentation, without those development artifacts or
historical validation logs. Links to omitted evidence point to the source
repository; unreleased evidence becomes available there after publication.
An existing installation can be removed and reinstalled from the clean directory;
keep `.specify/memory/codebase.md` and feature documents in place.

For the v1.1.0 release, install the clean ZIP asset:

```bash
specify preset add --from https://github.com/philo-x/spec-kit-preset-codebase-memory-context/releases/download/v1.1.0/codebase-memory-context.zip
```

Use the release asset rather than the GitHub source archive, which also includes
historical validation logs. Hosted download and installation passed; see the
[publication verification](docs/validation/release-v1.1.0.md).

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

The [v1.1.0 validation report](docs/validation/v1.1.0.md) distinguishes prompt
contract checks, real Spec Kit installation/rendering tests, optional backend
contracts, and agent behavior that remains unverified. Historical reports and
schema 1.0 artifacts describe their original releases, not the current schema
2.0 generator.

CI separates base validation without a graph backend from the optional backend
contract job. These tests do not execute an LLM generator.

Remove the preset with:

```bash
specify preset remove codebase-memory-context
```

## Usage

Run `speckit.codebase-memory` through the active coding agent after installing
the preset. Invoke it again whenever architecture, dependencies, deployment, or
repository conventions change materially.

The command:

- checks repository access, target ownership, and template requirements before
  hooks or broad analysis;
- processes pre-execution hooks (`before_codebase_memory`) using the official
  prompt behavior, within the generator's read-only and re-entrancy boundaries;
- discovers available and authorized repository-analysis tools before broad
  analysis, preferring structured navigation when useful and falling back to
  direct reads/search; no indexing call is required, and material conclusions
  must be verified against current source;
- identifies project technology stacks via manifest detection;
- follows seven steps: structure discovery, applicability assessment, mechanism
  inspection, representative traces, coverage review, synthesis, and safe writing;
- traces representative business flows (capped at five) prioritizing
  modification boundaries;
- audits evidence coverage and reports explicit boundaries and limitations;
- synthesizes context in memory, strictly preserving the human-maintained
  Project Overrides section on refresh;
- checks for intervening target changes, writes `.specify/memory/codebase.md`,
  and rereads the result under the centralized Output Contract; and
- processes post-execution hooks (`after_codebase_memory`) and reports actual
  hook outcomes separately from the file result.

The generator records repository-declared build, test, quality, run, and
deployment commands but does not execute them. It also prohibits other
network-dependent project commands; this restriction does not prohibit authorized
MCP tool use within the stated boundaries. It does not modify application
source, build files, configuration, tests, ignore files, deployment artifacts,
or any file other than `.specify/memory/codebase.md`. Ordinary non-sensitive
configuration and examples can supply evidence; credentials, production data,
and security-excluded paths remain inaccessible. Analysis tools and hooks cannot
expand these boundaries. Preconfigured MCP tools may use tool-managed indexes,
caches, or daemons only within existing authorization and without changing other
project files or Git state. Tool availability alone does not authorize these
side effects or `index_repository`; unclear authorization or effects require
direct reads/search. Feature artifacts and a clean working tree are not required.

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

Before writing, the generator checks that an existing target still matches the
content read before analysis, or that a new target is still absent. Observed
changes stop the update. It uses normal agent file-editing tools and verifies
the result; no lock or atomic-write capability is required. This check does not
guarantee protection against simultaneous edits.

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

## Lifecycle Hook Configuration

The generator reads `before_codebase_memory` and `after_codebase_memory` from
`.specify/extensions.yml`, following the `before_<command>` / `after_<command>`
convention. These are preset events, not built-in Spec Kit events or automatically
configured registrations. If using the previously documented `before_codebase-memory`
and `after_codebase-memory` keys, migrate them to the underscore names; hyphenated
aliases are not read. Commands must already be installed, invocable in the active agent,
read-only, and unable to re-enter the generator. For example:

```yaml
hooks:
  before_codebase_memory:
    - command: speckit.review-context-scope
      enabled: true
      optional: true
```

This example names a project-supplied command; the preset does not provide it.
Hook handling follows the official v1.1.2
[constitution](https://github.com/github/spec-kit/blob/v1.1.2/templates/commands/constitution.md)
command: both Pre-Execution Checks and Post-Execution Checks contain its complete
hook rules and output blocks, changing only event names and the business description.
Hooks are enabled by default, optional hooks displayed for
user invocation, and executable mandatory hooks actually invoked and awaited.
Non-empty conditions are skipped without evaluation and left to HookExecutor;
the prompt does not coordinate an evaluator or sort by priority. Missing
configuration means no hooks; invalid configuration is reported with the parser
error and generation continues with hooks unchecked, including mandatory hooks.
Scope Guard requires redacting secrets from all error messages, including YAML
parser errors.

Independent safety and output checks still halt unsafe work. Mandatory
status cannot authorize unsafe access, side effects, or generator re-entry; an
unsafe mandatory invocation halts the command. Actual failures and unavailable
commands are reported, and post-hook failures retain the target. A condition skip
is unevaluated, not proof that the condition was false or the hook succeeded.

## Development and Validation

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -m "not backend"
```

The development dependency pins Spec Kit 1.1.2. Base tests check the manifest,
seven-step prompt contract, schema 2.0 template, all six installed items, local
ZIP installation, and all five commands rendered and removed across Codex,
Claude, Copilot, and Gemini with Python, Bash, and PowerShell selection. Script
selection is checked; the generated shell/PowerShell workflows are not executed.

Optional third-party backend contracts:

```bash
.venv/bin/python -m pip install -r requirements-backend.txt
PRESET_REQUIRE_BACKEND=1 .venv/bin/python -m pytest -m backend
```

Without that environment variable, absent or sandbox-inaccessible backends may
skip locally; skips mean unverified. CI requires the backend job to fail in
those cases. Backend version, CLI flags, and MCP handshake tests verify the
third-party surface, not generation correctness.

The four consumer files start from the official v1.1.2 commands. Additions sit
between `CODEBASE CONTEXT START/END` comments. Tests remove those blocks and
compare every remaining nonblank line with versioned upstream fixtures, whose
SHA-256 hashes and source URL are recorded in
[provenance.json](tests/fixtures/upstream/spec-kit-v1.1.2/provenance.json). The
fixtures are also checked against the installed 1.1.2 core pack. On upgrade,
review upstream changes, update fixtures and provenance, reapply the additions,
and rerun integration checks.

Prompt tests check the written rules for official hook semantics, tool discovery,
and the unchanged analysis/output contracts. They cannot prove byte-preserving
refresh, secret exclusion, hook execution, or detection of intervening edits.
A real agent field run must record its environment, fixture/source identity,
invocation, actual changes, output,
and limitations before those behaviors are claimed verified. Do not add Python
simulations and label them generator end-to-end tests.

The current [Spring Petclinic field report](docs/validation/petclinic-v1.1.0.md)
records active-agent execution without graph access, protection outcomes and a
real downstream test-first change. The [follow-up report](docs/validation/petclinic-refresh-install.md)
records a historical lock-based implementation, now superseded by ordinary
file editing with a write-time content comparison and output verification.
Its lock and atomic-write results do not validate the current writing procedure.
See the [refresh simplification record](docs/validation/refresh-simplification.md)
for the current scope and focused verification.

See the historical [completion verification](docs/validation/completion.md) for
migration, replacement, hook, native Codex, graph and full local CI results.
Its hook outcomes describe the earlier semantics and do not validate the current
hook handling; the refactored prompt needs a new agent field run.

See the [release checklist](docs/publishing.md) for publishing and catalog updates.

## License

MIT. See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md)
for the retained Spec Kit command source.
