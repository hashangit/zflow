#!/usr/bin/env python3
"""
ZFlow Phase Output Validator

Validates that a phase output file exists and follows the expected template
structure before allowing a phase transition.

Usage:
    python3 validate-phase.py <phase-name> <output-file-path>

Phase names (dev workflow):
    scope, research-report, solution, reviewed-solution,
    ui-design-report, implementation-plan, impl-report, qa-report

Phase names (debug workflow):
    repro-report, investigation, root-cause, fix-design,
    fix-impl-report, verification

Exit codes:
    0 — valid
    1 — invalid (errors printed to stderr)
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Phase definitions: required H2-level sections for each phase output.
# The validator checks that at least one heading matching each pattern exists.
# ---------------------------------------------------------------------------

PHASE_REQUIREMENTS: Dict[str, Dict] = {
    # ── Dev workflow ──────────────────────────────────────────────────────
    "scope": {
        "display": "Phase 0: Brainstorm — scope.md",
        "required_sections": [
            "Problem Statement",
            "Success Criteria",
            "Constraints",
            "Scope Boundaries",
            "MVP Definition",
        ],
        # Sections that are often left as boilerplate — reject if unchanged
        "non_boilerplate_patterns": [
            ("Problem Statement", r"\[Describe"),
            ("Success Criteria", r"\[Define"),
            ("Constraints", r"\[List"),
        ],
    },
    "research-report": {
        "display": "Phase 1: Research — research-report.md",
        "required_sections": [
            "Architecture",
            "Dependencies",
            "Patterns",
            "Test Infrastructure",
            "Key Findings",
        ],
    },
    "solution": {
        "display": "Phase 2: Design — solution.md",
        "required_sections": [
            "Chosen Approach",
            "Architecture Overview",
            "Component Breakdown",
            "Data Flow",
            "Error Handling",
            "Testing Strategy",
            "Task Breakdown",
        ],
    },
    "reviewed-solution": {
        "display": "Phase 3: Review — reviewed-solution.md",
        "required_sections": [
            "Original Solution",
            "Review Appendix",
            "Self-Review Fixes",
        ],
    },
    "ui-design-report": {
        "display": "Phase 3.5: UI Design — ui-design-report.md",
        "required_sections": [
            "Design System",
            "Component Specifications",
            "Screen-by-Screen Layouts",
        ],
    },
    "implementation-plan": {
        "display": "Phase 4: Implement — implementation-plan.md",
        "required_sections": [
            "Overview",
            "Dependency Graph",
            "Tier Breakdown",
            "Execution Order",
        ],
    },
    "impl-report": {
        "display": "Phase 4: Implement — impl-report.md",
        "required_sections": [
            "Executive Summary",
            "Per-Task Reports",
            "Files Changed",
            "Deviations",
            "Ready for QA",
        ],
    },
    "qa-report": {
        "display": "Phase 5: QA — qa-report.md",
        "required_sections": [
            "Executive Summary",
            "Findings",
            "Severity Breakdown",
        ],
    },
    # ── Debug workflow ────────────────────────────────────────────────────
    "repro-report": {
        "display": "Phase D0: Reproduce — repro-report.md",
        "required_sections": [
            "Bug Description",
            "Reproduction Steps",
            "Expected Behavior",
            "Actual Behavior",
            "Environment",
        ],
    },
    "investigation": {
        "display": "Phase D1: Investigate — investigation.md",
        "required_sections": [
            "Executive Summary",
            "Call Chain Analysis",
            "Data Flow Analysis",
            "Pattern Scan Results",
            "Git History Findings",
            "Cross-Cutting Observations",
        ],
    },
    "root-cause": {
        "display": "Phase D2: Analyze — root-cause.md",
        "required_sections": [
            "Root Cause Statement",
            "Causal Chain",
            "Defect Location",
            "Confidence Level",
        ],
    },
    "fix-design": {
        "display": "Phase D3: Design Fix — fix-design.md",
        "required_sections": [
            "Root Cause Reference",
            "Proposed Fix",
            "Regression Risk Assessment",
        ],
    },
    "fix-impl-report": {
        "display": "Phase D4: Implement Fix — fix-impl-report.md",
        "required_sections": [
            "Executive Summary",
            "Per-Task Reports",
            "Files Changed",
            "Ready for QA",
        ],
    },
    "verification": {
        "display": "Phase D5: Verify — verification.md",
        "required_sections": [
            "Verification Summary",
            "Original Bug Verification",
            "Regression Test Results",
        ],
    },
}


# ---------------------------------------------------------------------------
# Markdown heading extraction
# ---------------------------------------------------------------------------

def extract_headings(content: str) -> List[Tuple[int, str]]:
    """
    Extract markdown headings from content.

    Returns a list of (level, heading_text) tuples.
    Handles both ATX (# Heading) and setext (underlined) styles.
    """
    headings: List[Tuple[int, str]] = []

    for line in content.splitlines():
        line_stripped = line.rstrip()

        # ATX-style headings: ## Heading
        atx_match = re.match(r"^(#{1,6})\s+(.+)$", line_stripped)
        if atx_match:
            level = len(atx_match.group(1))
            text = atx_match.group(2).strip()
            # Remove trailing hashes
            text = re.sub(r"\s*#+\s*$", "", text).strip()
            headings.append((level, text))

    return headings


def section_matches(required: str, actual: str) -> bool:
    """
    Check if an actual heading matches a required section name.

    Uses case-insensitive substring matching to be resilient to
    minor wording differences (e.g., "Architecture Overview" matches
    a heading "Architecture Overview & Design").
    """
    req_lower = required.lower()
    act_lower = actual.lower()
    return req_lower in act_lower


def is_boilerplate(section_name: str, content: str, pattern: str) -> bool:
    """
    Check if a section still contains boilerplate placeholder text.
    Returns True if the section appears to be unchanged from template.
    """
    # Find the section content (text between this heading and the next)
    in_section = False
    section_lines: List[str] = []

    for line in content.splitlines():
        heading_match = re.match(r"^#{1,6}\s+(.+)$", line)
        if heading_match:
            heading_text = heading_match.group(1).strip()
            heading_text = re.sub(r"\s*#+\s*$", "", heading_text).strip()
            if section_matches(section_name, heading_text):
                in_section = True
                continue
            elif in_section:
                # We've hit the next heading — stop collecting
                break
        elif in_section:
            section_lines.append(line)

    section_text = "\n".join(section_lines)
    return bool(re.search(pattern, section_text))


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------

def validate(phase_name: str, file_path: str) -> List[str]:
    """
    Validate a phase output file. Returns a list of error strings
    (empty list means valid).
    """
    errors: List[str] = []

    # 1. Check the phase is known
    if phase_name not in PHASE_REQUIREMENTS:
        errors.append(
            f"Unknown phase '{phase_name}'. "
            f"Valid phases: {', '.join(sorted(PHASE_REQUIREMENTS.keys()))}"
        )
        return errors

    phase_spec = PHASE_REQUIREMENTS[phase_name]

    # 2. Check the file exists
    if not os.path.isfile(file_path):
        errors.append(f"Output file does not exist: {file_path}")
        return errors

    # 3. Read file content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:
        errors.append(f"Cannot read file: {exc}")
        return errors

    if not content.strip():
        errors.append("Output file is empty")
        return errors

    # 4. Extract headings
    headings = extract_headings(content)
    heading_texts = [h[1] for h in headings]

    if not heading_texts:
        errors.append("No markdown headings found in output file")
        return errors

    # 5. Check required sections
    for required in phase_spec["required_sections"]:
        found = any(section_matches(required, ht) for ht in heading_texts)
        if not found:
            errors.append(
                f"Missing required section: '{required}' "
                f"(phase: {phase_spec['display']})"
            )

    # 6. Check for boilerplate (unfilled template placeholders)
    non_boilerplate = phase_spec.get("non_boilerplate_patterns", [])
    for section_name, pattern in non_boilerplate:
        if is_boilerplate(section_name, content, pattern):
            errors.append(
                f"Section '{section_name}' appears to contain unfilled "
                f"template boilerplate"
            )

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) != 3:
        print(
            "Usage: python3 validate-phase.py <phase-name> <output-file-path>\n"
            "\n"
            "Valid phase names:\n"
            f"  Dev:    {', '.join(p for p in PHASE_REQUIREMENTS if not p.startswith('repro') and not p.startswith('investigation') and not p.startswith('root') and not p.startswith('fix') and not p.startswith('verification'))}\n"
            f"  Debug:  repro-report, investigation, root-cause, fix-design, fix-impl-report, verification\n"
            "\n"
            "Exit codes: 0 = valid, 1 = invalid",
            file=sys.stderr,
        )
        sys.exit(1)

    phase_name = sys.argv[1]
    file_path = sys.argv[2]

    errors = validate(phase_name, file_path)

    if errors:
        print(f"Validation FAILED for phase '{phase_name}':", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        phase_spec = PHASE_REQUIREMENTS.get(phase_name, {})
        display = phase_spec.get("display", phase_name)
        print(f"Validation PASSED: {display}")
        sys.exit(0)


if __name__ == "__main__":
    main()
