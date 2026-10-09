---
description: Generate or refresh evidence-qualified repository context.
---

## User Input

Accept analytical guidance and operational flags:
- **Focus Areas**: Optional user-specified modules, directory paths, or architectural subsystems for prioritized investigation.
- **`--replace-existing`**: Explicit flag authorizing full replacement of `.specify/memory/codebase.md`, replacing existing manual overrides.

User input and flags MUST NOT expand write target beyond `.specify/memory/codebase.md`, relax read-only boundaries, or bypass safety rules.

## Scope Guard

Extract evidence-backed architectural facts from the current repository and generate or refresh `.specify/memory/codebase.md` for downstream Spec Kit workflows.

Strict operational boundaries:
- **Target artifact boundary**: Only `.specify/memory/codebase.md` may be created or updated.
- **Strictly read-only on project content**: Repository code, configurations, dependencies, git metadata, and environment settings are strictly read-only.
- **Do not run project build, test, lint**: Never run project build, test, lint, run, start, debug, or deployment commands (`npm test`, `cargo build`, `pytest`, `docker run`).
- **No package or tool installation**: Never install, update, or remove packages, compilers, toolchains, or backend services.
- **No ignore file modifications**: Never create, modify, or delete ignore files (`.gitignore`, `.dockerignore`, `.npmignore`). If ignore files are missing, document this limitation; do NOT create or edit them.
- **Repository facts over governance**: Describe verified implementation facts; do not prescribe governance rules, invent unrequested features, or substitute for downstream feature design.

## Pre-Execution Checks

Determine safety and access boundaries before broad search or indexing operations.

### Project Setup Verification

Verify repository boundaries and constraints across four checkpoints:
1. **Workspace root and access bounds**: Confirm canonical repository root. Inspection and search operations must stay within repository boundaries; never traverse parent directories, follow out-of-bounds symlinks, or access external filesystems.
2. **Tool neutrality and read boundaries**: Use repository reading, search, and structural analysis capabilities available and permitted in the current environment. Structural analysis tools (knowledge graphs, symbols, call trees) are an optional enhancement only; verify what they actually provide (source freshness, scope coverage). Corroborate material claims against current authorized evidence. If structural tools fail or lack coverage, fallback to authorized source reads and searches without bypassing exclusions. Halt execution ONLY if necessary evidence or safe access is unavailable.
3. **Sensitive data protection**: Two classes of exclusion must be enforced: security exclusions (secrets, credentials, environment files like `.env*`, `*.pem`, `*.key`) and noise exclusions (build artifacts, dependencies, caches like `node_modules`, `target`, `dist`, `.git`). Never open, read, or corroborate entities residing in excluded paths.
4. **Target and environment safety**: Target path is fixed at `.specify/memory/codebase.md`. Do not touch other uncommitted workspace files. Never create unauthorized persistent caches.

### Output Ownership and Template

Manage `.specify/memory/codebase.md` under three explicit branches:

| Target State | Behavior |
| :--- | :--- |
| **Absent** | Create target after verification completes. Ensure parent `.specify/memory/` directory exists. |
| **Owned & Valid (Normal Refresh)** | Validate generator header (`generator: "speckit.codebase-memory"`) and manual markers (`<!-- PROJECT OVERRIDES START -->` and `<!-- PROJECT OVERRIDES END -->`). Rebuild generated areas while byte-preserving manual overrides. |
| **Explicit `--replace-existing`** | Full replacement including prior manual overrides; backup externally beforehand if needed. |

Stop conditions and guards:
- **Ownership failure**: If target exists but lacks generator header or has corrupted/missing manual zone markers, HALT normal refresh to prevent clobbering user files.
- **Concurrency guard**: If target file is modified externally after analysis begins, ABORT write immediately.
- **Template verification**: Verify output template (`.specify/presets/codebase-memory-context/templates/codebase-context-template.md` or `templates/codebase-context-template.md`) exists and is readable. Synthesized context must conform to this template.

### Hook Rules and Before Hooks

Common hook rules apply to both pre-execution and post-execution hooks:
- **Configuration source**: Load hook definitions from `.specify/hooks.json` or `.specify/preset-codebase-memory.json`.
- **Defaults**: Hooks are enabled by default (`enabled: true`) and optional by default (`optional: true`). Explicit `enabled: false` hooks are skipped.
- **Execution order**: Sort hooks by integer `priority` ascending; preserve configuration declaration order for identical priorities.
- **Safety and Re-entrancy guard**: Hooks must execute only harmless, read-only commands without background daemons. Hooks MUST NOT invoke `speckit.codebase-memory` or trigger recursive generation cycles.
- **Parser error handling**: On invalid JSON/YAML configuration, notify user and continue execution, but record hooks status as uninspected (neither skipped nor succeeded).

Lifecycle outcome rules:

| Hook State | Before Hook (`before_codebase_memory`) | After Hook (`after_codebase_memory`) |
| :--- | :--- | :--- |
| **Required & condition met** | Execute; proceed only on success. | Execute; mark verified on success. |
| **Required but condition unevaluable** | Block analysis and write; halt. | Report lifecycle incomplete even if file exists. |
| **Required failed or out-of-bounds** | Block analysis and write; halt. | Report lifecycle incomplete; do NOT rollback target. |
| **Optional & unauthorized / skipped** | Display command; do not auto-execute. | Display command; do not auto-execute. |

