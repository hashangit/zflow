#!/usr/bin/env python3
"""
ZFlow Workflow Summary Generator

Reads the .zflow/ workspace and produces a summary of workflow progress
including current phase, phases completed, agents used, files changed,
QA issues, and time spent per phase.

Usage:
    python3 generate-summary.py [options]

Options:
    --format <markdown|json>   Output format (default: markdown)
    --output <path>            Write to file instead of stdout
    --workspace <path>         Path to .zflow directory (default: .zflow)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Workspace reader
# ---------------------------------------------------------------------------

class WorkspaceReader:
    """Reads and parses the .zflow/ workspace directory."""

    def __init__(self, workspace_path: str = ".zflow"):
        self.workspace = Path(workspace_path)
        self.errors: List[str] = []

    def exists(self) -> bool:
        return self.workspace.is_dir()

    def read_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """Read a JSON file, returning None on failure."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def read_current_phase(self) -> Dict[str, Any]:
        """Read current-phase.json."""
        path = self.workspace / "current-phase.json"
        data = self.read_json(path)
        return data if data else {}

    def read_config(self) -> Dict[str, Any]:
        """Read config.json."""
        path = self.workspace / "config.json"
        data = self.read_json(path)
        return data if data else {}

    def read_phase_meta(self, phase_dir: Path) -> Dict[str, Any]:
        """Read phase-meta.json from a phase directory."""
        meta_path = phase_dir / "phase-meta.json"
        data = self.read_json(meta_path)
        return data if data else {}

    def get_dev_phases(self) -> List[Dict[str, Any]]:
        """
        Read all dev phase directories under phases/ and return structured
        data for each.
        """
        phases_dir = self.workspace / "phases"
        if not phases_dir.is_dir():
            return []

        results: List[Dict[str, Any]] = []

        # Sort directories numerically
        try:
            phase_dirs = sorted(
                [d for d in phases_dir.iterdir() if d.is_dir()],
                key=lambda d: float(d.name.split("-")[0]),
            )
        except (ValueError, IndexError):
            phase_dirs = sorted(
                [d for d in phases_dir.iterdir() if d.is_dir()],
                key=lambda d: d.name,
            )

        for phase_dir in phase_dirs:
            meta = self.read_phase_meta(phase_dir)

            # Find output files (markdown files that are not phase-meta.json)
            output_files = []
            for f in phase_dir.iterdir():
                if f.is_file() and f.suffix == ".md":
                    output_files.append(f.name)

            # Count files in subdirectories (agent reports, etc.)
            sub_files = []
            for subdir in phase_dir.iterdir():
                if subdir.is_dir():
                    for f in subdir.iterdir():
                        if f.is_file():
                            sub_files.append(str(f.relative_to(phase_dir)))

            results.append({
                "name": phase_dir.name,
                "meta": meta,
                "output_files": output_files,
                "sub_files": sub_files,
            })

        return results

    def get_debug_sessions(self) -> List[Dict[str, Any]]:
        """Read all debug session directories."""
        debug_dir = self.workspace / "debug"
        if not debug_dir.is_dir():
            return []

        results: List[Dict[str, Any]] = []
        for session_dir in sorted(debug_dir.iterdir()):
            if not session_dir.is_dir():
                continue

            phases: List[Dict[str, Any]] = []
            for phase_dir in sorted(session_dir.iterdir()):
                if not phase_dir.is_dir():
                    continue
                meta = self.read_phase_meta(phase_dir)
                output_files = [
                    f.name
                    for f in phase_dir.iterdir()
                    if f.is_file() and f.suffix == ".md"
                ]
                phases.append({
                    "name": phase_dir.name,
                    "meta": meta,
                    "output_files": output_files,
                })

            results.append({
                "session": session_dir.name,
                "phases": phases,
            })

        return results


# ---------------------------------------------------------------------------
# Summary builder
# ---------------------------------------------------------------------------

