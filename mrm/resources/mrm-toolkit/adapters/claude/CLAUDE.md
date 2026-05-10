# Claude Code Instructions — ModularResearchDocWriter

Use this file as project-root `CLAUDE.md` for Claude Code.

## Project memory

ModularResearchDocWriter is a toolkit for creating Modular Research Markdown (MRM): atomic Markdown files with explicit AI context, validation, indexing, and assembly.

## Required context files

Read these before large documentation tasks:

- `mrm-toolkit/manifest.yaml`
- `mrm-toolkit/skills/modular-research-doc-writer/SKILL.md`
- `mrm-toolkit/workflows/MRM-WORKFLOW.md`
- `mrm-toolkit/contracts/OUTPUT-CONTRACT.md`
- `mrm-toolkit/contracts/QUALITY-RUBRIC.md`

## Working style

- Think in phases: scope, tree, file plan, author, index, validate, assemble.
- Keep plans separate from reusable skill instructions.
- Ask for clarification only when missing scope would change the tree or claims.
- Mark unsourced claims as assumptions rather than inventing citations.
- Validate local MRM trees with `python mrm-toolkit/scripts/mrm_validator.py validate <research_dir>`.
