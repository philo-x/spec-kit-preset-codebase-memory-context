---
schema_version: "1.0"
generator: "speckit.codebase-memory"
analysis_profiles:
  - generic
  - spring-boot-maven
source_commit: "88e37c15cf6fc8490b01bc3e8e2c800cec1ac272"
working_tree: "modified only by Spec Kit initialization and preset installation"
evidence_tier: "verify"
---

# Spring Petclinic Codebase Context

> Generated from current repository evidence. Inferred or unknown conclusions
> are marked explicitly. Repository paths are relative to the repository root.

## 1. System Purpose

Spring Petclinic is a sample clinic-management web application. It demonstrates
owners, pets, visits, veterinarians, server-rendered pages, persistence, and
database profile switching for Spring Boot users and contributors.

## 2. Technology Inventory

| Layer | Technology | Version / Detail | Usage Status | Confidence | Evidence |
|---|---|---|---|---|---|
| Runtime | Java | 17 or newer | Wired | Verified | `pom.xml`, `.github/workflows/maven-build.yml` |
| Framework | Spring Boot | parent 4.1.0 | Wired | Verified | `pom.xml` |
| Web | Spring MVC and Thymeleaf | controllers plus HTML templates | Wired | Corroborated | `pom.xml`, `src/main/java/**/**Controller.java`, `src/main/resources/templates/` |
| Persistence | Spring Data JPA | JPA repositories and entities | Wired | Corroborated | `pom.xml`, `src/main/java/**/**Repository.java`, entity annotations |
| Databases | H2, MySQL, PostgreSQL | H2 default; mysql/postgres profiles | Configured-only for external DBs | Verified | `application*.properties`, `docker-compose.yml` |
| Cache | Spring Cache and Caffeine | veterinarian cache | Wired | Corroborated | `pom.xml`, `system/CacheConfiguration.java`, `VetRepository.java` |
| Tests | JUnit/Spring Boot Test/Testcontainers | MVC slices, JPA slice, integration tests | Wired | Verified | `src/test/java/`, `pom.xml` |

## 3. Module and Package Map

### Module Tree

This is a single Maven module. Production Java code is under
`src/main/java/org/springframework/samples/petclinic`, grouped into `model`,
`owner`, `vet`, and `system`. Templates, messages, configuration, and database
scripts are under `src/main/resources`. Tests mirror those packages below
`src/test/java`.

### Dependency Direction

MVC controllers depend directly on Spring Data repository interfaces and domain
entities. Repositories operate on JPA entities; templates consume model values
prepared by controllers. The test tree depends on production code through MVC,
JPA, and full-application test slices. No separate service layer is present in
the representative owner/vet flows.

### Package Conventions

Feature code is grouped by domain (`owner`, `vet`); shared entity foundations
live in `model`; cross-cutting MVC/error/cache configuration lives in `system`.
Tests use the same package names to access package-visible behavior and mirror
the tested feature.

### Entry Points

- `PetClinicApplication.main` starts the Spring Boot application.
- Test-only main/application classes provide H2, MySQL, and PostgreSQL
  development/integration variants.
- Graph route discovery found 20 HTTP route instances across owner, pet, visit,
  vet, welcome, and crash handlers.

## 4. Request, Messaging, Job, and Data Flows

### Global Request and Exception Pipeline

Spring MVC dispatches annotated controller routes. `CrashController` and the
error template demonstrate error handling; static evidence does not establish
the complete runtime ordering of every framework filter or exception resolver.

### Representative Traces

1. Owner search: `GET /owners` ->
   `OwnerController.processFindForm` -> `addPaginationModel` ->
   `findPaginatedForOwnersLastName` ->
   `OwnerRepository.findByLastNameStartingWith` -> owners list or owner detail.
   The graph resolved repository calls with LSP confidence 0.95; controller and
   repository source corroborated the result and empty/multiple-result paths.
2. Owner creation: `POST /owners/new` -> bean validation ->
   `OwnerController.processCreationForm` -> `OwnerRepository.save` -> redirect
   to `/owners/{id}`. The graph missed the repository save edge, so this flow is
   based on direct controller source and the repository declaration, not a
   graph-only claim.
3. Veterinarian listing: `GET /vets.html` or `GET /vets` -> `VetController` ->
   cached `VetRepository.findAll` -> Thymeleaf page or serialized `Vets` model.

## 5. Persistence Model and Transaction Boundaries

JPA entities derive identifiers from `BaseEntity`, which uses identity-generated
integer IDs. Owners aggregate pets with cascade-all and eager fetching; pets
aggregate visits. SQL scripts initialize equivalent H2, MySQL, and PostgreSQL
schemas/data. `spring.jpa.hibernate.ddl-auto=none` makes repository SQL assets
authoritative for initialization. Explicit read-only transactions are declared
on veterinarian repository queries; other Spring Data repository writes rely on
framework repository transaction semantics, so exact runtime commit outcomes are
unknown from static evidence.

## 6. Integration Points

