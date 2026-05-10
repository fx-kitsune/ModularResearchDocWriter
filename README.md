# 🚀 mrm-toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**mrm-toolkit** là toolkit hoàn chỉnh nhất để biến các yêu cầu nghiên cứu phức tạp thành hệ thống Markdown module hóa. Được thiết kế tối ưu cho AI Agent (Codex, Claude, Gemini, Cursor), giúp đảm bảo tri thức luôn được cấu trúc, dễ đọc và an toàn cho context-window.

---

## 💎 Tại sao nên dùng MRM?

Trong kỷ nguyên AI, tài liệu truyền thống thường quá dài và thiếu cấu trúc, khiến AI Agent dễ bị "ảo giác" hoặc mất context. MRM (Modular Research Markdown) giải quyết vấn đề này bằng:

- **Atomic Design**: Chia nhỏ tài liệu thành các module < 300 dòng.
- **AI-Native Boundary**: Mỗi module đều có `ai_context` để định hướng Agent.
- **Progressive Disclosure**: Cấu trúc TL;DR -> Body giúp tiết kiệm token và tăng độ chính xác.
- **Unified Interface**: Một công cụ duy nhất để Quản lý - Kiểm định - Đóng gói.

---

## 🏗️ Kiến trúc 4 Lớp Excellence

1.  **Skill** (`skills/`): Định nghĩa hành vi và "tư duy" chuẩn MRM cho Agent.
2.  **Workflow** (`workflows/`): Quy trình làm việc từ Scoping, Research đến Validation.
3.  **Contracts** (`contracts/`): Tiêu chuẩn vàng cho Output và bộ Rubric đánh giá tự động.
4.  **Adapters** (`adapters/`): Cấu hình "mì ăn liền" cho Claude Code, Gemini, Copilot và Cursor.

---

## 📊 Chỉ số đo lường hiệu quả (Metrics)

| Chỉ số | Mục tiêu | Lợi ích |
|---|---|---|
| **Modularity Ratio** | 100% | Đảm bảo không có module nào quá 300 dòng |
| **Context Safety** | 99.9% | Mọi file đều có `ai_context` hợp lệ |
| **Structural Integrity** | 100% | Tự động phát hiện broken links và sai heading |
| **Agent Readiness** | < 1 min | Thời gian tích hợp vào một dự án mới |

---

## 🛠️ Cài đặt nhanh

```bash
# Cài đặt chính thức từ PyPI
pip install mrm-toolkit

# Hoặc cài đặt bản development từ GitHub
pip install git+https://github.com/fx-kitsune/mrm-toolkit.git
```

---

## 🕹️ Unified CLI (Lệnh `mrm`)

Chúng tôi đã hợp nhất mọi công cụ vào một lệnh duy nhất để tối ưu trải nghiệm:

### 1. Cài đặt Agent Skill
```bash
mrm install-skill --overwrite
```

### 2. Cài đặt Adapter cho IDE
```bash
mrm install-adapter claude ./my-project
mrm install-adapter cursor ./my-project
```

### 3. Kiểm định chất lượng (Validator)
```bash
mrm validate ./research
```

### 4. Đóng gói báo cáo (Assembler)
```bash
mrm assemble ./research ./output/final-report.md
```

---

## 🌐 Landing Page
Xem giới thiệu trực quan tại: [https://fx-kitsune.github.io/mrm-toolkit/](https://fx-kitsune.github.io/mrm-toolkit/)

---

## 📜 License
MIT License. Được phát triển bởi [**fx-kitsune**](https://github.com/fx-kitsune).
