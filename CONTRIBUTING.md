# Contributing to Software Tester Skills

We welcome contributions from QA engineers, SDETs, and software testers worldwide!

This repository follows the open **Agent Skills specification** ([agentskills.io](https://agentskills.io/specification)), ensuring that all skills work seamlessly across Google Antigravity, Claude Code, OpenAI Codex, Cursor, Gemini CLI, OpenCode, and others.

---

## 🛠️ Adding a New Skill

1. **Create a Directory**: Under `skills/<your-skill-name>/` (use lowercase, numbers, and hyphens only).
2. **Create `SKILL.md`**: Each skill requires a `SKILL.md` file.
3. **YAML Frontmatter**:
   ```yaml
   ---
   name: your-skill-name
   description: Use when [specific triggering symptoms or conditions]
   ---
   ```
   - **`name`**: Must match the folder name exactly.
   - **`description`**: Must start with `"Use when..."` and clearly state when an AI agent should trigger this skill. Do NOT simply summarize the workflow; describe the triggering conditions.
4. **Skill Content**:
   - Write clear, practical, production-grade instructions.
   - Include checklists, anti-patterns, heuristics, and recommended tooling.
   - Include runnable code snippets where relevant.

---

## 🧪 Validating Your Changes

Before submitting a Pull Request, run the local validation suite:

```bash
python3 tests/validate_skills.py
```

All skills must pass validation without errors.
