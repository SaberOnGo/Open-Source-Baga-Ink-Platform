# Baga Ink License History

## Current default

For Baga-authored Platform/OEM-side software first published after the licensing cutover, the repository default is the **PolyForm Noncommercial License 1.0.0** unless a file or directory explicitly states another license.

See:

- `LICENSE`
- `docs/en/governance/02_baga-ink-licensing-policy.md`
- `COMMERCIAL_LICENSE.md`

## Historical Apache-2.0 releases

Before the licensing cutover, Baga-authored repository material was published under the Apache License 2.0 unless otherwise stated.

The final `main` commit before the licensing-model cutover is:

```text
3517970a221dd2e40d8931e1f68399032c343789
```

Recipients who obtained Baga-authored material under Apache-2.0 retain the rights already granted for those historical versions. The project does not claim that changing the repository's current default license retroactively withdraws an already granted Apache-2.0 license.

The historical Apache-2.0 `LICENSE` text remains available through Git history at that revision.

## File-specific and third-party licenses

A file or directory carrying an explicit license notice overrides the repository default for that material.

Third-party code and assets always retain their upstream copyright and license terms. The Baga licensing cutover does not relicense any third-party component.

## Why the model changed

Baga Ink is intended to remain easy to use for individuals, researchers, educators, hobbyists, and ordinary App developers while preserving a sustainable commercial model for OEM/device/platform deployments.

The current policy therefore separates:

```text
community / noncommercial Platform use
commercial OEM/platform licensing
permissively licensed App-facing examples/SDK where published
proprietary LifeBook product code
third-party upstream software
```

For the canonical policy, use `docs/en/governance/02_baga-ink-licensing-policy.md` rather than inferring current terms from old commits.
