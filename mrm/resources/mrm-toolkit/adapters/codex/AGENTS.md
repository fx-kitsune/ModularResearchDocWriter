# Codex Instructions — ModularResearchDocWriter

Use this file as the project-root `AGENTS.md` when enabling MRM in an OpenAI Codex workspace.

## Scope

These instructions apply to Markdown research/documentation files in this repository unless a deeper `AGENTS.md` overrides them.

## Load order

1. Read `mrm-toolkit/manifest.yaml`.
2. Read `mrm-toolkit/skills/modular-research-doc-writer/SKILL.md`.
3. Follow `mrm-toolkit/workflows/MRM-WORKFLOW.md`.
4. Enforce `mrm-toolkit/contracts/OUTPUT-CONTRACT.md` and `mrm-toolkit/contracts/QUALITY-RUBRIC.md`.

## Codex behavior

- Before editing many files, present a concise plan and target tree.
- Keep skill instructions stable; put temporary implementation plans in `docs/` or issues.
- Use `rg --files` or targeted file reads to inspect repositories.
- When changing MRM files, run validation if Python is available:
  `python mrm-toolkit/scripts/mrm_validator.py validate <research_dir>`.
- Commit only coherent toolkit or document changes.

## MRM authoring rules

- Every MRM file must include `id`, `title`, `status`, `tags`, `summary`, and `ai_context`.
- Every MRM file must include one H1 matching `title` and one `> **TL;DR**:` line.
- Keep each file to one topic and under 300 content lines.
- Use `[[frontmatter-id]]` or verified Markdown links for references.
