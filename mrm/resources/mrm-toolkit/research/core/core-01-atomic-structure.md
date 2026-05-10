---
id: core-01-atomic-structure
title: "Atomic File Structure - Cấu trúc File Nguyên tử"
status: final
tags: [atomicity, chunking, file-structure]
summary: "Quy tắc tổ chức file theo nguyên tắc atomic: 1 file = 1 chủ đề, giới hạn 300 dòng."
ai_context: "Dùng cho AI hiểu và áp dụng quy tắc chunking. Khi gặp nội dung dài, tự động đề xuất tách file con."
---

# Atomic File Structure - Cấu trúc File Nguyên tử

> **TL;DR**: Mỗi file Markdown chứa đúng 1 chủ đề con, tối đa 300 dòng nội dung.

## Tại sao cần Atomicity?

File monolithic (đơn khối) dài gây ra vấn đề:

- **Người đọc**: Không biết bắt đầu từ đâu, bỏ qua section quan trọng
- **AI**: Tràn bộ nhớ đệm, mất tập trung vào ngữ cảnh chính
- **Version control**: Merge conflict khi nhiều người sửa cùng file

## Quy tắc Vàng

### Giới hạn Kích thước

| Loại file | Tối đa | Ghi chú |
|-----------|--------|---------|
| Note thông thường | 250 dòng | Không tính frontmatter |
| Core module | 300 dòng | Có thể có appendix |
| Reference/Template | 400 dòng | Ngoại lệ cho template phức tạp |

### Dấu hiệu Cần Tách File

Khi nội dung có ≥1 trong các dấu hiệu sau:

1. **Vượt 300 dòng** nội dung chính
2. **≥5 heading cấp 2** (`##`) độc lập
3. **≥3 chủ đề con** có thể đứng riêng
4. **Có bảng/phụ lục** dài >50 dòng

## Chiến lược Tách File

### Pattern 1: Theo Chủ đề Con

```
core-01-parent.md       # Giữ intro + overview
├── core-01-child-01.md # Chủ đề con 1
├── core-01-child-02.md # Chủ đề con 2
└── core-01-child-03.md # Chủ đề con 3
```

### Pattern 2: Theo Mức độ Chi tiết

```
core-02-main.md         # Nội dung chính (executive summary)
└── core-02-appendix.md # Chi tiết kỹ thuật, data raw
```

### Pattern 3: Theo Timeline

```
note-2024-01-15.md      # Session 1
note-2024-01-22.md      # Session 2
note-2024-01-29.md      # Session 3
```

## Cross-Reference giữa Các File

### Wikilink Format (Ưu tiên)

```markdown
Xem chi tiết tại [[core-01-child-01]].
```

*Lưu ý: Wikilink là reference logic, không yêu cầu file tồn tại ngay.*

### Markdown Link (Khi cần path cụ thể)

```markdown
[Chi tiết kỹ thuật](./core-01-child-01.md#section-3)
```

### Quy tắc Đặt tên ID

- **Format**: `[loại]-[số]-[mô-tả-ngắn]`
- **Ví dụ**: `meta-01-overview`, `core-03-evaluation`, `note-2024-01-15`
- **ID duy nhất**: Không trùng trong toàn bộ dự án

## Checklist Trước khi Tách File

- [ ] File gốc vượt 300 dòng?
- [ ] Có thể nhóm nội dung thành ≥2 chủ đề độc lập?
- [ ] Mỗi file con có ý nghĩa khi đọc riêng?
- [ ] Đã thêm cross-reference hai chiều?
- [ ] Đã cập nhật index.md?

> [!AI-NOTE]
> Khi xử lý file dài, AI phải:
> 1. Đếm số dòng nội dung (không tính frontmatter)
> 2. Nếu >300 dòng → Đề xuất táchfile với tree mới
> 3. Giữ nguyên ID của file gốc, thêm suffix `-child-XX` cho file con
> 4. Task downstream: auto-chunking, generate child files

## Tài liệu Liên quan

- [[meta-01-project-overview]] - Tổng quan MRM Framework (✅ tồn tại)
- [[core-02-progressive-disclosure]] - Progressive disclosure pattern (sẽ tạo)
- [[core-03-frontmatter-standard]] - Chuẩn frontmatter (sẽ tạo)

> [!NOTE] Wikilink có thể trỏ đến file chưa tồn tại - đây là placeholder cho nội dung tương lai.
