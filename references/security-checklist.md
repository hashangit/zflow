# OWASP Top 10 2025 Deep Audit Checklist

Comprehensive security reference for the ZFlow security-auditor agent. Covers all OWASP categories plus additional checks.

---

## Overview

This checklist is used by the `security-auditor.md` agent during Phase 5 (QA). The auditor thinks like an attacker: not rubber-stamping code but systematically searching for every way it can be exploited, abused, or made to behave unexpectedly.

The checklist follows the OWASP Top 10 2025 rankings, with additional checks for secrets exposure, CSRF, file upload, and API security.

Each category includes:
- **What to scan for:** Specific vulnerability patterns to look for
- **Verification methods:** How to confirm whether a vulnerability exists
- **Severity guidance:** How to rate findings

---

## A01: Broken Access Control (Rank #1)

### What to Scan For

- **Insecure Direct Object Reference (IDOR):** Can user A access user B's resources by changing an ID in the URL, request body, or API parameter?
- **Missing access control checks:** API endpoints that perform data access without verifying the requesting user's authorization
- **Horizontal privilege escalation:** Users with the same role accessing each other's data
- **Vertical privilege escalation:** Regular users accessing admin or elevated-privilege functions
- **CORS misconfiguration:** `Access-Control-Allow-Origin: *` combined with credentials, or overly permissive origin whitelists
- **Server-Side Request Forgery (SSRF):** Application making HTTP requests to URLs controlled by user input
- **Forced browsing:** Accessing unauthenticated API endpoints or static resources through direct URL manipulation
- **Metadata manipulation:** Tampering with JWT claims, session tokens, or hidden form fields to escalate privileges

### Verification Methods

1. **Trace authorization checks before ALL data access operations:**
   - Every database query must be preceded by an authorization check
   - Check that ownership validation exists (requesting user must own the resource)
   - Verify that role/permission checks are enforced server-side (not just UI hiding)

2. **Confirm object ownership validation:**
   - For every endpoint that takes an ID parameter, verify the code checks that the authenticated user owns or has access to that resource
   - Pattern to look for: database queries that select by ID without a user constraint

3. **Check role/permission validation per endpoint:**
   - Map all API endpoints and their expected authorization levels
   - Verify middleware or decorator-based auth is applied consistently
   - Check that authorization is not bypassed by HTTP method changes (e.g., GET vs DELETE)

4. **Verify CORS headers are restrictive:**
   - `Access-Control-Allow-Origin` should not be `*` when credentials are sent
   - `Access-Control-Allow-Methods` should list only needed methods
   - Check that CORS configuration is not dynamically reflecting the `Origin` header

5. **Test for SSRF:**
   - Find all places where user input becomes a URL for outbound requests
   - Check for allow-lists of permitted domains/URLs
   - Verify that internal IP ranges (10.x, 172.16-31.x, 192.168.x, 127.x) are blocked

---

## A02: Security Misconfiguration (Rank #2)

### What to Scan For

- **Default credentials** still enabled (admin/admin, test/test, default passwords)
- **Verbose error messages** exposing stack traces, file paths, SQL queries, internal IPs
- **Missing security headers:** Content-Security-Policy (CSP), X-Frame-Options, Strict-Transport-Security (HSTS), X-Content-Type-Options
- **Debug mode** enabled in production configuration
- **Exposed configuration files** containing secrets (.env, config.yml, settings.py with hardcoded values)
- **Unnecessary services/features** enabled (directory listing, admin panels, API documentation endpoints)
- **Cloud storage misconfiguration:** Public S3 buckets, open Firebase rules, unauthenticated database access
- **Default framework settings:** Django DEBUG=True, Flask debug mode, Express default error handler

### Verification Methods

1. **Search for default credential patterns:**
   - Search for `admin`, `password`, `root`, `test`, `default` in configuration files and source
   - Look for hardcoded connection strings with credentials
   - Look for default API keys or secrets

