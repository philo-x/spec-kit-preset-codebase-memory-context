# Tasks: Shared Pet Birth-Date Validation

**Input**: `specs/001-pet-birthdate/` design documents.
**Tests**: Required by FR-004; use tests before implementation.

## Phase 1: Setup

- [X] T001 Verify current source anchors and the focused command in specs/001-pet-birthdate/research.md against pom.xml and the existing validator tests.

## Phase 2: Foundational

- [X] T002 Verify existing required-date, type, and 30-character name constraints in src/main/java/org/springframework/samples/petclinic/owner/PetValidator.java and the existing Errors fixture in src/test/java/org/springframework/samples/petclinic/owner/PetValidatorTests.java; make no infrastructure or schema changes.

## Phase 3: US1 — Consistent validation (P1)

**Goal**: Shared validator rejects future dates and retains current behavior.
**Independent Test**: Future-date error has the specified code, today/past succeed,
null date retains required, and related controller tests remain valid.

- [X] T003 [US1] Add tomorrow rejection with typeMismatch.birthDate code and today acceptance tests for "required; must not be strictly after today's local date" in src/test/java/org/springframework/samples/petclinic/owner/PetValidatorTests.java; observe a real failing assertion before implementation.
- [X] T004 [US1] Implement the non-null future-date branch with typeMismatch.birthDate while preserving required errors in src/main/java/org/springframework/samples/petclinic/owner/PetValidator.java.
- [X] T005 [US1] Run the selected validator and controller suites for src/test/java/org/springframework/samples/petclinic/owner/PetValidatorTests.java and src/test/java/org/springframework/samples/petclinic/owner/PetControllerTests.java; inspect actual results and document baseline/environment blockers separately.

## Phase 4: Polish & Cross-Cutting Concerns

- [X] T006 Review the two-file application diff and record actual commands, results, and limitations in specs/001-pet-birthdate/validation.md; mark tasks complete only when their stated work has been performed.

## Dependencies and Parallel Execution

T001 → T002 → T003 → T004 → T005 → T006. One user story; no parallel task markers
because implementation depends on the red regression and both suites share the
same build output. Independent documentation review can occur after T005.

## Implementation Strategy

US1 is the complete MVP. Reuse PetValidator and its existing test class, without
creating a service, initializing the application again, or changing persistence.
If the red test cannot run because of the environment, halt before T004 and
record the blocker; do not treat a build error as proof of a failing regression.
