# Validation Guide

Prerequisites: JDK 17+ and Maven wrapper/dependency access. Run from repository
root, with an isolated MAVEN_USER_HOME and Maven repository under the temporary
validation parent. No Docker or service startup is required by the selected tests.

1. Add the two validator tests before changing production source.
2. Run `./mvnw -B -Dtest=PetValidatorTests test`: the future-date assertion should
   fail. Dependency/build failures are environment failures, not a red test.
3. Implement the validator rule and run
   `./mvnw -B -Dtest=PetValidatorTests,PetControllerTests test`.
4. Expect zero selected test failures and only the validator/test application
   files changed. Inspect Surefire XML rather than relying on test definitions.

If a wrapper, dependency, or baseline build problem occurs, document it and do
not claim tests passed. The context's validation command table remains a record
of discovery during generation, not this later execution result.
