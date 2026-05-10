---
id: integration-05-cursor
title: "Tích hợp MRM với Cursor IDE"
status: final
tags: [integration, cursor, rules, mdc]
summary: "Cấu hình Cursor IDE rules và commands để MRM tự động áp dụng khi edit file Markdown."
ai_context: "Dùng khi người dùng dùng Cursor IDE. File mrm.mdc trong adapters/ đã sẵn sàng — chỉ cần install-adapter."
---

# Tích hợp MRM với Cursor IDE

> **TL;DR**: Chạy `install-adapter cursor` để cài rule tự động, hoặc copy `adapters/cursor/mrm.mdc` vào `.cursor/rules/`.

## Cài đặt nhanh qua CLI

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter cursor /path/to/project
```

Tạo `.cursor/rules/mrm.mdc` trong project đích với nội dung từ `adapters/cursor/mrm.mdc`.

## Cấu hình thủ công — `.cursor/rules/mrm.mdc`

```markdown
---
description: ModularResearchDocWriter rules for MRM projects
globs: ["**/*.md", "**/*.mdx"]
alwaysApply: false
---

# Cursor Rule — ModularResearchDocWriter

- Load mrm-toolkit/skills/modular-research-doc-writer/SKILL.md
- Follow mrm-toolkit/contracts/OUTPUT-CONTRACT.md
- Review with mrm-toolkit/contracts/QUALITY-RUBRIC.md
- Keep one topic per file, stay under 300 content lines
- Require MRM frontmatter: id, title, status, tags, summary, ai_context
- Include a one-line TL;DR after the H1
```

## Composer Mode

Dùng `Cmd/Ctrl+K` với prompt:

```
@workspace Tạo project MRM hoàn chỉnh cho chủ đề: [Your Topic]

Requirements:
- 5-7 core modules, mỗi module ≤300 dòng
- Full frontmatter, cross-references chuẩn
- Auto-generated index

Output: Full directory tree + content for each file
```

> [!AI-NOTE]
> `alwaysApply: false` trong mrm.mdc có nghĩa rule chỉ kích hoạt khi edit
> file .md hoặc .mdx — không ảnh hưởng code files.
