# MRM Output Contract

This contract defines the stable output shape every agent must produce when using ModularResearchDocWriter.
It separates reusable skill behavior from planning artifacts so Codex, Claude Code, Gemini, and agent IDEs can apply the toolkit consistently.

## 1. Required agent response shape

For every non-trivial documentation task, return these sections in order:

1. **Scope Analysis** — domain, audience, depth, constraints, sources, and unresolved assumptions.
2. **Proposed Tree** — target folder tree before writing content.
3. **File Plan** — table of file IDs, titles, purpose, dependencies, and status.
4. **MRM Files** — each Markdown file using the canonical frontmatter and body structure.
5. **Index Draft** — navigation file or update plan for an existing index.
6. **Validation Report** — checklist results, known risks, and commands to run.
7. **Next Actions** — concise steps for review, source collection, or assembly.

Small edits to a single existing file may return only: scope, changed file, validation report, next actions.

## 2. Canonical MRM file shape

```markdown
---
id: core-01-example
title: "Clear Title"
status: draft
tags: [topic, mrm]
summary: "One or two sentences describing scope and contribution."
ai_context: "Concrete downstream instruction for AI readers. State what to preserve and what not to invent."
---

# Clear Title

> **TL;DR**: One-line decision, claim, or takeaway.

## Scope
- Define the single topic owned by this file.
- List assumptions and boundaries.

## Main Content
- Use bullets and tables for scanability.
- Cross-reference with `[[file-id]]` or verified Markdown links.

> [!AI-NOTE]
> Explain how downstream agents should summarize, extend, translate, critique, or assemble this file.
```

## 3. File naming rules

| Type | Pattern | Example | Purpose |
|---|---|---|---|
| Meta | `meta-XX-topic.md` | `meta-01-project-overview.md` | Scope, assumptions, glossary, sources |
| Core | `core-XX-topic.md` | `core-02-methodology.md` | Primary argument or module |
| Note | `note-YYYY-MM-DD-topic.md` | `note-2026-05-10-interview.md` | Atomic observation or session note |
| Reference | `ref-topic.md` | `ref-bibliography.md` | Bibliography, dataset, appendix |
| Output | `final-report.md` | `final-report.md` | Assembled deliverable |

## 4. Cross-reference rules

- Prefer `[[frontmatter-id]]` for semantic references inside an MRM project.
- Use Markdown links only when the file path exists or is created in the same patch.
- Do not create vague references such as `[[related]]`, `[[todo]]`, or `[[future-file]]`.
- If a target is intentionally missing, place it in the File Plan as `planned` and mark validation risk.

## 5. Refusal and clarification rules

Ask for clarification only when missing information would materially change the tree or claims.
If sources are required but absent, create structure and mark claims as placeholders instead of inventing facts.