def compute_duration(started: Optional[str], completed: Optional[str]) -> Optional[str]:
    """Compute a human-readable duration between two ISO timestamps."""
    if not started or not completed:
        return None
    try:
        fmt = "%Y-%m-%dT%H:%M:%S"
        # Handle various ISO formats
        started_clean = started[:19].replace("Z", "")
        completed_clean = completed[:19].replace("Z", "")
        s = datetime.strptime(started_clean, fmt)
        e = datetime.strptime(completed_clean, fmt)
        delta = e - s
        total_seconds = int(delta.total_seconds())
        if total_seconds < 60:
            return f"{total_seconds}s"
        elif total_seconds < 3600:
            return f"{total_seconds // 60}m {total_seconds % 60}s"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    except (ValueError, TypeError):
        return None


def build_summary(reader: WorkspaceReader) -> Dict[str, Any]:
    """Build a structured summary dict from the workspace."""
    current = reader.read_current_phase()
    config = reader.read_config()
    workflow = current.get("workflow", "dev")

    summary: Dict[str, Any] = {
        "workflow_type": workflow,
        "current_phase": current.get("phase", "unknown"),
        "current_status": current.get("status", "unknown"),
        "phases_completed": [],
        "phases_in_progress": None,
        "total_agents_used": 0,
        "total_files_changed": 0,
        "qa_issues": {
            "critical": 0,
            "blocker": 0,
            "major": 0,
            "minor": 0,
            "note": 0,
        },
        "time_per_phase": [],
        "phase_details": [],
    }

    if workflow == "dev":
        phases = reader.get_dev_phases()
    else:
        # For debug, read the active session
        sessions = reader.get_debug_sessions()
        if sessions:
            # Use the latest session
            latest_session = sessions[-1]
            phases = latest_session["phases"]
            summary["debug_session"] = latest_session["session"]
        else:
            phases = []

    for phase in phases:
        meta = phase.get("meta", {})
        status = meta.get("status", "unknown")
        phase_name = phase.get("name", "unknown")

        # Track agents
        agent_count = meta.get("agent_count", 0)
        summary["total_agents_used"] += agent_count

        # Track files changed
        files_changed = meta.get("files_changed", [])
        summary["total_files_changed"] += len(files_changed) if isinstance(files_changed, list) else 0

        # Track duration
        duration = compute_duration(
            meta.get("started_at"),
            meta.get("completed_at"),
        )

        phase_info = {
            "name": phase_name,
            "status": status,
            "agents": agent_count,
            "files_changed": len(files_changed) if isinstance(files_changed, list) else 0,
            "duration": duration,
            "output_files": phase.get("output_files", []),
        }

        summary["phase_details"].append(phase_info)

        if status == "completed":
            summary["phases_completed"].append(phase_name)
        elif status == "in_progress":
            summary["phases_in_progress"] = phase_name

        if duration:
            summary["time_per_phase"].append({
                "phase": phase_name,
                "duration": duration,
            })

    # Try to parse QA report for issue counts
    summary["qa_issues"] = parse_qa_issues(reader, workflow)

    return summary


