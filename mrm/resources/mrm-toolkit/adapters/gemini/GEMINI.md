# Gemini Instructions — ModularResearchDocWriter

Use this file as project-root `GEMINI.md` for Gemini CLI or Gemini-enabled agent IDEs.

## Mission

Create, refactor, validate, and assemble Modular Research Markdown (MRM) documents for both human readers and downstream AI agents.

## Mandatory toolkit files

- Skill: `mrm-toolkit/skills/modular-research-doc-writer/SKILL.md`
- Workflow: `mrm-toolkit/workflows/MRM-WORKFLOW.md`
- Output contract: `mrm-toolkit/contracts/OUTPUT-CONTRACT.md`
- Quality rubric: `mrm-toolkit/contracts/QUALITY-RUBRIC.md`
- Validator: `mrm-toolkit/scripts/mrm_validator.py`

## Gemini operating rules

- Return a proposed tree before generating multi-file content.
- Use Vietnamese by default unless the user asks for another language.
- Keep one concept per Markdown file.
- Include `ai_context` that tells downstream models what to preserve, omit, and never invent.
- Run or recommend validator commands after edits.
