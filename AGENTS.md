# AGENTS.md

Instructions for AI coding agents working **in this repository** (Claude Code, Codex, Cursor, Gemini CLI, Antigravity and others).

## What this repo is
A library of **Agent Skills** (`skills/<name>/SKILL.md`) and **slash commands** (`commands/*.md`) for software testing and QA, plus tooling that generates the README catalog, per-tool command adapters and the GitHub Pages site.

## Golden rules
1. **Source of truth is `skills/` and `commands/`.** Never hand-edit generated files: `README.md` marked blocks, `adapters/**`, `.claude-plugin/*.json`, `_site/**`.
2. After changing skills or commands run, in this order:
   ```bash
   python3 scripts/build_adapters.py
   python3 scripts/build_readme.py
   python3 tests/validate_skills.py
   ```
   All must succeed before you commit. CI runs the same checks.
3. Python scripts are **stdlib only** and must run on Python 3.9+. Do not add dependencies.
4. `install.sh` must stay Bash 3.2 compatible (macOS) and must never overwrite files it did not create.

## Writing or editing a skill
- Path: `skills/<kebab-case-name>/SKILL.md`; the directory name must equal `name`.
- Frontmatter (required): `name`, `description`, `license`, and `metadata` with `category` (one of the ids in `scripts/stsk.py` `CATEGORIES`), `version`, `tags`.
- `description` is the routing key: start with **"Use when …"**, list concrete triggers and keywords, stay under 1024 characters, no marketing language.
- Body: a `# Title`, when to use / not use, a procedure, real copy-paste commands, checklists, pitfalls, and a `## Related` line listing other skills in backticks (each must exist).
- Be specific and correct: real flags, real tool names, no invented APIs. Prefer tables and checklists over prose. Target 60–150 lines; move long material to `references/*.md`.
- Security-related skills must state the authorization requirement and keep the guidance defensive.
- New skills must also be added to the routing table in `skills/qa-skill-router/SKILL.md` (the validator enforces this).

## Writing or editing a command
- `commands/<verb-noun>.md` with frontmatter `description` (≤ 100 chars) and a **quoted** `argument-hint`.
- The body is instructions *for the agent*, uses `$ARGUMENTS`, names the skills it uses as ``Use the `skill-a` and `skill-b` skills.`` and ends with a concrete output.
- Regenerate adapters afterwards.

## Using these skills in a project (for agents reading this file elsewhere)
For any testing, QA, test-planning or test-review task, first consult `skills/qa-skill-router/SKILL.md` and load the 1–3 skills it points to. Run security and load tests only against systems the user owns or is authorized to test.
