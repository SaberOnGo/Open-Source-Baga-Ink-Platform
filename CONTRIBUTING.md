# Contributing to Baga Ink

Thanks for contributing to Baga Ink. The project is designed for long-term collaboration across device vendors, operating systems, countries, human languages, and human/AI contributors.

**简体中文:** [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md)

## Before you start

Read:

1. [`README.md`](README.md)
2. [`AGENTS.md`](AGENTS.md) if you are an AI/automation contributor
3. [`docs/en/00_baga-ink-documentation-index.md`](docs/en/00_baga-ink-documentation-index.md)
4. [`docs/en/governance/00_baga-ink-development-governance.md`](docs/en/governance/00_baga-ink-development-governance.md)
5. the governing Standard / Design / Reference App / Plan for your work
6. [`docs/en/governance/02_baga-ink-licensing-policy.md`](docs/en/governance/02_baga-ink-licensing-policy.md) when your change adds code, dependencies, SDK output, examples, packaging, or distributable artifacts

Use [`docs/localization/catalog.json`](docs/localization/catalog.json) to map stable localized Document IDs to maintained locale paths.

## Branch / PR workflow

`main` is protected:

```text
main
→ short-lived feature/task branch
→ implementation + tests + docs
→ Pull Request
→ required CI checks
→ merge main
```

Do not use permanent feature branches as project memory.

## Public documentation languages

Long-lived localized prose exists under:

```text
docs/en/
docs/zh-CN/
```

Localized public categories are Standards, Design, Reference Apps, Governance, and Status.

English filenames:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese filenames:

```text
NN_中文名称.md
```

Do not create legacy mixed-language public directories or ad-hoc locale layouts.

Engineering plans under `docs/plans/` are public operational engineering material. They are not required to duplicate every Task / AI Execution Prompt across locales, but they remain public repository documentation.

## Public writing standard

Every tracked documentation file in this public repository is written for external readers. This includes README files, contributor guides, Governance, Standards, Design, Reference Apps, Status, `docs/plans/`, Task Designs, and AI Execution Prompts.

Tracked documentation must:

- state project requirements, decisions, implementation steps, and rationale directly;
- be understandable without private conversation history;
- use language appropriate to its actual public audience;
- keep confidential commercial strategy and private project discussion outside the public repository.

Do not commit private-consultation language such as personal recommendations to the repository owner, references to a previous private conversation, audience-psychology speculation, confidential monetization rationale, negotiation tactics, or unpublished pricing strategy.

Normative instructions to a documented public role are appropriate, for example `Contributor MUST`, `Task MUST`, and `OEM Port SHOULD`.

Confidential material belongs in an ignored local `private/` directory or a separate private repository.

Required check:

```bash
python3 tools/check_public_writing.py
```

## Code / machine-interface language

Use English for source identifiers, comments/docstrings, public API names, schema keys/IDs, machine error codes, CLI commands/flags, test names, dependency manifests, and commit subjects.

Do not translate stable technical identifiers into incompatible names.

## Required checks

As applicable:

```bash
python3 tools/check_docs_i18n.py
python3 tools/check_readme_languages.py
python3 tools/check_platform_port_plans.py
python3 tools/check_licensing.py
python3 tools/check_public_writing.py
```

Create new localized public docs with:

```bash
python3 tools/new_localized_doc.py ...
```

Create Platform Port Task / Execution Prompt structures with:

```bash
python3 tools/new_platform_port_task.py ...
```

Do not weaken validators merely to make invalid structure or content pass.

## Architecture changes

If implementation evidence requires changing an approved Standard, Design, or Architecture Freeze, update the governing decision first or in the same reviewed PR. Do not silently change architecture only in code or an execution prompt.

## License / provenance

Baga Ink applies different licensing policies to different asset classes.

The default for Baga-authored Platform/OEM-side software is the root community license unless a file/directory explicitly states otherwise. App-facing SDK/examples may carry a separate permissive license. LifeBook production code is proprietary and is not part of the public Baga Platform source distribution. Third-party dependencies always retain their upstream licenses.

See:

```text
LICENSE
docs/en/governance/02_baga-ink-licensing-policy.md
COMMERCIAL_LICENSE.md
LICENSE_HISTORY.md
THIRD_PARTY_NOTICES.md
```

A contribution that adds or changes a dependency must record enough provenance to identify:

```text
project / source
version or commit
license
where it is used
whether code is bundled / modified / linked / invoked externally
required notices or source obligations
```

## Contribution rights / future dual licensing

The project supports community use and separately licensed commercial OEM/platform deployments. That model requires sufficient rights to distribute Baga-authored contributions under the applicable community and commercial terms.

By submitting material, you must have the legal right to submit it. Do not copy third-party code into Baga-authored files solely because the code is publicly visible.

External contributions to dual-licensed Baga Platform / Device Adapter code may require a Contributor License Agreement (CLA) before merge. Until a legally reviewed CLA is published and executed, maintainers may defer external code contributions whose license terms are incompatible with the intended distribution model of the target component.

Building and selling an IKP App that targets the documented Baga App APIs is separate from shipping Baga Platform/Adapter code in a commercial device.

## LifeBook boundary

Public LifeBook Reference App documentation validates Baga architecture. The production LifeBook application is proprietary and is not part of this public repository's Platform source distribution.

Do not add proprietary LifeBook product code, backend code, product algorithms, credentials, commercial assets, or private product data to this public repository unless a specific component is intentionally published under a stated license.

## Translations

The root README language switch is governed by:

```text
docs/localization/readme-languages.json
```

To add a new maintained locale:

1. propose the locale through documentation governance;
2. identify maintenance/review ownership;
3. add the locale tree and terminology guidance as needed;
4. register the README translation if provided;
5. update all managed language-switch blocks;
6. extend localization CI/registry rules;
7. do not create an ad-hoc language directory.

A translation is an edition of the same logical document, not permission to create a different protocol or architecture.

## Completion

A feature is not complete solely because it compiles. Run relevant tests, record real-device/conformance evidence where required, verify licensing/provenance for distributable changes, verify the public-writing rule for tracked documentation, and update Project Status when a meaningful milestone changes.
