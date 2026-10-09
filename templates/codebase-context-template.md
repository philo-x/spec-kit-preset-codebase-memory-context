---
schema_version: "2.0"
generator: "speckit.codebase-memory"
analysis_profiles:
  - generic
source_commit: "[SOURCE_COMMIT]"
working_tree: "[WORKING_TREE]"
evidence_tier: "verify"
---

# [PROJECT_NAME] Codebase Context

> Generated from current repository evidence. Inferred or unknown conclusions
> are marked explicitly. Repository paths are relative to the repository root.

## 1. Architecture Overview and Module Map

### System Purpose and Technology Stack
[Describe the system's core responsibilities and primary technology stack (languages, runtimes, primary frameworks, key libraries, and versions).]

### Module Layout and Boundaries
[List repository modules, packages, or directory structure in build/dependency order, describing verified dependency directions and major boundaries.]

### Entry Points and Code Anchors
[List deployable web servers, CLI binaries, background jobs, event listeners, or public library exports, citing concrete source files and code anchors.]

## 2. Core Flows and Interface Boundaries

### Request Pipeline and Middleware
[Describe the global request or execution pipeline: routing mechanism, filters, middlewares, interceptors, and error handling conventions in verified execution order. If not applicable (e.g. pure library or CLI), state why.]

### Security and Trust Boundaries
[Describe authentication mechanisms, token/session validation, authorization guards/RBAC, tenant/data isolation, credential boundaries, and public versus protected endpoint conventions without secret values.]

### Representative Traces
[Summarize one to five representative business flows with their entry point, major hops across layers, transaction boundary, side effects (cache, events, external calls), and failure path. Prioritize flows explaining modification boundaries; do not fabricate traces when not applicable.]

### External Integrations
[List external databases, caches, message brokers, third-party APIs, and downstream services with verified usage status, consumer mechanism, and evidence. If not applicable, state why.]

## 3. Data Persistence and Storage Model

### Storage and Entity Conventions
[Describe storage technologies, entity/model base classes, primary key/identifier strategies, auditing fields, logical deletion, and tenant/data scoping conventions. If no persistence layer exists, state why.]

### Transactions and Schema Migrations
[Describe transaction demarcation patterns (declarative or programmatic boundaries, rollback rules) and database migration/schema management tooling. If not applicable, state why.]

## 4. Development Conventions and Validation Commands

### Coding and Design Patterns
[Describe repository-specific patterns for organizing services, interfaces/implementations, dependency injection, validation, and error envelopes.]

### Modification Anchors and Extension Patterns
[For common change types, identify similar existing implementations, mechanisms to reuse (base classes, registration points, common utilities), boundaries to protect, and validation entry points.]

### Testing Strategy
[Describe test frameworks in actual use, unit/integration boundaries, test data/fixture setup, mock conventions, and representative test files.]

### Operational Constraints and Packaging
[Describe required runtimes, profiles, containerization/packaging behavior (Docker, OCI, JAR, standalone binary), environment configuration, and port/network conventions.]

### Validation Commands

| Purpose | Command | Working Directory | Preconditions | Evidence | Execution Status |
|---|---|---|---|---|---|
| [Build / Test / Lint / Run / Package / Deploy] | `[Repository-declared command]` | [Repository-relative directory] | [Required profile, runtime, or env] | [Config, CI, wrapper, or README path] | Not executed (discovered only) |

## 5. Evidence and Coverage Limitations

[Record verified bounded scopes, excluded or inaccessible paths, unverified external dependencies, and any conclusion that remains inferred or unknown. If a code graph backend was used, record the graph project and index coverage status; otherwise, record the direct file inspection and search scopes.]

## 6. Project Overrides

<!-- PROJECT OVERRIDES START -->

> Human-maintained and preserved verbatim on normal refresh. The generator checks
> ownership, marker structure, and secret safety, but does not verify these notes
> as repository facts or use them to raise confidence in generated findings.

<!-- PROJECT OVERRIDES END -->
