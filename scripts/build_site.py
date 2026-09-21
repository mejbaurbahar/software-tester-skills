#!/usr/bin/env python3
"""Build the static GitHub Pages site into _site/ (stdlib only).

  python3 scripts/build_site.py            # build
  python3 scripts/build_site.py --serve    # build and serve on :8000
"""
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stsk  # noqa: E402

OUT = stsk.ROOT / "_site"
SITE = stsk.ROOT / "site"
BASE = stsk.SITE_URL
TODAY = date.today().isoformat()
e = html.escape

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600'
         '&family=Schibsted+Grotesk:wght@400;500;600;700&display=swap">')

INSTALL = f"{BASE}/install.sh"

TABS = [
    ("claude", "Claude Code",
     "/plugin marketplace add mejbaurbahar/software-tester-skills\n/plugin install software-tester-skills@software-tester-skills",
     "Installs all skills plus namespaced slash commands such as <code>/software-tester-skills:test-plan</code>. "
     "Prefer plain copies? Run the installer with <code>--claude</code>."),
    ("any", "Any tool (auto-detect)",
     f"curl -fsSL {INSTALL} | bash -s -- --auto",
     "Detects Claude Code, Antigravity, Gemini CLI, Codex and Cursor on your machine and installs into each. "
     "It never overwrites files it did not create. Add <code>--dry-run</code> to preview."),
    ("antigravity", "Antigravity",
     f"curl -fsSL {INSTALL} | bash -s -- --antigravity",
     "Skills go to <code>~/.gemini/config/skills</code>. In Antigravity every skill is a slash command: "
     "type <code>/unit-testing</code> or <code>/qa-skill-router</code>."),
    ("gemini", "Gemini CLI",
     f"curl -fsSL {INSTALL} | bash -s -- --gemini",
     "Installs skills to <code>~/.gemini/skills</code> and commands to <code>~/.gemini/commands/qa</code>. "
     "Run <code>/commands reload</code>, then use <code>/qa:test-plan</code>."),
    ("codex", "Codex",
     f"curl -fsSL {INSTALL} | bash -s -- --codex",
     "Skills go to <code>~/.agents/skills</code>; prompts to <code>~/.codex/prompts</code> "
     "(invoke <code>/prompts:qa-test-plan</code>)."),
    ("cursor", "Cursor",
     f"curl -fsSL {INSTALL} | bash -s -- --cursor",
     "Skills go to <code>~/.cursor/skills</code>; commands to <code>~/.cursor/commands</code> (invoke <code>/qa-test-plan</code>)."),
    ("project", "This project only",
     f"curl -fsSL {INSTALL} | bash -s -- --project",
     "Copies skills to <code>.agents/skills</code> in the current repo (plus <code>.claude</code>, <code>.cursor</code> and "
     "<code>.gemini</code> skill folders that already exist) so your whole team gets them via git."),
]

FAQ = [
    ("What are agent skills?",
     "A skill is a folder with a SKILL.md file that teaches an AI coding agent how to do one job well. The agent reads the short "
     "description, loads the full playbook only when your task matches, and follows it. This library follows the open Agent Skills format, "
     "so the same files work across tools."),
    ("Which AI tools does it work with?",
     "Claude Code (plugin or plain skills), Google Antigravity, Gemini CLI, OpenAI Codex, Cursor, and any tool that reads Agent Skills "
     "from .agents/skills. The installer detects what you have and puts files in the right place."),
    ("How do I use a skill?",
     "Just describe the job (for example, write API tests for my orders endpoint) and the agent picks the matching skill. You can also name it "
     "directly, run a slash command like /api-tests, or ask the qa-skill-router skill which skills fit."),
    ("Is it free to use?",
     "Yes. Everything is MIT licensed and open source. Copy it, change it, and use it in commercial projects."),
    ("Can it run tests against production or third-party sites?",
     "The security and load skills tell the agent to test only systems you own or are authorized to test, to prefer staging, and never to use real customer data or live payment credentials."),
    ("How do I add or improve a skill?",
     "Open a pull request. CONTRIBUTING.md has the template, and CI validates the format, links and catalog automatically."),
]


