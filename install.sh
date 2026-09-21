#!/usr/bin/env bash
# software-tester-skills installer
# Installs the skills (and, where the tool supports them, slash commands) for
# Claude Code, Google Antigravity, Gemini CLI, OpenAI Codex, Cursor and any
# Agent-Skills-compatible tool.
#
#   ./install.sh                     # auto-detect installed tools
#   ./install.sh --all               # every supported tool
#   ./install.sh --claude --skill unit-testing,api-testing
#   curl -fsSL https://raw.githubusercontent.com/mejbaurbahar/software-tester-skills/main/install.sh | bash -s -- --auto
#
# Safe by design: never overwrites a directory/file it did not create unless
# --force is given (then the original is moved to <name>.bak-<timestamp>).

set -euo pipefail

REPO="mejbaurbahar/software-tester-skills"
VERSION="2.0.0"
MARKER=".installed-by-software-tester-skills"

# --------------------------------------------------------------------------- locate sources
SELF="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="$(cd "$(dirname "$SELF")" 2>/dev/null && pwd || echo "")"
TMP_DL=""
cleanup() { [ -n "$TMP_DL" ] && rm -rf "$TMP_DL"; return 0; }
trap cleanup EXIT

if [ -z "$SCRIPT_DIR" ] || [ ! -d "$SCRIPT_DIR/skills" ]; then
  # Running via curl | bash (or copied elsewhere): fetch the repo tarball.
  command -v curl >/dev/null 2>&1 || { echo "curl is required for remote install" >&2; exit 1; }
  TMP_DL="$(mktemp -d)"
  echo "==> Downloading $REPO (main)…"
  curl -fsSL "https://github.com/$REPO/archive/refs/heads/main.tar.gz" | tar -xz -C "$TMP_DL"
  SCRIPT_DIR="$TMP_DL/$(ls "$TMP_DL" | head -n 1)"
fi
SKILLS_SRC="$SCRIPT_DIR/skills"
ADAPTERS_SRC="$SCRIPT_DIR/adapters"
COMMANDS_SRC="$SCRIPT_DIR/commands"

# --------------------------------------------------------------------------- options
TARGETS=""          # space separated: claude antigravity gemini codex cursor agents project
ONLY_SKILLS=""      # comma separated
WITH_COMMANDS=1
DRY=0
FORCE=0
UNINSTALL=0
LIST=0

usage() {
  cat <<EOF
software-tester-skills installer v$VERSION

Usage: ./install.sh [targets] [options]

Targets (combine freely; default is --auto):
  --auto           Detect installed tools (~/.claude, ~/.gemini, ~/.codex, ~/.cursor)
  --claude         Claude Code        skills -> ~/.claude/skills      commands -> ~/.claude/commands
  --antigravity    Google Antigravity skills -> ~/.gemini/config/skills (+ legacy ~/.gemini/antigravity/skills if present)
  --gemini         Gemini CLI         skills -> ~/.gemini/skills      commands -> ~/.gemini/commands/qa/*.toml  (/qa:<name>)
  --codex          OpenAI Codex       skills -> ~/.agents/skills      prompts  -> ~/.codex/prompts/qa-*.md
  --cursor         Cursor             skills -> ~/.cursor/skills      commands -> ~/.cursor/commands/qa-*.md
  --agents         Generic Agent Skills dir  ~/.agents/skills (OpenCode, Goose, Pi, Hermes, ...)
  --project        This project: .agents/skills (+ .claude/skills, .cursor/skills, .gemini/skills if those dirs exist)
  --all            All of the above except --project

Options:
  --skill a,b,c    Install only these skills (see --list)
  --no-commands    Skills only, skip slash commands / prompts
  --list           List available skills and commands, then exit
  --dry-run        Show what would happen; change nothing
  --force          Replace existing non-managed copies (original is backed up as .bak-<timestamp>)
  --uninstall      Remove everything this installer put in the chosen targets
  -h, --help       This help

Tip for Claude Code users: the plugin route gives namespaced commands and easy updates:
  /plugin marketplace add $REPO
  /plugin install software-tester-skills@software-tester-skills
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --auto) TARGETS="$TARGETS auto" ;;
    --claude|--antigravity|--gemini|--codex|--cursor|--agents|--project) TARGETS="$TARGETS ${1#--}" ;;
    --all) TARGETS="$TARGETS claude antigravity gemini codex cursor agents" ;;
    --skill|--skills) shift; [ $# -gt 0 ] || { echo "--skill needs a value" >&2; exit 2; }; ONLY_SKILLS="$1" ;;
    --no-commands) WITH_COMMANDS=0 ;;
    --list) LIST=1 ;;
    --dry-run|-n) DRY=1 ;;
    --force|-f) FORCE=1 ;;
    --uninstall) UNINSTALL=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

# --------------------------------------------------------------------------- helpers
say()  { printf '%s\n' "$*"; }
tilde() { case "$1" in "$HOME"*) printf '~%s' "${1#"$HOME"}";; *) printf '%s' "$1";; esac; }
act()  { if [ "$DRY" = 1 ]; then say "   [dry-run] $*"; return 0; fi; return 1; }
ts()   { date +%Y%m%d-%H%M%S; }

all_skill_names() { for d in "$SKILLS_SRC"/*/; do [ -f "$d/SKILL.md" ] && basename "$d"; done; }

