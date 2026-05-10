# ModularResearchDocWriter

ModularResearchDocWriter là **agent skill/framework** để hướng dẫn AI viết, tách module, kiểm định và lắp ráp tài liệu nghiên cứu dạng Markdown theo chuẩn Modular Research Markdown (MRM). Trọng tâm của repo là năng lực authoring cho agent, không phải chỉ là một validator CLI.

## Điểm vào chính

- Skill prompt: [`mrm-toolkit/docs/MRM-Skill-ModularResearchDocWriter.md`](mrm-toolkit/docs/MRM-Skill-ModularResearchDocWriter.md)
- Toolkit hỗ trợ skill: [`mrm-toolkit/README.md`](mrm-toolkit/README.md)
- Integration guide: [`mrm-toolkit/integration/AGENT-INTEGRATION-GUIDE.md`](mrm-toolkit/integration/AGENT-INTEGRATION-GUIDE.md)
- Upgrade plan theo hướng agent skill: [`mrm-toolkit/docs/UPGRADE-PLAN-AgentSkill.md`](mrm-toolkit/docs/UPGRADE-PLAN-AgentSkill.md)

## Hướng nâng cấp đề xuất

Repo hiện đã có prompt/skill, template, research tree mẫu và script hỗ trợ, nhưng skill contract cho agent viết docs vẫn còn rời rạc: thiếu workflow manifest, output contract, rubric tự kiểm, cookbook tình huống và bộ ví dụ đánh giá. Kế hoạch nâng cấp tập trung biến ModularResearchDocWriter thành skill agent hoàn chỉnh để nhận yêu cầu nghiên cứu, lập outline, tạo atomic notes, cross-reference, assemble báo cáo và tự phản biện chất lượng đầu ra.
