---
id: integration-01-overview
title: "Tích hợp MRM — Tổng quan Kiến trúc"
status: final
tags: [integration, architecture, mrm, overview]
summary: "Tổng quan các phương thức tích hợp MRM toolkit vào IDE và AI agents, kèm so sánh ưu nhược điểm."
ai_context: "Dùng để định hướng người dùng chọn phương thức tích hợp phù hợp. Cross-ref đến các file integration-XX để biết chi tiết từng phương thức."
---

# Tích hợp MRM — Tổng quan Kiến trúc

> **TL;DR**: MRM toolkit hỗ trợ 6 phương thức tích hợp từ AI Chat đơn giản đến Custom Agent API đầy đủ tự động hóa.

## Kiến trúc tích hợp

```
┌─────────────────────────────────────────────┐
│                USER WORKFLOW                │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   VS Code    │  │   Obsidian   │  │    Cursor    │
│   + Copilot  │  │   + LLM      │  │     IDE      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       └─────────────────┼─────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   MRM System Prompt    │
            │ (ModularResearchDoc    │
            │   Writer Skill)        │
            └───────────┬────────────┘
                        │
                        ▼
            ┌────────────────────────┐
            │   AI Agent / LLM API   │
            │  (GPT-4, Claude, ...)  │
            └───────────┬────────────┘
                        │
                        ▼
           ┌────────────────────────┐
           │   Output: MRM Files    │
           │  research/*.md         │
           │  index.md              │
           └───────────┬────────────┘
                       │
                       ▼
           ┌────────────────────────┐
           │   Git + CI/CD Pipeline │
           │  Auto validate/assemble│
           └────────────────────────┘
```

## So sánh phương thức tích hợp

| Phương thức | Độ khó | Flexibility | Automation | Phù hợp cho |
|-------------|--------|-------------|------------|-------------|
| ChatGPT/Claude | Dễ | Trung bình | Thấp | Cá nhân, quick tasks |
| VS Code + Copilot | Trung bình | Cao | Trung bình | Developers, tech writers |
| Obsidian | Trung bình | Rất cao | Cao | Researchers |
| Cursor IDE | Dễ | Cao | Cao | AI-native developers |
| Custom Agent API | Khó | Tối đa | Tối đa | Production pipelines |
| GitHub Actions | Trung bình | Trung bình | Tự động | Team collaboration |

## Quick Start Checklist

- [ ] Copy system prompt vào AI agent ưa thích
- [ ] Cài extensions/plugins cần thiết cho IDE
- [ ] Tạo templates với snippets
- [ ] Setup git hooks cho auto-validation
- [ ] Cấu hình CI/CD pipeline
- [ ] Test workflow với 1-2 files mẫu

## Tài liệu chi tiết

- [[integration-02-chat-agents]] — AI Chat Agents (ChatGPT, Claude, Gemini)
- [[integration-03-vscode]] — VS Code + Extensions + Copilot
- [[integration-04-obsidian]] — Obsidian + Templater + Dataview
- [[integration-05-cursor]] — Cursor IDE rules & commands
- [[integration-06-copilot]] — GitHub Copilot Workspace
- [[integration-07-custom-agent]] — Custom Agent API (Python)
- [[integration-08-cicd]] — Git Hooks & GitHub Actions CI/CD
- [[integration-09-best-practices]] — Best Practices & Troubleshooting
