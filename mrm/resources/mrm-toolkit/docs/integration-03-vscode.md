---
id: integration-03-vscode
title: "Tích hợp MRM với VS Code"
status: final
tags: [integration, vscode, copilot, extensions, snippets]
summary: "Cấu hình VS Code với extensions, snippets và tasks để làm việc với MRM hiệu quả."
ai_context: "Dùng khi người dùng muốn tích hợp MRM vào VS Code workflow. Bao gồm extensions, workspace settings, snippets và VS Code tasks."
---

# Tích hợp MRM với VS Code

> **TL;DR**: Cài 4 extensions, thêm snippets và tasks để có MRM workflow đầy đủ trong VS Code.

## Extensions cần thiết

```
Markdown All in One        (yzhang.markdown-all-in-one)
Markdown Preview Enhanced  (shd101wyy.markdown-preview-enhanced)
YAML                       (redhat.vscode-yaml)
Todo Tree                  (Gruntfuggly.todo-tree)
```

## Workspace settings (`.vscode/settings.json`)

```json
{
  "markdown-preview-enhanced.enableFrontMatterParser": true,
  "markdownlint.config": {
    "MD001": false,
    "MD013": { "line_length": 120 },
    "MD025": false
  },
  "todo-tree.general.tags": ["TODO", "FIXME", "AI-NOTE", "REVIEW", "DRAFT"]
}
```

## Snippets MRM (`.vscode/mrm-snippets.code-snippets`)

```json
{
  "MRM Note Template": {
    "prefix": "mrm-note",
    "body": [
      "---",
      "id: ${1:module-XX}",
      "title: \"${2:Tiêu đề rõ nghĩa}\"",
      "status: ${3|draft,review,final|}",
      "tags: [${4:tag1, tag2}]",
      "summary: \"${5:1-2 câu mô tả phạm vi}\"",
      "ai_context: \"${6:Hướng dẫn cho AI downstream}\"",
      "---", "",
      "# ${2}", "",
      "> **TL;DR**: ${7:1 dòng kết luận chính}", "",
      "## ${8:Mục 1}",
      "${9:Nội dung}"
    ],
    "description": "Tạo file MRM note với full frontmatter"
  },
  "MRM Cross Reference": {
    "prefix": "mrm-ref",
    "body": "[[${1:id-file}]]",
    "description": "Chèn cross-reference wikilink"
  },
  "MRM AI Note": {
    "prefix": "mrm-ainote",
    "body": ["> [!AI-NOTE]", "> ${1:Hướng dẫn cho AI}"],
    "description": "Chèn AI-NOTE callout"
  }
}
```

## VS Code Tasks (`.vscode/tasks.json`)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "MRM: Validate Project",
      "type": "shell",
      "command": "python mrm-toolkit/scripts/mrm_validator.py validate research/",
      "group": "build"
    },
    {
      "label": "MRM: Generate Index",
      "type": "shell",
      "command": "python mrm-toolkit/scripts/mrm_validator.py generate-index research/",
      "group": "build"
    },
    {
      "label": "MRM: Assemble Report",
      "type": "shell",
      "command": "python mrm-toolkit/scripts/mrm_validator.py assemble research/ outputs/final-report.md",
      "group": "build"
    },
    {
      "label": "MRM: Count Lines",
      "type": "shell",
      "command": "python mrm-toolkit/scripts/mrm_validator.py count-lines ${file}",
      "group": "test"
    }
  ]
}
```

**Sử dụng**: `Ctrl+Shift+P` → `Tasks: Run Task` → Chọn task MRM

> [!AI-NOTE]
> Khi hướng dẫn setup VS Code, ưu tiên tasks.json vì cho phép chạy validator
> với phím tắt. Snippets giúp tạo file MRM mới nhanh mà không sai frontmatter.
