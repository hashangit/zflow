# Security Reference: Configuration, Supply Chain & Logging

Covers OWASP A02 (Security Misconfiguration), A03 (Supply Chain), A06 (Insecure Design), A09 (Logging Failures). Load this when auditing configuration, dependencies, business logic, or observability.

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

