#!/usr/bin/env python3
"""Validate the whole repository (stdlib only). Exit 1 on any error.

Checks
  skills    Agent Skills format, category/tags/license metadata, description length,
            relative links, `Related` cross-references, size sanity
  commands  frontmatter, referenced skills exist, argument hint quoted
  router    qa-skill-router mentions every skill
  manifests plugin.json / marketplace.json valid, versions and counts in sync
  readme    skill/command counts and generated catalog are current
  adapters  generated per-tool command files are current
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import stsk  # noqa: E402

errors, warnings = [], []
err = errors.append
warn = warnings.append
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def check_skills(skills):
    names = {s["name"] for s in skills}
    for s in skills:
        d, f = s["dir"], stsk.SKILLS_DIR / s["dir"] / "SKILL.md"
        text = f.read_text(encoding="utf-8")
        fm, _ = stsk.parse_frontmatter(text)
        if fm is None:
            err(f"{d}: SKILL.md must start with YAML frontmatter"); continue
        if fm.get("name") != d:
            err(f"{d}: frontmatter name '{fm.get('name')}' != directory name")
        if not NAME_RE.match(d) or len(d) > 64:
            err(f"{d}: name must be kebab-case, <= 64 chars")
        desc = fm.get("description", "")
        if not desc:
            err(f"{d}: missing description"); continue
        if len(desc) > 1024:
            err(f"{d}: description is {len(desc)} chars (max 1024)")
        if len(desc) < 60:
            err(f"{d}: description too short to route on ({len(desc)} chars)")
        if not re.match(r"^Use (when|whenever|this|for|to)\b", desc):
            warn(f"{d}: description should start with 'Use when …' so agents route on it")
        if fm.get("license") is None:
            err(f"{d}: missing license")
        meta = fm.get("metadata")
        if not isinstance(meta, dict):
            err(f"{d}: missing metadata block (category, version, tags)")
        else:
            if meta.get("category") not in stsk.CATEGORIES:
                err(f"{d}: metadata.category '{meta.get('category')}' not in {sorted(stsk.CATEGORIES)}")
            if not meta.get("tags"):
                err(f"{d}: metadata.tags is empty")
            if not meta.get("version"):
                err(f"{d}: metadata.version missing")
        body = s["body"]
        if not re.search(r"^# .+", body, re.M):
            err(f"{d}: body needs a top-level '# Title'")
        if s["lines"] < 20:
            warn(f"{d}: only {s['lines']} lines; consider deepening")
        for m in re.finditer(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", body):
            target = (f.parent / m.group(1).split("#")[0]).resolve()
            if not target.exists():
                err(f"{d}: broken relative link -> {m.group(1)}")
        for m in re.finditer(r"\[\[([a-z0-9-]+)\]\]", body):
            if m.group(1) not in names:
                err(f"{d}: [[{m.group(1)}]] refers to an unknown skill")
        rel = re.search(r"^## Related( skills)?\s*\n(.+?)(?:\n## |\Z)", body, re.M | re.S)
        if rel:
            for ref in re.findall(r"`([a-z0-9-]+)`", rel.group(2)):
                if ref not in names:
                    err(f"{d}: Related section references unknown skill `{ref}`")
                if ref == d:
                    warn(f"{d}: Related section references itself")
        for extra in s["extras"]:
            if extra.endswith(".md") and not (stsk.SKILLS_DIR / d / extra).stat().st_size:
                err(f"{d}: empty reference file {extra}")


def check_commands(commands, skills):
    names = {s["name"] for s in skills}
    if not commands:
        err("no commands found in commands/")
    for c in commands:
        n = c["name"]
        if not NAME_RE.match(n):
            err(f"command {n}: name must be kebab-case")
        if not c["description"] or len(c["description"]) > 100:
            err(f"command {n}: description missing or > 100 chars")
        raw = (stsk.COMMANDS_DIR / f"{n}.md").read_text(encoding="utf-8")
        if not re.search(r'^argument-hint: ".*"$', raw, re.M):
            err(f"command {n}: argument-hint must be a quoted string")
        if n in names:
            warn(f"command {n}: same name as a skill (Antigravity invokes skills as /<name>)")
        used = set()
        for line in c["body"].splitlines():
            if re.match(r"^Use the .*skills?", line):
                used |= set(re.findall(r"`([a-z0-9-]+)`", line))
        if not used:
            err(f"command {n}: does not reference any skill with 'Use the `skill` skill'")
        for u in used:
            if u not in names:
                err(f"command {n}: references unknown skill `{u}`")
        if "$ARGUMENTS" not in c["body"] and n != "qa-help":
            warn(f"command {n}: does not use $ARGUMENTS")


def check_router(skills):
    f = stsk.SKILLS_DIR / "qa-skill-router" / "SKILL.md"
    if not f.exists():
        err("qa-skill-router skill missing"); return
    text = f.read_text(encoding="utf-8")
    for s in skills:
        if s["name"] != "qa-skill-router" and f"`{s['name']}`" not in text:
            err(f"qa-skill-router does not route to `{s['name']}`")


def check_manifests(skills, commands):
    plugin = stsk.ROOT / ".claude-plugin" / "plugin.json"
    market = stsk.ROOT / ".claude-plugin" / "marketplace.json"
    data = {}
    for p in (plugin, market):
        try:
            data[p.name] = json.loads(p.read_text(encoding="utf-8"))
        except Exception as ex:  # noqa: BLE001
            err(f"{p.name}: invalid JSON ({ex})")
    if len(data) == 2:
        pv = data["plugin.json"].get("version")
        mv = data["marketplace.json"]["plugins"][0].get("version")
        if pv != mv:
            err(f"plugin.json version {pv} != marketplace.json plugin version {mv}")
        for label, desc in (("plugin.json", data["plugin.json"].get("description", "")),
                            ("marketplace.json", data["marketplace.json"]["plugins"][0].get("description", ""))):
            if str(len(skills)) not in desc:
                err(f"{label}: description should mention the current skill count ({len(skills)})")
    if not (stsk.ROOT / "commands").is_dir():
        err("commands/ directory missing (needed by the Claude Code plugin)")


def check_readme(skills, commands):
    r = (stsk.ROOT / "README.md").read_text(encoding="utf-8")
    if "<!-- catalog:start -->" not in r or "<!-- catalog:end -->" not in r:
        err("README.md is missing catalog markers"); return
    res = subprocess.run([sys.executable, str(stsk.ROOT / "scripts" / "build_readme.py"), "--check"],
                         capture_output=True, text=True)
    if res.returncode:
        err("README catalog out of date; run: python3 scripts/build_readme.py")


def check_adapters():
    res = subprocess.run([sys.executable, str(stsk.ROOT / "scripts" / "build_adapters.py"), "--check"],
                         capture_output=True, text=True)
    if res.returncode:
        err(res.stdout.strip() or "adapters out of date")


def main():
    strict = "--strict" in sys.argv
    skills, commands = stsk.load_skills(), stsk.load_commands()
    check_skills(skills)
    check_commands(commands, skills)
    check_router(skills)
    check_manifests(skills, commands)
    if (stsk.ROOT / "scripts" / "build_readme.py").exists():
        check_readme(skills, commands)
    if (stsk.ROOT / "scripts" / "build_adapters.py").exists():
        check_adapters()

    print("=== software-tester-skills validation ===")
    print(f"skills: {len(skills)}   commands: {len(commands)}   errors: {len(errors)}   warnings: {len(warnings)}")
    for w in warnings:
        print(f"  warn  {w}")
    for x in errors:
        print(f"  ERROR {x}")
    if errors or (strict and warnings):
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