def parse_qa_issues(reader: WorkspaceReader, workflow: str) -> Dict[str, int]:
    """
    Attempt to parse the QA report to extract issue counts by severity.
    Falls back to zeros if the report is missing or unparseable.
    """
    counts: Dict[str, int] = {
        "critical": 0,
        "blocker": 0,
        "major": 0,
        "minor": 0,
        "note": 0,
    }

    if workflow == "dev":
        qa_path = reader.workspace / "phases" / "05-qa" / "qa-report.md"
    else:
        # For debug, look in the latest session's d5-verify
        debug_dir = reader.workspace / "debug"
        if debug_dir.is_dir():
            sessions = sorted(debug_dir.iterdir())
            if sessions:
                qa_path = sessions[-1] / "d5-verify" / "verification.md"
            else:
                return counts
        else:
            return counts

    if not qa_path.is_file():
        return counts

    try:
        content = qa_path.read_text(encoding="utf-8").lower()
        # Look for severity patterns in the QA report
        for severity in counts:
            # Match patterns like "Critical: 3" or "critical: 3" or
            # "[CRITICAL]" repeated
            import re
            # Count explicit labels
            pattern = rf"\b{severity}\b"
            matches = re.findall(pattern, content)
            counts[severity] = len(matches)
    except Exception:
        pass

    return counts


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_markdown(summary: Dict[str, Any]) -> str:
    """Format the summary as a markdown report."""
    lines: List[str] = []

    lines.append("# ZFlow Workflow Summary")
    lines.append("")
    lines.append(f"**Workflow**: {summary['workflow_type']}")
    lines.append(f"**Current Phase**: {summary['current_phase']}")
    lines.append(f"**Status**: {summary['current_status']}")
    lines.append("")

    # Phases completed
    completed = summary.get("phases_completed", [])
    lines.append(f"**Phases Completed**: {len(completed)}")
    if completed:
        for p in completed:
            lines.append(f"  - {p}")
    lines.append("")

    if summary.get("phases_in_progress"):
        lines.append(f"**Phase In Progress**: {summary['phases_in_progress']}")
        lines.append("")

    # Overall stats
    lines.append("## Overall Statistics")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total agents used | {summary['total_agents_used']} |")
    lines.append(f"| Total files changed | {summary['total_files_changed']} |")
    lines.append("")

    # QA issues
    qa = summary.get("qa_issues", {})
    total_issues = sum(qa.values())
    if total_issues > 0:
        lines.append("## QA Issues")
        lines.append("")
        lines.append(f"| Severity | Count |")
        lines.append(f"|----------|-------|")
        for sev, count in qa.items():
            if count > 0:
                lines.append(f"| {sev.capitalize()} | {count} |")
        lines.append("")

    # Time per phase
    time_entries = summary.get("time_per_phase", [])
    if time_entries:
        lines.append("## Time Spent Per Phase")
        lines.append("")
        lines.append(f"| Phase | Duration |")
        lines.append(f"|-------|----------|")
        for entry in time_entries:
            lines.append(f"| {entry['phase']} | {entry['duration']} |")
        lines.append("")

    # Detailed phase breakdown
    phase_details = summary.get("phase_details", [])
    if phase_details:
        lines.append("## Phase Details")
        lines.append("")
        for phase in phase_details:
            status_icon = {
                "completed": "[x]",
                "in_progress": "[~]",
                "pending": "[ ]",
                "not_started": "[ ]",
                "unknown": "[?]",
            }.get(phase["status"], "[?]")
            lines.append(
                f"### {status_icon} {phase['name']} ({phase['status']})"
            )
            if phase.get("output_files"):
                lines.append(f"- Output: {', '.join(phase['output_files'])}")
            if phase.get("agents"):
                lines.append(f"- Agents: {phase['agents']}")
            if phase.get("files_changed"):
                lines.append(f"- Files changed: {phase['files_changed']}")
            if phase.get("duration"):
                lines.append(f"- Duration: {phase['duration']}")
            lines.append("")

    return "\n".join(lines)


def format_json(summary: Dict[str, Any]) -> str:
    """Format the summary as JSON."""
    return json.dumps(summary, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a ZFlow workflow summary report"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Write to file instead of stdout",
    )
    parser.add_argument(
        "--workspace",
        default=".zflow",
        help="Path to .zflow directory (default: .zflow)",
    )
    args = parser.parse_args()

    reader = WorkspaceReader(args.workspace)

    if not reader.exists():
        print(
            f"Error: Workspace directory '{args.workspace}' not found. "
            "Run a ZFlow workflow (which auto-initializes) or run init-workspace.sh manually.",
            file=sys.stderr,
        )
        sys.exit(1)

    summary = build_summary(reader)

    if args.format == "json":
        output = format_json(summary)
    else:
        output = format_markdown(summary)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Summary written to {args.output}")
        except OSError as exc:
            print(f"Error writing file: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
