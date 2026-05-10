---
id: integration-02-chat-agents
title: "Tích hợp MRM với AI Chat Agents"
status: final
tags: [integration, chatgpt, claude, gemini, chat]
summary: "Hướng dẫn cài đặt MRM skill vào ChatGPT, Claude và Gemini qua Custom Instructions."
ai_context: "Dùng khi người dùng muốn dùng MRM qua giao diện chat thông thường. Không cần cài đặt gì ngoài copy system prompt."
---

# Tích hợp MRM với AI Chat Agents

> **TL;DR**: Paste nội dung SKILL.md vào Custom Instructions của ChatGPT/Claude/Gemini để bắt đầu.

## Bước 1 — Cài Custom Instructions

**ChatGPT:**
1. Vào `Settings` → `Custom Instructions`
2. Paste nội dung `mrm-toolkit/skills/modular-research-doc-writer/SKILL.md`
3. Thêm dòng đầu: `You are ModularResearchDocWriter, follow MRM framework strictly.`

**Claude:**
1. Tạo conversation mới
2. Paste toàn bộ SKILL.md vào message đầu tiên
3. Lưu làm template: "MRM Document Writer"

**Gemini:**
1. Vào `Settings` → `Custom instructions`
2. Thêm MRM skill vào phần working style

## Bước 2 — Prompt khởi tạo dự án

```markdown
Áp dụng ModularResearchDocWriter.
Chủ đề: [topic]
Domain: [domain]
Type: [research_paper | tech_doc | internal_wiki | lab_log]
Depth: [executive | standard | deep_dive]
Audience: [audience]
Downstream AI task: [summary | slides | extraction | critique]

Hãy trả về: Scope Analysis, Proposed Tree, File Plan,
MRM Files, Index Draft, Validation Report, Next Actions.
```

## Bước 3 — Template prompts hay dùng

| Tác vụ | Prompt |
|--------|--------|
| Khởi tạo tree | `Tạo cấu trúc MRM cho [topic]. Đề xuất 5-7 core modules, mỗi module ≤300 dòng.` |
| Viết file đơn | `Viết file MRM với id: core-05-[topic]. Cross-ref đến: [[core-01]], [[core-03]].` |
| Review | `Review file [path.md] theo checklist MRM. Chỉ ra vi phạm và đề xuất sửa.` |
| Assemble | `Ghép tất cả files trong research/core/ thành báo cáo. Thêm transition paragraphs.` |

> [!AI-NOTE]
> Khi hướng dẫn người dùng dùng AI Chat, nhấn mạnh rằng validation tự động
> (mrm_validator.py) chỉ chạy được khi có filesystem access. Trong chat-only,
> agent tự checklist theo QUALITY-RUBRIC.md.
