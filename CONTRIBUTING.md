# Contributing to Baga Ink

Thanks for contributing to Baga Ink. The project is designed for long-term collaboration across device vendors, operating systems, languages, and human/AI contributors.

**简体中文:** [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md)

## Before you start

Read:

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/README.md`](docs/README.md)
3. the relevant Standards / Design / Reference App documents for your work

During the documentation migration, use [`docs/localization/catalog.json`](docs/localization/catalog.json) to resolve the current location of a public document.

## Branch and PR workflow

`main` is protected. Work should follow:

```text
main
  ↓
short-lived feature/task branch
  ↓
implementation + tests + documentation
  ↓
Pull Request
  ↓
required CI checks
  ↓
merge to main
```

Do not use permanent feature branches as project memory.

## Documentation languages

Public long-lived prose is localized under:

```text
docs/en/
docs/zh-CN/
```

Public categories are Standards, Design, Reference Apps, Governance, and Status.

English filenames use:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese filenames use:

```text
NN_中文名称.md
```

Do not add new public docs to the legacy mixed-language directories.

Engineering plans under `docs/plans/` are working material and are not required to duplicate every Task or AI execution prompt across languages.

## Code and machine interfaces

Use English for source identifiers, comments/docstrings, public API names, schema keys/IDs, machine error codes, CLI commands/flags, test names, dependency manifests, and commit subjects.

Do not translate stable technical identifiers into incompatible names.

## Required checks

Before submitting documentation/plan changes, run as applicable:

```bash
python3 tools/check_docs_i18n.py
python3 tools/check_platform_port_plans.py
```

For new public localized documents, prefer:

```bash
python3 tools/new_localized_doc.py ...
```

For Platform Port Task / execution prompt scaffolding, prefer:

```bash
python3 tools/new_platform_port_task.py ...
```

Do not weaken a validator merely to make an invalid structure pass.

## Architecture changes

If implementation evidence requires changing an approved Standard, Design, or Architecture Freeze, update the governing document first (or in the same reviewed change) rather than silently changing the architecture in code.

## Completion

A feature is not complete only because it compiles. Run the relevant tests, record device/conformance evidence where required, and update the current Project Status when a meaningful milestone changes.
