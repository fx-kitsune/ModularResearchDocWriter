---
id: core-02-progressive-disclosure
title: "Progressive Disclosure - Trình bày Thông tin Phân tầng"
status: draft
tags: [ux, readability, structure]
summary: "Pattern trình bày thông tin theo lớp từ tổng quan đến chi tiết, giúp người đọc không bị quá tải."
ai_context: "Dùng cho AI tóm tắt tài liệu dài. Luôn bắt đầu bằng TL;DR trước khi đi vào chi tiết."
---

# Progressive Disclosure - Trình bày Thông tin Phân tầng

> **TL;DR**: Thông tin được trình bày theo 4 lớp: Summary → TL;DR → Nội dung chính → Phụ lục.

## Tại sao cần Progressive Disclosure?

Não người xử lý thông tin theo cơ chế "chunking" - nhóm nhỏ từng phần. File dài 1000+ dòng gây:

- **Overwhelm**: Người đọc không biết bắt đầu từ đâu
- **Mất tập trung**: Khó xác định thông tin ưu tiên
- **Bỏ sót**: Section quan trọng bị lướt qua

## 4 Lớp Thông tin Chuẩn

### Lớp 1: Summary (Frontmatter)

```yaml
summary: "1-2 câu mô tả phạm vi & đóng góp của file này."
```

**Mục đích**: Giúp AI và người đọc hiểu nhanh ngữ cảnh.

### Lớp 2: TL;DR (Blockquote)

```markdown
> **TL;DR**: 1 dòng nêu kết luận/lựa chọn chính. Không giải thích thêm.
```

**Mục đích**: Dành cho người bận rộn, chỉ cần kết quả cuối cùng.

### Lớp 3: Nội dung Chính (Headings H2-H3)

- Cô đọng, mỗi section ≤50 dòng
- Dùng bảng so sánh khi có ≥3 yếu tố
- Bullet points thay vì paragraph dài

### Lớp 4: Phụ lục/Chi tiết (Appendix)

- Data raw, code snippets dài
- Tham khảo bổ sung
- Link đến file con nếu cần mở rộng

## Pattern Áp dụng

### Pattern A: Tài liệu Kỹ thuật

```
1. Summary (frontmatter)
2. TL;DR - Giải pháp được chọn
3. Vấn đề & Yêu cầu
4. Giải pháp Chi tiết
5. Benchmark/Kết quả
6. Appendix: Code, Config
```

### Pattern B: Research Paper

```
1. Summary (frontmatter)
2. TL;DR - Phát hiện chính
3. Abstract
4. Methodology
5. Results
6. Discussion
7. References (file riêng)
```

### Pattern C: Báo cáo Tiến độ

```
1. Summary (frontmatter)
2. TL;DR - Status: On track / At risk
3. Completed (tuần này)
4. Next Steps (tuần tới)
5. Blockers/Risks
6. Metrics/KPIs
```

## Anti-Patterns Cần Tránh

| Sai lầm | Hậu quả | Cách sửa |
|---------|---------|----------|
| TL;DR dài >2 dòng | Mất tác dụng tóm tắt | Cắt xuống 1 dòng |
| Summary kỹ thuật quá mức | Người mới không hiểu | Viết cho audience rộng |
| Nhồi nhét chi tiết vào section chính | Quá tải nhận thức | Đẩy xuống appendix |
| Không có hierarchy rõ | Khó điều hướng | Dùng heading đúng cấp |

## Checklist Áp dụng

- [ ] Frontmatter có `summary` ≤2 câu?
- [ ] TL;DR xuất hiện ngay sau title?
- [ ] TL;DR ≤1 dòng, không giải thích?
- [ ] Nội dung chính chia thành sections ≤50 dòng?
- [ ] Chi tiết dài đã đẩy xuống appendix hoặc file con?
- [ ] Có bảng/mục lục cho section dài?

> [!AI-NOTE]
> Khi tóm tắt file dài, AI phải:
> 1. Đọc TL;DR trước tiên để nắm ý chính
> 2. Nếu không có TL;DR → Tự sinh từ nội dung
> 3. Ưu tiên giữ lại conclusions và recommendations
> 4. Đẩy chi tiết kỹ thuật xuống appendix trong summary
> 5. Task downstream: executive-summary, slide-generation

## Tài liệu Liên quan

- [[meta-01-project-overview]] - Tổng quan MRM Framework (✅ tồn tại)
- [[core-01-atomic-structure]] - Atomic file structure (✅ tồn tại)
- [[core-03-frontmatter-standard]] - Chuẩn frontmatter chi tiết (sẽ tạo)

> [!NOTE] Wikilink có thể trỏ đến file chưa tồn tại - đây là placeholder cho nội dung tương lai.
