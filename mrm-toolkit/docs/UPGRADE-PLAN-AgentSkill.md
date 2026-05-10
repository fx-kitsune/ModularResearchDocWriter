---
id: upgrade-plan-agent-skill
title: "Kế hoạch nâng cấp ModularResearchDocWriter thành agent skill hoàn chỉnh"
status: draft
tags: [roadmap, agent-skill, modular-research-markdown, authoring-workflow]
summary: "Đánh giá hiện trạng ModularResearchDocWriter dưới góc nhìn agent skill viết tài liệu nghiên cứu, không phải chỉ là validator/toolkit kỹ thuật. Tài liệu đề xuất lộ trình biến skill thành workflow có contract, rubric, ví dụ, guardrails và lớp automation hỗ trợ."
ai_context: "Dùng cho AI hoặc maintainer triển khai nâng cấp ModularResearchDocWriter. Khi biến thành backlog, ưu tiên cải thiện prompt contract, workflow viết tài liệu, output format, self-check và integration guide trước khi mở rộng script validator."
ai_note: "Không diễn giải MRM như một CLI validator thuần túy. Validator chỉ là support tool; sản phẩm chính là skill giúp agent viết, chunk, cross-reference, assemble và tự kiểm tài liệu nghiên cứu."
---

# Kế hoạch nâng cấp ModularResearchDocWriter thành agent skill hoàn chỉnh

> **TL;DR**: Nâng cấp trọng tâm từ “script kiểm định Markdown” sang “agent skill viết tài liệu nghiên cứu module hóa”, trong đó validator chỉ là lớp hỗ trợ chất lượng.

## 1. Diễn giải đúng phạm vi dự án

ModularResearchDocWriter nên được hiểu là **MRM authoring skill cho agent**:

- Agent nhận yêu cầu nghiên cứu/tài liệu từ người dùng.
- Agent phân tích audience, depth, downstream AI task và ràng buộc xuất bản.
- Agent lập cây tài liệu theo atomic file structure.
- Agent viết từng module theo progressive disclosure.
- Agent gắn metadata để AI downstream hiểu ranh giới ngữ cảnh.
- Agent tạo cross-reference, index và bản assemble cuối.
- Agent tự kiểm trước khi trả output hoặc ghi file.

Script validator, index generator và assembler là **công cụ phụ trợ** để skill vận hành nhất quán; chúng không phải sản phẩm chính.

## 2. Chẩn đoán hiện trạng theo góc nhìn agent skill

| Mảng | Hiện có | Thiếu để thành skill agent hoàn chỉnh |
| --- | --- | --- |
| Skill identity | Có file skill prompt mô tả vai trò ModularResearchDocWriter. | Chưa có manifest mô tả capability, trigger, inputs, outputs, constraints và fallback behavior. |
| Authoring workflow | Có nguyên tắc atomicity, progressive disclosure, AI-native boundary và cross-reference. | Chưa tách thành state machine rõ: intake → plan → draft → link → assemble → self-review → deliver. |
| Output contract | Có template frontmatter và ví dụ chunk. | Chưa có contract cho nhiều chế độ trả về: `tree_only`, `stubs`, `full_docs`, `patch`, `assembled_report`. |
| Agent usability | Có prompt mẫu cho người dùng. | Chưa có cookbook tình huống, decision tree khi thiếu ngữ cảnh, hoặc policy hỏi lại vs tự giả định. |
| Quality rubric | Có checklist tự thẩm định. | Chưa có rubric chấm điểm đầu ra, severity lỗi và golden examples để regression-test skill. |
| Tool support | Có validator, generate-index và assemble script. | Chưa mô tả rõ agent gọi tool ở bước nào; automation đang lấn át định nghĩa skill. |
| Integration | Có guide tích hợp IDE/agents. | Cần viết lại quanh “agent authoring workflow”, không quanh CLI validation. |

## 3. Kiến trúc skill đề xuất

```text
ModularResearchDocWriter Skill
├── Skill contract
│   ├── capability: write modular research markdown
│   ├── trigger: user asks for research/doc/wiki/lab log/knowledge base
│   ├── inputs: domain, type, depth, audience, downstream task, sources
│   ├── outputs: tree, markdown modules, index, assembled report, review notes
│   └── guardrails: no unsupported facts, no broken refs, no monolithic docs
├── Authoring workflow
│   ├── 1_intake_context
│   ├── 2_plan_document_tree
│   ├── 3_write_atomic_modules
│   ├── 4_create_cross_references
│   ├── 5_generate_index_and_assembly
│   └── 6_self_review_and_delivery
├── Knowledge assets
│   ├── templates
│   ├── examples
│   ├── checklists
│   ├── rubrics
│   └── integration recipes
└── Support tools
    ├── frontmatter/link/TL;DR validation
    ├── line/token counting
    ├── index generation
    └── report assembly
```