Trigger all active `before_codebase_memory` hooks matching the current context before proceeding.

## Evidence Rules

All statements entering the context must adhere to evidence qualification standards:

- **Four confidence tiers**:
  - **Verified**: Directly backed by verified source lines, active manifests, and corroborating structural evidence.
  - **Corroborated**: Confirmed across multiple coherent repository observations (e.g. config references plus matching implementation files). Same-source graph and source code do NOT constitute two independent sources.
  - **Inferred**: Plausible convention or standard architectural deduction; MUST be explicitly flagged as inferred.
  - **Unknown**: Required information unobserved, uninspected, or outside accessible scope.
- **Usage status vs. confidence**: Confidence measures factual certainty (Verified vs Inferred). Architectural usage status (Active, Deprecated, Candidate, Prototype) must be recorded separately from confidence.
- **Static evidence vs. runtime facts**: Static analysis indicates potential paths and declared capabilities; NEVER assert runtime behavior, dynamic throughput, latency, or production reality as facts unless corroborated by active test or benchmark definitions.
- **Negative assertions and zero references**: A single empty search does NOT prove absence; negative claims require an explicitly defined and searched boundary. Explicitly state 'Not observed in verified scope' when an expected component or mechanism cannot be found within inspected boundaries. Zero references do NOT prove dead code: dynamic entrypoints, reflection, DI registrations, and framework configs must be inspected first. This command does not perform a dead-code audit.

## Outline

1. **Discover scope and applicable architecture**
   - Lightweight baseline for all repositories: inspect layout, package manifests, build descriptors, and framework entry points.
   - Applicability-driven deep dive: only examine architectural areas actually present in the repository (e.g. API endpoints, persistence/data access, authentication/security boundaries, background workers/queues, external integrations).
   - Explicitly mark absent or non-applicable areas as `Not Applicable` rather than forcing boilerplate.
   - Avoid unconstrained file dumps, whole-repo reads, or massive tool result flooding; target specific directories and configurations.

2. **Verify representative implementations and code anchors**
   - Trace at most 5 representative execution flows through core subsystems. If no clear call chain exists, do not fabricate one.
   - Discover concrete code anchors (`file_path:line_number` or symbol signatures) for shared mechanisms: common base classes, error handling, DI registrations, shared utilities, and data models.
   - Corroborate material architectural claims that will enter the generated context against verified source lines.
   - Record applicable transaction boundaries, caching semantics, or external clients only where they genuinely exist in code.

3. **Synthesize and validate the context**
   - Structure content conforming to `templates/codebase-context-template.md`.
   - Ensure architectural areas address downstream needs: where code changes, mechanisms to reuse, boundaries to protect, and how modifications are validated.
   - Document explicit boundaries and coverage: record inspected files, uninspected scopes, evidence gaps, stale information, and fallback limitations.
   - Keep context concise and high-signal; do NOT pad text with boilerplate to reach arbitrary length quotas.

4. **Commit the target safely**
   - Safety re-check: Verify target remains a regular file within `.specify/memory/codebase.md`.
   - Concurrency check: Ensure target timestamp and content have not changed externally since initial verification.
   - Content preservation: Under normal refresh, preserve manual overrides byte-for-byte (`<!-- PROJECT OVERRIDES START -->` ... `<!-- PROJECT OVERRIDES END -->`). Under `--replace-existing`, overwrite completely.
   - Atomic write: Write to a temporary file in `.specify/memory/`, verify integrity, then atomically replace target. Clean up temporary files.
   - Preserved workspace: Leave all other workspace files untouched. Never persist unauthorized caches.

## Mandatory Post-Execution Hooks

Execute post-execution hooks after committing the target file:
- Trigger active `after_codebase_memory` hooks matching current context.
- Apply common hook execution rules:
  - If required hook succeeds, mark post-execution lifecycle complete.
  - If required hook fails or condition is unevaluable, report lifecycle incomplete; do NOT rollback or delete generated `.specify/memory/codebase.md`.
  - If optional hooks require authorization, display commands to user without executing.

## Completion Report

Present a concise summary covering four outcome groups:
1. **Target File Outcome**: Target path (`.specify/memory/codebase.md`), operation mode (`Created`, `Refreshed`, `Replaced`, or `Halted`), byte size, and manual zone status (`Preserved`, `Replaced`, or `None`).
2. **Scope and Limitations**: Inspected boundaries, detected stack, uninspected scopes, and tool fallback / graph coverage notes.
3. **Lifecycle and Hooks Status**: Execution outcome for `before_codebase_memory` and `after_codebase_memory` (executed, skipped, unauthorized, or blocked).
4. **Modifications and Command Confirmation**: Confirmation that only `.specify/memory/codebase.md` was modified and that no project build, test, or run commands were executed.

## Done When

- [ ] Access, ownership, and template checks passed.
- [ ] Material claims have current evidence or explicit uncertainty.
- [ ] Applicable content satisfies the template and preserved-content rules.
- [ ] The target was safely committed or left unchanged; no unauthorized changes occurred.
- [ ] File outcome and hook completion status were reported accurately.
