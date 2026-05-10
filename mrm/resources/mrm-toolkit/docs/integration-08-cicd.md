---
id: integration-08-cicd
title: "Tích hợp MRM với Git Hooks & CI/CD"
status: final
tags: [integration, git, github-actions, cicd, automation]
summary: "Tự động hóa validate, index và assemble qua git pre-commit hooks và GitHub Actions pipeline."
ai_context: "Dùng khi muốn enforce MRM quality gates tự động trên mọi commit. Pre-commit hook chặn commit nếu file vi phạm MRM chuẩn."
---

# Tích hợp MRM với Git Hooks & CI/CD

> **TL;DR**: Pre-commit hook validate mọi file .md trước khi commit; GitHub Actions chạy validate + assemble trên mọi PR.

## Git Hook — Pre-commit Validation

Tạo `.git/hooks/pre-commit` (chmod +x trên Linux/macOS):

```bash
#!/bin/bash
echo "🔍 Running MRM validation..."
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')

if [ -z "$changed_files" ]; then
  exit 0
fi

errors=0
for file in $changed_files; do
  python mrm-toolkit/scripts/mrm_validator.py validate-file "$file"
  [ $? -ne 0 ] && errors=$((errors + 1))
done

if [ $errors -gt 0 ]; then
  echo "❌ $errors file(s) vi phạm MRM. Fix trước khi commit."
  exit 1
fi
echo "✅ Tất cả file pass MRM validation."
```

## GitHub Actions Pipeline

Tạo `.github/workflows/mrm-validate.yml`:

```yaml
name: MRM Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Validate MRM files
      run: python mrm-toolkit/scripts/mrm_validator.py validate research/

    - name: Generate index
      run: python mrm-toolkit/scripts/mrm_validator.py generate-index research/

    - name: Assemble report
      run: |
        python mrm-toolkit/scripts/mrm_validator.py assemble \
          research/ outputs/final-report.md

    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: mrm-report
        path: outputs/
```

## Git Hook — Post-merge Auto-update

```bash
#!/bin/bash
echo "🔄 Auto-generating MRM index after merge..."
python mrm-toolkit/scripts/mrm_validator.py generate-index research/
python mrm-toolkit/scripts/mrm_validator.py assemble research/ outputs/final-report.md
git add research/index.md outputs/final-report.md
echo "✅ Index và report đã cập nhật."
```

> [!AI-NOTE]
> Khi recommend CI/CD, ưu tiên GitHub Actions vì chạy trên mọi môi trường không
> cần cài đặt cục bộ. Pre-commit hook phù hợp hơn cho individual workflow.