| Integration | Mechanism | Consumer | Usage Status | Confidence | Evidence |
|---|---|---|---|---|---|
| H2 | in-memory JDBC profile and SQL initialization | default application | Wired | Verified | `application.properties`, `db/h2/` |
| MySQL | JDBC driver, profile, Docker Compose/Testcontainers | mysql profile and tests | Configured-only | Verified | `application-mysql.properties`, `docker-compose.yml`, `MySqlIntegrationTests.java` |
| PostgreSQL | JDBC driver, profile, Docker Compose | postgres profile and tests | Configured-only | Verified | `application-postgres.properties`, `docker-compose.yml`, `PostgresIntegrationTests.java` |
| Browser clients | Spring MVC HTML forms and Thymeleaf | owners, pets, visits, vets | Wired | Corroborated | controllers and `templates/` |
| Actuator | HTTP management endpoints | development/testing operators | Wired | Verified | `pom.xml`, `application.properties` |

## 7. Security Model

No Spring Security dependency or application authentication/authorization code
was observed in `pom.xml` and the verified production Java scope. Treat the
sample as unauthenticated unless deployment adds controls outside this
repository. Bean Validation protects form fields, but it is not an authorization
boundary. All actuator endpoints are exposed by the default properties with an
explicit development/testing warning.

## 8. Testing Strategy

Controller tests use `@WebMvcTest`; persistence tests use `@DataJpaTest`; full
application tests use `@SpringBootTest`. MySQL integration tests use
Testcontainers and are disabled when Docker is unavailable; PostgreSQL tests
enable Docker Compose. The Maven build binds formatting, Checkstyle/nohttp,
tests, and JaCoCo reporting, while CI runs `./mvnw -B verify` on Java 17.

## 9. Coding and Repository Modification Conventions

Keep domain code in its feature package, shared entity identity/name behavior in
`model`, and cross-cutting web configuration in `system`. Use constructor
injection, Jakarta validation annotations on form-backed entities, MVC slice
tests for controllers, and JPA/full integration tests for persistence behavior.
Changes must satisfy Spring Java Format, Checkstyle/nohttp, and the repository's
DCO requirement.

## 10. Operational Constraints and Automation

Java 17+ is required. The default application runs on port 8080 with an
in-memory H2 database. MySQL and PostgreSQL require the matching active profile
and an external database, available through Docker Compose. Spring Boot can
build an OCI image without a repository Dockerfile. GitHub Actions validates
Maven and Gradle builds and contains a cluster deployment/test workflow.

## 11. Known Risks and Technical Debt

| Finding | Impact | Confidence | Evidence | Recommendation |
|---|---|---|---|---|
| Default config exposes all actuator endpoints | Sensitive management data/actions may be reachable if reused outside development | Verified | `src/main/resources/application.properties` | Restrict exposure and add authentication in any non-sample deployment |
| Compose files contain sample database credentials | Copying them into a real environment would create weak credentials | Verified | `docker-compose.yml` | Keep sample-only and inject secrets for deployed environments |
| SQL files have reported partial parser ranges | Graph-only schema conclusions may be incomplete | Verified | `index_status` generation `2026-08-25T23:28:19Z` | Read SQL directly for schema or migration changes |

## 12. Build, Test, Quality, and Run Commands

| Purpose | Command | Preconditions | Evidence |
|---|---|---|---|
| Verify Maven build | `./mvnw -B verify` | Java 17+ | `.github/workflows/maven-build.yml` |
| Run application | `./mvnw spring-boot:run` | Java 17+ | `README.md` |
| Build OCI image | `./mvnw spring-boot:build-image` | Docker daemon | `README.md` |
| Start MySQL | `docker compose up mysql` | Docker Compose | `README.md`, `docker-compose.yml` |
| Start PostgreSQL | `docker compose up postgres` | Docker Compose | `README.md`, `docker-compose.yml` |
| Rebuild CSS | `./mvnw package -P css` | Java 17+ | `README.md`, `pom.xml` |

## 13. Evidence and Coverage Limitations

The fresh, non-persistent full index was
`private-tmp-spec-kit-field-validation-spring-petclinic`, status `ready`, with
2,076 nodes and 4,385 edges. Exact checks across the POM, README, Compose, Maven
CI, application profiles, bootstrap, representative controller/repository/entity,
and controller tests, plus bounded production/test Java scopes, reported no
recorded issue with matching generation metadata. This remains a best-effort
signal. Seven files had partial parser ranges, including H2/PostgreSQL schema
and PostgreSQL data SQL; those material files were read directly. Static
analysis cannot prove active profiles, database availability, request frequency,
authorization added by an external platform, or successful transactions. The
generator did not execute builds, tests, containers, or the application.

<!-- PROJECT OVERRIDES START -->
## 14. Project Overrides

> Human-maintained and preserved verbatim. The generator does not validate this
> section or use it to raise the confidence of generated findings.

<!-- PROJECT OVERRIDES END -->
