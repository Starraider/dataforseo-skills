#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-.}"

python3 - "$REPO_ROOT" <<'PY'
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
errors = []

def require(path: str) -> Path:
    target = root / path
    if not target.exists():
        errors.append(f"missing required path: {path}")
    return target

for path in (
    "README.md",
    "LICENSE-MIT",
    "LICENSE-CC-BY-SA-4.0",
    ".gitignore",
    ".claude-plugin/plugin.json",
    ".github/workflows/release.yml",
    "composer.json",
    "package.json",
):
    require(path)

if (root / "LICENSE").exists():
    errors.append("bare LICENSE is forbidden; use the two split-license files")
if (root / "composer.lock").exists():
    errors.append("composer.lock must not be committed")

try:
    plugin = json.loads((root / ".claude-plugin/plugin.json").read_text())
except Exception as exc:
    errors.append(f"invalid plugin.json: {exc}")
    plugin = {}

skill_paths = plugin.get("skills", [])
if not isinstance(skill_paths, list) or not skill_paths:
    errors.append("plugin.json skills must be a non-empty array")
    skill_paths = []
if plugin.get("license") != "(MIT AND CC-BY-SA-4.0)":
    errors.append("plugin.json has an invalid license")
if plugin.get("author", {}).get("url", "").rstrip("/") != "https://www.skom.de":
    errors.append("plugin.json author.url must be https://www.skom.de")

