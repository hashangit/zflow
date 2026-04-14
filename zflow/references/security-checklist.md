# OWASP Top 10 2025 Deep Audit Checklist

Security reference for the ZFlow security-auditor agent (Phase 5 QA). Covers OWASP categories plus additional checks. The auditor thinks like an attacker: systematically searching for every exploitation path.

Each category includes: **what to scan for**, **verification methods**, and **severity guidance**.

---

## A01: Broken Access Control (Rank #1)

### What to Scan For

- **IDOR:** Can user A access user B's resources by changing an ID in URL/body/API param?
- **Missing access control:** API endpoints doing data access without authorization checks
- **Horizontal privilege escalation:** Same-role users accessing each other's data
- **Vertical privilege escalation:** Regular users accessing admin functions
- **CORS misconfiguration:** `Access-Control-Allow-Origin: *` with credentials, or overly permissive origins
- **SSRF:** App making HTTP requests to user-controlled URLs
- **Forced browsing:** Accessing unauthenticated endpoints/resources via direct URL
- **Metadata manipulation:** Tampering JWT claims, session tokens, hidden fields to escalate

### Verification Methods

1. **Trace authorization before ALL data access:**
   - Every DB query preceded by authorization check
   - Ownership validation exists (requesting user must own resource)
   - Role/permission checks enforced server-side (not just UI hiding)

2. **Confirm object ownership validation:**
   - Endpoints taking ID params must verify authenticated user owns/accesses that resource
   - Look for: DB queries selecting by ID without user constraint

3. **Check role/permission validation per endpoint:**
   - Map all API endpoints and expected authorization levels
   - Verify middleware/decorator auth applied consistently
   - Authorization not bypassed by HTTP method changes (GET vs DELETE)

4. **Verify CORS headers are restrictive:**
   - `Access-Control-Allow-Origin` not `*` when credentials sent
   - `Access-Control-Allow-Methods` lists only needed methods
   - CORS config not dynamically reflecting `Origin` header

5. **Test for SSRF:**
   - Find where user input becomes outbound request URLs
   - Check for allow-lists of permitted domains/URLs
   - Internal IP ranges blocked (10.x, 172.16-31.x, 192.168.x, 127.x)

---

## A02: Security Misconfiguration (Rank #2)

### What to Scan For

- **Default credentials** (admin/admin, test/test, default passwords)
- **Verbose errors** exposing stack traces, file paths, SQL, internal IPs
- **Missing security headers:** CSP, X-Frame-Options, HSTS, X-Content-Type-Options
- **Debug mode** enabled in production
- **Exposed config files** with secrets (.env, config.yml, hardcoded settings.py)
- **Unnecessary services** (directory listing, admin panels, API docs endpoints)
- **Cloud misconfiguration:** Public S3 buckets, open Firebase rules, unauthenticated DB access
- **Default framework settings:** Django DEBUG=True, Flask debug, Express default error handler

### Verification Methods

1. **Search default credential patterns:**
   - `admin`, `password`, `root`, `test`, `default` in config files and source
   - Hardcoded connection strings with credentials
   - Default API keys or secrets

2. **Check error handling:**
   - Production errors: no stack traces, framework versions, server types, or file paths
   - Debug flag not `true` in production configs

3. **Verify security headers:**
   - CSP: restrict script sources to same-origin or specific CDNs
   - X-Frame-Options: DENY or SAMEORIGIN
   - HSTS: enabled, max-age >= 1 year
   - X-Content-Type-Options: nosniff

4. **Confirm debug off in production:**
   - Environment-specific configs checked
   - Debug controlled by env vars
   - Deploy scripts set correct environment

5. **Check exposed endpoints:**
   - `/admin`, `/debug`, `/status`, `/metrics`, `/health` with sensitive data
   - Swagger/OpenAPI accessible in production
   - PHP info, ASP.NET trace.axd, Spring Boot actuator endpoints

---

## A03: Software Supply Chain Failures (Rank #3)

