# Publishing readiness — v1.1.0 candidate

Reference: [Spec Kit Preset Publishing Guide](https://github.com/github/spec-kit/blob/main/presets/PUBLISHING.md).
The command baseline is the immutable Spec Kit v1.1.2 tag; the publishing guide
is the current main-branch document reviewed on 2026-10-09.

## Local requirements

- Manifest: schema 1.0, ID `codebase-memory-context`, version `1.1.0`, MIT,
  concise description, four tags, five commands and one output template.
  `THIRD_PARTY_NOTICES.md` retains the upstream Spec Kit copyright and MIT text.
- All declared files exist and resolve with Spec Kit 1.1.2.
- README describes this preset, usage, fit, non-fit, conflicts, and valid
  `specify preset add` commands. Current-checkout installation uses `--dev` with a clean directory from
  `python3 tools/package_preset.py`, not the development checkout.
- Real directory and locally constructed tag-layout ZIP installation are tested.
- All commands render for Codex, Claude, Copilot, and Gemini with all three
  script choices; uninstall restores the four core consumers.
- Command additions reference the six-section schema 2.0 context. Upstream
  portions are preserved outside marked augmentation blocks.
- Historical field-validation artifacts belong to old releases. Current prompt
  checks and backend contracts must not be advertised as LLM execution evidence.

See [the current validation record](validation/v1.1.0.md) and the
[Spring Petclinic field report](validation/petclinic-v1.1.0.md) for observed results.
The [refresh/install follow-up](validation/petclinic-refresh-install.md) records
successful refresh and clean installation under a historical lock-based writing
procedure. That procedure is superseded by ordinary agent editing, a write-time
content comparison and output verification; no concurrency guarantee is made.
See the [simplification record](validation/refresh-simplification.md) for current
verification. Historical lock results must not be presented as current behavior.
These local checks do not establish that a public release exists or that the
catalog has been updated.

## Before publishing

1. Run base tests in the backend-free CI environment and the strict backend
   contract job with the pinned 0.10.8 backend. Record run links/results.
2. Perform and record current-agent field validation on an established repository
   without graph access, then optionally with graph enhancement. Cover creation,
   refresh, override preservation, unowned/malformed targets, source changes,
   excluded paths, hooks, and safe commit availability. Inspect actual outcomes.
   Record incomplete or blocked cases honestly; do not simulate generator logic
   in Python and call that end-to-end validation.
3. Confirm intended release version. Keep the manifest at the candidate version,
   then move the Unreleased changelog into a dated release only at release time.
4. Create/push the tag and release through the maintainer's normal release flow.
   The current repair does not create tags, push, or publish.
5. Download and test the actual hosted archive with `specify preset add --from`,
   inspect `preset info`, all six `preset resolve` results, agent outputs, and
   `preset remove` in a disposable project. The local ZIP test is not this step.
6. Replace README's historical v1.0.2 archive example with the exact verified
   v1.1.0 download URL; ensure it matches the catalog `download_url`.
7. Update the existing entry in `presets/catalog.community.json` and its row in
   `docs/community/presets.md` through an upstream PR. Preserve creation date,
   update modification date, and use five commands/one template. Keep catalog
   entries ordered by ID and the docs table ordered by display name.

## Prepared catalog update

[catalog-entry.v1.1.0.json](catalog-entry.v1.1.0.json) is a draft replacement for
the existing entry, not a submitted or published catalog. It uses the candidate
tag README URL and clean release-asset download URL, which require the release above. No archive
checksum is supplied until the actual hosted archive can be hashed.

Suggested community docs row:

```markdown
| Verified Codebase Context | Generates evidence-qualified repository context with optional graph enhancement for planning, tasks, analysis, and implementation. | 1 templates, 5 commands | — | [spec-kit-preset-codebase-memory-context](https://github.com/philo-x/spec-kit-preset-codebase-memory-context) |
```

A preset README, valid manifest, license, working release, and real-project
validation remain prerequisites for catalog publishing. The repair prepares
local readiness and submission material; external release and catalog checks
remain pending until their evidence exists.

The v1.1.0 catalog draft points to the clean ZIP release asset, rather than the
GitHub source archive: source archives include historical validation logs that
can interfere with host-wide scanners. `.github/workflows/release.yml` builds,
tests, publishes and downloads that asset only when a matching version tag is
pushed. The workflow tests the downloaded archive in a disposable project.

Current hosted CI: [three jobs passed](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/actions/runs/37905447930).
The [completion record](validation/completion.md) lists the candidate validation
branch and release boundary. [catalog-update.v1.1.0.patch](catalog-update.v1.1.0.patch)
is the verified two-file upstream update, dependent on the clean asset publication.