selected_skills() {
  if [ -z "$ONLY_SKILLS" ]; then all_skill_names; return; fi
  local s
  for s in $(echo "$ONLY_SKILLS" | tr ',' ' '); do
    if [ -f "$SKILLS_SRC/$s/SKILL.md" ]; then echo "$s"; else echo "Unknown skill: $s (try --list)" >&2; exit 2; fi
  done
}

# install_skill <name> <dest_root>
install_skill() {
  local name="$1" root="$2" src="$SKILLS_SRC/$1" dest="$2/$1"
  if [ -d "$dest" ] || [ -L "$dest" ]; then
    if [ -f "$dest/$MARKER" ]; then
      act "update  $dest" || { rm -rf "$dest"; }
    elif [ "$FORCE" = 1 ]; then
      act "backup+replace  $dest" || { mv "$dest" "$dest.bak-$(ts)"; }
    else
      say "   skip     $dest (exists, not installed by this tool; use --force to replace with backup)"
      SKIPPED=$((SKIPPED + 1)); return 0
    fi
  else
    act "install $dest" || true
  fi
  if [ "$DRY" = 0 ]; then
    mkdir -p "$root"
    cp -R "$src" "$dest"
    printf 'software-tester-skills %s\n' "$VERSION" > "$dest/$MARKER"
  fi
  INSTALLED=$((INSTALLED + 1))
}

# install_file <src> <dest>   (managed commands/prompts carry the marker in a sidecar list)
install_file() {
  local src="$1" dest="$2"
  if [ -e "$dest" ]; then
    if grep -q "Generated from commands/.*build_adapters.py\|software-tester-skills-command" "$dest" 2>/dev/null; then
      act "update  $dest" || cp "$src" "$dest"
      CMDS=$((CMDS + 1)); return 0
    elif [ "$FORCE" = 1 ]; then
      act "backup+replace  $dest" || { mv "$dest" "$dest.bak-$(ts)"; cp "$src" "$dest"; }
      CMDS=$((CMDS + 1)); return 0
    else
      say "   skip     $dest (exists, not ours; use --force)"; SKIPPED=$((SKIPPED + 1)); return 0
    fi
  fi
  if [ "$DRY" = 0 ]; then mkdir -p "$(dirname "$dest")"; cp "$src" "$dest"; else act "install $dest" || true; fi
  CMDS=$((CMDS + 1))
}

# install_claude_command: canonical files carry no generated header, so tag them.
install_claude_command() {
  local src="$1" dest="$2"
  local tmp; tmp="$(mktemp)"
  { cat "$src"; printf '\n<!-- software-tester-skills-command -->\n'; } > "$tmp"
  install_file "$tmp" "$dest"; rm -f "$tmp"
}