### What to Scan For

- **Dependencies with known CVEs** (`npm audit`, `pip-audit`, `cargo audit`)
- **Outdated/unmaintained dependencies** (no updates 2+ years, deprecated)
- **Untrusted package sources** (non-official registries)
- **Missing lock files** (package-lock.json, poetry.lock, Pipfile.lock, yarn.lock)
- **No integrity verification** (no checksums, no SRI)
- **Typosquatting risk** (names similar to popular packages)
- **Build script injection** (post-install scripts, pre-build hooks executing code)

### Verification Methods

1. **Run dependency audits:**

   | Ecosystem | Command |
   |-----------|---------|
   | Node.js | `npm audit --production` / `yarn audit` |
   | Python | `pip-audit -r requirements.txt` / `safety check` |
   | Go | Check vulnerability databases |
   | Ruby | `bundle audit check --update` |
   | Java | OWASP dependency-check plugin |

2. **Check package reputation:**
   - Few maintainers = higher risk
   - Last publish date recent
   - Package is official (not fork or similarly named)

3. **Verify lock files exist and are committed:**
   - `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - `poetry.lock`, `Pipfile.lock`, `Gemfile.lock`
   - All tracked in version control

4. **Check suspicious package names:**
   - Cross-reference typosquatting databases
   - Verify names match official docs
   - Flag names very similar to popular packages

5. **Review CI/CD pipeline security:**
   - No secrets in pipeline config
   - Pinned Docker image digests (not just tags)
   - Signed artifacts and commits
   - Minimal build agent permissions

---

## A04: Cryptographic Failures (Rank #4)

### What to Scan For

- **Weak hashing** for passwords: MD5, SHA1, SHA256 without salt
- **Hardcoded keys/salts** in source code
- **Missing encryption** for data at rest (PII, financial, health records)
- **Missing TLS** (HTTP endpoints, non-HTTPS API calls)
- **Predictable RNG** (standard random for tokens, nonces, IDs)
- **Poor key management** (keys in source, plaintext config, no rotation)
- **Weak TLS** (1.0/1.1, weak ciphers, no cert validation)
- **Insecure password storage** (plaintext, reversible encryption)

### Verification Methods

1. **Search MD5/SHA1 in auth contexts:**
   - `md5`/`sha1` calls in auth code = always wrong
   - Non-security checksums (file integrity): document why acceptable

2. **Search hardcoded key patterns:**
   - Long hex/base64 strings in source
   - Variables named `SECRET_KEY`, `ENCRYPTION_KEY`, `API_KEY`
   - 32+ char alphanumeric strings in non-test files

3. **Confirm password hashing:**

   | Algorithm | Minimum Parameters |
   |-----------|-------------------|
   | bcrypt | Cost factor >= 12 |
   | scrypt | N=2^17, r=8, p=1 |
   | argon2id | Recommended parameters |

4. **Verify HTTPS enforcement:**
   - HTTP-to-HTTPS redirect active
   - HSTS header set
   - No mixed content
   - No `http://` URLs in production API configs

5. **Check RNG for security contexts:**
   - Tokens: cryptographic random (`crypto.randomBytes()`, `secrets` module)
   - Session IDs: cryptographically random
   - Password reset tokens: unpredictable
   - Flag non-cryptographic random in security contexts

---

## A05: Injection (Rank #5)

### What to Scan For

- **SQL injection:** String concat/f-strings in SQL with user input
- **NoSQL injection:** User input into MongoDB operators (`$where`, `$gt`, `$ne`)
- **OS command injection:** User input to shell execution
- **XSS:**
  - Reflected: user input in HTML without encoding
  - Stored: user input rendered without encoding
  - DOM-based: `innerHTML`, `document.write` with user input
- **Template injection:** User input in engines (Jinja2, Handlebars, EJS, Thymeleaf)
- **LDAP/XPath injection:** User input in LDAP/XPath expressions
- **LLM prompt injection:** User input in AI prompts without sanitization

### Verification Methods

