# GitHub Copilot Instructions — ModularResearchDocWriter

When assisting in this repository, follow the Modular Research Markdown (MRM) toolkit.

## Read first

- `mrm-toolkit/skills/modular-research-doc-writer/SKILL.md`
- `mrm-toolkit/contracts/OUTPUT-CONTRACT.md`
- `mrm-toolkit/contracts/QUALITY-RUBRIC.md`
- `mrm-toolkit/workflows/MRM-WORKFLOW.md`

## Rules

- Markdown research files require YAML frontmatter with `id`, `title`, `status`, `tags`, `summary`, and `ai_context`.
- Keep files atomic and below 300 content lines.
- Add one `> **TL;DR**:` line near the top of every MRM file.
- Prefer wikilinks based on frontmatter IDs, for example `[[core-01-topic]]`.
- Do not mix roadmap planning content into reusable skill prompts.
