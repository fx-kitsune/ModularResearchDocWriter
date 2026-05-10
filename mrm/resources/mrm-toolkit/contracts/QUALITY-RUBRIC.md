# MRM Quality Rubric

Use this rubric as the self-review checklist before an agent returns, commits, or assembles MRM documents.

## Pass/fail gates

| Gate | Pass condition | Failure response |
|---|---|---|
| Atomicity | One file owns one topic and stays under 300 content lines. | Split into child files and update index. |
| Frontmatter | `id`, `title`, `status`, `tags`, `summary`, `ai_context` exist and parse as YAML. | Fix metadata before writing more content. |
| Progressive disclosure | Summary, TL;DR, main content, and optional details appear in that order. | Reorder the file. |
| AI boundary | `ai_context` states downstream task and anti-hallucination constraints. | Rewrite `ai_context` with concrete instructions. |
| Cross-reference integrity | All required references resolve to IDs or paths in the tree. | Add missing files to plan or remove the reference. |
| Readability | Uses short paragraphs, bullets, tables, and active language. | Refactor dense prose. |

## Scoring rubric

| Score | Meaning | Criteria |
|---|---|---|
| 5 | Production-ready | All gates pass, source boundaries clear, index and assembly path ready. |
| 4 | Review-ready | Minor warnings only, no broken structure or missing metadata. |
| 3 | Draft-ready | Usable draft with known gaps listed in validation report. |
| 2 | Needs refactor | Multiple gates fail or files mix unrelated topics. |
| 1 | Unsafe | Missing sources, invented claims, or no AI boundary. |

## Required validation report format

```markdown
## Validation Report
- Atomicity: pass/fail — note
- Frontmatter: pass/fail — note
- TL;DR: pass/fail — note
- Cross-references: pass/fail — note
- Line limits: pass/fail — note
- Source boundaries: pass/fail — note
- Overall score: 1-5
```