1. **Trace ALL user input to query/command execution:**
   - HTTP params, headers, body fields
   - URL path segments, cookie values
   - File uploads (filenames, content)
   - User-influenceable environment variables

2. **Confirm parameterized queries:**
   - SQL: parameterized queries, not string concat
   - NoSQL: typed comparisons, not string-based query construction
   - ORM generally safe but check for raw query escapes

3. **Verify context-appropriate output encoding:**

   | Context | Encoding |
   |---------|----------|
   | HTML | Entity encoding |
   | JavaScript | String escaping |
   | URL | URL encoding |
   | CSS | CSS escaping |
   | Auto-escaping frameworks (React, Angular, Jinja2) | Verify not bypassed |

4. **Check for dangerous functions:**
   - JS: `dangerouslySetInnerHTML`, `innerHTML`, `eval()`, `Function()`, `document.write()`
   - Python: `eval()`, `exec()`, subprocess with `shell=True`
   - Java: `Runtime.exec()`, `ProcessBuilder` with unsanitized input
   - PHP: `eval()`, shell execution, backtick operator

---

## A06: Insecure Design (Rank #6)

### What to Scan For

- **Business logic flaws:** Workflow steps skippable? Limits bypassable? Multi-step short-circuitable?
- **Race conditions:** Concurrent requests causing double-spending, duplicates, inconsistent state
- **TOCTOU:** Check and action not atomic
- **Missing rate limiting** on sensitive ops (login, signup, password reset, API)
- **Insufficient validation** for business rules (negative quantities, wrong dates, exceeded max)
- **Missing anti-automation** (CAPTCHA, proof-of-work, bot detection)
- **Predictable IDs** (sequential, allowing enumeration)
- **Insecure default flows** (registration without verification, reset without token expiry)

### Verification Methods

1. **Review authorization at each workflow step:**
   - Multi-step workflows: auth validated at every step
   - Step completion tracked server-side

2. **Check atomic operations on sensitive changes:**
   - Balance updates: DB transactions
   - Inventory decrements: atomic (not read-modify-write without locking)
   - `SELECT ... FOR UPDATE` or equivalent

3. **Verify rate limiting:**

   | Endpoint | Limit |
   |----------|-------|
   | Login | 5-10 attempts/min per IP/account |
   | Signup | 3-5/hour per IP |
   | Password reset | 3-5/hour per account |
   | API endpoints | Reasonable per user/key |

4. **Test workflow bypass:**
   - Can step 3 of 5 be accessed directly?
   - Can payment confirm without prior steps?
   - Can resources be accessed outside expected flow?

---

## A07: Authentication Failures (Rank #7)

### What to Scan For

- **Weak password requirements** (under 12 chars, no complexity, common passwords allowed)
- **No brute-force protection** (no lockout, no rate limiting)
- **Insecure session management** (predictable tokens, no expiration, no logout invalidation, fixation)
- **Missing MFA** for high-value/admin accounts
- **Credential recovery flaws** (user enumeration via different responses)
- **Hardcoded credentials** in source or config
- **Credential stuffing** (no bulk login detection)
- **Session fixation** (session ID not regenerated post-login)
- **Long-lived tokens** (JWT without expiration, refresh tokens without rotation)

### Verification Methods

1. **Check password policy:**
   - Min 12 chars recommended (8 absolute minimum)
   - Not in top 10,000 common passwords
   - Check for max length truncation
   - Hashing uses bcrypt/scrypt/Argon2

2. **Confirm lockout after failed attempts:**
   - Temporary lockout (15-30 min) after 5-10 failures
   - Progressive delays between attempts
   - Account holder notified
   - Lockout is server-side

3. **Verify session token properties:**
   - Cryptographically random
   - Expiration (absolute + idle timeout)
   - Invalidated on logout
   - Regenerated after login
   - HttpOnly, Secure, SameSite cookie flags

4. **Check no credentials in logs/errors:**
   - Passwords never in logs (even masked)
   - Errors don't reveal username existence
   - Generic "Invalid username or password"

