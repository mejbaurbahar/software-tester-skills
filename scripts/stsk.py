"""Shared helpers for software-tester-skills tooling (stdlib only)."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
COMMANDS_DIR = ROOT / "commands"
REPO = "mejbaurbahar/software-tester-skills"
REPO_URL = f"https://github.com/{REPO}"
SITE_URL = "https://mejbaurbahar.github.io/software-tester-skills"
RAW_URL = f"https://raw.githubusercontent.com/{REPO}/main"

# Category id -> (label, one-line blurb). Order = display order.
CATEGORIES = {
    "strategy": ("Strategy, Planning & Metrics", "Decide what to test, plan it, report on it."),
    "functional": ("Functional & Acceptance", "Black-box, exploratory, regression and release-gate testing."),
    "code-level": ("Code-Level & White-Box", "Unit, integration, property, fuzz, mutation and TDD."),
    "automation": ("Automation & CI", "Frameworks, environments, flaky tests, coverage and pipelines."),
    "web": ("Web, UI & UX", "Browsers, E2E, visual, accessibility, i18n, SEO and PWAs."),
    "api-backend": ("API, Backend & Messaging", "REST, GraphQL, real-time, contracts, events and microservices."),
    "data": ("Data & Databases", "Databases, ETL, migrations and test data."),
    "non-functional": ("Performance & Reliability", "Load, scalability, chaos, recovery and compatibility."),
    "operations": ("Operations & Production", "Observability, infrastructure and shift-right monitoring."),
    "security": ("Security & Privacy", "Defensive security testing, auth, supply chain and IaC."),
    "compliance": ("Compliance", "GDPR, HIPAA, PCI, SOC 2, audit evidence."),
    "ai": ("AI, ML & LLM", "Models, LLM apps, RAG, agents, chatbots and MCP."),
    "platform": ("Platforms", "Mobile, desktop, CLI, IoT, games, blockchain and serverless."),
    "domain": ("Domain-Specific", "Payments, email, analytics and experimentation."),
}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    data, section = {}, None
    for line in m.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and section:
            k, _, v = line.strip().partition(":")
            data[section][k.strip()] = v.strip().strip('"').strip("'")
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v == "":
            data[k] = {}
            section = k
        else:
            data[k] = v.strip('"').strip("'") if not v.startswith(">") else v
            section = None
    return data, m.group(2)


def load_skills():
    skills = []
    for d in sorted(SKILLS_DIR.iterdir()):
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        fm, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        fm = fm or {}
        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        skills.append({
            "name": fm.get("name", d.name),
            "dir": d.name,
            "description": fm.get("description", ""),
            "category": meta.get("category", "strategy"),
            "version": meta.get("version", "1.0"),
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "body": body,
            "lines": body.count("\n") + 1,
            "extras": sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name != "SKILL.md"),
        })
    return skills


def load_commands():
    cmds = []
    for f in sorted(COMMANDS_DIR.glob("*.md")):
        fm, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        fm = fm or {}
        cmds.append({"name": f.stem, "description": fm.get("description", ""),
                     "hint": fm.get("argument-hint", ""), "body": body.strip() + "\n"})
    return cmds


def short_desc(desc, limit=180):
    d = re.sub(r"^Use when\s+", "", desc.strip(), flags=re.I)
    d = d[0].upper() + d[1:] if d else d
    if len(d) <= limit:
        return d
    cut = d[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(",;—- ") + "…"


# ---------------------------------------------------------------- markdown
def _inline(s, names):
    s = html.escape(s, quote=False)
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", stash, s)
    s = re.sub(r"\[\[([a-z0-9-]+)\]\]",
               lambda m: f'<a href="../{m.group(1)}/">{m.group(1)}</a>' if m.group(1) in names else m.group(1), s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])", r"<em>\1</em>", s)

    def unstash(m):
        code = codes[int(m.group(1))]
        code_html = html.escape(code, quote=False)
        if code in names:
            return f'<a href="../{code}/"><code>{code_html}</code></a>'
        return f"<code>{code_html}</code>"

    return re.sub(r"\x00(\d+)\x00", unstash, s)


def render_markdown(md, names=frozenset()):
    out, lines, i = [], md.split("\n"), 0
    para, list_stack = [], []

    def flush_para():
        if para:
            out.append("<p>" + _inline(" ".join(para), names) + "</p>")
            para.clear()

    def close_lists(to=0):
        while len(list_stack) > to:
            out.append(f"</{list_stack.pop()[0]}>")

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_para(); close_lists()
            lang = line[3:].strip()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            label = f' data-lang="{html.escape(lang)}"' if lang else ""
            out.append(f'<pre{label}><code>{html.escape(chr(10).join(buf), quote=False)}</code></pre>')
            i += 1
            continue
        if re.match(r"^\s*\|.*\|\s*$", line) and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush_para(); close_lists()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and re.match(r"^\s*\|.*\|\s*$", lines[i]):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            t = ['<div class="table-wrap"><table><thead><tr>' + "".join(f"<th>{_inline(h, names)}</th>" for h in header) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{_inline(c, names)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para(); close_lists()
            lvl = min(len(m.group(1)) + 1, 6) if len(m.group(1)) == 1 else len(m.group(1))
            text = m.group(2)
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{lvl} id="{slug}">{_inline(text, names)}</h{lvl}>')
            i += 1
            continue
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            flush_para(); close_lists(); out.append("<hr>"); i += 1; continue
        if line.startswith(">"):
            flush_para(); close_lists()
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip()); i += 1
            out.append("<blockquote>" + _inline(" ".join(buf), names) + "</blockquote>")
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            flush_para()
            depth = len(m.group(1)) // 2
            kind = "ol" if m.group(2)[0].isdigit() else "ul"
            while len(list_stack) > depth + 1:
                out.append(f"</{list_stack.pop()[0]}>")
            if len(list_stack) < depth + 1:
                list_stack.append((kind,)); out.append(f"<{kind}>")
            elif list_stack[-1][0] != kind:
                out.append(f"</{list_stack.pop()[0]}>"); list_stack.append((kind,)); out.append(f"<{kind}>")
            out.append("<li>" + _inline(m.group(3), names) + "</li>")
            i += 1
            continue
        if not line.strip():
            flush_para(); close_lists(); i += 1; continue
        if list_stack and line.startswith("  "):
            out.append(out.pop()[:-5] + " " + _inline(line.strip(), names) + "</li>")
            i += 1
            continue
        close_lists()
        para.append(line.strip())
        i += 1
    flush_para(); close_lists()
    return "\n".join(out)


def catalog_json(skills, commands):
    return {
        "name": "software-tester-skills",
        "repository": REPO_URL,
        "homepage": SITE_URL + "/",
        "skill_count": len(skills),
        "command_count": len(commands),
        "categories": [{"id": k, "label": v[0], "description": v[1]} for k, v in CATEGORIES.items()],
        "skills": [{k: s[k] for k in ("name", "description", "category", "version", "tags")} |
                   {"url": f"{SITE_URL}/skills/{s['name']}/", "source": f"{REPO_URL}/tree/main/skills/{s['dir']}"}
                   for s in skills],
        "commands": [{"name": c["name"], "description": c["description"], "argument_hint": c["hint"]} for c in commands],
    }


if __name__ == "__main__":
    s = load_skills()
    print(json.dumps(catalog_json(s, load_commands()), indent=2)[:600])