allowed_frontmatter = {
    "name", "description", "license", "compatibility", "metadata", "allowed-tools"
}
registered_skills = []
for relative in skill_paths:
    skill_file = root / relative / "SKILL.md"
    if not skill_file.is_file():
        errors.append(f"missing registered skill: {skill_file.relative_to(root)}")
        continue
    text = skill_file.read_text()
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:30]:
        errors.append(f"invalid frontmatter delimiters: {skill_file.relative_to(root)}")
        continue
    closing = lines[1:30].index("---") + 1
    frontmatter = lines[1:closing]
    fields = {
        match.group(1): match.group(2).strip().strip('"')
        for line in frontmatter
        if (match := re.match(r"^([a-z_-]+):\s*(.*)$", line))
    }
    extra = set(fields) - allowed_frontmatter
    if extra:
        errors.append(f"unsupported frontmatter fields in {relative}: {sorted(extra)}")
    name = fields.get("name", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        errors.append(f"invalid skill name in {relative}: {name!r}")
    elif name != Path(relative).name:
        errors.append(f"skill name does not match directory in {relative}: {name!r}")
    else:
        registered_skills.append(name)
    if not fields.get("description", "").startswith("Use when"):
        errors.append(f"description must start with 'Use when' in {relative}")
    if len(re.findall(r"\S+", text)) > 500:
        errors.append(f"SKILL.md exceeds 500 words: {relative}")

for name in registered_skills:
    readme_path = require(f"skills/{name}/README.md")
    eval_path = require(f"skills/{name}/evals/evals.json")
    agent_path = require(f"agents/{name}.yaml")
    metadata_path = require(f"metadata/{name}.yaml")

    if readme_path.is_file() and not readme_path.read_text().startswith("# "):
        errors.append(f"skill README must begin with an H1: skills/{name}/README.md")
    if readme_path.is_file() and "\n## Why this analysis matters\n" not in readme_path.read_text():
        errors.append(f"skill README is missing '## Why this analysis matters': skills/{name}/README.md")
    if metadata_path.is_file() and f"slug: {name}\n" not in metadata_path.read_text():
        errors.append(f"distribution metadata slug mismatch: metadata/{name}.yaml")
    if agent_path.is_file() and "interface:\n" not in agent_path.read_text():
        errors.append(f"agent metadata is missing interface: agents/{name}.yaml")

    if eval_path.is_file():
        try:
            eval_data = json.loads(eval_path.read_text())
        except Exception as exc:
            errors.append(f"invalid eval JSON for {name}: {exc}")
            continue
        if eval_data.get("skill_name") != name:
            errors.append(f"eval skill_name mismatch for {name}")
        evals = eval_data.get("evals")
        if not isinstance(evals, list) or not evals:
            errors.append(f"evals must be a non-empty array for {name}")
            continue
        seen_ids = set()
        for index, item in enumerate(evals):
            label = f"{name} eval {index}"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object")
                continue
            eval_id = item.get("id")
            if eval_id in seen_ids:
                errors.append(f"duplicate eval id for {name}: {eval_id!r}")
            seen_ids.add(eval_id)
            for field in ("prompt", "expected_output"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f"{label} has invalid {field}")
            if not isinstance(item.get("files"), list):
                errors.append(f"{label} files must be an array")
            assertions = item.get("assertions")
            if assertions is not None and (
                not isinstance(assertions, list)
                or not assertions
                or not all(isinstance(value, str) and value.strip() for value in assertions)
            ):
                errors.append(f"{label} assertions must be a non-empty string array when present")

for path in (
    "skills/seo-page-metadata/references/data-contract.md",
    "skills/seo-page-metadata/templates/report-template.md",
    "skills/seo-page-metadata/scripts/metadata_support.py",
    "skills/seo-page-metadata/tests/fixtures/onpage_success.json",
    "skills/seo-page-metadata/tests/fixtures/related_keywords_success.json",
    "skills/seo-page-metadata/tests/test_metadata_support.py",
    "skills/seo-full-report/references/report-contract.md",
    "skills/seo-full-report/templates/report-template.md",
    "skills/seo-full-report/scripts/select_reports.py",
    "skills/seo-ranking-watchlist/scripts/rank_watchlist_api.py",
    "skills/seo-ranking-watchlist/tests/test_rank_watchlist_api.py",
    "skills/seo-full-report/tests/test_select_reports.py",
):
    require(path)

try:
    composer = json.loads((root / "composer.json").read_text())
except Exception as exc:
    errors.append(f"invalid composer.json: {exc}")
    composer = {}
if composer.get("name") != "Starraider/dataforseo-skills":
    errors.append("composer package name must be Starraider/dataforseo-skills")
if composer.get("type") != "ai-agent-skill":
    errors.append("composer type must be ai-agent-skill")
if composer.get("license") != "(MIT AND CC-BY-SA-4.0)":
    errors.append("composer license is invalid")
composer_skills = composer.get("extra", {}).get("ai-agent-skill", [])
if isinstance(composer_skills, str):
    composer_skills = [composer_skills]
for path in composer_skills:
    if not (root / path).is_file():
        errors.append(f"composer skill path does not exist: {path}")

try:
    package = json.loads((root / "package.json").read_text())
except Exception as exc:
    errors.append(f"invalid package.json: {exc}")
    package = {}
npm_skills = package.get("aiAgentSkill", [])
if isinstance(npm_skills, str):
    npm_skills = [npm_skills]
if not isinstance(npm_skills, list) or not npm_skills:
    errors.append("package.json aiAgentSkill must be a non-empty path or array")
    npm_skills = []
for path in npm_skills:
    if not (root / path).is_file():
        errors.append(f"npm skill path does not exist: {path}")

plugin_files = {str(Path(path) / "SKILL.md").removeprefix("./") for path in skill_paths}
if plugin_files != set(composer_skills):
    errors.append("plugin.json and composer.json register different skills")
if plugin_files != set(npm_skills):
    errors.append("plugin.json and package.json register different skills")

readme = (root / "README.md").read_text() if (root / "README.md").exists() else ""
for heading in (
    "What this skill solves", "Use when", "Expected outputs", "Context requirements",
    "Example prompts", "Related skills", "Installation", "Contributing", "License",
):
    if f"## {heading}\n" not in readme:
        errors.append(f"README is missing exact heading: ## {heading}")

if errors:
    print("Skill repository validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Skill repository is valid: {len(skill_paths)} registered skill(s)")
PY

python3 "$REPO_ROOT/skills/seo-technical-page-audit/tests/test_fetch_task_onpage_fixture.py"
python3 "$REPO_ROOT/skills/seo-page-metadata/tests/test_metadata_support.py"
python3 "$REPO_ROOT/skills/seo-full-report/tests/test_select_reports.py"
python3 "$REPO_ROOT/skills/seo-ranking-watchlist/tests/test_rank_watchlist_api.py"
