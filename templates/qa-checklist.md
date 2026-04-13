# QA Checklist

> Quick reference checklist for each QA dimension.
> Use as a hand-off summary or rapid verification guide.

---

## Completeness Check

- [ ] Every task from reviewed-solution.md has a corresponding implementation
- [ ] No tasks marked complete that have partial implementations
- [ ] All success criteria from the task breakdown are met
- [ ] No TODO/FIXME/HACK comments indicating incomplete work
- [ ] No placeholder values (empty functions, stubbed logic, fake data)
- [ ] New modules are imported and wired into the system
- [ ] New routes/endpoints are registered
- [ ] New database tables/migrations are referenced
- [ ] No orphan files (created but never used)

---

## UX Review

- [ ] API function names are self-explanatory
- [ ] Parameter names are clear and consistent with codebase conventions
- [ ] Required vs. optional parameters follow a logical pattern
- [ ] Error messages explain the problem AND suggest a fix
- [ ] Error messages are written for users, not developers
- [ ] Validation errors are specific (not "invalid input")
- [ ] HTTP status codes are correct and consistent
- [ ] Edge cases handled: empty input, null values, extreme sizes
- [ ] Concurrent operations handled gracefully
- [ ] External dependency failures have graceful degradation
- [ ] Public APIs are documented with examples
- [ ] Documentation matches actual behavior
- [ ] Naming conventions are consistent with existing codebase
- [ ] Error handling patterns are consistent (not mix-and-match)
- [ ] If UI: interactive elements are keyboard-navigable
- [ ] If UI: form fields have associated labels
- [ ] If UI: color is not the only visual indicator

---

## Code Quality (Karpathy Enforcement)

### Scope Traceability
- [ ] Every changed line traces to a requirement in scope.md or a task in reviewed-solution.md
- [ ] No code exists that cannot be traced to scope

### Speculative Code Detection
- [ ] No configuration options that were not requested
- [ ] No abstractions created "for future use" or "for flexibility"
- [ ] No code handling scenarios not in the scope or design
- [ ] No extra logging/telemetry beyond what the design specified
- [ ] No unused helper/utility functions

### Unnecessary Abstraction Detection
- [ ] No interfaces or abstract classes with a single implementation
- [ ] No factory patterns used only once
- [ ] No strategy patterns used only once
- [ ] No wrapper functions that add no value
- [ ] No configuration-driven behavior with only one configuration
- [ ] No generic implementations where a specific one suffices

### Surgical Changes
- [ ] No refactored code outside the scope area
- [ ] No reformatted code outside the change area
- [ ] No comment changes unrelated to the implementation
- [ ] No import changes that do not correspond to new code
- [ ] No renamed variables/functions outside the change area

### Traditional Quality
- [ ] Naming conventions consistent with codebase
- [ ] No unused imports or variables
- [ ] Functions under 50 lines (or justifiably longer)
- [ ] No deeply nested logic (more than 3 levels)
- [ ] No copy-pasted code within the changes
- [ ] No swallowed exceptions (catch blocks that do nothing)
- [ ] No generic catch-all where specific errors should be handled
- [ ] No sensitive data in log statements
- [ ] Log levels used consistently

---

## Test Coverage

- [ ] Every new/modified unit has a corresponding test file
- [ ] Test files actually test the target code (not just import it)
- [ ] Happy path tested for each unit
- [ ] Error paths tested for each unit
- [ ] Edge cases tested (empty, null, max, zero)
- [ ] Integration points tested
- [ ] Tests have clear Arrange-Act-Assert structure
- [ ] Test names are descriptive
- [ ] Assertions are specific (not just "not null")
- [ ] Tests do not depend on execution order
- [ ] Tests do not share mutable state
- [ ] External dependencies are mocked/stubbed
- [ ] No time-dependent assertions without time control
- [ ] No tests that rely on network or external services
- [ ] No hardcoded timeouts (prefer event-based waiting)

---

## Design Alignment

- [ ] Overall architecture matches the architecture overview
- [ ] Component boundaries are where the design placed them
- [ ] No new components introduced without design approval
- [ ] Data flow matches the designed data flow
- [ ] State management follows the designed approach
- [ ] Data contracts (input/output) match the design
- [ ] Persistence follows the designed schema/storage
- [ ] Failure modes match the design's failure table
- [ ] Recovery strategies are implemented as designed
- [ ] User-facing error messages follow design specifications
- [ ] Edge cases from the design are handled as specified
- [ ] No features implemented that are NOT in the design (scope drift)
- [ ] No design features silently dropped without justification
- [ ] All documented deviations in impl-report.md have valid justification

