# 🚀 Hướng Dẫn Tích Hợp MRM Agent Skill Vào IDE & AI Agents

Hướng dẫn chi tiết cách tích hợp **ModularResearchDocWriter** skill vào các môi trường làm việc phổ biến.

---

## 📋 Mục Lục

1. [Tổng quan kiến trúc tích hợp](#tổng-quan-kiến-trúc-tích-hợp)
2. [Tích hợp với AI Chat Agents](#tích-hợp-với-ai-chat-agents)
3. [Tích hợp với VS Code + Extensions](#tích-hợp-với-vs-code--extensions)
4. [Tích hợp với Obsidian](#tích-hợp-với-obsidian)
5. [Tích hợp với Cursor IDE](#tích-hợp-với-cursor-ide)
6. [Tích hợp với GitHub Copilot Workspace](#tích-hợp-với-github-copilot-workspace)
7. [Tích hợp API Custom Agent](#tích-hợp-api-custom-agent)
8. [Automation với Git Hooks & CI/CD](#automation-với-git-hooks--cicd)
9. [Best Practices & Troubleshooting](#best-practices--troubleshooting)

---

## 🏗️ Tổng quan kiến trúc tích hợp

```
┌─────────────────────────────────────────────────────────────┐
│                    USER WORKFLOW                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   VS Code    │  │   Obsidian   │  │    Cursor    │      │
│  │   + Copilot  │  │   + LLM      │  │     IDE      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│                           ▼                                 │
│              ┌────────────────────────┐                     │
│              │   MRM System Prompt    │                     │
│              │   (ModularResearch     │                     │
│              │    DocWriter Skill)    │                     │
│              └───────────┬────────────┘                     │
│                          │                                  │
│                          ▼                                  │
│              ┌────────────────────────┐                     │
│              │   AI Agent / LLM API   │                     │
│              │   (GPT-4, Claude,      │                     │
│              │    Local LLM, etc.)    │                     │
│              └───────────┬────────────┘                     │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Output: MRM Files    │
              │   - research/*.md      │
              │   - index.md           │
              │   - validation report  │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │   Git + CI/CD Pipeline │
              │   - Auto validate      │
              │   - Auto assemble      │
              │   - Deploy             │
              └────────────────────────┘
```

---

## 💬 Tích hợp với AI Chat Agents

### 1. ChatGPT / Claude / Gemini

#### Bước 1: Tạo Custom Instructions / System Prompt

**ChatGPT:**
1. Vào `Settings` → `Custom Instructions`
2. Paste nội dung từ `skills/ModularResearchDocWriter.md` vào ô *"How would you like ChatGPT to respond?"*
3. Thêm dòng đầu tiên:
   ```
   You are ModularResearchDocWriter, an expert in creating modular research documentation.
   Always follow the MRM framework principles.
   ```

**Claude:**
1. Tạo mới conversation
2. Paste toàn bộ system prompt vào message đầu tiên
3. Lưu conversation làm template: "MRM Document Writer"

**Gemini:**
1. Vào `Settings` → `Custom instructions`
2. Thêm MRM skill vào phần working style

#### Bước 2: Prompt mẫu để bắt đầu

```markdown
@MRM_DocWriter 

Yêu cầu: Viết tài liệu về [CHỦ ĐỀ]

Context:
- Domain: Machine Learning Operations
- Type: research_paper
- Depth: deep_dive
- Audience: chuyên gia ML + AI pipeline
- Downstream AI Task: tóm tắt 1 trang, sinh slide, trích xuất bảng số liệu

Hãy:
1. Phân tích phạm vi và đề xuất cây thư mục
2. Viết từng file theo chuẩn MRM
3. Generate index.md
4. Chạy self-validation checklist

Output format: JSON tree + Markdown content
```

#### Bước 3: Lưu template prompts

Tạo file `.chatgpt-mrm-prompts.md` trong project:

```markdown
# MRM Quick Prompts

## Khởi tạo dự án mới
```
Tạo cấu trúc MRM cho dự án nghiên cứu về [topic]. 
Đề xuất 5-7 core modules, mỗi module ≤300 dòng.
```

## Viết file đơn lẻ
```
Viết file MRM với id: core-05-[topic]. 
Nội dung: [mô tả ngắn]. 
Cross-ref đến: [[core-01]], [[core-03]].
```

## Review & Refactor
```
Review file [file-path.md] theo checklist MRM.
Chỉ ra vi phạm và đề xuất sửa.
```

## Generate Report
```
Ghép tất cả files trong research/core/ thành báo cáo hoàn chỉnh.
Thêm transition paragraphs giữa các module.
```
```

---

## 💻 Tích hợp với VS Code + Extensions

### Setup 1: Cài đặt extensions cần thiết

```bash
# Trong VS Code, cài các extensions sau:
- Markdown All in One (yzhang.markdown-all-in-one)
- Markdown Preview Enhanced (shd101wyy.markdown-preview-enhanced)
- YAML (redhat.vscode-yaml)
- Front Matter (ms-vscode.vscode-markdown-frontmatter-preview)
- Todo Tree (Gruntfuggly.todo-tree)
- GitLens (eamodio.gitlens)
```

### Setup 2: Cấu hình workspace settings

Tạo file `.vscode/settings.json`:

```json
{
  "markdown-preview-enhanced.enableFrontMatterParser": true,
  "yaml.schemas": {
    "https://raw.githubusercontent.com/mrm-toolkit/main/schema.json": "*.md"
  },
  "files.associations": {
    "*.md": "markdown"
  },
  "markdownlint.config": {
    "MD001": false,
    "MD013": {
      "line_length": 120
    },
    "MD025": false
  },
  "todo-tree.general.tags": [
    "TODO",
    "FIXME",
    "AI-NOTE",
    "REVIEW",
    "DRAFT"
  ],
  "gitlens.blame.preserveFocus": true
}
```

### Setup 3: Tạo snippets cho MRM

Tạo file `.vscode/mrm-snippets.code-snippets`:

```json
{
  "MRM Note Template": {
    "prefix": "mrm-note",
    "body": [
      "---",
      "id: ${1|module-XX,note-YYYY-MM-DD|}",
      "title: \"${2:Tiêu đề rõ nghĩa}\"",
      "status: ${3|draft,review,final|}",
      "tags: [${4:tag1, tag2}]",
      "summary: \"${5:1-2 câu mô tả phạm vi}\"",
      "ai_context: \"${6:Hướng dẫn cho AI downstream}\"",
      "created: ${7:$(date -Iseconds)}",
      "updated: ${8:$(date -Iseconds)}",
      "authors: [${9:tên}] ",
      "version: 1.0.0",
      "---",
      "",
      "# ${2}",
      "",
      "> **TL;DR**: ${10:1 dòng kết luận chính}",
      "",
      "## ${11:Mục 1}",
      "${12:Nội dung}",
      "",
      "> [!AI-NOTE]",
      "> ${13:Hướng dẫn cụ thể cho AI}",
      ""
    ],
    "description": "Tạo file MRM note với full frontmatter"
  },
  "MRM Cross Reference": {
    "prefix": "mrm-ref",
    "body": "[[${1:id-file}]]",
    "description": "Chèn cross-reference wikilink"
  },
  "MRM AI Note Callout": {
    "prefix": "mrm-ainote",
    "body": [
      "> [!AI-NOTE]",
      "> ${1:Hướng dẫn cho AI khi xử lý file này}"
    ],
    "description": "Chèn AI-NOTE callout"
  }
}
```

### Setup 4: Tích hợp với GitHub Copilot Chat

Tạo file `.github/copilot-instructions.md`:

```markdown
# GitHub Copilot Instructions for MRM Projects

Khi làm việc trong project này, luôn tuân thủ:

1. **Cấu trúc file**: Mỗi file ≤300 dòng, 1 chủ đề duy nhất
2. **Frontmatter**: Luôn bắt đầu với YAML frontmatter đầy đủ 9 trường
3. **Progressive Disclosure**: Summary → TL;DR → Nội dung → Chi tiết
4. **Cross-refs**: Dùng [[id]] hoặc [text](./path.md)
5. **AI Context**: Mỗi file phải có ai_context rõ ràng

Khi được yêu cầu viết tài liệu:
- Đề xuất tree structure trước
- Viết từng file riêng biệt
- Tự động generate index.md
- Chạy validation checklist

Không bao giờ:
- Tạo file >300 dòng
- Thiếu frontmatter
- Dùng placeholder mơ hồ
- Tạo circular references
```

### Setup 5: Tasks tự động hóa

Tạo file `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "MRM: Validate Project",
      "type": "shell",
      "command": "python scripts/mrm_validator.py validate research/",
      "group": "build",
      "problemMatcher": []
    },
    {
      "label": "MRM: Generate Index",
      "type": "shell",
      "command": "python scripts/mrm_validator.py generate-index research/",
      "group": "build",
      "problemMatcher": []
    },
    {
      "label": "MRM: Assemble Report",
      "type": "shell",
      "command": "python scripts/mrm_validator.py assemble research/ outputs/final-report.md",
      "group": "build",
      "problemMatcher": []
    },
    {
      "label": "MRM: Count Lines",
      "type": "shell",
      "command": "python scripts/mrm_validator.py count-lines ${file}",
      "group": "test",
      "problemMatcher": []
    }
  ]
}
```

**Sử dụng**: `Ctrl+Shift+P` → `Tasks: Run Task` → Chọn task MRM

---

## 🔮 Tích hợp với Obsidian

### Bước 1: Cài đặt plugins cần thiết

Trong Obsidian Settings → Community Plugins:

```
✅ Templater
✅ Dataview
✅ QuickAdd
✅ Calendar
✅ Periodic Notes
✅ Outliner
✅ Various Complements
```

### Bước 2: Cấu hình Templater

Tạo folder `Templates/MRM/` và file `MRM-Note-Template.md`:

```markdown
---
id: <% tp.file.title | slugify %>
title: "<% tp.file.title %>"
status: draft
tags: []
summary: ""
ai_context: ""
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
updated: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
authors: ["<% tp.system.prompt('Author name') %>"]
version: 1.0.0
---

# <% tp.file.title %>

> **TL;DR**: <% tp.system.prompt("TL;DR - 1 dòng kết luận") %>

## <% tp.system.prompt("Heading đầu tiên") %>



> [!AI-NOTE]
> <% tp.system.prompt("Hướng dẫn cho AI downstream") %>
```

### Bước 3: Cấu hình QuickAdd cho MRM workflow

Thêm macro `Create MRM Note`:

```javascript
// QuickAdd script: CreateMRMNote.js
module.exports = async (params) => {
  const title = await params.quickAddApi.inputPrompt("Note title?");
  const folder = await params.quickAddApi.inputPrompt("Folder? (core/meta/notes)");
  
  const id = `${folder}-${Date.now().toString().slice(-4)}`;
  const path = `research/${folder}/${id}-${title}.md`;
  
  // Create file with template
  await params.quickAddApi.fileSystem.createFile(path, templateContent);
  
  // Open file
  await params.quickAddApi.fileSystem.openFile(path);
};
```

### Bước 4: Dataview queries cho dashboard

Tạo file `research/_index-dashboard.md`:

```markdown
```dataview
TABLE status, length(rows.file.text) as lines, created
FROM "research"
WHERE contains(file.path, "research/")
SORT created DESC
```

```dataview
LIST
FROM "research"
WHERE status = "draft"
SORT updated ASC
```

```dataview
TABLE without id file.link as "File", tags
FROM "research"
WHERE contains(tags, "urgent")
```
```

### Bước 5: Hotkeys setup

Vào Settings → Hotkeys, gán phím tắt:

```
Templater: Insert template        →  Ctrl+Alt+N
QuickAdd: Create MRM Note        →  Ctrl+Alt+M
Dataview: Refresh all queries    →  Ctrl+Alt+R
```

---

## 🎯 Tích hợp với Cursor IDE

### Bước 1: Cấu hình .cursorrules

Tạo file `.cursorrules` trong root project:

```markdown
# Cursor Rules for MRM Projects

## Role
You are ModularResearchDocWriter, expert in creating modular research documentation.

## Core Principles
1. Atomic files: ≤300 lines, 1 topic per file
2. Progressive disclosure: Summary → TL;DR → Content → Details
3. Mandatory YAML frontmatter with 9 fields
4. Clear AI context boundaries
5. Standardized cross-references

## Workflow
1. ALWAYS propose directory tree BEFORE writing
2. Write files one by one, respecting line limits
3. Auto-chunk if content exceeds 300 lines
4. Generate index.md after all files
5. Run self-validation checklist

## Output Format
- Use markdown code blocks with language identifier
- Include full file paths
- Show diff when modifying existing files

## Forbidden
- Files >300 lines without chunking
- Missing ai_context field
- Vague placeholders
- Circular references
```

### Bước 2: Custom Commands

Tạo file `.cursor/commands/mrm.json`:

```json
{
  "commands": [
    {
      "name": "mrm-init",
      "description": "Khởi tạo cấu trúc MRM project",
      "prompt": "Tạo cấu trúc thư mục MRM tiêu chuẩn với research/, templates/, scripts/. Đề xuất 5 core modules ban đầu."
    },
    {
      "name": "mrm-write",
      "description": "Viết file MRM mới",
      "prompt": "Viết file MRM với nội dung: {{input}}. Tuân thủ đầy đủ checklist MRM."
    },
    {
      "name": "mrm-review",
      "description": "Review file theo chuẩn MRM",
      "prompt": "Review file {{file}} theo checklist MRM. Chỉ ra vi phạm và đề xuất sửa."
    },
    {
      "name": "mrm-assemble",
      "description": "Ghép các module thành báo cáo",
      "prompt": "Ghép tất cả files trong research/core/ thành báo cáo hoàn chỉnh với transitions mượt mà."
    }
  ]
}
```

### Bước 3: Sử dụng Composer Mode

Trong Cursor, dùng `Cmd+K` (Composer) với prompt:

```
@workspace /new mrm-project

Tạo project MRM hoàn chỉnh cho chủ đề: [Your Topic]

Requirements:
- 5-7 core modules
- Mỗi module ≤300 dòng
- Full frontmatter
- Cross-references chuẩn
- Auto-generated index

Output: Full directory tree + content for each file
```

---

## 🤖 Tích hợp với GitHub Copilot Workspace

### Bước 1: Tạo copilot-instructions.md

```markdown
# GitHub Copilot Workspace Instructions

Project type: Modular Research Documentation (MRM)

## Standards
- File structure: Atomic notes (≤300 lines)
- Frontmatter: YAML với 9 trường bắt buộc
- Navigation: Progressive disclosure
- References: [[wikilinks]] hoặc [markdown](./path.md)

## When I ask to write documentation:
1. Propose directory structure first
2. Ask clarifying questions if scope unclear
3. Write one file at a time
4. Validate against MRM checklist
5. Suggest next steps

## When I ask to review:
1. Check frontmatter completeness
2. Verify line count ≤300
3. Validate cross-references
4. Check ai_context clarity
5. Suggest improvements

## Auto-suggestions:
- Remind me if file approaching 300 lines
- Suggest splitting large topics
- Propose related modules to create
- Flag missing cross-references
```

### Bước 2: Sử dụng trong Workspace

1. Mở GitHub Copilot Chat trong VS Code
2. Gõ `/workspace` để activate context
3. Dùng prompts:

```
@workspace Tạo cấu trúc MRM cho research paper về Transformer models

@workspace Review file research/core/core-03-attention.md theo chuẩn MRM

@workspace Generate index.md cho toàn bộ research/ folder
```

---

## 🔌 Tích hợp API Custom Agent

### Kiến trúc agent custom

```python
# agents/mrm_agent.py
import openai
import yaml
from pathlib import Path

class MRAgent:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        with open("skills/ModularResearchDocWriter.md", "r") as f:
            return f.read()
    
    def generate_structure(self, topic: str, depth: str = "standard") -> dict:
        """Đề xuất cấu trúc thư mục"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Đề xuất cấu trúc MRM cho: {topic}. Depth: {depth}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def write_file(self, file_id: str, topic: str, cross_refs: list = None) -> str:
        """Viết file MRM đơn lẻ"""
        prompt = f"""
        Viết file MRM với:
        - ID: {file_id}
        - Chủ đề: {topic}
        - Cross-refs: {cross_refs or []}
        
        Output: Full markdown content với frontmatter
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    
    def validate_file(self, content: str) -> dict:
        """Validate file theo checklist MRM"""
        prompt = f"""
        Validate file sau theo checklist MRM:
        {content}
        
        Trả về JSON với keys: valid, violations, suggestions
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def full_workflow(self, topic: str, output_dir: str):
        """Chạy toàn bộ workflow MRM"""
        # Step 1: Generate structure
        structure = self.generate_structure(topic)
        print(f"Structure: {structure}")
        
        # Step 2: Write each file
        for module in structure['modules']:
            content = self.write_file(
                file_id=module['id'],
                topic=module['topic'],
                cross_refs=module.get('cross_refs', [])
            )
            
            # Step 3: Validate
            validation = self.validate_file(content)
            if not validation['valid']:
                print(f"Violations in {module['id']}: {validation['violations']}")
            
            # Step 4: Save file
            path = Path(output_dir) / f"{module['id']}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        
        # Step 5: Generate index
        index_content = self.generate_index(structure)
        (Path(output_dir) / "index.md").write_text(index_content)
```

### Sử dụng agent

```python
# main.py
from agents.mrm_agent import MRAgent

agent = MRAgent(api_key="your-openai-key")

agent.full_workflow(
    topic="Retrieval Augmented Generation for Enterprise Knowledge Base",
    output_dir="research/"
)
```

---

## ⚙️ Automation với Git Hooks & CI/CD

### Git Hook: Pre-commit validation

Tạo file `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "🔍 Running MRM validation..."

# Validate all changed .md files
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')

if [ -z "$changed_files" ]; then
  echo "No markdown files changed."
  exit 0
fi

errors=0
for file in $changed_files; do
  if [ -f "$file" ]; then
    echo "Checking $file..."
    python scripts/mrm_validator.py validate-file "$file"
    if [ $? -ne 0 ]; then
      errors=$((errors + 1))
    fi
  fi
done

if [ $errors -gt 0 ]; then
  echo "❌ Found $errors files with MRM violations."
  echo "Please fix before committing."
  exit 1
fi

echo "✅ All files pass MRM validation."
exit 0
```

### GitHub Actions: CI/CD Pipeline

Tạo file `.github/workflows/mrm-validate.yml`:

```yaml
name: MRM Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install pyyaml
    
    - name: Validate MRM files
      run: |
        python scripts/mrm_validator.py validate research/
    
    - name: Generate index
      run: |
        python scripts/mrm_validator.py generate-index research/
    
    - name: Assemble report
      run: |
        python scripts/mrm_validator.py assemble research/ outputs/final-report.md
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: mrm-report
        path: outputs/
```

### Git Hook: Post-merge auto-update

Tạo file `.git/hooks/post-merge`:

```bash
#!/bin/bash

echo "🔄 Auto-generating MRM index after merge..."
python scripts/mrm_validator.py generate-index research/

echo "📦 Assembling final report..."
python scripts/mrm_validator.py assemble research/ outputs/final-report.md

git add research/index.md outputs/final-report.md
echo "✅ Index and report updated."
```

---

## 🎓 Best Practices & Troubleshooting

### Best Practices

#### 1. Quy trình làm việc nhóm

```
Day 1: Architect proposes structure → Team reviews
Day 2-5: Each member writes assigned modules
Day 6: Cross-review + validation
Day 7: Assemble + publish
```

#### 2. Version control strategy

```bash
# Branch naming
feature/mrm-add-evaluation-module
fix/mrm-core-03-typo
docs/mrm-update-examples

# Commit messages
feat(core): add core-05-deployment module
fix(meta): update ai_context in meta-01
docs(index): regenerate after module addition
```

#### 3. Quality gates

- ✅ Tất cả files pass validation trước khi merge
- ✅ Line count ≤300 cho mọi file
- ✅ Cross-refs không broken
- ✅ ai_context rõ ràng cho mỗi file

### Troubleshooting

#### Vấn đề 1: File vượt quá 300 dòng

**Giải pháp:**
```markdown
Khi AI cảnh báo file >300 dòng:
1. Yêu cầu AI tự động tách thành child files
2. Giữ phần giới thiệu trong parent file
3. Di chuyển chi tiết sang child-01, child-02
4. Cập nhật cross-refs
```

#### Vấn đề 2: Thiếu ai_context

**Giải pháp:**
```markdown
Prompt cho AI:
"Thêm ai_context cho file này, chỉ rõ:
- Task downstream nào sẽ dùng file này?
- AI cần tránh hallucination gì?
- Ưu tiên giữ/bỏ thông tin gì?"
```

#### Vấn đề 3: Broken cross-references

**Giải pháp:**
```bash
# Chạy validator để tìm broken links
python scripts/mrm_validator.py validate research/

# Hoặc dùng script custom
grep -r "\[\[.*\]\]" research/ | while read line; do
  ref=$(echo $line | grep -oP '\[\[\K[^\]]+')
  if ! find research/ -name "*$ref*" | head -1; then
    echo "Broken ref: $ref in $line"
  fi
done
```

#### Vấn đề 4: AI hallucination trong số liệu

**Giải pháp:**
```markdown
Trong ai_context, thêm:
"KHÔNG tự sinh số liệu nếu không có nguồn trích dẫn.
Nếu thiếu dữ liệu, đánh dấu [CẦN NGUỒN] thay vì bịa số.
Ưu tiên trích dẫn từ 2022+."
```

---

## 📊 So sánh các phương thức tích hợp

| Phương thức | Độ khó | Flexibility | Automation | Phù hợp cho |
|-------------|--------|-------------|------------|-------------|
| ChatGPT/Claude | Dễ | Trung bình | Thấp | Cá nhân, quick tasks |
| VS Code + Copilot | Trung bình | Cao | Trung bình | Developers, technical writers |
| Obsidian | Trung bình | Rất cao | Cao | Researchers, knowledge workers |
| Cursor IDE | Dễ | Cao | Cao | AI-native developers |
| Custom Agent API | Khó | Tối đa | Tối đa | Production pipelines |
| GitHub Actions | Trung bình | Trung bình | Tự động | Team collaboration |

---

## 🚀 Quick Start Checklist

```markdown
- [ ] Copy system prompt vào AI agent ưa thích
- [ ] Cài đặt extensions/plugins cần thiết cho IDE
- [ ] Tạo templates với snippets
- [ ] Setup git hooks cho auto-validation
- [ ] Cấu hình CI/CD pipeline
- [ ] Test workflow với 1-2 files mẫu
- [ ] Train team members qua ví dụ thực tế
- [ ] Iterate và cải thiện dựa trên feedback
```

---

## 📚 Tài liệu tham khảo thêm

- [MRM Skill Definition](../skills/ModularResearchDocWriter.md)
- [Template Examples](../templates/)
- [Validation Scripts](../scripts/mrm_validator.py)
- [Example Projects](../examples/)

---

**Cập nhật lần cuối**: 2025
**Tác giả**: MRM Toolkit Team
**License**: MIT
