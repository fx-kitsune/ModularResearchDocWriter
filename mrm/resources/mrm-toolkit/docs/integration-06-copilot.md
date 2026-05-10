---
id: integration-06-copilot
title: "Tích hợp MRM với GitHub Copilot"
status: final
tags: [integration, copilot, github, workspace]
summary: "Cài GitHub Copilot instructions để Copilot Chat hiểu và tuân thủ chuẩn MRM trong repository."
ai_context: "Dùng khi người dùng muốn Copilot Chat tự động theo chuẩn MRM. File copilot-instructions.md được đặt trong .github/ để áp dụng cho toàn repo."
---

# Tích hợp MRM với GitHub Copilot

> **TL;DR**: Chạy `install-adapter copilot` để tạo `.github/copilot-instructions.md` cho repo.

## Cài đặt nhanh qua CLI

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter copilot /path/to/project
```

Tạo `.github/copilot-instructions.md` từ `adapters/copilot/copilot-instructions.md`.

## Nội dung copilot-instructions.md

```markdown
# GitHub Copilot Instructions — ModularResearchDocWriter

When assisting in this repository, follow the MRM toolkit.

## Read first
- mrm-toolkit/skills/modular-research-doc-writer/SKILL.md
- mrm-toolkit/contracts/OUTPUT-CONTRACT.md
- mrm-toolkit/contracts/QUALITY-RUBRIC.md
- mrm-toolkit/workflows/MRM-WORKFLOW.md

## Rules
- Markdown research files require YAML frontmatter with id, title,
  status, tags, summary, and ai_context.
- Keep files atomic and below 300 content lines.
- Add one > **TL;DR**: line near the top of every MRM file.
- Prefer wikilinks based on frontmatter IDs: [[core-01-topic]]
```

## Sử dụng trong Copilot Chat

```
@workspace Tạo cấu trúc MRM cho research paper về Transformer models

@workspace Review file research/core/core-03-attention.md theo chuẩn MRM

@workspace Generate index.md cho toàn bộ research/ folder
```

> [!AI-NOTE]
> `.github/copilot-instructions.md` áp dụng cho toàn bộ repository và tất cả
> thành viên dùng Copilot Chat — đây là cách hiệu quả nhất để đồng bộ chuẩn
> MRM trong team mà không cần mỗi người tự cấu hình.
