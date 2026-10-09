---
schema_version: "2.0"
generator: "speckit.codebase-memory"
analysis_profiles:
  - generic
  - spring-boot-jpa
  - maven
  - gradle
source_commit: "500158f732419217507c7656904b8e6aa1bcc0d6"
working_tree: "tracked application source unchanged; untracked Spec Kit metadata present"
evidence_tier: "verify"
---

# Spring Petclinic Codebase Context

> Generated from current repository evidence using direct file reads and bounded
> searches. Inferred or unknown conclusions are identified. Paths are relative
> to the repository root. No graph backend was used.

## 1. Architecture Overview and Module Map

### System Purpose and Technology Stack

Verified: this repository implements a veterinary clinic sample: owners have
pets, pets have visits, and veterinarians have specialties. The primary user
interface is Spring MVC with server-rendered Thymeleaf views, not a separate
frontend SPA. `pom.xml` and `build.gradle` both declare Spring Boot 4.1.0 and
Java 17; the project artifact is `spring-petclinic` 4.0.0-SNAPSHOT. This is
repository-declared configuration, not a successful build result.

The build manifests declare JPA, validation, web MVC, Thymeleaf, caching, and
actuator dependencies. H2, MySQL, PostgreSQL, Caffeine, and WebJars dependencies
are present. Java packages import `jakarta.persistence` and `jakarta.validation`.
Frontend assets include Bootstrap 5.3.8, Font Awesome 4.7.0, and local CSS, while
localization files live under `src/main/resources/messages`. Maven and Gradle
both exist; neither build is executed during context generation.

### Module Layout and Boundaries

This is one application module. `src/main/java/org/springframework/samples/petclinic`
is the production package root. Its `model` package provides `BaseEntity`,
`NamedEntity`, and `Person`. The `owner` package owns Owner, Pet, Visit, PetType,
repositories, formatters, validators, and their controllers. The `vet` package
contains Vet, Specialty, the Vets response container, repository, and controller.
The `system` package handles welcome/error demonstrations, localization, and
cache configuration. `PetClinicApplication` and `PetClinicRuntimeHints` are
application-level bootstrap and native-image hint mechanisms.

The inspected controllers depend directly on repository interfaces, rather
than a separate application service layer. Owner owns a pet collection; Pet
owns visit objects. Shared model types have no controller dependency. MVC
controllers return view names backed by `src/main/resources/templates`, with
forms reusing `templates/fragments`. The `/vets` response is a distinct
object-serialization boundary. Source conventions cannot prove all framework
runtime call edges or the precise order of infrastructure outside the checkout.

`src/main/resources/db/{h2,mysql,postgres}` contains dialect-specific schema and
sample data. Main application properties select these resources. Tests are in
`src/test/java`, largely mirroring owner, vet, model, and system areas.
`src/checkstyle` provides no-HTTP checks. `.github/workflows/maven-build.yml` and
`gradle-build.yml` define CI build entry points. Kubernetes deployment material
is in `k8s`; secret objects or their values are outside this analysis scope.

### Entry Points and Code Anchors

`PetClinicApplication.main` invokes `SpringApplication.run` and has
`@SpringBootApplication` plus `@ImportRuntimeHints(PetClinicRuntimeHints.class)`.
`OwnerController` registers owner create, find, edit, and detail routes.
`PetController` registers pet forms beneath `/owners/{ownerId}`.
`VisitController` registers visit creation beneath owner and pet identifiers.
`VetController.showVetList` serves `/vets.html`, whereas
`showResourcesVetList` serves `/vets`. `CrashController.triggerException`
registers `/oups` as an intentional exception demonstration.

`PetClinicIntegrationTests.main` is a development/test application entry point,
not a second production service. Native resource/reflection requirements are
registered in `PetClinicRuntimeHints.registerHints`.

## 2. Core Flows and Interface Boundaries

### Request Pipeline and Middleware

Verified local wiring: MVC discovers annotated controllers; their constructors
receive repository dependencies. `WebConfiguration.addInterceptors` registers
`LocaleChangeInterceptor`, whose `lang` parameter selects language.
`localeResolver` creates a session locale resolver with English as default.
A session here is evidence of locale persistence, not user authentication.
Framework dispatcher/filter order is outside the directly inspected source.

Owner and visit binders disallow `id` and nested `*.id` fields. Pet binding
installs `PetValidator`. Form handlers use `@Valid`, BindingResult, view names,
and redirect flash messages. `CrashController` throws deliberately and
`templates/error.html` supplies an error view; a project-wide REST error
response envelope was not established by the inspected MVC sources.

### Security and Trust Boundaries

Verified: form binding limits and validation exist. Controllers expose path
identifiers and request parameters, so ownership lookup and ID matching are
relevant change boundaries. `OwnerController.processUpdateOwnerForm` checks the
form owner ID against the URL before saving. Pet and visit handling resolve
pets through an Owner. These are data-integrity mechanisms, not proof of
access control for an authenticated principal.

