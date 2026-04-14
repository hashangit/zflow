#!/usr/bin/env bash
# =============================================================================
# ZFlow Workspace Initializer (Optional CLI Convenience)
#
# NOTE: The ZFlow orchestrator handles workspace initialization automatically
# when a workflow starts. This script is an optional convenience for users who
# want to pre-initialize a workspace from the command line before invoking ZFlow.
#
# Usage:
#   ./init-workspace.sh [dev|debug]
#
# Arguments:
#   dev   - Initialize for development workflow (default)
#   debug - Initialize for debugging workflow
#
# The script is idempotent — safe to run multiple times without side effects.
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKFLOW_TYPE="${1:-dev}"
ZFLOW_DIR=".zflow"
PHASES_DIR="${ZFLOW_DIR}/phases"
DEBUG_DIR="${ZFLOW_DIR}/debug"

# Dev workflow phases (directory name => starting output file)
declare -A DEV_PHASES=(
  ["00-brainstorm"]="scope.md"
  ["01-research"]="research-report.md"
  ["02-design"]="solution.md"
  ["03-review"]="reviewed-solution.md"
  ["03.5-ui-design"]="ui-design-report.md"
  ["04-implement"]="implementation-plan.md"
  ["05-qa"]="qa-report.md"
  ["06-document"]="changes-summary.md"
)

# Debug workflow phases
declare -A DEBUG_PHASES=(
  ["d0-reproduce"]="repro-report.md"
  ["d1-investigate"]="investigation.md"
  ["d2-analyze"]="root-cause.md"
  ["d3-design-fix"]="fix-design.md"
  ["d4-implement-fix"]="fix-impl-report.md"
  ["d5-verify"]="verification.md"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

info()  { echo "[zflow] $*"; }
warn()  { echo "[zflow] WARNING: $*" >&2; }
error() { echo "[zflow] ERROR: $*" >&2; }

# Generate a timestamp suitable for directory names (ISO 8601 compact)
timestamp() {
  date +"%Y%m%dT%H%M%S"
}

# Write a JSON file only if it does not already exist (idempotent).
# Usage: write_if_missing <path> <content>
write_if_missing() {
  local path="$1"
  local content="$2"

  if [[ -f "${path}" ]]; then
    info "Already exists (kept): ${path}"
    return 0
  fi

  echo "${content}" > "${path}"
  info "Created: ${path}"
}

# Create a directory only if it does not already exist.
mkdir_if_missing() {
  local dir="$1"

  if [[ -d "${dir}" ]]; then
    return 0
  fi

  mkdir -p "${dir}"
  info "Created directory: ${dir}"
}

# ---------------------------------------------------------------------------
# Default config.json content (from design plan Section 11.1)
# ---------------------------------------------------------------------------

DEFAULT_CONFIG=$(cat <<'CONFIG_EOF'
{
  "workflow": {
    "gates": {
      "brainstorm": "human",
      "research": "auto",
      "design": "human",
      "review": "human",
      "ui_design": "human",
      "implement": "auto",
      "qa": "human",
      "document": "auto"
    },
    "skip_phases": [],
    "max_parallel_agents": 5
  },
  "ui": {
    "pencil_enabled": "auto",
    "design_system": null,
    "component_library": null
  },
  "security": {
    "audit_depth": "full",
    "owasp_categories": "all",
    "dependency_scan": true,
    "secrets_scan": true,
    "security_severity_threshold": "medium"
  },
  "debug": {
    "escalation_threshold": 3,
    "auto_run_tests": true,
    "security_impact_assessment": true,
    "gates": {
      "reproduce": "auto",
      "investigate": "auto",
      "analyze": "human",
      "design_fix": "human",
      "implement_fix": "auto",
      "verify": "auto"
    }
  },
  "karpathy": {
    "simplicity_enforcement": "strict",
    "surgical_changes_enforcement": "strict",
    "require_success_criteria": true
  },
  "preferences": {
    "commit_style": "conventional",
    "test_command": "npm test",
    "lint_command": "npm run lint",
    "language": "typescript"
  }
}
CONFIG_EOF
)

# ---------------------------------------------------------------------------
# Phase-meta.json template (written into each phase directory)
# ---------------------------------------------------------------------------

phase_meta_template() {
  local phase_name="$1"
  cat <<META_EOF
{
  "phase": "${phase_name}",
  "status": "pending",
  "started_at": null,
  "completed_at": null,
  "agent_count": 0,
  "files_changed": [],
  "notes": []
}
META_EOF
}

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

if [[ "${WORKFLOW_TYPE}" != "dev" && "${WORKFLOW_TYPE}" != "debug" ]]; then
  error "Unknown workflow type '${WORKFLOW_TYPE}'. Use 'dev' or 'debug'."
  exit 1
fi

# If a workspace already exists for a *different* workflow type, warn.
if [[ -f "${ZFLOW_DIR}/config.json" ]]; then
  existing_workflow=$(python3 -c "
import json, sys
try:
    with open('${ZFLOW_DIR}/config.json') as f:
        print(json.load(f).get('_zflow_workflow', 'dev'))
except Exception:
    print('dev')
" 2>/dev/null || echo "dev")

  if [[ "${existing_workflow}" != "${WORKFLOW_TYPE}" ]]; then
    warn "Existing workspace is for '${existing_workflow}' workflow. Re-initializing for '${WORKFLOW_TYPE}'."
  fi
fi

# ---------------------------------------------------------------------------
# Create workspace root
# ---------------------------------------------------------------------------

mkdir_if_missing "${ZFLOW_DIR}"
mkdir_if_missing "${PHASES_DIR}"

# ---------------------------------------------------------------------------
# Initialize based on workflow type
# ---------------------------------------------------------------------------

if [[ "${WORKFLOW_TYPE}" == "dev" ]]; then

  # -- Dev workflow --
  info "Initializing DEV workflow workspace..."

  # current-phase.json — starts at brainstorm
  write_if_missing "${ZFLOW_DIR}/current-phase.json" '{
  "workflow": "dev",
  "phase": "brainstorm",
  "status": "not_started",
  "started_at": null,
  "updated_at": null
}'

  # config.json — stamp the workflow type inside the config
  if [[ ! -f "${ZFLOW_DIR}/config.json" ]]; then
    # Inject _zflow_workflow field so we can detect the type later
    CONFIG_WITH_TAG=$(echo "${DEFAULT_CONFIG}" | python3 -c "
import json, sys
cfg = json.load(sys.stdin)
cfg['_zflow_workflow'] = 'dev'
print(json.dumps(cfg, indent=2))
")
    write_if_missing "${ZFLOW_DIR}/config.json" "${CONFIG_WITH_TAG}"
  fi

  # Phase directories
  for phase_dir in "${!DEV_PHASES[@]}"; do
    full_dir="${PHASES_DIR}/${phase_dir}"
    mkdir_if_missing "${full_dir}"

    # phase-meta.json
    write_if_missing "${full_dir}/phase-meta.json" "$(phase_meta_template "${phase_dir}")"

    # Create subdirectories used by some phases
    case "${phase_dir}" in
      01-research)
        mkdir_if_missing "${full_dir}/agent-reports"
        ;;
      03-review)
        mkdir_if_missing "${full_dir}/reviewer-reports"
        ;;
      03.5-ui-design)
        # conditional — created anyway for idempotency
        ;;
      04-implement)
        mkdir_if_missing "${full_dir}/task-reports"
        ;;
      05-qa)
        mkdir_if_missing "${full_dir}/dimension-reports"
        ;;
    esac
  done

  info "DEV workspace initialized at ${ZFLOW_DIR}/"