## 4. Skill contract cần bổ sung

### 4.1 Inputs chuẩn

| Input | Bắt buộc | Mục đích |
| --- | --- | --- |
| `domain` | Có | Xác định thuật ngữ, loại nguồn và cấu trúc nội dung. |
| `doc_type` | Có | Chọn flow cho research paper, tech doc, internal wiki, lab log hoặc progress report. |
| `depth` | Có | Điều chỉnh mức chi tiết: executive, standard, deep dive. |
| `audience` | Có | Tối ưu readability cho người mới, chuyên gia, auditor hoặc AI pipeline. |
| `downstream_ai_task` | Có | Ghi vào `ai_context`/`ai_note` để giảm hallucination ở bước sau. |
| `source_policy` | Có nếu có dữ kiện | Quy định trích nguồn, xử lý missing source và không tự sinh số liệu. |
| `delivery_mode` | Có | Chọn trả tree, stubs, full docs, patch hoặc assembled report. |

### 4.2 Outputs chuẩn

Skill nên luôn trả theo một contract dễ parse:

1. **Assumptions**: giả định đã dùng và câu hỏi còn thiếu.
2. **Document tree**: cây file dự kiến trước khi viết nội dung dài.
3. **Module specs**: id, title, purpose, dependencies, downstream task.
4. **Markdown files**: nội dung từng file theo template MRM.
5. **Index draft**: navigation và trạng thái từng file.
6. **Assembly notes**: thứ tự ghép báo cáo và phần nào nên xuất bản.
7. **Self-review**: checklist pass/fail, cảnh báo link/source/line limit.

### 4.3 Modes cần hỗ trợ

| Mode | Khi dùng | Hành vi agent |
| --- | --- | --- |
| `plan_only` | Người dùng mới mô tả chủ đề lớn. | Chỉ trả scope, tree và module specs; chưa viết full docs. |
| `stub_first` | Cần review cấu trúc trước. | Tạo file stub với frontmatter, TL;DR placeholder rõ nghĩa và checklist. |
| `full_authoring` | Có đủ context và source. | Viết đầy đủ module, index và assembly notes. |
| `repair_existing` | Repo đã có tài liệu rời rạc. | Đọc file hiện có, đề xuất tách/đổi id/cross-reference, tránh rewrite không cần thiết. |
| `publish_ready` | Cần báo cáo cuối. | Assemble, chuẩn hóa headings, ghi chú phần chưa đủ nguồn. |

## 5. Roadmap nâng cấp

### Phase 0 — Chỉnh lại product narrative

**Mục tiêu**: Toàn bộ repo truyền đạt nhất quán rằng ModularResearchDocWriter là agent skill viết docs.

- Cập nhật README, integration guide và upgrade plan để tránh định vị sai là validator toolkit.
- Tách “skill layer” và “support tools layer” trong tài liệu.
- Bổ sung glossary: MRM, atomic note, AI-native boundary, downstream task, assembly.

**Acceptance criteria**:
- Người đọc mới hiểu flow chính là agent authoring trong 5 phút.
- Validator được mô tả là quality gate phụ trợ, không phải sản phẩm trung tâm.

### Phase 1 — Viết skill manifest và workflow spec

**Mục tiêu**: Agent biết khi nào kích hoạt skill và phải làm gì theo từng bước.

- Thêm `skill-manifest.md` hoặc `skill.yaml` mô tả capability, triggers, inputs, outputs, modes và constraints.
- Chuyển quy trình hiện có thành workflow 6 bước: intake, plan, draft, link, assemble, self-review.
- Thêm decision tree: hỏi lại khi thiếu nguồn, tự giả định khi chỉ thiếu preference, từ chối khi yêu cầu bịa số liệu.

**Acceptance criteria**:
- Có thể đưa manifest cho agent khác đọc và tái hiện cùng workflow.
- Mỗi bước có entry criteria, actions, exit criteria và artifact đầu ra.

### Phase 2 — Chuẩn hóa template, contract và rubric

**Mục tiêu**: Đầu ra của skill nhất quán giữa nhiều agent/lần chạy.

- Cập nhật frontmatter chuẩn để có `ai_context` và `ai_note` như mô tả dự án.
- Bổ sung template cho `index.md`, `module-spec.md`, `source-note.md`, `assembly-plan.md`.
- Viết output contract cho các modes: `plan_only`, `stub_first`, `full_authoring`, `repair_existing`, `publish_ready`.
- Thêm rubric tự chấm: structure, atomicity, source integrity, AI boundary, readability, integration readiness.

**Acceptance criteria**:
- Mỗi output có checklist cụ thể trước khi agent trả lời.
- Template đủ để agent tạo project MRM mới mà không cần suy diễn cấu trúc.

