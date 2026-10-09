# Data Model

Existing Pet extends NamedEntity and stores LocalDate birthDate. Identity,
relationships, columns, and schemas remain unchanged.

## Constraints

- Name: "nonblank, at most 30 characters" — existing validator rule.
- Type: "required for a new pet" — existing validator rule.
- Birth date: "required; must not be strictly after today's local date".
- Null date: retain `required` error.
- Future date: use `typeMismatch.birthDate`.
- Today and historical dates remain valid when other fields are valid.

There is no new entity or state transition. Owner/Pet cascades and database
constraints are outside this feature's change scope.
