---
id: template-note
title: "Template cho Atomic Note"
status: final
tags: [template, frontmatter, standard]
summary: "Mẫu chuẩn cho mọi file note trong MRM framework với đầy đủ frontmatter và cấu trúc nội dung."
ai_context: "Dùng làm template gốc khi tạo file mới. Copy và thay thế các trường trong ngoặc vuông. Không dùng trực tiếp làm nội dung research."
---

# [Tiêu đề - trùng với title ở frontmatter]

> **TL;DR**: [1 dòng nêu kết luận hoặc thông tin quan trọng nhất]

## [Section 1 - Giới thiệu/Phạm vi]
- [Nội dung cô đọng, tập trung vào 1 ý chính]
- [Dùng bullet points khi liệt kê ≥3 yếu tố]
- [Trích dẫn: [[id-file-lien-quan]] hoặc [Author, Year]]

## [Section 2 - Nội dung chính]
- [Giữ tính độc lập: người đọc không cần mở file khác để hiểu logic cốt lõi]
- [Câu văn ngắn ≤25 từ, loại bỏ từ filler]

## [Section 3 - Kết luận/Khuyến nghị]
- [Tóm tắt điểm then chốt]
- [Cross-reference đến file liên quan nếu cần]

> [!AI-NOTE]
> Khi xử lý file này, AI phải:
> 1. Giữ nguyên giả định đầu vào đã nêu trong [[id-file-goc]]
> 2. Không tự sinh số liệu nếu không có nguồn trích dẫn
> 3. Ưu tiên cross-reference đến [[id-lien-quan-1]], [[id-lien-quan-2]]
> 4. Task downstream phù hợp: [tóm tắt | dịch | sinh code | phản biện]

---

## Ghi chú sử dụng template:
- Thay thế tất cả nội dung trong `[...]` bằng thông tin thực tế
- Xóa section không phù hợp với nội dung
- Đảm bảo tổng số dòng ≤300 (không tính frontmatter & comment)
- Kiểm tra checklist trước khi lưu file