### Phase 3 — Xây example pack và evaluation set

**Mục tiêu**: Skill có ví dụ vàng để agent học cách áp dụng, đồng thời kiểm regression.

- Thêm 3-5 golden examples cho research paper, tech doc, internal wiki, lab log và knowledge base.
- Mỗi example gồm input prompt, expected tree, một số module mẫu, index và self-review.
- Thêm counter-examples: file monolithic, frontmatter thiếu `ai_note`, link placeholder, TL;DR quá dài.
- Thêm evaluation checklist để reviewer chấm output của agent.

**Acceptance criteria**:
- Agent mới có thể copy pattern từ examples mà không cần đọc toàn bộ repo.
- Reviewer có baseline để nói output nào đạt/chưa đạt MRM.

### Phase 4 — Tái thiết integration guide quanh agent workflow

**Mục tiêu**: Tích hợp vào IDE/agent theo quy trình viết docs, không chỉ gọi script validate.

- Viết recipe cho Cursor/Codex/Copilot/Obsidian: khi user yêu cầu viết docs thì load skill, tạo tree, xin xác nhận, ghi file, self-review.
- Định nghĩa handoff giữa agent và support tools: validator chạy sau draft, indexer sau link, assembler khi publish.
- Thêm prompt snippets cho các tình huống: tạo docs mới, refactor docs cũ, assemble report, review cross-ref.

**Acceptance criteria**:
- Integration guide có luồng end-to-end từ prompt người dùng đến file Markdown hoàn chỉnh.
- Các script được gọi đúng vai trò support quality gate.

### Phase 5 — Nâng cấp support tools đúng vai trò

**Mục tiêu**: Tooling củng cố skill chứ không thay thế skill.

- Đồng bộ validator với schema mới có `ai_note`.
- Thêm báo cáo JSON tùy chọn để agent đọc lỗi dễ hơn.
- Thêm lệnh hỗ trợ authoring: gợi ý split theo heading, phát hiện orphan note, tạo index theo module specs.
- Thêm test/fixtures cho validator dựa trên golden examples.

**Acceptance criteria**:
- Tool report trả về actionable feedback cho agent sửa docs.
- Không yêu cầu người dùng hiểu Python script để dùng skill ở mức cơ bản.

## 6. Backlog ưu tiên 2 tuần đầu

1. Đổi wording trong README và docs từ “toolkit validator” sang “agent authoring skill + support tools”.
2. Tạo `mrm-toolkit/docs/MRM-Skill-Manifest.md` với triggers, inputs, outputs, modes và guardrails.
3. Cập nhật template note để thêm `ai_note` và hướng dẫn downstream AI task.
4. Viết `mrm-toolkit/docs/MRM-Authoring-Workflow.md` mô tả workflow 6 bước cho agent.
5. Viết `mrm-toolkit/docs/MRM-Output-Contract.md` cho `plan_only`, `stub_first`, `full_authoring`, `repair_existing`, `publish_ready`.
6. Thêm `mrm-toolkit/examples/` với ít nhất 2 golden examples end-to-end.
7. Sau khi skill contract ổn định, mới nâng validator để kiểm được `ai_note`, output JSON và source/link policy.

## 7. Rủi ro và quyết định cần chốt

- **Nhầm trọng tâm sản phẩm**: Nếu tiếp tục ưu tiên CLI/package trước, repo sẽ thành validator rời rạc và không giải quyết bài toán agent viết docs.
- **Prompt quá dài**: Skill cần progressive disclosure cho chính instruction của nó; agent chỉ load phần liên quan theo mode.
- **Thiếu nguồn dữ liệu**: Skill phải có policy rõ khi thiếu source, không được tự tạo số liệu hoặc citation.
- **Quá nhiều output một lần**: Với chủ đề lớn, nên bắt đầu bằng `plan_only` hoặc `stub_first` rồi mới viết full modules.
- **Không đồng bộ template và validator**: Khi thêm `ai_note`, template, skill prompt và validator phải cùng cập nhật.

## 8. Definition of Done cho agent skill hoàn chỉnh

Repo đạt trạng thái agent skill hoàn chỉnh khi:

- Skill có manifest rõ capability, trigger, inputs, outputs, modes và guardrails.
- Agent có workflow authoring end-to-end từ yêu cầu người dùng đến module Markdown, index và báo cáo assemble.
- Template và output contract bắt buộc có `ai_context`, `ai_note`, status, tags, TL;DR và cross-reference policy.
- Có golden examples và rubric để đánh giá chất lượng output của agent.
- Integration guide hướng dẫn IDE/agent load skill, viết docs, gọi support tools và tự review.
- Validator/indexer/assembler được mô tả và nâng cấp như support tools phục vụ skill, không phải điểm dùng chính.