elif [[ "${WORKFLOW_TYPE}" == "debug" ]]; then

  # -- Debug workflow --
  info "Initializing DEBUG workflow workspace..."

  SESSION_TS=$(timestamp)
  SESSION_DIR="${DEBUG_DIR}/session-${SESSION_TS}"

  # current-phase.json — starts at reproduce
  write_if_missing "${ZFLOW_DIR}/current-phase.json" "{
  \"workflow\": \"debug\",
  \"session\": \"session-${SESSION_TS}\",
  \"phase\": \"reproduce\",
  \"status\": \"not_started\",
  \"started_at\": null,
  \"updated_at\": null
}"

  # config.json
  if [[ ! -f "${ZFLOW_DIR}/config.json" ]]; then
    CONFIG_WITH_TAG=$(echo "${DEFAULT_CONFIG}" | python3 -c "
import json, sys
cfg = json.load(sys.stdin)
cfg['_zflow_workflow'] = 'debug'
print(json.dumps(cfg, indent=2))
")
    write_if_missing "${ZFLOW_DIR}/config.json" "${CONFIG_WITH_TAG}"
  fi

  # Debug session directories
  for phase_dir in "${!DEBUG_PHASES[@]}"; do
    full_dir="${SESSION_DIR}/${phase_dir}"
    mkdir_if_missing "${full_dir}"
    write_if_missing "${full_dir}/phase-meta.json" "$(phase_meta_template "${phase_dir}")"
  done

  info "DEBUG workspace initialized at ${SESSION_DIR}/"

fi

info "Done. Workflow type: ${WORKFLOW_TYPE}"
