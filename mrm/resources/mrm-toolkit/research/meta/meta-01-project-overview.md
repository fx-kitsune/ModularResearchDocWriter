---
id: meta-01-project-overview
title: "Tổng quan Dự án MRM Framework"
status: final
tags: [overview, mrm, architecture]
summary: "Giới thiệu kiến trúc Modular Research Markdown Framework và các nguyên tắc cốt lõi."
ai_context: "Dùng cho AI hiểu ngữ cảnh tổng thể của dự án. Ưu tiên trích dẫn đến các file core-XX khi cần chi tiết."
---

# Tổng quan Dự án MRM Framework

> **TL;DR**: MRM là kiến trúc tài liệu nghiên cứu module hóa, tối ưu cho cả người đọc và AI xử lý.

## Vấn đề Giải quyết

Markdown truyền thống dạng monolithic (file đơn dài hàng nghìn dòng) gây ra 3 điểm nghẽn:

| Đối tượng | Vấn đề | Hậu quả |
|-----------|--------|---------|
| Con người | Quá tải nhận thức | Khó điều hướng, nản khi đọc file dài |
| AI | Mất ngữ cảnh | Hallucination, lãng phí token |
| Quy trình | Version control khó | Merge conflict, không trace được nguồn |

## Giải pháp MRM

### 5 Nguyên tắc Cốt lõi

1. **Atomicity** - 1 file = 1 chủ đề con, ≤300 dòng
2. **Progressive Disclosure** - Trình bày theo tầng: Summary → TL;DR → Nội dung → Phụ lục
3. **AI-Native Boundary** - Frontmatter chuẩn với `ai_context` rõ ràng
4. **Human-First Readability** - Bullet points, bảng so sánh, câu ngắn
5. **Cross-Reference Chuẩn** - Dùng `[[id]]` hoặc link tương đối kiểm chứng

### Cấu trúc Thư mục

```
research/
├── index.md              # Mục lục tự động
├── meta/                 # Metadata & overview
├── notes/                # Atomic notes
├── core/                 # Nội dung chính
└── outputs/              # Báo cáo đã assemble
```

## Lợi ích Kỳ vọng

- **Người đọc**: Giảm 60-80% thời gian duyệt tài liệu
- **AI xử lý**: Tăng độ chính xác, giảm hallucination
- **Nhóm làm việc**: Dễ review theo module, giảm merge conflict

## Tài liệu Liên quan

- [[core-01-atomic-structure]] - Atomic file structure (✅ tồn tại)
- [[core-02-progressive-disclosure]] - Progressive disclosure pattern (sẽ tạo)
- [[core-03-ai-native-boundary]] - AI-Native boundary và frontmatter (sẽ tạo)
- [[meta-02-workflow-guide]] - Hướng dẫn workflow tích hợp (sẽ tạo)

> [!NOTE] Wikilink có thể trỏ đến file chưa tồn tại - đây là placeholder cho nội dung tương lai.

> [!AI-NOTE]
> Khi tóm tắt file này, AI phải:
> 1. Giữ nguyên 5 nguyên tắc cốt lõi không thay đổi
> 2. Cross-reference đến file core-XX khi người dùng hỏi chi tiết
> 3. Task downstream phù hợp: sinh slide giới thiệu, tạo FAQ, onboarding người mới
