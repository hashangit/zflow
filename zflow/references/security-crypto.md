# Security Reference: Crypto, Integrity & Infrastructure

Covers OWASP A04 (Cryptographic Failures), A08 (Integrity Failures), plus additional checks for secrets, CSRF, file upload, API security, and the security audit output format. Load this when auditing crypto, secrets, data integrity, or infrastructure security.

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
   - Node.js: deserialized data to dangerous functions
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
