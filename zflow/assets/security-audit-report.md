# Security Audit Report

> Produced by ZFlow Phase 5: QA -- Security Auditor Agent.
> Agent: security-auditor.md (OWASP Top 10 2025 systematic audit).
> Input: reviewed-solution.md + impl-report.md + actual code changes + scope.md.

## Template Guidance

This template provides a recommended structure. Sections marked **Required** must
be present — downstream phases depend on them. Sections marked **Expected** should
be present unless you note a reason for omission. Sections marked **Optional** are
suggestions — include, restructure, or omit as the task demands. Produce output
proportional to complexity.

---

---

## Executive Summary

- **Total findings**: N
- **Critical**: N | **High**: N | **Medium**: N | **Low**: N | **Informational**: N
- **OWASP categories with findings**: {list, e.g., A01, A05, A09}
- **OWASP categories clean**: {list, e.g., A02, A03, A04, A06, A07, A08, A10}

---

## Findings

### [SEV-001] {Finding Title}

- **Severity**: Critical | High | Medium | Low | Informational
- **OWASP Category**: A01 | A02 | A03 | A04 | A05 | A06 | A07 | A08 | A09 | A10 | Additional
- **Location**: `file:line`
- **Description**: {What was found. Factual description of the vulnerability or weakness.}
- **Attack Scenario**: {Step-by-step how an attacker could exploit this. Concrete, not
  theoretical. Must demonstrate actual exploitability in context.}
- **Evidence**:
  ```
  {Code snippet showing the vulnerability. Include surrounding context for clarity.}
  ```
- **Remediation**: {Specific fix with code example showing the corrected approach.}
  ```
  {Corrected code snippet}
  ```
- **Verification**: {How to confirm the fix works. Specific test or check to perform.}

### [SEV-002] {Finding Title}

- **Severity**: {Level}
- **OWASP Category**: {Category}
- **Location**: `file:line`
- **Description**: {What was found}
- **Attack Scenario**: {How this could be exploited}
- **Evidence**:
  ```
  {Code snippet}
  ```
- **Remediation**: {Fix with code example}
- **Verification**: {How to confirm}

{Continue for each finding. Number sequentially as SEV-001, SEV-002, etc.}

---

## Clean Categories

The following OWASP categories were systematically reviewed and no findings
were identified:

| Category | Name | Areas Checked |
|----------|------|---------------|
| {A0X} | {Category Name} | {What was reviewed} |
| {A0X} | {Category Name} | {What was reviewed} |

{List all categories where no vulnerabilities were found. This is important:
it confirms the audit was performed, not skipped.}

---

## Dependency Audit

- **Command run**: {e.g., `npm audit --production` or `pip-audit`}
- **Results summary**: {High-level summary of audit output}
- **Total dependencies scanned**: N
- **Vulnerabilities found**:

| Package | Severity | CVE | Description | Status |
|---------|----------|-----|-------------|--------|
| {name} | {level} | {CVE-ID} | {brief description} | Fixable / No fix available |

- **Recommendations**:
  - {Update package X to version Y}
  - {Replace package Z with alternative}
  - {Pin package W to safe version}

---

## Recommendations

### Immediate Actions (Critical / High Findings)

These must be addressed before the code is merged:

1. **[SEV-XXX]**: {Action} -- {Timeline: before merge}
2. **[SEV-XXX]**: {Action} -- {Timeline: before merge}

### Short-Term Improvements (Medium Findings)

These should be addressed in the near term to reduce risk:

1. **[SEV-XXX]**: {Action}
2. **[SEV-XXX]**: {Action}

### Long-Term Security Posture (Low / Informational)

These enhance overall security posture over time:

1. **[SEV-XXX]**: {Action}
2. {General recommendation based on audit patterns observed}

---

## Audit Scope and Methodology

- **Audit type**: OWASP Top 10 2025 systematic code review
- **Additional checks**: Secrets exposure, CSRF, file upload, API security
- **Files reviewed**: {count} files ({list key files)}
- **Scope**: Code changes from Phase 4 implementation only
- **Limitations**: {Any categories or areas that could not be fully audited,
  e.g., "runtime configuration not verifiable from code review alone"}