def esc_json(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def title_of(skill):
    m = re.search(r"^#\s+(.+)$", skill["body"], re.M)
    return m.group(1).strip() if m else skill["name"]


def head(title, desc, canonical, root, extra="", og_type="website"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="theme-color" content="#101A2B">
<meta name="author" content="Mejbaur Bahar">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Software Tester Skills">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Software Tester Skills: testing skills and slash commands for AI coding agents">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{BASE}/assets/og.png">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{root}assets/style.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="{root or './'}">software-tester-<b>skills</b></a>
<nav aria-label="Primary"><a href="{root}#install">Install</a><a href="{root}#commands">Commands</a><a href="{root}#skills">Skills</a><a href="{root}#faq">FAQ</a>
<a class="gh" href="{stsk.REPO_URL}" rel="noopener">GitHub</a></nav>
</div></header>
"""


def footer(root):
    return f"""<footer><div class="wrap">
<span>MIT licensed. Built by <a href="https://github.com/mejbaurbahar" rel="noopener">Mejbaur Bahar</a>.</span>
<span><a href="{stsk.REPO_URL}" rel="noopener">Source</a> &nbsp; <a href="{stsk.REPO_URL}/blob/main/CONTRIBUTING.md" rel="noopener">Contribute</a> &nbsp;
<a href="{root}llms.txt">llms.txt</a> &nbsp; <a href="{root}skills.json">skills.json</a></span>
</div></footer>
<script src="{root}assets/app.js" defer></script>
</body></html>
"""


REPORT = [
    ("p", "✓", "unit-testing", "91% branch coverage"),
    ("p", "✓", "api-testing", "42 operations valid"),
    ("f", "✗", "e2e-testing", "checkout.spec 18% flaky"),
    ("w", "!", "security-testing", "2 High, 1 Medium"),
    ("p", "✓", "accessibility-testing", "0 critical WCAG issues"),
]


def build_index(skills, commands):
    n, c = len(skills), len(commands)
    by_cat = {}
    for s in skills:
        by_cat.setdefault(s["category"], []).append(s)
    title = f"Software Tester Skills: {n} AI Agent Skills for QA & Testing"
    desc = (f"Open-source testing skills and {c} slash commands for Claude Code, Antigravity, Gemini CLI, Codex and Cursor. "
            "Unit, API, E2E, security, performance, accessibility and AI testing.")
    ld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Software Tester Skills", "url": BASE + "/",
         "description": desc, "inLanguage": "en"},
        {"@context": "https://schema.org", "@type": "SoftwareSourceCode", "name": "software-tester-skills",
         "description": desc, "codeRepository": stsk.REPO_URL, "url": BASE + "/", "license": "https://opensource.org/licenses/MIT",
         "programmingLanguage": "Markdown", "author": {"@type": "Person", "name": "Mejbaur Bahar", "url": "https://github.com/mejbaurbahar"},
         "keywords": "software testing, QA, SDET, agent skills, Claude Code, Antigravity, Gemini CLI, Codex, Cursor, test automation"},
        {"@context": "https://schema.org", "@type": "ItemList", "name": "Software testing agent skills",
         "numberOfItems": n,
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["name"], "url": f"{BASE}/skills/{s['name']}/"}
                             for i, s in enumerate(skills)]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    extra = "".join(f'<script type="application/ld+json">{esc_json(x)}</script>' for x in ld)
    out = [head(title, desc, BASE + "/", "", extra)]

    rows = "".join(
        f'<div class="row" style="--i:{i}"><span class="{k}">{g}</span><span>{nm}</span><span>{e(d)}</span></div>'
        for i, (k, g, nm, d) in enumerate(REPORT, 1))
    out.append(f"""<main id="main">
<section class="hero"><div class="wrap grid">
<div>
<h1>Give your AI agent a senior tester's playbook</h1>
<p class="lede">{n} open-source skills and {c} slash commands for unit, API, end-to-end, security, performance, accessibility and AI testing, with a clear procedure for each.</p>
<p class="tools"><strong>Works in</strong> Claude Code, Antigravity, Gemini CLI, Codex and Cursor.</p>
<div class="cta"><a class="btn" href="#install">Install in one command</a><a class="btn alt" href="#skills">Browse {n} skills</a></div>
</div>
<div>
<div class="report" role="img" aria-label="Example output of the qa-audit command: passing checks for unit, API and accessibility testing, one flaky end-to-end test and a security warning">
<div class="bar"><span>example run</span><span>~/shop-api</span></div>
<div class="cmd">$ /qa-audit</div>{rows}
<div class="foot">next: /flaky-triage checkout.spec</div>
</div>
<p class="caption">Illustrative output. Your agent reads your repo and reports its own results.</p>
</div>
</div></section>
""")

    tabs = "".join(
        f'<button role="tab" id="t-{k}" aria-controls="p-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{lbl}</button>'
        for i, (k, lbl, _, _) in enumerate(TABS))
    panels = "".join(
        f'<div class="panel" role="tabpanel" id="p-{k}" aria-labelledby="t-{k}"{"" if i == 0 else " hidden"}>'
        f'<button class="copy" type="button">Copy</button><pre><code>{e(cmd)}</code></pre><p>{note}</p></div>'
        for i, (k, _, cmd, note) in enumerate(TABS))
    out.append(f"""<section id="install"><div class="wrap">
<h2>Install</h2>
<p class="sub">Pick your tool. Each option installs the skills and, where the tool supports it, the slash commands.</p>
<div class="tabs" role="tablist" aria-label="Install method">{tabs}</div>{panels}
</div></section>
""")

    cmd_items = "".join(
        f'<li><code>/{e(x["name"])}</code><span>{e(x["description"])}</span></li>' for x in commands)
    out.append(f"""<section id="commands"><div class="wrap">
<h2>{c} slash commands</h2>
<p class="sub">Each command loads the right skills and runs a complete workflow, from a risk-based test plan to a go/no-go release check.</p>
<ul class="cmds">{cmd_items}</ul>
<p class="note">Prefix by tool: Claude Code plugin <code>/software-tester-skills:test-plan</code> (or <code>/test-plan</code>), Gemini CLI <code>/qa:test-plan</code>,
Cursor <code>/qa-test-plan</code>, Codex <code>/prompts:qa-test-plan</code>. In Antigravity, invoke any skill as <code>/skill-name</code>. Not sure where to start? Ask for the <code>qa-skill-router</code> skill.</p>
</div></section>
""")

    chips = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-cat="{k}" aria-pressed="false">{e(v[0])}</button>'
        for k, v in stsk.CATEGORIES.items() if k in by_cat)
    cats = []
    for k, (label, blurb) in stsk.CATEGORIES.items():
        if k not in by_cat:
            continue
        lis = "".join(
            f'<li data-s="{e((s["name"] + " " + s["description"] + " " + " ".join(s["tags"])).lower())}">'
            f'<a href="skills/{s["name"]}/">{s["name"]}</a><p>{e(stsk.short_desc(s["description"]))}</p></li>'
            for s in by_cat[k])
        cats.append(f'<div class="cat" data-cat="{k}"><h3>{e(label)} <small>{e(blurb)}</small></h3><ul class="skills">{lis}</ul></div>')
    out.append(f"""<section id="skills"><div class="wrap">
<h2>The skill catalog</h2>
<p class="sub">Every skill is a plain Markdown playbook with when-to-use rules, a procedure, real commands and pitfalls. Press <kbd>/</kbd> to search.</p>
<div class="finder"><input id="q" type="search" placeholder="Search {n} skills: flaky, GraphQL, WCAG, k6, RAG…" aria-label="Search skills">
<span id="count" aria-live="polite" class="sub">{n} skills</span></div>
<div class="chips" role="group" aria-label="Filter by category">{chips}</div>
{"".join(cats)}
<p class="empty" id="empty" hidden>No skill matches. Try a broader word, or <a href="{stsk.REPO_URL}/issues/new" rel="noopener">request one</a>.</p>
</div></section>
""")

    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ)
    out.append(f'<section id="faq"><div class="wrap"><h2>Questions</h2>{faq}</div></section>\n</main>\n')
    out.append(footer(""))
    return "".join(out)


def build_skill(s, skills, names):
    h1 = title_of(s)
    cat_label = stsk.CATEGORIES.get(s["category"], (s["category"],))[0]
    url = f"{BASE}/skills/{s['name']}/"
    desc = stsk.short_desc(s["description"], 155)
    title = f"{h1}: AI Agent Skill for Testing | Software Tester Skills"
    body = re.sub(r"^#\s+.+\n", "", s["body"].lstrip(), count=1)
    article = stsk.render_markdown(body, names)
    related = [x for x in skills if x["category"] == s["category"] and x["name"] != s["name"]][:7]
    rel = "".join(f'<li><a href="../{r["name"]}/">{r["name"]}</a></li>' for r in related)
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in s["tags"])
    ld = [
        {"@context": "https://schema.org", "@type": "TechArticle", "headline": h1, "description": desc, "url": url,
         "inLanguage": "en", "dateModified": TODAY, "keywords": ", ".join(s["tags"]),
         "author": {"@type": "Person", "name": "Mejbaur Bahar"},
         "isPartOf": {"@type": "WebSite", "name": "Software Tester Skills", "url": BASE + "/"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Software Tester Skills", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": cat_label, "item": BASE + "/#skills"},
            {"@type": "ListItem", "position": 3, "name": s["name"], "item": url}]},
    ]
    extra = "".join(f'<script type="application/ld+json">{esc_json(x)}</script>' for x in ld)
    src = f"{stsk.REPO_URL}/blob/main/skills/{s['dir']}/SKILL.md"
    page = [head(title, desc, url, "../../", extra, "article")]
    page.append(f"""<main id="main"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Home</a> / <a href="../../#skills">Skills</a> / {e(cat_label)}</nav>
<div class="doc">
<article>
<h1>{e(h1)}</h1>
<p class="sub">{e(stsk.short_desc(s["description"], 400))}</p>
{article}
</article>
<aside>
<div class="box"><h2>Install this skill</h2>
<pre><code>curl -fsSL {INSTALL} | bash -s -- --auto --skill {s['name']}</code></pre>
<h2 style="margin-top:14px">Use it</h2>
<p>Ask your agent: <em>“Use the {s['name']} skill to …”</em><br>In Antigravity: <code>/{s['name']}</code></p>
<p><a href="{src}" rel="noopener">View SKILL.md on GitHub</a></p></div>
<div class="box"><h2>{e(cat_label)}</h2>{tags}<ul>{rel}</ul></div>
</aside></div></div></main>
""")
    page.append(footer("../../"))
    return "".join(page)


def build_404():
    return (head("Page not found | Software Tester Skills", "This page does not exist.", BASE + "/404.html", "/software-tester-skills/")
            .replace('<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">', '<meta name="robots" content="noindex">')
            + '<main id="main"><section><div class="wrap"><h1>Page not found</h1>'
              '<p class="lede">That page is missing. Try the <a href="/software-tester-skills/#skills">skill catalog</a>.</p></div></section></main>'
            + footer("/software-tester-skills/"))


def build_llms(skills, commands, full=False):
    lines = ["# Software Tester Skills", "",
             f"> {len(skills)} open-source agent skills and {len(commands)} slash commands for software testing and QA, "
             "usable in Claude Code, Google Antigravity, Gemini CLI, OpenAI Codex and Cursor. MIT licensed.", "",
             f"Repository: {stsk.REPO_URL}", f"Install: curl -fsSL {INSTALL} | bash -s -- --auto", ""]
    for k, (label, _) in stsk.CATEGORIES.items():
        group = [s for s in skills if s["category"] == k]
        if not group:
            continue
        lines += [f"## {label}", ""]
        lines += [f"- [{s['name']}]({BASE}/skills/{s['name']}/): {stsk.short_desc(s['description'], 200)}" for s in group]
        lines.append("")
    lines += ["## Slash commands", ""] + [f"- /{c['name']}: {c['description']}" for c in commands] + [""]
    if full:
        for s in skills:
            lines += ["", "---", "", f"# Skill: {s['name']}", "", s["description"], "", s["body"].strip(), ""]
    return "\n".join(lines) + "\n"


def main():
    skills, commands = stsk.load_skills(), stsk.load_commands()
    names = frozenset(s["name"] for s in skills)
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in ("style.css", "app.js", "favicon.svg", "og.png"):
        if (SITE / f).exists():
            shutil.copy(SITE / f, OUT / "assets" / f)
    (OUT / "index.html").write_text(build_index(skills, commands), encoding="utf-8")
    for s in skills:
        d = OUT / "skills" / s["name"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(build_skill(s, skills, names), encoding="utf-8")
    (OUT / "404.html").write_text(build_404(), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    (OUT / "skills.json").write_text(json.dumps(stsk.catalog_json(skills, commands), indent=2), encoding="utf-8")
    (OUT / "llms.txt").write_text(build_llms(skills, commands), encoding="utf-8")
    (OUT / "llms-full.txt").write_text(build_llms(skills, commands, full=True), encoding="utf-8")
    shutil.copy(stsk.ROOT / "install.sh", OUT / "install.sh")
    urls = [BASE + "/"] + [f"{BASE}/skills/{s['name']}/" for s in skills]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(skills)} skill pages + index into {OUT.relative_to(stsk.ROOT)}/ "
          f"({sum(1 for _ in OUT.rglob('*') if _.is_file())} files)")
    if "--serve" in sys.argv:
        import functools
        import http.server
        import socketserver
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
            print("serving http://127.0.0.1:8000/")
            httpd.serve_forever()


if __name__ == "__main__":
    main()
