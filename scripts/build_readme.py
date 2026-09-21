#!/usr/bin/env python3
"""Regenerate the generated parts of README.md and the plugin manifests.

  python3 scripts/build_readme.py           # write
  python3 scripts/build_readme.py --check   # exit 1 if anything is stale (used by CI)

Generated blocks in README.md (edit everything else by hand):
  <!-- tagline:start --> ... <!-- tagline:end -->
  <!-- badges:start --> ... <!-- badges:end -->
  <!-- commands:start --> ... <!-- commands:end -->
  <!-- catalog:start --> ... <!-- catalog:end -->
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stsk  # noqa: E402

README = stsk.ROOT / "README.md"
PLUGIN = stsk.ROOT / ".claude-plugin" / "plugin.json"
MARKET = stsk.ROOT / ".claude-plugin" / "marketplace.json"
VERSION = "2.0.0"


def badges(n, c):
    r = stsk.REPO
    return "\n".join([
        f"[![CI](https://github.com/{r}/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/{r}/actions/workflows/validate-skills.yml)",
        f"[![Skills](https://img.shields.io/badge/skills-{n}-0B6B52.svg)]({stsk.SITE_URL}/#skills)",
        f"[![Slash commands](https://img.shields.io/badge/slash%20commands-{c}-0B5CAD.svg)](#-slash-commands)",
        "[![Agent Skills](https://img.shields.io/badge/standard-agentskills.io-101A2B.svg)](https://agentskills.io)",
        f"[![Website](https://img.shields.io/badge/website-live-8A5A00.svg)]({stsk.SITE_URL}/)",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)",
        f"[![Stars](https://img.shields.io/github/stars/{r}?style=flat&logo=github)](https://github.com/{r}/stargazers)",
    ])


def tagline(n, c):
    return (f"**{n} open-source Agent Skills and {c} slash commands** for unit, API, end-to-end, security, performance, "
            "accessibility, data, mobile, AI/LLM testing and more. Works in **Claude Code, Google Antigravity, Gemini CLI, "
            "OpenAI Codex and Cursor**.")


def commands_table(commands):
    rows = ["| Command | What it does | Example |", "| :--- | :--- | :--- |"]
    for c in commands:
        hint = c["hint"].strip("[]")
        rows.append(f"| `/{c['name']}` | {c['description']} | `/{c['name']} {hint}` |")
    return "\n".join(rows)


def catalog(skills):
    out = []
    for k, (label, blurb) in stsk.CATEGORIES.items():
        group = [s for s in skills if s["category"] == k]
        if not group:
            continue
        out.append(f"### {label} ({len(group)})\n\n_{blurb}_\n")
        for s in group:
            out.append(f"- **[`{s['name']}`](skills/{s['dir']}/SKILL.md)**: {stsk.short_desc(s['description'], 170)}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def replace_block(text, name, body):
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(text):
        raise SystemExit(f"README.md is missing <!-- {name}:start/end --> markers")
    return pat.sub(lambda m: f"{start}\n{body.rstrip(chr(10))}\n{end}", text, count=1)


def manifests(n, c):
    desc = (f"{n} Agent Skills and {c} slash commands for software testing and QA: unit, API, E2E, performance, security, "
            "accessibility, data, mobile, AI/LLM and more. Works in Claude Code, Antigravity, Gemini CLI, Codex and Cursor.")
    author = {"name": "Mejbaur Bahar", "email": "mejbaur.bahar@gmail.com", "url": "https://github.com/mejbaurbahar"}
    plugin = {
        "name": "software-tester-skills",
        "description": desc,
        "version": VERSION,
        "author": author,
        "homepage": stsk.SITE_URL + "/",
        "repository": stsk.REPO_URL + ".git",
        "license": "MIT",
        "keywords": ["testing", "qa", "sdet", "software-testing", "test-automation", "agent-skills", "claude-code",
                     "antigravity", "gemini-cli", "codex", "cursor", "playwright", "api-testing", "security-testing",
                     "performance-testing", "accessibility", "llm-testing", "quality-assurance"],
    }
    market = {
        "name": "software-tester-skills",
        "description": "Software testing and QA skills and commands for AI coding agents",
        "owner": {"name": author["name"], "email": author["email"]},
        "plugins": [{"name": "software-tester-skills", "description": desc, "version": VERSION, "source": "./",
                     "author": {"name": author["name"], "email": author["email"]},
                     "category": "testing", "keywords": plugin["keywords"][:10]}],
    }
    return plugin, market


def main():
    skills, commands = stsk.load_skills(), stsk.load_commands()
    n, c = len(skills), len(commands)
    text = README.read_text(encoding="utf-8")
    new = replace_block(text, "badges", badges(n, c))
    new = replace_block(new, "commands", commands_table(commands))
    new = replace_block(new, "catalog", catalog(skills))
    new = replace_block(new, "tagline", tagline(n, c))
    plugin, market = manifests(n, c)
    targets = {README: new,
               PLUGIN: json.dumps(plugin, indent=2, ensure_ascii=False) + "\n",
               MARKET: json.dumps(market, indent=2, ensure_ascii=False) + "\n"}
    if "--check" in sys.argv:
        stale = [str(p.relative_to(stsk.ROOT)) for p, t in targets.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        if stale:
            print("stale generated files: " + ", ".join(stale) + "\nrun: python3 scripts/build_readme.py")
            sys.exit(1)
        print("README and manifests up to date")
        return
    for p, t in targets.items():
        p.write_text(t, encoding="utf-8")
    print(f"updated README.md, plugin.json, marketplace.json ({n} skills, {c} commands)")


if __name__ == "__main__":
    main()
