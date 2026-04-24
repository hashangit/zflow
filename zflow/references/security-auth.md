# Security Reference: Access Control & Authentication

Covers OWASP A01 (Broken Access Control) and A07 (Authentication Failures). Load this when auditing authorization, session management, password handling, and token security.

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
