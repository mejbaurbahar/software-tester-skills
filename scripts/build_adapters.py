#!/usr/bin/env python3
"""Generate per-tool slash-command files from the canonical commands/*.md.

Canonical format = Claude Code (frontmatter + $ARGUMENTS).
  adapters/gemini/commands/qa/<name>.toml   -> Gemini CLI   (/qa:<name>)
  adapters/cursor/commands/qa-<name>.md     -> Cursor       (/qa-<name>)
  adapters/codex/prompts/qa-<name>.md       -> Codex CLI    (/prompts:qa-<name>)
Antigravity has no adapter: any skill is invocable as /<skill-name>.
Use --check to fail if generated files are out of date (CI).
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stsk  # noqa: E402

OUT = stsk.ROOT / "adapters"
HEADER = "Generated from commands/{n}.md by scripts/build_adapters.py - do not edit by hand."


def gemini(c):
    body = c["body"].replace("$ARGUMENTS", "{{args}}").replace("'''", "'' '")
    desc = c["description"].replace('"', "'")
    return f'# {HEADER.format(n=c["name"])}\ndescription = "{desc}"\nprompt = \'\'\'\n{body}\'\'\'\n'


def cursor(c):
    body = c["body"].replace("$ARGUMENTS", "the text the user typed after this command (ask if none)")
    return f'<!-- {HEADER.format(n=c["name"])} -->\n# {c["description"]}\n\n{body}'


def codex(c):
    hint = c["hint"].replace('"', "'")
    return (f'---\ndescription: {c["description"]}\nargument-hint: "{hint}"\n---\n'
            f'<!-- {HEADER.format(n=c["name"])} -->\n\n{c["body"]}')


def render():
    files = {}
    for c in stsk.load_commands():
        files[f"gemini/commands/qa/{c['name']}.toml"] = gemini(c)
        files[f"cursor/commands/qa-{c['name']}.md"] = cursor(c)
        files[f"codex/prompts/qa-{c['name']}.md"] = codex(c)
    return files


def main():
    files = render()
    if "--check" in sys.argv:
        stale = [p for p, txt in files.items() if not (OUT / p).exists() or (OUT / p).read_text() != txt]
        existing = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()} if OUT.exists() else set()
        stale += sorted(existing - set(files))
        if stale:
            print("adapters out of date; run: python3 scripts/build_adapters.py\n  " + "\n  ".join(stale))
            sys.exit(1)
        print(f"adapters up to date ({len(files)} files)")
        return
    if OUT.exists():
        shutil.rmtree(OUT)
    for p, txt in files.items():
        f = OUT / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(txt, encoding="utf-8")
    print(f"wrote {len(files)} adapter files to {OUT.relative_to(stsk.ROOT)}/")


if __name__ == "__main__":
    main()
