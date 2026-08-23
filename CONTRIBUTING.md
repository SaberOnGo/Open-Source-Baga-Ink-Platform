# Contributing to Baga Ink

Thanks for contributing to Baga Ink. The project is designed for long-term collaboration across device vendors, operating systems, countries, human languages, and human/AI contributors.

**简体中文:** [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md)

## Before you start

Read:

1. [`README.md`](README.md)
2. [`AGENTS.md`](AGENTS.md) if you are an AI/automation contributor
3. [`docs/en/00_baga-ink-documentation-index.md`](docs/en/00_baga-ink-documentation-index.md)
4. the governing Standard / Design / Reference App / Plan for your work

Use [`docs/localization/catalog.json`](docs/localization/catalog.json) to map stable public Document IDs to maintained locale paths.

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

Public long-lived prose exists only under:

```text
docs/en/
docs/zh-CN/
```

Public categories are Standards, Design, Reference Apps, Governance, and Status.

English filenames:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese filenames:

```text
NN_中文名称.md
```

Do not create legacy mixed-language public directories or ad-hoc locale layouts.

Engineering plans under `docs/plans/` are working material and are not required to duplicate every Task / AI Execution Prompt across locales.

## Code / machine-interface language

Use English for source identifiers, comments/docstrings, public API names, schema keys/IDs, machine error codes, CLI commands/flags, test names, dependency manifests, and commit subjects.

Do not translate stable technical identifiers into incompatible names.

## Required checks

As applicable:

```bash
python3 tools/check_docs_i18n.py
python3 tools/check_readme_languages.py
python3 tools/check_platform_port_plans.py
```

Create new public localized docs with:

```bash
python3 tools/new_localized_doc.py ...
```

Create Platform Port Task / Execution Prompt structures with:

```bash
python3 tools/new_platform_port_task.py ...
```

Do not weaken validators merely to make invalid structure pass.

## Architecture changes

If implementation evidence requires changing an approved Standard, Design, or Architecture Freeze, update the governing decision first or in the same reviewed PR. Do not silently change architecture only in code or an execution prompt.

## License / provenance

Baga-authored material defaults to Apache License 2.0 unless a file/directory says otherwise.

Third-party dependencies retain their upstream licenses. Contributions that add or change a dependency must record enough provenance to understand:

```text
project / source
version or commit
license
where it is used
whether code is bundled / modified / linked / invoked externally
required notices or source obligations
```

See [`LICENSE`](LICENSE), [`NOTICE`](NOTICE), and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

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

A feature is not complete only because it compiles. Run relevant tests, record real-device/conformance evidence where required, and update Project Status when a meaningful milestone changes.