Bounded searches of production Java and both manifests did not find an explicit
SecurityFilterChain, EnableWebSecurity, or declared Spring Security dependency.
Authentication, CSRF enforcement, tenant isolation, deployment ingress policy,
and authorization are therefore not observed in verified scope; no runtime
security guarantee is made. `application.properties` configures broad actuator
web exposure; deployment protection remains unknown. Datasource credential
keys were observed with values redacted and must not be copied into context.

### Representative Traces

1. Owner search: `/owners` binds the requested page and last name;
   `OwnerController.processFindForm` normalizes absent/whitespace last names,
   calls `findPaginatedForOwnersLastName`, and uses
   `OwnerRepository.findByLastNameStartingWith`. Invalid requested pages redirect
   to page 1, preserving a nonempty search term. An empty result rejects the
   lastName field and returns the find form. One result redirects to detail;
   multiple results populate pagination attributes and render the owner list.
   The page size is five in the inspected helper.
2. New pet: `PetController` resolves the Owner and available PetTypes. The pet
   binder applies `PetValidator`. `processCreationForm` checks duplicate names
   against existing owner pets and rejects future birth dates. Validation
   failures return the pet form. Otherwise `Owner.addPet` and
   `OwnerRepository.saveAndFlush` persist the aggregate. A duplicate-name
   integrity exception is converted to a form error; unrelated integrity
   exceptions are propagated. Success flashes a message and redirects to owner
   detail. This is source order; transaction commit success was not observed.
3. Visit booking: `VisitController.loadPetWithVisit` resolves the owner and pet,
   fails for missing identifiers, adds model attributes, and creates a Visit.
   `minVisitDate` and the Visit constructor use tomorrow as the minimum/default.
   The POST handler rejects today or earlier, returns the form on errors,
   otherwise adds the visit through Owner and saves the Owner aggregate.
4. Vet listing: `/vets.html` creates a safe pageable request, invokes the
   paged VetRepository method, redirects invalid pages, and renders pagination
   attributes. `/vets` invokes the collection repository method, fills a Vets
   wrapper, and returns a response body. Both repository reads declare
   `@Transactional(readOnly = true)` and `@Cacheable("vets")`. Their annotations
   show intended proxy behavior; runtime cache hits and provider selection were
   not measured.

### External Integrations

H2 is the default database selection in `application.properties`. MySQL and
PostgreSQL are configured in profile-specific properties, with environment
placeholder inputs for connection settings. They are configured alternatives,
not confirmed running external services. Test source includes MySQL
Testcontainers and PostgreSQL integration setup; neither was started here.
Caching is wired through `CacheConfiguration` and VetRepository, while the
actual selected cache provider at runtime is unknown. External HTTP business
clients, messaging consumers, and scheduled production jobs were not observed
in bounded production Java inspection. Deployment manifests reference an image
and PostgreSQL profile, not evidence of a healthy deployment.

## 3. Data Persistence and Storage Model

### Storage and Entity Conventions

`BaseEntity` is a mapped superclass with an Integer identity-generated ID;
`isNew` means the ID is null. `NamedEntity` adds a nonblank name. `Person` adds
nonblank first/last names limited to 30 characters. Owner extends Person;
Pet extends NamedEntity; Visit extends BaseEntity. Owner address and city are
nonblank with maximum lengths 255 and 80. Telephone is constrained to ten digits.

Owner's pets use eager one-to-many cascading, join column `owner_id`, and name
ordering. Pet's visits also use eager cascading with `pet_id` and date ordering.
PetType is a many-to-one relation. `Owner.addPet` avoids inserting the same
object or an already-associated persisted identifier twice. Its name lookup is
case-insensitive and permits excluding new pets for duplicate checks.

The H2 schema gives pet names a case-insensitive column and a unique
`(owner_id, name)` constraint. This corroborates the duplicate form check while
providing a separate database enforcement boundary. Other dialect SQL must be
reviewed before assuming identical collation or constraint semantics. Auditing,
soft-delete, and tenant fields were not observed in the inspected model types;
this is a scoped finding, not an exhaustive database analysis.

### Transactions and Schema Migrations

VetRepository methods explicitly declare read-only transactions. OwnerRepository
extends JpaRepository and exposes derived owner search plus Optional lookup;
CRUD transaction implementation is external framework code. Controller
operations should not be described as an application-level multi-step
transaction without further evidence.

Application properties set Hibernate DDL generation to none, disable
open-in-view, and select schema/data SQL by the database key. The inspected
H2 schema contains destructive drop/create statements, fitting a sample reset
workflow rather than versioned production migration. Profile SQL initialization
is configured for MySQL/PostgreSQL. Flyway and Liquibase were not observed in
bounded manifest/production-source searches. Framework startup behavior and
active profile need runtime verification before any migration operation.

## 4. Development Conventions and Validation Commands

### Coding and Design Patterns

The inspected implementation uses constructor injection, package-scoped MVC
controllers, public entities/repository interfaces, and field constraints on
models. Tabs and Spring Java Format conventions are visible in representative
source and are enforced by Maven validation. Repository-specific structure
should guide modifications; adding generic controllers/services/DTO layers
would require an intentional architectural decision.

