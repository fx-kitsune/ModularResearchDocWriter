# MRM Agent Workflow

This workflow is the canonical procedure for all adapters. It keeps skills, plans, prompts, and validation responsibilities separate.

## Phase 0 — Load context

1. Read `mrm-toolkit/manifest.yaml` if present.
2. Read `mrm-toolkit/skills/modular-research-doc-writer/SKILL.md` for behavior.
3. Read `mrm-toolkit/contracts/OUTPUT-CONTRACT.md` for output shape.
4. Read `mrm-toolkit/contracts/QUALITY-RUBRIC.md` before final response.
5. Inspect the target project tree and existing MRM files before proposing changes.

## Phase 1 — Scope and plan

- Identify domain, document type, audience, depth, language, source requirements, and downstream AI tasks.
- Propose a tree before writing long content.
- Separate stable files (`meta/`, `core/`, `refs/`) from generated files (`outputs/`).
- Keep roadmap or upgrade tasks in `docs/` or issue trackers, not inside the skill prompt.

## Phase 2 — Author atomic modules

- Write one file per concept.
- Keep content under 300 content lines.
- Use canonical frontmatter and a one-line TL;DR.
- Record assumptions in `meta/` files, not scattered in every core file.
- Add `AI-NOTE` callouts only when they add downstream handling guidance.

## Phase 3 — Link and index

- Use `[[frontmatter-id]]` for MRM internal references.
- Generate or update `index.md` after adding files.
- Avoid references to non-existent files unless the File Plan marks them as planned.

## Phase 4 — Validate

Run the validator when files exist locally:

```bash
python mrm-toolkit/scripts/mrm_validator.py validate mrm-toolkit/research
```

For external projects, use the project-specific research folder:

```bash
python mrm-toolkit/scripts/mrm_validator.py validate <project>/research
```

## Phase 5 — Assemble

Create deliverables from reviewed modules only:

```bash
python mrm-toolkit/scripts/mrm_validator.py assemble <research_dir> <output.md>
```

Include transition paragraphs manually when the target audience needs a narrative report rather than a module dump.