---

## Security Audit (OWASP Top 10 2025)

### A01: Broken Access Control
- [ ] Authorization checks before ALL data access operations
- [ ] Object ownership validation (requesting user owns the resource)
- [ ] Role/permission validation per endpoint
- [ ] No IDOR vulnerabilities
- [ ] CORS headers are restrictive (not wildcard with credentials)
- [ ] No SSRF vulnerabilities

### A02: Security Misconfiguration
- [ ] No default credentials enabled
- [ ] Error messages are generic to users (no stack traces/paths)
- [ ] Security headers present (CSP, X-Frame-Options, HSTS, X-Content-Type-Options)
- [ ] Debug mode disabled in production
- [ ] No exposed configuration with secrets

### A03: Supply Chain
- [ ] Dependency audit run (npm audit / pip-audit / equivalent)
- [ ] No known CVEs in dependencies
- [ ] Lock files exist and are committed
- [ ] No suspicious or typosquatted package names

### A04: Cryptographic Failures
- [ ] No weak hashing (MD5/SHA1) for passwords
- [ ] No hardcoded encryption keys or salts
- [ ] Sensitive data encrypted at rest
- [ ] TLS enforced for data in transit
- [ ] Secure random number generation for security values
- [ ] Passwords hashed with bcrypt/scrypt/Argon2

### A05: Injection
- [ ] All user input traced to query/command execution
- [ ] Parameterized queries/prepared statements used
- [ ] Output encoding is context-appropriate
- [ ] No string concatenation in queries
- [ ] No dynamic code evaluation with user input
- [ ] No direct shell execution with user-controlled input

### A06: Insecure Design
- [ ] Business logic steps cannot be skipped
- [ ] No race conditions in financial/sensitive operations
- [ ] Rate limiting on login, signup, sensitive API calls
- [ ] Input validation enforces business rules
- [ ] Workflows cannot be bypassed via direct API calls

### A07: Authentication Failures
- [ ] Password policy meets minimum strength requirements
- [ ] Brute-force protection (lockout after N failures)
- [ ] Session tokens are cryptographically random with expiration
- [ ] No credentials in logs or error responses
- [ ] No hardcoded credentials

### A08: Integrity Failures
- [ ] No insecure deserialization of untrusted data
- [ ] Integrity checks on external data
- [ ] CI/CD config does not expose secrets

### A09: Logging Failures
- [ ] Security events logged (login, access denied, privilege changes)
- [ ] No secrets in log output
- [ ] Log entries include sufficient context for incident response
- [ ] Log output is sanitized (no injection)

### A10: Exception Handling
- [ ] No "failing open" (defaulting to allow on error)
- [ ] No silently swallowed exceptions
- [ ] No sensitive information in error responses to users
- [ ] All critical paths have proper error handling

### Additional Security Checks
- [ ] No secrets/API keys in source code
- [ ] .env files are in .gitignore
- [ ] CSRF tokens on state-changing requests
- [ ] File upload validation (type, size, path traversal)
- [ ] API rate limiting, input validation, size limits
- [ ] No sensitive data in URL parameters

---

## UI Visual QA (Conditional)

*Only applicable when UI work is in scope and Pencil.dev designs exist.*

### Design Token Compliance
- [ ] Color values match design tokens (not hardcoded approximations)
- [ ] Font family, size, and weight match design tokens
- [ ] Spacing follows the design system grid
- [ ] Border radii are consistent with design system
- [ ] Shadows and elevation values match specifications

### Component Fidelity
- [ ] Component structure matches design hierarchy
- [ ] Interactive states correct (hover, focus, active, disabled)
- [ ] Transitions and animations as specified
- [ ] Icons and imagery are correct and properly sized
- [ ] Implementation matches exported screenshot references

### Responsive Behavior
- [ ] Desktop layout matches design
- [ ] Tablet layout reflows as designed
- [ ] Mobile layout reflows as designed
- [ ] Touch targets meet minimum 44x44px
- [ ] Content readable at all sizes (no truncation/overflow)
- [ ] Images scale correctly

### Accessibility
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 text, 3:1 large)
- [ ] Interactive elements have visible focus indicators
- [ ] Form inputs have associated labels
- [ ] Images have alt text
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] ARIA attributes used correctly where needed
- [ ] Tab order follows visual layout

### Consistency
- [ ] Same components render identically across contexts
- [ ] Spacing between sections is consistent
- [ ] Color usage follows design system (no off-system values)
- [ ] Typography scale applied consistently
- [ ] Loading and error states follow same patterns
