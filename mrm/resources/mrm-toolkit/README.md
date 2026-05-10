# MRM Toolkit - Modular Research Markdown Agent Toolkit

MRM Toolkit là bộ công cụ giúp agent và con người **plan → write → validate → index → assemble** tài liệu nghiên cứu dạng Markdown theo chuẩn Modular Research Markdown.

## Vấn đề repo này giải quyết

Nhiều dự án research/doc bị lẫn lộn 3 thứ:

- **Skill**: agent phải hành xử như thế nào.
- **Plan**: việc cần làm trong một lần nâng cấp/tác vụ cụ thể.
- **Content**: tài liệu nghiên cứu thật sự.

Toolkit này tách chúng thành các lớp rõ ràng để dùng được với Codex, Claude Code, Gemini, Copilot, Cursor và các agent IDE khác.

## Kiến trúc thư mục

```text
mrm-toolkit/
├── manifest.yaml                         # Máy đọc được: entrypoints, adapters, commands
├── skills/
│   └── modular-research-doc-writer/
│       └── SKILL.md                       # Skill canonical, không chứa roadmap tạm thời
├── workflows/
│   └── MRM-WORKFLOW.md                    # Quy trình agent chuẩn
├── contracts/
│   ├── OUTPUT-CONTRACT.md                 # Shape output bắt buộc
│   └── QUALITY-RUBRIC.md                  # Rubric tự kiểm định
├── adapters/
│   ├── codex/AGENTS.md                    # OpenAI Codex
│   ├── claude/CLAUDE.md                   # Claude Code
│   ├── gemini/GEMINI.md                   # Gemini CLI / IDE
│   ├── copilot/copilot-instructions.md    # GitHub Copilot
│   ├── cursor/mrm.mdc                     # Cursor rules
│   └── agent-ide/AGENT-RULES.md           # Generic agent IDE
├── docs/
│   ├── index.md                           # Mục lục hướng dẫn tích hợp
│   ├── integration-01-overview.md         # Tổng quan kiến trúc
│   ├── integration-02-chat-agents.md      # AI Chat (ChatGPT, Claude, Gemini)
│   ├── integration-03-vscode.md           # VS Code + extensions
│   ├── integration-04-obsidian.md         # Obsidian
│   ├── integration-05-cursor.md           # Cursor IDE
│   ├── integration-06-copilot.md          # GitHub Copilot
│   ├── integration-07-custom-agent.md     # Custom Agent API
│   ├── integration-08-cicd.md             # Git Hooks & CI/CD
│   └── integration-09-best-practices.md   # Best Practices
├── prompts/
│   └── quickstart-prompts.md              # Prompt cookbook
├── templates/
│   └── note-template.md                   # Atomic note template
├── scripts/
│   ├── mrm_validator.py                   # Entry point CLI (thin wrapper)
│   └── mrm/                               # Package: validator, indexer, assembler, adapter, cli
├── research/                              # Research tree mẫu
└── integration/                           # (trống) — nội dung đã chuyển sang docs/
```

## Cài đặt nhanh

### Yêu cầu

- Python 3.8+
- Không cần dependency ngoài cho validation cơ bản; validator có parser frontmatter tối giản tích hợp.
- Có thể cài PyYAML riêng nếu workflow nội bộ của bạn cần parse YAML đầy đủ.

## Cài skill Codex qua pip

Dùng script cài đặt khi muốn đưa skill canonical vào thư mục skills của Codex thay vì chỉ copy adapter `AGENTS.md`. Script dùng `python -m pip install` với `--target` vào thư mục tạm, sau đó chạy installer để copy `SKILL.md` vào `$CODEX_HOME/skills/modular-research-doc-writer` hoặc `~/.codex/skills/modular-research-doc-writer`.

```bash
scripts/install-skill.sh
OVERWRITE=1 scripts/install-skill.sh /path/to/codex/skills .
```

```powershell
./scripts/install-skill.ps1
./scripts/install-skill.ps1 "C:\codex\skills" . -Overwrite
```

Có thể thay đối số thứ hai bằng nguồn pip hợp lệ như `git+https://github.com/<owner>/<repo>.git`.

## Dùng với agent

### Codex

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter codex /path/to/project
```

Tạo `/path/to/project/AGENTS.md` từ adapter Codex.

### Claude Code

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter claude /path/to/project
```

Tạo `/path/to/project/CLAUDE.md`.

### Gemini

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter gemini /path/to/project
```

Tạo `/path/to/project/GEMINI.md`.

### GitHub Copilot

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter copilot /path/to/project
```

Tạo `/path/to/project/.github/copilot-instructions.md`.

### Cursor

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter cursor /path/to/project
```

Tạo `/path/to/project/.cursor/rules/mrm.mdc`.

## Quy trình chuẩn

1. Agent đọc `manifest.yaml`.
2. Agent nạp skill tại `skills/modular-research-doc-writer/SKILL.md`.
3. Agent làm theo `workflows/MRM-WORKFLOW.md`.
4. Agent xuất nội dung theo `contracts/OUTPUT-CONTRACT.md`.
5. Agent tự kiểm với `contracts/QUALITY-RUBRIC.md`.
6. Agent chạy validator nếu có filesystem.

## Lệnh CLI

### Validate thư mục

```bash
python mrm-toolkit/scripts/mrm_validator.py validate mrm-toolkit/research
```

### Validate file đơn lẻ

```bash
python mrm-toolkit/scripts/mrm_validator.py validate-file mrm-toolkit/research/core/core-01-atomic-structure.md
```

### Đếm dòng nội dung

```bash
python mrm-toolkit/scripts/mrm_validator.py count-lines mrm-toolkit/research/core/core-01-atomic-structure.md
```

### Sinh index

```bash
python mrm-toolkit/scripts/mrm_validator.py generate-index mrm-toolkit/research
```

### Assemble report

```bash
python mrm-toolkit/scripts/mrm_validator.py assemble mrm-toolkit/research mrm-toolkit/research/outputs/final-report.md
```

### Cài adapter

```bash
python mrm-toolkit/scripts/mrm_validator.py install-adapter <adapter> <project_root> [--overwrite]
```

Adapter hợp lệ: `codex`, `claude`, `claude_code`, `gemini`, `copilot`, `cursor`, `agent_ide`.

## Checklist MRM

- [ ] YAML frontmatter có đủ `id`, `title`, `status`, `tags`, `summary`, `ai_context`.
- [ ] `summary` không quá 2 câu.
- [ ] TL;DR đúng 1 dòng.
- [ ] File chỉ chứa 1 chủ đề.
- [ ] Nội dung không quá 300 dòng.
- [ ] Cross-reference dùng `[[frontmatter-id]]` hoặc Markdown link tồn tại.
- [ ] `ai_context` nói rõ task downstream và điều không được bịa.
- [ ] Roadmap hoặc plan tạm thời không nằm trong skill canonical.

## Prompt mẫu

Xem [`prompts/quickstart-prompts.md`](prompts/quickstart-prompts.md) để copy prompt khởi tạo, refactor, review và assemble.

## Ghi chú legacy

Các file trong `docs/` vẫn được giữ để tham khảo lịch sử. Với agent mới, ưu tiên `manifest.yaml`, `skills/`, `workflows/`, `contracts/`, và `adapters/`.
