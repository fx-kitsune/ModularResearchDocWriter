---
id: integration-09-best-practices
title: "MRM Integration — Best Practices & Troubleshooting"
status: final
tags: [integration, best-practices, troubleshooting, team, workflow]
summary: "Quy trình làm việc nhóm, version control strategy và giải pháp cho các vấn đề phổ biến khi dùng MRM."
ai_context: "Dùng khi người dùng gặp vấn đề với MRM workflow hoặc muốn thiết lập quy trình nhóm. Ưu tiên giải pháp tự động hóa qua script."
---

# MRM Integration — Best Practices & Troubleshooting

> **TL;DR**: Tổ chức theo sprint, dùng branch naming chuẩn, và enforce quality gates trước merge.

## Quy trình làm việc nhóm

```
Day 1:   Architect đề xuất structure → Team review
Day 2-5: Mỗi người viết modules được phân công
Day 6:   Cross-review + validation
Day 7:   Assemble + publish
```

## Version Control Strategy

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

## Quality Gates trước khi merge

- ✅ Tất cả files pass `mrm_validator.py validate`
- ✅ Line count ≤ 300 cho mọi file
- ✅ Cross-refs không broken
- ✅ `ai_context` rõ ràng cho mỗi file

## Troubleshooting

### File vượt 300 dòng

```
Yêu cầu AI tự động tách thành child files:
1. Giữ phần giới thiệu trong parent file
2. Di chuyển chi tiết sang child-01, child-02
3. Cập nhật cross-refs hai chiều
4. Chạy validate lại
```

### Thiếu ai_context

```
Prompt cho AI:
"Thêm ai_context cho file này, chỉ rõ:
- Task downstream nào sẽ dùng file này?
- AI cần tránh hallucination gì?
- Ưu tiên giữ/bỏ thông tin gì?"
```

### Broken cross-references

```bash
# Tìm broken wikilinks tự động
python mrm-toolkit/scripts/mrm_validator.py validate research/
# Validator sẽ warn về mọi [[id]] không tìm thấy file đích
```

### AI hallucination trong số liệu

```
Thêm vào ai_context:
"KHÔNG tự sinh số liệu nếu không có nguồn trích dẫn.
Nếu thiếu dữ liệu, đánh dấu [CẦN NGUỒN] thay vì bịa số."
```

> [!AI-NOTE]
> Troubleshooting phổ biến nhất là file quá dài và broken cross-references.
> Validator tự động phát hiện cả hai — recommend chạy validate sau mỗi
> batch edit thay vì chờ đến CI/CD.
