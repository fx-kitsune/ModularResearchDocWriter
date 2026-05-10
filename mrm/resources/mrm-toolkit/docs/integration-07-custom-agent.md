---
id: integration-07-custom-agent
title: "Tích hợp MRM qua Custom Agent API"
status: final
tags: [integration, api, python, openai, custom-agent]
summary: "Xây dựng agent Python tùy chỉnh dùng OpenAI API để tự động hóa toàn bộ MRM workflow."
ai_context: "Dùng khi cần production pipeline tự động hóa hoàn toàn. Code mẫu dưới đây chỉ để minh họa kiến trúc — thay api_key và model phù hợp."
---

# Tích hợp MRM qua Custom Agent API

> **TL;DR**: Tạo class `MRMAgent` bọc OpenAI API để tự động generate structure, viết file, validate và assemble.

## Kiến trúc agent

```python
# agents/mrm_agent.py
import json
import openai
from pathlib import Path

class MRMAgent:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        skill_path = Path("mrm-toolkit/skills/modular-research-doc-writer/SKILL.md")
        self.system_prompt = skill_path.read_text(encoding="utf-8")

    def generate_structure(self, topic: str) -> dict:
        """Đề xuất cấu trúc thư mục MRM."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Đề xuất cấu trúc MRM cho: {topic}"},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    def write_file(self, file_id: str, topic: str, cross_refs: list = None) -> str:
        """Viết một file MRM."""
        prompt = (
            f"Viết file MRM: id={file_id}, chủ đề={topic}, "
            f"cross-refs={cross_refs or []}. Output: full markdown."
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    def full_workflow(self, topic: str, output_dir: str) -> None:
        """Chạy toàn bộ workflow MRM tự động."""
        structure = self.generate_structure(topic)
        for module in structure["modules"]:
            content = self.write_file(
                file_id=module["id"],
                topic=module["topic"],
                cross_refs=module.get("cross_refs", []),
            )
            path = Path(output_dir) / f"{module['id']}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        # Validate sau khi sinh xong
        import subprocess
        subprocess.run(
            ["python", "mrm-toolkit/scripts/mrm_validator.py", "validate", output_dir]
        )
```

## Sử dụng

```python
from agents.mrm_agent import MRMAgent

agent = MRMAgent(api_key="your-key")
agent.full_workflow(
    topic="Retrieval Augmented Generation for Enterprise Knowledge Base",
    output_dir="research/",
)
```

> [!AI-NOTE]
> Code trên là skeleton để minh họa kiến trúc. Khi triển khai production cần thêm:
> retry logic, rate limiting, error handling per-file, và validation sau mỗi file
> thay vì chỉ sau khi xong tất cả.
