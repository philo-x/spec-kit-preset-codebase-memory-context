# Actual implementation validation

Temporary source: Spring Petclinic commit 500158f732419217507c7656904b8e6aa1bcc0d6.

Command (executed from the Petclinic root):

```sh
MAVEN_USER_HOME=/private/tmp/preset-petclinic-validation-20261009/maven-home ./mvnw -B -Dmaven.repo.local=/private/tmp/preset-petclinic-validation-20261009/maven-repository -Dtest=PetValidatorTests test
# after implementation
MAVEN_USER_HOME=/private/tmp/preset-petclinic-validation-20261009/maven-home ./mvnw -B -Dmaven.repo.local=/private/tmp/preset-petclinic-validation-20261009/maven-repository -Dtest=PetValidatorTests,PetControllerTests test
```

The initial sandbox attempt could not download the wrapper; the approved network
retry reached Maven. Its first build failed before tests: directory installation
copied the preset's development .venv, producing 790 nohttp violations. Moving
only that copied environment outside the temporary application root fixed the
interference without disabling checks or changing pom.xml.

Red: 9 tests, 1 failure, 0 errors/skips, exit 1. The failure was precisely
rejectsFutureBirthDateWithExistingErrorCode, before production was modified.
Green: 23 tests, 0 failures/errors/skips, exit 0. These are focused validator and
controller suites, not a full Maven verify or database/native-image matrix.
Existing build checks also passed in the selected test lifecycle.

The production diff adds LocalDate and the non-null future-date branch using the
existing error code. Two tests were added to the existing test class. No route,
schema, persistence or controller source changed. Native implement setup added
ignore patterns, preserving wrapper-jar exceptions. git diff --check passed.

The pre-feature codebase.md remains unchanged; it is a snapshot, not proof of
current future-date behavior. Plan and implementation verified anchors directly
against current source. No commit, push, deployment or publication occurred.