2. **Check error handling returns generic messages:**
   - Production error responses should not include stack traces
   - Error pages should not reveal framework version, server type, or file paths
   - Look for debug flag set to true in production configs

3. **Verify security headers are set:**
   - CSP should restrict script sources to same-origin or specific CDNs
   - X-Frame-Options should be DENY or SAMEORIGIN
   - HSTS should be enabled with a max-age of at least 1 year
   - X-Content-Type-Options should be nosniff
   - Check middleware configuration for these headers

4. **Confirm debug is off in production configs:**
   - Check environment-specific configuration files
   - Verify that debug mode is controlled by environment variables
   - Ensure production deployment scripts set the correct environment

5. **Check for exposed configuration endpoints:**
   - `/admin`, `/debug`, `/status`, `/metrics`, `/health` with sensitive data
   - Swagger/OpenAPI documentation endpoints accessible in production
   - PHP info pages, ASP.NET trace.axd, Spring Boot actuator endpoints

---

## A03: Software Supply Chain Failures (Rank #3)

### What to Scan For

- **Dependencies with known CVEs** (check via `npm audit`, `pip-audit`, `cargo audit`, etc.)
- **Outdated or unmaintained dependencies** (no updates in 2+ years, deprecated packages)
- **Untrusted package sources** (packages from non-official registries)
- **Missing lock files** (no package-lock.json, poetry.lock, Pipfile.lock, yarn.lock)
- **No integrity verification** on dependencies (no checksums, no SRI)
- **Typosquatting risk** (package names similar to popular packages but with subtle misspellings)
- **Build script injection** (post-install scripts, pre-build hooks that execute arbitrary code)

### Verification Methods

1. **Execute dependency audit commands:**
   - Node.js: `npm audit --production` or `yarn audit`
   - Python: `pip-audit -r requirements.txt` or `safety check`
   - Go: check against vulnerability databases
   - Ruby: `bundle audit check --update`
   - Java: OWASP dependency-check plugin

2. **Check package publish dates and maintainer reputation:**
   - Look for packages with very few maintainers
   - Check if the last publish date is recent
   - Verify the package is the official one (not a fork or similarly named package)

