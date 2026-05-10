# Generic Agent IDE Rules — ModularResearchDocWriter

Copy or symlink this file into the instruction location of any agent IDE that does not have a dedicated adapter.

## Minimal rules

1. Read `mrm-toolkit/skills/modular-research-doc-writer/SKILL.md`.
2. Follow `mrm-toolkit/workflows/MRM-WORKFLOW.md`.
3. Produce outputs matching `mrm-toolkit/contracts/OUTPUT-CONTRACT.md`.
4. Self-review with `mrm-toolkit/contracts/QUALITY-RUBRIC.md`.
5. Validate local files with `mrm-toolkit/scripts/mrm_validator.py` when possible.

## MRM invariants

- One file equals one topic.
- Frontmatter is mandatory.
- TL;DR is mandatory.
- `ai_context` must state downstream task and anti-hallucination constraints.
- Roadmaps and temporary plans belong in `docs/`, not inside reusable skills.
