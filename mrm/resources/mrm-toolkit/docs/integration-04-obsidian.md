---
id: integration-04-obsidian
title: "Tích hợp MRM với Obsidian"
status: final
tags: [integration, obsidian, templater, dataview, quickadd]
summary: "Cấu hình Obsidian với Templater, QuickAdd và Dataview để dùng MRM trong personal knowledge base."
ai_context: "Dùng khi người dùng muốn MRM workflow trong Obsidian. Wikilink [[id]] trong MRM tương thích tự nhiên với Obsidian graph view."
---

# Tích hợp MRM với Obsidian

> **TL;DR**: MRM wikilink `[[id]]` tương thích hoàn toàn với Obsidian — cài Templater + Dataview để có workflow đầy đủ.

## Plugins cần thiết

```
✅ Templater
✅ Dataview
✅ QuickAdd
✅ Periodic Notes
✅ Various Complements
```

## Templater — MRM Note Template

Tạo `Templates/MRM/MRM-Note-Template.md`:

```markdown
---
id: <% tp.file.title | slugify %>
title: "<% tp.file.title %>"
status: draft
tags: []
summary: ""
ai_context: ""
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
---

# <% tp.file.title %>

> **TL;DR**: <% tp.system.prompt("TL;DR - 1 dòng kết luận") %>

## <% tp.system.prompt("Heading đầu tiên") %>



> [!AI-NOTE]
> <% tp.system.prompt("Hướng dẫn cho AI downstream") %>
```

## QuickAdd — Tạo MRM Note nhanh

```javascript
// QuickAdd script: CreateMRMNote.js
module.exports = async (params) => {
  const title = await params.quickAddApi.inputPrompt("Note title?");
  const folder = await params.quickAddApi.inputPrompt("Folder? (core/meta/notes)");
  const id = `${folder}-${Date.now().toString().slice(-4)}`;
  const path = `research/${folder}/${id}-${title}.md`;
  await params.quickAddApi.fileSystem.createFile(path, "");
  await params.quickAddApi.fileSystem.openFile(path);
};
```

## Dataview Dashboard

```dataview
TABLE status, created
FROM "research"
WHERE contains(file.path, "research/")
SORT created DESC
```

```dataview
LIST FROM "research" WHERE status = "draft" SORT updated ASC
```

## Hotkeys

| Action | Phím tắt |
|--------|----------|
| Insert template | `Ctrl+Alt+N` |
| Create MRM Note | `Ctrl+Alt+M` |
| Refresh queries | `Ctrl+Alt+R` |

> [!AI-NOTE]
> MRM `[[frontmatter-id]]` và Obsidian wikilink dùng cùng cú pháp — graph view
> tự động hiển thị mạng lưới cross-reference giữa các module MRM.
