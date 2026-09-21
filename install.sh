#!/usr/bin/env bash
# Software Tester Skills Universal Installer
# Compatible with Google Antigravity, Claude Code, OpenAI Codex, Cursor, Gemini CLI, OpenCode

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"

print_help() {
  cat << EOF
Software Tester Skills Universal Installer

Usage:
  ./install.sh [options]

Options:
  --antigravity    Install skills globally for Google Antigravity & Gemini CLI (~/.gemini/config/skills)
  --claude         Install skills globally for Claude Code (~/.claude/skills)
  --agents         Install skills into user cross-runtime agent directory (~/.agents/skills)
  --project        Install skills into current project (.agents/skills)
  --all            Install into all global locations (Antigravity, Claude, .agents)
  --help           Show this help message

If no options are passed, the script prompts for target or defaults to --all.
EOF
}

install_to() {
  local target="$1"
  local name="$2"
  echo "==> Installing 46 Software Tester Skills to $name ($target)..."
  mkdir -p "$target"
  
  local count=0
  for skill_path in "$SKILLS_DIR"/*; do
    if [ -d "$skill_path" ]; then
      local skill_name
      skill_name="$(basename "$skill_path")"
      local dest="$target/$skill_name"
      
      # Copy files cleanly
      rm -rf "$dest"
      cp -R "$skill_path" "$dest"
      count=$((count + 1))
    fi
  done
  echo "    Successfully installed $count skills to $target."
}

MODE="${1:-}"

case "$MODE" in
  --antigravity)
    install_to "$HOME/.gemini/config/skills" "Google Antigravity / Gemini CLI"
    ;;
  --claude)
    install_to "$HOME/.claude/skills" "Claude Code"
    ;;
  --agents)
    install_to "$HOME/.agents/skills" "Cross-runtime Agents Directory"
    ;;
  --project)
    install_to "$(pwd)/.agents/skills" "Project Workspace (.agents/skills)"
    ;;
  --all|"")
    install_to "$HOME/.gemini/config/skills" "Google Antigravity / Gemini CLI"
    install_to "$HOME/.claude/skills" "Claude Code"
    install_to "$HOME/.agents/skills" "Cross-runtime Agents Directory"
    ;;
  --help|-h)
    print_help
    exit 0
    ;;
  *)
    echo "Unknown option: $MODE"
    print_help
    exit 1
    ;;
esac

echo ""
echo "Done! Your AI coding agents now have access to all Software Tester skills."