Validation combines Bean Validation on Owner/Person/Visit with a dedicated
PetValidator installed by the PetController binder. PetValidator currently
requires text in the name, limits names to 30 characters, requires type for new
pets, and requires a birth date. Temporal checks and duplicate-name logic are
currently in PetController. Error codes are passed through BindingResult,
with locale messages in resources. Verify the exact error code and handler
integration when extending these rules.

### Modification Anchors and Extension Patterns

For a pet form validation change, inspect `owner/PetValidator.java`,
`owner/PetController.java`, `templates/pets/createOrUpdatePetForm.html`, and
`owner/PetValidatorTests.java` plus `PetControllerTests.java`. Reuse its Errors
and MapBindingResult test pattern; protect birth-date, type, duplicate-name,
and ownership behaviors. A validator-only rule need not introduce a table or
migration unless it changes stored data requirements.

For owner pagination, use `OwnerController.processFindForm`,
`OwnerRepository.findByLastNameStartingWith`, and OwnerControllerTests; preserve
single-result redirects, empty-result errors, and page-reset search terms.
For vet list changes use VetController/VetRepository and VetControllerTests;
protect cache semantics and the HTML/serialized boundary distinction.
Changes to shared IDs or collections require reviewing BaseEntity, Owner, Pet,
SQL for every supported database, and persistence tests together.

### Testing Strategy

PetValidatorTests use JUnit Jupiter, MockitoExtension, nested tests, and
MapBindingResult for direct validation without database setup. OwnerControllerTests
use `@WebMvcTest`, MockMvc, and `@MockitoBean OwnerRepository` with explicit
model/view/redirect assertions. Several tests disable native/AOT execution;
that is a declared test scope, not proof of native behavior.
PetClinicIntegrationTests run a random-port Spring Boot application and make
HTTP assertions; other integration fixtures exercise database alternatives.
Some full suites may require Docker or local networking. Definitions show
intended checks; this generator did not run or claim successful tests.

### Operational Constraints and Packaging

CI uses Java 17 and Maven Wrapper verification or Gradle build. Maven wrapper
configuration selects Maven 3.9.16. Spring Java Format, no-HTTP Checkstyle,
JaCoCo, Spring Boot build-info, Git metadata, native-image tooling, and SBOM
plugins are declared in the Maven build. The CSS profile regenerates committed
CSS and may require additional prerequisites. Runtime and database commands
may access networks or start services and are recorded only.

Kubernetes material exposes application port 8080 and references PostgreSQL
binding through a secret. Secret contents and production configuration are
excluded. The README documents local startup and image creation; current
configuration has not been executed, so deployment readiness remains unknown.

### Validation Commands

| Purpose | Command | Working Directory | Preconditions | Evidence | Execution Status |
|---|---|---|---|---|---|
| Maven build/test/quality | `./mvnw -B verify` | `.` | JDK 17+, wrapper and dependencies; integration prerequisites as applicable | `.github/workflows/maven-build.yml`, `pom.xml` | Not executed (discovered only) |
| Gradle build/test | `./gradlew build` | `.` | Compatible JDK/toolchain, dependencies and integration prerequisites | `.github/workflows/gradle-build.yml`, `build.gradle` | Not executed (discovered only) |
| Local Maven run | `./mvnw spring-boot:run` | `.` | JDK and available dependencies/profile | `README.md` | Not executed (discovered only) |
| Local Gradle run | `./gradlew bootRun` | `.` | Gradle toolchain and dependencies/profile | `README.md` | Not executed (discovered only) |
| Image packaging | `./mvnw spring-boot:build-image` | `.` | JDK, network and Docker daemon | `README.md` | Not executed (discovered only) |
| CSS generation/package | `./mvnw package -P css` | `.` | CSS profile dependencies and tooling | `README.md`, `pom.xml` | Not executed (discovered only) |

## 5. Evidence and Coverage Limitations

Direct inspection covered both manifests, wrappers, Maven/Gradle CI, bootstrap,
shared models, Owner/Pet/Visit controllers and repositories, vet interfaces,
cache and localization configuration, the H2 schema, relevant templates,
representative validator/MVC/integration tests, and redacted application config.
Bounded searches considered transaction, security, middleware, scheduling, and
migration declarations in production Java and both manifests. There is no
graph project, node count, or graph coverage claim.

All cited locations were checked against the current checkout. The tracked
application files were unchanged when synthesis completed. Ignored/generated
build outputs, caches, Git internals, deployment secrets, and credential values
were excluded. Static analysis cannot prove profiles, endpoint availability,
transaction outcomes, framework internals, provider selection, or cache hits.
SQL dialect parity, all message translations, every test assertion, and all
static assets were not exhaustively inspected. Hook configuration was absent,
so there were no registered pre/post generation hooks in this invocation.

<!-- PROJECT OVERRIDES START -->
## 6. Project Overrides

> Human-maintained and preserved verbatim on normal refresh. The generator checks
> ownership, marker structure, and secret safety, but does not verify these notes
> as repository facts or use them to raise confidence in generated findings.

<!-- PROJECT OVERRIDES END -->
