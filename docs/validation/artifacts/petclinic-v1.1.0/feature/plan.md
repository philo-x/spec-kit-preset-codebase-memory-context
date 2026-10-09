# Implementation Plan: Shared Pet Birth-Date Validation

**Branch**: `001-pet-birthdate` | **Date**: 2026-10-09 | **Spec**: [spec.md](spec.md)
**Input**: `specs/001-pet-birthdate/spec.md`

## Summary

Add the existing future-birth-date rule to PetValidator so direct callers receive
consistent rejection. Preserve controller checks and all model/storage behavior.
Write regressions first, observe a failure, implement the rule, and rerun the
validator plus related controller suites.

## Technical Context

**Language/Version**: Java 17 source; local execution JDK 21.
**Primary Dependencies**: Declared Spring Boot 4.1.0, Spring validation, JPA and
MVC; corroborated against pom.xml and PetValidator/PetController imports.
**Storage**: Existing H2/MySQL/PostgreSQL configurations; no storage change.
**Testing**: JUnit Jupiter, existing MapBindingResult/Errors validator fixtures;
MockMvc controller regression tests. No database required by the focused validator.
**Target Platform**: Existing JVM Spring MVC application.
**Project Type**: Single module, server-rendered web application.
**Performance Goals**: Retain constant-time field validation; no benchmark claim.
**Constraints**: Preserve `required` and `typeMismatch.birthDate` codes, local
LocalDate semantics, routes and schemas. No new dependencies or service layer.
**Scale/Scope**: One production file and its existing test file.

## Constitution Check

Before research: PASS. Existing structure retained, tests first, validation
mechanism reused, no deployment or remote Git changes planned.
After design: PASS. No migrations, new dependencies, route changes, or exceptions.

## Project Structure

### Documentation (this feature)

`specs/001-pet-birthdate/{spec,plan,research,data-model,quickstart,tasks}.md` and
`contracts/pet-form.md` describe the feature.

### Source Code (repository root)

- `src/main/java/org/springframework/samples/petclinic/owner/PetValidator.java`
- `src/test/java/org/springframework/samples/petclinic/owner/PetValidatorTests.java`
- Existing unchanged regression anchor:
  `src/test/java/org/springframework/samples/petclinic/owner/PetControllerTests.java`

**Structure Decision**: Use the existing `owner` package and validator extension
point identified by `.specify/memory/codebase.md`, then verified against current
source. Do not create generic `services/`, a DTO layer, or a database migration.

## Complexity Tracking

No constitutional violations or complexity exceptions.
