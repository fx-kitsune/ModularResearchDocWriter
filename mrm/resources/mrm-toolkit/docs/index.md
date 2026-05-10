---
id: docs-integration-index
title: "Hướng dẫn Tích hợp MRM — Mục lục"
status: final
tags: [index, integration, docs]
summary: "Mục lục các hướng dẫn tích hợp MRM toolkit vào các IDE và AI agents khác nhau."
ai_context: "Dùng để định hướng người dùng đến tài liệu tích hợp phù hợp. Mỗi file integration-XX là atomic module độc lập."
---

# Hướng dẫn Tích hợp MRM — Mục lục

> **TL;DR**: 9 file tích hợp từ AI Chat đến CI/CD, mỗi file ≤ 120 dòng, có MRM frontmatter đầy đủ.

## Danh sách tài liệu

| File | Nội dung |
|------|----------|
| [[integration-01-overview]] | Kiến trúc tổng quan & so sánh phương thức |
| [[integration-02-chat-agents]] | ChatGPT, Claude, Gemini — Custom Instructions |
| [[integration-03-vscode]] | VS Code — extensions, snippets, tasks |
| [[integration-04-obsidian]] | Obsidian — Templater, QuickAdd, Dataview |
| [[integration-05-cursor]] | Cursor IDE — mrm.mdc rules |
| [[integration-06-copilot]] | GitHub Copilot — copilot-instructions.md |
| [[integration-07-custom-agent]] | Custom Agent API (Python + OpenAI) |
| [[integration-08-cicd]] | Git Hooks & GitHub Actions CI/CD |
| [[integration-09-best-practices]] | Best Practices & Troubleshooting |

## Cấu trúc gốc cũ

File `integration/AGENT-INTEGRATION-GUIDE.md` (918 dòng) đã được tách
thành 9 module này. Mỗi module ≤ 120 dòng, có frontmatter MRM đầy đủ.