remove_managed_skills() {
  local root="$1" d
  [ -d "$root" ] || return 0
  for d in "$root"/*/; do
    [ -f "$d/$MARKER" ] || continue
    act "remove  ${d%/}" || rm -rf "${d%/}"
    REMOVED=$((REMOVED + 1))
  done
}

remove_managed_files() { # dir glob
  local f
  for f in "$1"/$2; do
    [ -f "$f" ] || continue
    if grep -q "Generated from commands/.*build_adapters.py\|software-tester-skills-command" "$f" 2>/dev/null; then
      act "remove  $f" || rm -f "$f"; REMOVED=$((REMOVED + 1))
    fi
  done
}

# --------------------------------------------------------------------------- validate --skill early
if [ -n "$ONLY_SKILLS" ]; then
  for s in $(echo "$ONLY_SKILLS" | tr ',' ' '); do
    [ -f "$SKILLS_SRC/$s/SKILL.md" ] || { echo "Unknown skill: $s (try --list)" >&2; exit 2; }
  done
fi

# --------------------------------------------------------------------------- list
if [ "$LIST" = 1 ]; then
  say "Skills ($(all_skill_names | wc -l | tr -d ' ')):"; all_skill_names | sed 's/^/  /'
  say ""; say "Slash commands:"
  for f in "$COMMANDS_SRC"/*.md; do echo "  /$(basename "$f" .md)"; done
  exit 0
fi

# --------------------------------------------------------------------------- resolve targets
[ -z "$TARGETS" ] && TARGETS="auto"
if echo "$TARGETS" | grep -qw auto; then
  TARGETS="$(echo "$TARGETS" | sed 's/\bauto\b//')"
  [ -d "$HOME/.claude" ]  && TARGETS="$TARGETS claude"
  [ -d "$HOME/.gemini" ]  && TARGETS="$TARGETS antigravity gemini"
  [ -d "$HOME/.codex" ]   && TARGETS="$TARGETS codex"
  [ -d "$HOME/.cursor" ]  && TARGETS="$TARGETS cursor"
  if [ -z "$(echo "$TARGETS" | tr -d ' ')" ]; then
    say "No known AI tool directory found; installing to the generic ~/.agents/skills."
    TARGETS="agents"
  fi
fi
TARGETS="$(echo "$TARGETS" | tr ' ' '\n' | awk 'NF && !s[$0]++' | tr '\n' ' ')"

INSTALLED=0; CMDS=0; SKIPPED=0; REMOVED=0
SEEN_ROOTS=""
once() { case " $SEEN_ROOTS " in *" $1 "*) return 1;; esac; SEEN_ROOTS="$SEEN_ROOTS $1"; return 0; }

do_skills() { # label root
  once "$2" || return 0
  if [ "$UNINSTALL" = 1 ]; then say "==> $1: removing skills from $(tilde "$2")"; remove_managed_skills "$2"; return; fi
  say "==> $1: skills -> $(tilde "$2")"
  local s; for s in $(selected_skills); do install_skill "$s" "$2"; done
}

# --------------------------------------------------------------------------- run
for t in $TARGETS; do
  case "$t" in
    claude)
      do_skills "Claude Code" "$HOME/.claude/skills"
      if [ "$WITH_COMMANDS" = 1 ]; then
        if [ "$UNINSTALL" = 1 ]; then remove_managed_files "$HOME/.claude/commands" "*.md"
        else
          say "==> Claude Code: commands -> ~/.claude/commands"
          for f in "$COMMANDS_SRC"/*.md; do install_claude_command "$f" "$HOME/.claude/commands/$(basename "$f")"; done
        fi
      fi ;;
    antigravity)
      do_skills "Google Antigravity" "$HOME/.gemini/config/skills"
      [ -d "$HOME/.gemini/antigravity" ] && do_skills "Google Antigravity (legacy path)" "$HOME/.gemini/antigravity/skills"
      say "   (in Antigravity every skill is invocable as /<skill-name>, e.g. /unit-testing or /qa-skill-router)" ;;
    gemini)
      do_skills "Gemini CLI" "$HOME/.gemini/skills"
      if [ "$WITH_COMMANDS" = 1 ]; then
        if [ "$UNINSTALL" = 1 ]; then remove_managed_files "$HOME/.gemini/commands/qa" "*.toml"
        else
          say "==> Gemini CLI: commands -> ~/.gemini/commands/qa  (use /qa:<name>; run /commands reload)"
          for f in "$ADAPTERS_SRC"/gemini/commands/qa/*.toml; do install_file "$f" "$HOME/.gemini/commands/qa/$(basename "$f")"; done
        fi
      fi ;;
    codex)
      do_skills "OpenAI Codex" "$HOME/.agents/skills"
      if [ "$WITH_COMMANDS" = 1 ]; then
        if [ "$UNINSTALL" = 1 ]; then remove_managed_files "$HOME/.codex/prompts" "qa-*.md"
        else
          say "==> Codex: prompts -> ~/.codex/prompts  (invoke /prompts:qa-<name>)"
          for f in "$ADAPTERS_SRC"/codex/prompts/*.md; do install_file "$f" "$HOME/.codex/prompts/$(basename "$f")"; done
        fi
      fi ;;
    cursor)
      do_skills "Cursor" "$HOME/.cursor/skills"
      if [ "$WITH_COMMANDS" = 1 ]; then
        if [ "$UNINSTALL" = 1 ]; then remove_managed_files "$HOME/.cursor/commands" "qa-*.md"
        else
          say "==> Cursor: commands -> ~/.cursor/commands  (invoke /qa-<name>)"
          for f in "$ADAPTERS_SRC"/cursor/commands/*.md; do install_file "$f" "$HOME/.cursor/commands/$(basename "$f")"; done
        fi
      fi ;;
    agents) do_skills "Generic (.agents)" "$HOME/.agents/skills" ;;
    project)
      do_skills "Project (.agents)" "$(pwd)/.agents/skills"
      for extra in .claude .cursor .gemini; do
        [ -d "$(pwd)/$extra" ] && do_skills "Project ($extra)" "$(pwd)/$extra/skills"
      done ;;
  esac
done

say ""
if [ "$UNINSTALL" = 1 ]; then
  say "Done. Removed $REMOVED item(s)."
else
  say "Done. Installed/updated $INSTALLED skill copy(ies) and $CMDS command file(s); skipped $SKIPPED."
  [ "$DRY" = 1 ] && say "(dry-run: nothing was changed)"
  say "Restart your AI tool (or reload commands/skills) so it re-scans. Then try: \"Use the qa-skill-router skill to help me test <your app>\"."
fi
