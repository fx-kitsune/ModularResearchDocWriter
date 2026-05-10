# MRM Quickstart Prompts

## Create a new research tree

```markdown
Áp dụng ModularResearchDocWriter.
Chủ đề: [topic]
Domain: [domain]
Type: [research_paper | tech_doc | internal_wiki | lab_log]
Depth: [executive | standard | deep_dive]
Audience: [audience]
Downstream AI task: [summary | slides | extraction | critique]

Hãy trả về: Scope Analysis, Proposed Tree, File Plan, MRM Files, Index Draft, Validation Report, Next Actions.
```

## Refactor an existing monolithic document

```markdown
Áp dụng ModularResearchDocWriter để tách file sau thành MRM atomic modules.
Giữ nguyên claim đã có, không tự thêm số liệu.
Đầu ra gồm tree mới, mapping section cũ → file mới, và checklist validation.
```

## Review one file

```markdown
Review file này theo MRM Quality Rubric.
Chỉ ra lỗi frontmatter, TL;DR, atomicity, cross-reference, line limit, và ai_context.
Đề xuất patch tối thiểu.
```

## Assemble a report

```markdown
Ghép các module MRM đã review thành báo cáo hoàn chỉnh cho [audience].
Giữ source boundary, thêm transition paragraphs, và liệt kê module IDs đã dùng.
```
