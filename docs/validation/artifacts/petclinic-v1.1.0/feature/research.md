# Research Decisions

## Validation location

- Decision: Add a non-null future-date branch in PetValidator.
- Rationale: Context Section 4 identifies the binder and validator as the reuse
  mechanism. Current PetController registers PetValidator and already rejects
  future dates with `typeMismatch.birthDate` in create/update handlers.
- Alternatives considered: Controller-only rule leaves direct validator calls
  inconsistent; entity annotations would introduce a different validation path;
  a new service or persistence constraint is unnecessary.

## Date/error contract

- Decision: Compare LocalDate with LocalDate.now(); preserve the existing code.
- Rationale: Current source already uses those semantics. No unresolved API or
  dependency question requires external research for this scoped change.
- Alternatives considered: Introduce Clock/timezone injection, rejected as scope
  expansion for this field-validation feature.

## Validation command

- Decision: Derive `./mvnw -B -Dtest=PetValidatorTests,PetControllerTests test` from
  the Maven test lifecycle used by the verified CI `./mvnw -B verify` command.
- Rationale: Focused tests avoid container-only integration fixtures. Use an
  isolated Maven cache under the validation directory to avoid user cache writes.
- Alternatives considered: Full verify and Gradle build remain broader follow-up
  checks; they are not needed to establish the two changed files' regressions.