5. **Verify JWT security:**
   - Algorithm: RS256/ES256 (not `none` or HS256 with weak key)
   - Access tokens: 15 min or less
   - Refresh token rotation on each use
   - Claims validated (iss, aud, exp, nbf)
   - No sensitive data in payload (not encrypted, only signed)

---

## A08: Software and Data Integrity Failures (Rank #8)

### What to Scan For

- **Insecure deserialization** (pickle, ObjectInputStream, unserialize with user input)
- **Missing integrity checks** (no signatures, HMAC, checksums)
- **CI/CD gaps** (no branch protection, no reviews, secrets in pipeline config)
- **Auto-update without verification** (code execution without signature check)
- **Unsigned artifacts** (no signatures/checksums on binaries, containers, packages)
- **Untrusted CDN** (scripts without Subresource Integrity)
- **Build reproducibility** (non-deterministic builds, floating versions)

### Verification Methods

1. **Search insecure deserialization:**
   - Python: `pickle.loads()`, `yaml.load()` without SafeLoader, `marshal.loads()`
   - Java: `ObjectInputStream.readObject()`, `XMLDecoder`
   - PHP: `unserialize()` with user input
   - Node.js: deserialized data to dangerous eval functions
   - .NET: `BinaryFormatter.Deserialize()`, `LosFormatter.Deserialize()`

2. **Verify integrity checks on external data:**
   - Webhooks: HMAC signature verification
   - Downloads: checksums/signatures
   - Third-party APIs: TLS + certificate pinning
   - DB migrations: checksums for tamper detection

3. **Check CI/CD config:**
   - Branch protection (no direct pushes to main)
   - PR reviews required
   - Secrets in vault (not pipeline YAML)
   - Minimal build agent permissions
   - Production deployment requires approval

4. **Check SRI on CDN resources:**
   - External scripts need `integrity` + `crossorigin` attributes
   - Flag external scripts without SRI

---

## A09: Security Logging and Alerting Failures (Rank #9)

### What to Scan For

- **Missing logging** of security events (login, access denied, privilege changes, data export)
- **Secrets in logs** (passwords, tokens, API keys in plaintext)
- **Insufficient context** (missing timestamp, user ID, IP, action, resource)
- **Log injection** (user input in logs without sanitization)
- **No alerting** on suspicious patterns (brute force, escalation, unusual access)
- **Log storage issues** (no integrity protection, no retention, no tamper detection)
- **Missing audit trail** for sensitive ops (data modification, admin actions, config changes)

### Verification Methods

1. **Confirm auth events logged with context:**
   - Login attempts: timestamp, user ID, IP, user agent, result
   - Password changes: timestamp, user ID, IP
   - Access denied: timestamp, user ID, resource, reason
   - Privilege changes: timestamp, actor, target, old/new role

2. **Search sensitive data in logs:**
   - Passwords: never (even partially)
   - API keys, tokens, session IDs: redacted
   - PII (SSN, credit card, health): not in logs

3. **Verify log output sanitized:**
   - User input encoded or delimited
   - Prevent log injection (newlines, control chars)
   - Structured logging (JSON) over string concatenation

4. **Check alerting config:**
   - Brute force: multiple failed logins from same IP
   - Privilege escalation: user gaining admin access
   - Data exfiltration: bulk access or export
   - Unusual patterns: off-hours access, unusual locations

---

## A10: Mishandling of Exceptional Conditions (Rank #10)

### What to Scan For

- **Failing open** (auth exception grants access)
- **Swallowed exceptions** (empty catch blocks, `pass` in except handlers)
- **Sensitive error responses** (stack traces, SQL, file paths, internal IPs)
- **Unhandled exceptions** in critical paths (payments, auth, data modification)
- **Missing boundary validation** (null, empty string, zero, max values, negatives)
- **DoS via error paths** (unbounded logging, recursive handling, resource exhaustion)
- **Inconsistent error handling** across endpoints