3. **Verify lock files exist and are committed:**
   - `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - `poetry.lock`, `Pipfile.lock`
   - `Gemfile.lock`
   - These should be tracked in version control

4. **Check for unusual or suspicious package names:**
   - Cross-reference with known typosquatting databases
   - Verify package names match official documentation
   - Check for packages with very similar names to popular ones

5. **Review CI/CD pipeline security:**
   - No secrets in pipeline configuration files
   - Pinned Docker image digests (not just tags)
   - Signed artifacts and commits
   - Minimal permissions for build agents

---

## A04: Cryptographic Failures (Rank #4)

### What to Scan For

- **Weak hashing algorithms** for passwords: MD5, SHA1, SHA256 without salt
- **Hardcoded encryption keys or salts** in source code
- **Missing encryption** for sensitive data at rest (PII, financial data, health records)
- **Missing TLS enforcement** (HTTP endpoints, non-HTTPS API calls)
- **Predictable random number generation** (language-standard random functions for security-critical values like tokens, nonces, IDs)
- **Poor key management** (keys in source, keys in plaintext config, no key rotation)
- **Weak TLS configuration** (TLS 1.0/1.1, weak cipher suites, no certificate validation)
- **Insecure password storage** (plaintext, reversible encryption instead of hashing)

### Verification Methods

1. **Search for MD5/SHA1 usage in authentication contexts:**
   - Look for md5 and sha1 function calls in auth-related code
   - In password handling, these are always wrong
   - For non-security checksums (file integrity), document why they are acceptable

2. **Search for hardcoded key patterns:**
   - Long hex or base64 strings in source code
   - Variable names like `SECRET_KEY`, `ENCRYPTION_KEY`, `API_KEY`
   - Patterns matching 32+ character alphanumeric strings in non-test files

3. **Confirm passwords use bcrypt/scrypt/Argon2 with adequate cost:**
   - bcrypt with cost factor 12 or higher
   - scrypt with N=2^17, r=8, p=1 or stronger
   - argon2id with recommended parameters

4. **Verify HTTPS enforcement:**
   - HTTP-to-HTTPS redirect middleware is active
   - HSTS header is set
   - No mixed content (HTTP resources on HTTPS pages)
   - No http:// URLs in API configurations for production

5. **Check random number generation for security contexts:**
   - Token generation must use cryptographic random functions (e.g., `crypto.randomBytes()` in Node.js, `secrets` module in Python)
   - Session IDs must be cryptographically random
   - Password reset tokens must be unpredictable
   - Flag any use of non-cryptographic random in security contexts

---

## A05: Injection (Rank #5)

### What to Scan For

- **SQL injection:** String concatenation or f-strings in SQL queries with user input
- **NoSQL injection:** User input flowing directly into MongoDB query operators (`$where`, `$gt`, `$ne`)
- **OS command injection:** User input passed to shell execution functions
- **XSS (Cross-Site Scripting):**
  - Reflected: User input reflected in HTML without encoding
  - Stored: User input stored and later rendered without encoding
  - DOM-based: Client-side JavaScript rendering user input via innerHTML, document.write
- **Template injection:** User input in template engines (Jinja2, Handlebars, EJS, Thymeleaf)
- **LDAP/XPath injection:** User input in LDAP queries or XPath expressions
- **LLM prompt injection:** User input flowing into AI model prompts without sanitization

### Verification Methods

1. **Trace ALL user input from entry point to query/command execution:**
   - HTTP parameters, headers, body fields
   - URL path segments
   - Cookie values
   - File uploads (filenames, content)
   - Environment variables that can be influenced by users

2. **Confirm parameterized queries/prepared statements:**
   - SQL: use parameterized queries (e.g., `db.query('SELECT * FROM users WHERE id = ?', [id])`) not string concatenation
   - NoSQL: Use typed comparisons, not string-based query construction
   - ORM usage is generally safe but check for raw query escapes

3. **Verify output encoding is context-appropriate:**
   - HTML context: HTML entity encoding
   - JavaScript context: JavaScript string escaping
   - URL context: URL encoding
   - CSS context: CSS escaping
   - Frameworks with auto-escaping (React, Angular, Jinja2 autoescape) help but verify they are not bypassed

4. **Check for dangerous functions:**
   - JavaScript: `dangerouslySetInnerHTML`, `innerHTML`, `eval()`, `Function()`, `document.write()`
   - Python: `eval()`, `exec()`, subprocess calls with shell=True
   - Java: `Runtime.exec()`, `ProcessBuilder` with unsanitized input
   - PHP: `eval()`, shell execution functions, backtick operator

---

## A06: Insecure Design (Rank #6)

### What to Scan For

- **Business logic flaws:** Can workflow steps be skipped? Can limits be bypassed? Can multi-step processes be short-circuited?
- **Race conditions:** Concurrent requests causing double-spending, duplicate creation, or inconsistent state
- **TOCTOU (Time-of-Check/Time-of-Use):** Check and action not atomic, allowing state changes between them
- **Missing rate limiting** on sensitive operations (login, signup, password reset, API calls)
- **Insufficient input validation** for business rules (negative quantities, future dates in past-only fields, exceeding maximum values)
- **Missing anti-automation controls** (CAPTCHA, proof-of-work, bot detection on critical flows)
- **Predictable resource identifiers** (sequential IDs allowing enumeration)
- **Insecure default flows** (registration without email verification, password reset without token expiry)

### Verification Methods

1. **Review business logic flows for authorization at each step:**
   - Multi-step workflows should validate authorization at every step, not just the first
   - Step completion should be tracked server-side, not trust client-side state

2. **Check for atomic operations on financial/sensitive changes:**
   - Balance updates should use database transactions
   - Inventory decrements should be atomic (not read-modify-write without locking)
   - Use `SELECT ... FOR UPDATE` or equivalent where needed

3. **Verify rate limiting exists:**
   - Login endpoint: max 5-10 attempts per minute per IP/account
   - Signup: max 3-5 per hour per IP
   - Password reset: max 3-5 per hour per account
   - API endpoints: reasonable limits per user/API key
   - Check for rate limiting middleware or configuration

4. **Test workflow bypass:**
   - Can step 3 of a 5-step process be accessed directly via API?
   - Can payment be confirmed without completing prior steps?
   - Can a resource be accessed without going through the expected flow?

---

## A07: Authentication Failures (Rank #7)

### What to Scan For

- **Weak password requirements** (minimum length under 12, no complexity requirements, allows common passwords)
- **Missing brute-force protection** (no lockout, no rate limiting on login attempts)
- **Insecure session management** (predictable tokens, no expiration, no invalidation on logout, session fixation)
- **Missing MFA** for high-value or admin accounts
- **Credential recovery flaws** (user enumeration via "forgot password" -- different responses for existing vs non-existing users)
- **Hardcoded credentials** in source code or configuration
- **Credential stuffing vulnerability** (no detection of bulk login attempts from known-breached credentials)
- **Session fixation** (session ID not regenerated after login)
- **Long-lived tokens** (JWT without expiration, refresh tokens without rotation)

### Verification Methods

1. **Check password policy:**
   - Minimum 12 characters recommended (8 absolute minimum)
   - Should not be in common password lists (check against top 10,000 passwords)
   - Check for maximum length (some systems truncate, weakening security)
   - Verify password hashing uses bcrypt/scrypt/Argon2

2. **Confirm lockout after N failed attempts:**
   - Temporary lockout (15-30 minutes) after 5-10 failed attempts
   - Progressive delays between attempts
   - Account lockout notification to the account holder
   - Check that lockout is server-side (not just UI)

3. **Verify session token properties:**
   - Cryptographically random (not predictable)
   - Has expiration (absolute and idle timeout)
   - Invalidated on logout
   - Regenerated after login (prevents session fixation)
   - HttpOnly, Secure, SameSite cookie flags

4. **Check no credentials in logs or error responses:**
   - Passwords should never appear in logs (even masked)
   - Error messages should not reveal whether a username exists
   - Use generic "Invalid username or password" rather than specific failure reasons

5. **Verify JWT security if used:**
   - Strong signing algorithm (RS256, ES256 -- not none or HS256 with weak key)
   - Short expiration (access tokens: 15 minutes or less)
   - Refresh token rotation (new refresh token on each use)
   - Claims validated (iss, aud, exp, nbf)
   - No sensitive data in JWT payload (it is not encrypted, just signed)

---

## A08: Software and Data Integrity Failures (Rank #8)

### What to Scan For

- **Insecure deserialization** of untrusted data (pickle, ObjectInputStream, unserialize with user input)
- **Missing integrity checks** on critical data (no signatures, no HMAC, no checksums)
- **CI/CD pipeline security gaps** (no branch protection, no review requirements, secrets in pipeline config)
- **Auto-update without verification** (downloading and executing code without signature verification)
- **Unsigned artifacts** (binaries, containers, packages without signatures or checksums)
- **Untrusted CDN resources** (scripts loaded from CDNs without Subresource Integrity)
- **Build reproducibility issues** (non-deterministic builds, floating dependency versions)

### Verification Methods

1. **Search for insecure deserialization patterns:**
   - Python: `pickle.loads()`, `yaml.load()` without safe loader, `marshal.loads()`
   - Java: `ObjectInputStream.readObject()`, `XMLDecoder`
   - PHP: `unserialize()` with user-controlled input
   - Node.js: deserialized data passed to dangerous evaluation functions
   - .NET: `BinaryFormatter.Deserialize()`, `LosFormatter.Deserialize()`

2. **Verify integrity checks on external data:**
   - Webhook payloads: HMAC signature verification
   - File downloads: checksums or signatures
   - API responses from third parties: TLS plus certificate pinning where appropriate
   - Database migrations: checksums to detect tampering

3. **Check CI/CD configuration:**
   - Branch protection rules (no direct pushes to main)
   - Pull request reviews required
   - Secrets stored in vault (not in pipeline YAML)
   - Build agent permissions are minimal
   - Deployment requires approval for production

4. **Check for Subresource Integrity (SRI) on CDN resources:**
   - External scripts should have `integrity` and `crossorigin` attributes
   - Flag any external scripts without SRI

---

## A09: Security Logging and Alerting Failures (Rank #9)

### What to Scan For

- **Missing logging** of security-relevant events (login, access denied, privilege changes, data export)
- **Secrets in log output** (passwords, tokens, API keys logged in plaintext)
- **Insufficient log context** for incident response (missing timestamp, user ID, IP, action, resource)
- **Log injection vulnerabilities** (user input in log messages without sanitization, allowing log forgery)
- **No alerting** on suspicious patterns (brute force, privilege escalation, unusual data access)
- **Log storage issues** (logs stored without integrity protection, no retention policy, no tamper detection)
- **Missing audit trail** for sensitive operations (data modification, admin actions, configuration changes)

### Verification Methods

1. **Confirm auth events are logged with adequate context:**
   - Every login attempt (success and failure): timestamp, user ID, IP, user agent, result
   - Password changes: timestamp, user ID, IP
   - Access denied events: timestamp, user ID, requested resource, reason
   - Privilege changes: timestamp, actor, target user, old role, new role

2. **Search for sensitive data in log statements:**
   - Passwords should never be logged (even partially)
   - API keys, tokens, session IDs should be redacted
   - PII (SSN, credit card, health data) should not appear in logs

3. **Verify log output is sanitized:**
   - User input in log messages should be encoded or delimited
   - Prevent log injection (newline characters, control characters in user input)
   - Use structured logging (JSON) rather than string concatenation for log messages

4. **Check for alerting configuration:**
   - Brute force detection: multiple failed logins from same IP
   - Privilege escalation: user gaining admin access
   - Data exfiltration: bulk data access or export
   - Unusual patterns: access at unusual times, from unusual locations

---

## A10: Mishandling of Exceptional Conditions (Rank #10)

### What to Scan For

- **"Failing open"** -- defaulting to allow on error (auth check throws exception, access is granted)
- **Silently swallowed exceptions** (empty catch blocks, pass statements in except handlers)
- **Sensitive information in error responses** (stack traces, SQL queries, file paths, internal IPs in API error responses)
- **Unhandled exceptions in critical paths** (payment processing, authentication, data modification without error handling)
- **Missing boundary validation** (null, empty string, zero, maximum values, negative numbers)
- **Denial of service via error paths** (unbounded error logging, recursive error handling, resource exhaustion on error)
- **Inconsistent error handling** (some endpoints handle errors, others do not)

### Verification Methods

1. **Check all catch blocks actually handle the error:**
   - Empty catch blocks are always suspicious
   - Each catch should either: recover, retry, log with context, or propagate as a generic error
   - Look for empty handlers and pass statements in exception blocks

2. **Verify errors fail securely (deny by default):**
   - If auth check throws, the user should be denied, not granted access
   - If validation throws, the operation should be rejected, not accepted
   - If rate limiting check throws, the request should be throttled, not allowed

3. **Confirm error messages are generic to users:**
   - API error responses should use generic messages
   - Detailed error info (stack trace, query, file path) should go to server logs only
   - Different HTTP status codes for different error types but no details in the body for 5xx

4. **Check boundary validation:**
   - Null/undefined checks before accessing properties
   - Empty string/array validation
   - Numeric range validation (min/max, positive numbers for quantities)
   - Date validation (not in future when should be past, not expired)
   - Collection size limits

---

## Additional Checks (Beyond OWASP)

### Secrets and Credentials Exposure

**What to scan for:**
- API keys, passwords, tokens in source code (regex patterns for long alphanumeric strings in non-test files)
- `.env` files not in `.gitignore`
- Credentials in configuration files committed to repo
- Common patterns: `api_key=`, `password=`, `secret=`, `token=`, `AWS_`, `DATABASE_URL` with embedded credentials
- Private keys (`.pem`, `.key` files) in the repository
- Credentials in Docker images or docker-compose files

**Verification methods:**
- Check `.gitignore` includes `.env`, `*.pem`, `*.key`
- Search for credential patterns in tracked files
- Verify secrets are loaded from environment variables or secret managers
- Run secret scanning tools if available

### CSRF (Cross-Site Request Forgery) Protection

**What to scan for:**
- State-changing requests (POST/PUT/DELETE) without CSRF protection
- Missing CSRF tokens in forms and AJAX requests
- SameSite cookie attribute not set
- API endpoints that accept actions based solely on cookies without additional verification

**Verification methods:**
- Verify CSRF tokens on all state-changing requests
- Check `SameSite=Strict` or `SameSite=Lax` on session cookies
- For API-only backends: verify token-based auth (Bearer tokens) instead of cookie-based
- Verify CORS policy restricts which origins can make requests

### File Upload Security

**What to scan for:**
- No file type validation (or only extension-based, not content-based)
- No upload size limits
- Uploaded files served from the application domain (allowing uploaded scripts to execute)
- Path traversal in filenames (directory traversal sequences)
- No virus/malware scanning on uploaded files
- Predictable upload paths or filenames

**Verification methods:**
- Check file type validation uses magic bytes (file signature), not just extension
- Verify upload size limits are enforced (max file size in config)
- Confirm uploaded files are served from a different domain or CDN (not the app domain)
- Sanitize filenames: remove path separators, use generated filenames
- Check for `Content-Disposition: attachment` header on file downloads

### API Security

**What to scan for:**
- No rate limiting on API endpoints
- Missing input validation and size limits
- Improper HTTP method enforcement (GET for data modification)
- No API versioning for breaking changes
- Sensitive data in URL parameters (tokens, passwords, PII in query strings)
- Missing pagination on list endpoints (enabling data harvesting)
- Bulk operations without rate limiting or confirmation

**Verification methods:**
- Verify rate limiting middleware is applied to all API routes
- Check input validation on all endpoints (type, format, size, range)
- Confirm HTTP methods are correct (GET = read only, POST = create, PUT/PATCH = update, DELETE = delete)
- Check API versioning strategy (URL-based or header-based)
- Verify sensitive parameters are in the request body, not the URL
- Check that list endpoints have pagination with reasonable page size limits

---

## Security Audit Output Format

All findings follow this format in `security-audit-report.md`:

```
[SEV-NNN] Finding Title
- Severity: Critical | High | Medium | Low | Informational
- OWASP Category: A01-A10 or "Additional"
- Location: file:line
- Description: What was found
- Attack Scenario: How this could be exploited (required for all Critical/High)
- Evidence: Code snippet showing the vulnerability
- Remediation: Specific fix with code example
- Verification: How to confirm the fix works
```

### Severity Rating Guidelines

| Severity | Criteria |
|----------|----------|
| Critical | Remote code execution, data breach, auth bypass. Exploitable without special access. |
| High | Significant security impact but requires specific conditions. Privilege escalation, significant data exposure. |
| Medium | Limited impact or requires authenticated access. Information leakage, DoS, limited injection. |
| Low | Minimal impact. Configuration weaknesses, information hints, theoretical vulnerabilities. |
| Informational | Best practice recommendations. No direct vulnerability but improves security posture. |

### Clean Categories

For each OWASP category reviewed with no findings, the report confirms:
- Which areas were checked
- That no vulnerabilities were identified in this category

This confirms the audit was performed, not skipped.
