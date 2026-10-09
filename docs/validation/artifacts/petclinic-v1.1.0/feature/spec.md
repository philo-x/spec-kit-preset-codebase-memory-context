# Feature Specification: Shared Pet Birth-Date Validation

**Feature Branch**: `001-pet-birthdate`
**Status**: Draft for disposable field verification
**Input**: Reject future pet birth dates in the shared PetValidator while retaining
existing null/date/type/name behavior. Add focused regression tests first.

## User Scenarios & Testing

### User Story 1 — Consistent validation (Priority: P1)

As a caller of the shared PetValidator, I receive the existing birth-date error
code for a date after today, even when I am not invoking a controller.

**Independent Test**: Direct validator tests prove tomorrow is rejected and today
is accepted; the existing past-date and null-date tests continue to pass.

**Acceptance Scenarios**:
1. Given an otherwise valid pet with tomorrow's birth date, validation reports
   `birthDate` with error code `typeMismatch.birthDate`.
2. Given an otherwise valid pet with today's or a past birth date, validation
   reports no birth-date error.
3. Given a null birth date, validation retains the existing `required` error.

### Edge Cases

- Compare LocalDate values with the local current date, matching existing MVC
  semantics; no new timezone conversion or injectable clock requirement.
- Preserve the 30-character name limit and new-pet type requirement.

## Requirements

- **FR-001**: PetValidator MUST reject a birth date strictly after LocalDate.now()
  using the existing error code `typeMismatch.birthDate`.
- **FR-002**: PetValidator MUST accept today's and past dates when the other fields
  are valid.
- **FR-003**: Existing null-date, name, type, controller, route, and schema behavior
  MUST be retained.
- **FR-004**: Focused tests MUST precede implementation, exercise the error code,
  and report their actual result; unrelated baseline failures must be separated.

## Success Criteria

- **SC-001**: The focused validator suite passes including tomorrow rejection and
  today acceptance.
- **SC-002**: Related PetController tests pass, or any environment/baseline failure
  is documented without claiming verification.
- **SC-003**: Only one production validator and its existing test class change.