### Verification Methods

1. **Check all catch blocks handle errors:**
   - Empty catches = suspicious
   - Each catch: recover, retry, log with context, or propagate as generic error

2. **Verify fail-secure (deny by default):**
   - Auth exception -> deny
   - Validation exception -> reject
   - Rate limit exception -> throttle

3. **Confirm generic error messages:**
   - API responses: generic messages only
   - Details (trace, query, path) to server logs
   - Different HTTP status codes but no details in 5xx bodies

4. **Check boundary validation:**
   - Null/undefined checks before property access
   - Empty string/array validation
   - Numeric ranges (min/max, positive for quantities)
   - Date validation (past/future as appropriate)
   - Collection size limits

---

## Additional Checks (Beyond OWASP)

### Secrets and Credentials Exposure

**Scan for:**
- API keys, passwords, tokens in source (regex for long alphanumeric in non-test files)
- `.env` not in `.gitignore`
- Credentials in committed config files
- Patterns: `api_key=`, `password=`, `secret=`, `token=`, `AWS_`, `DATABASE_URL`
- Private keys (`.pem`, `.key`) in repo
- Credentials in Docker images/compose files

**Verify:**
- `.gitignore` includes `.env`, `*.pem`, `*.key`
- Credential patterns absent from tracked files
- Secrets from env vars or secret managers
- Run secret scanning tools

### CSRF Protection

**Scan for:**
- State-changing requests (POST/PUT/DELETE) without CSRF protection
- Missing CSRF tokens in forms/AJAX
- SameSite cookie attribute not set
- Cookie-only auth without additional verification

**Verify:**
- CSRF tokens on all state-changing requests
- `SameSite=Strict` or `SameSite=Lax` on session cookies
- API-only backends: Bearer tokens (not cookies)
- CORS policy restricts requesting origins

### File Upload Security

**Scan for:**
- No file type validation (or extension-only, not content-based)
- No upload size limits
- Uploaded files served from app domain (scripts can execute)
- Path traversal in filenames
- No malware scanning
- Predictable upload paths/filenames

**Verify:**
- File type by magic bytes, not just extension
- Size limits enforced in config
- Files served from different domain/CDN
- Sanitized filenames (remove path separators, use generated names)
- `Content-Disposition: attachment` on downloads

### API Security

**Scan for:**
- No rate limiting
- Missing input validation and size limits
- Wrong HTTP methods (GET for data modification)
- No API versioning
- Sensitive data in URL params (tokens, passwords, PII)
- Missing pagination on list endpoints
- Bulk ops without rate limiting

**Verify:**
- Rate limiting middleware on all routes
- Input validation (type, format, size, range) on all endpoints
- HTTP methods correct (GET=read, POST=create, PUT/PATCH=update, DELETE=delete)
- Versioning strategy (URL or header-based)
- Sensitive params in body, not URL
- Pagination with reasonable page size limits

---

## Security Audit Output Format

All findings in `security-audit-report.md`:

```
[SEV-NNN] Finding Title
- Severity: Critical | High | Medium | Low | Informational
- OWASP Category: A01-A10 or "Additional"
- Location: file:line
- Description: What was found
- Attack Scenario: How this could be exploited (required for Critical/High)
- Evidence: Code snippet showing the vulnerability
- Remediation: Specific fix with code example
- Verification: How to confirm the fix works
```

### Severity Rating

| Severity | Criteria |
|----------|----------|
| Critical | RCE, data breach, auth bypass. Exploitable without special access. |
| High | Significant impact, requires specific conditions. Privilege escalation, major data exposure. |
| Medium | Limited impact or requires auth. Info leakage, DoS, limited injection. |
| Low | Minimal impact. Config weaknesses, info hints, theoretical vulns. |
| Informational | Best practices. No direct vuln, improves security posture. |

### Clean Categories

For OWASP categories with no findings, confirm: which areas were checked and that no vulnerabilities were identified. This proves the audit was performed, not skipped.
