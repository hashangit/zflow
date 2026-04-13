#!/usr/bin/env bash
# =============================================================================
# ZFlow Pencil.dev Availability Checker
#
# Detects whether Pencil.dev MCP tools are available to the current
# Claude Code session. Used by the ZFlow orchestrator to decide whether
# to offer the Pencil.dev design-first UI workflow (Phase 3.5).
#
# The primary mechanism checks for Pencil MCP server configuration in
# Claude Code settings files and for .pencil/ project artifacts.
#
# Exit codes:
#   0 — Pencil.dev appears to be available
#   1 — Pencil.dev is not available
#
# Usage:
#   ./check-pencil-availability.sh
# =============================================================================

set -uo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Directories to check for Pencil configuration
CANDIDATE_SETTINGS_DIRS=(
  "."
  ".."
)

# Settings file names (checked in order of specificity)
SETTINGS_FILES=(
  ".claude/settings.json"
  ".claude/settings.local.json"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

info()  { echo "[pencil-check] $*"; }
debug() { :; }  # no-op by default; set DEBUG=1 to enable

# ---------------------------------------------------------------------------
# Check 1: Look for .pencil/ directory in the project tree
# ---------------------------------------------------------------------------

check_pencil_dir() {
  local found=1  # 1 = not found

  # Check current directory and parent
  for dir in "${CANDIDATE_SETTINGS_DIRS[@]}"; do
    if [[ -d "${dir}/.pencil" ]]; then
      debug "Found .pencil/ in ${dir}"
      found=0
      break
    fi
  done

  # Check home directory for global .pencil config
  if [[ -d "${HOME}/.pencil" ]]; then
    debug "Found ~/.pencil/"
    found=0
  fi

  return ${found}
}

# ---------------------------------------------------------------------------
# Check 2: Look for Pencil MCP server in Claude Code settings
# ---------------------------------------------------------------------------

check_claude_settings() {
  local found=1  # 1 = not found

  for dir in "${CANDIDATE_SETTINGS_DIRS[@]}"; do
    for settings_file in "${SETTINGS_FILES[@]}"; do
      local full_path="${dir}/${settings_file}"
      if [[ -f "${full_path}" ]]; then
        debug "Checking ${full_path}"
        # Look for "pencil" in the MCP servers configuration.
        # Claude Code stores MCP servers under mcpServers or similar keys.
        if python3 -c "
import json, sys
try:
    with open('${full_path}') as f:
        data = json.load(f)
    # Check common locations for MCP server definitions
    mcp = data.get('mcpServers', data.get('mcp_servers', {}))
    for key in mcp:
        if 'pencil' in key.lower():
            sys.exit(0)
    sys.exit(1)
except (json.JSONDecodeError, FileNotFoundError, KeyError):
    sys.exit(1)
" 2>/dev/null; then
          debug "Found Pencil MCP config in ${full_path}"
          found=0
          break 2
        fi
      fi
    done
  done

  # Also check global Claude settings
  local global_settings="${HOME}/.claude/settings.json"
  if [[ -f "${global_settings}" ]]; then
    if python3 -c "
import json, sys
try:
    with open('${global_settings}') as f:
        data = json.load(f)
    mcp = data.get('mcpServers', data.get('mcp_servers', {}))
    for key in mcp:
        if 'pencil' in key.lower():
            sys.exit(0)
    sys.exit(1)
except (json.JSONDecodeError, FileNotFoundError, KeyError):
    sys.exit(1)
" 2>/dev/null; then
      debug "Found Pencil MCP config in global settings"
      found=0
    fi
  fi

  return ${found}
}

# ---------------------------------------------------------------------------
# Check 3: Look for .pen files in the project
# ---------------------------------------------------------------------------

check_pen_files() {
  local found=1  # 1 = not found

  # Quick check for any .pen files (depth-limited to avoid slow searches)
  if command -v find &>/dev/null; then
    if find . -maxdepth 3 -name "*.pen" -type f 2>/dev/null | head -1 | grep -q .; then
      debug "Found .pen files in project"
      found=0
    fi
  fi

  return ${found}
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

available=false
reasons=()

# Run all checks — any one passing is sufficient
if check_pencil_dir; then
  available=true
  reasons+=(".pencil/ directory found")
fi

if check_claude_settings; then
  available=true
  reasons+=("Pencil MCP server configured in Claude settings")
fi

if check_pen_files; then
  available=true
  reasons+=(".pen design files found in project")
fi

# Output result
if ${available}; then
  echo "available"
  info "Pencil.dev IS available"
  for r in "${reasons[@]}"; do
    info "  Reason: ${r}"
  done
  exit 0
else
  echo "unavailable"
  info "Pencil.dev is NOT available"
  info "No .pencil/ directory, MCP config, or .pen files found."
  info "To enable: install the Pencil MCP server for Claude Code."
  exit 1
fi
