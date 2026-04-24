# Vulnerability Patterns: General Web

Cross-language vulnerability patterns for web applications. Load this when auditing web endpoints, sessions, auth flows, or redirects regardless of backend language.

Each pattern includes: what to search for, why it is dangerous, how to recognize it, and how to fix it.

**Note:** Code examples illustrate vulnerable patterns for educational purposes only.

---

## General Web Patterns

### CORS Misconfiguration

**Search for:** `Access-Control-Allow-Origin` with wildcard or dynamic origin

**Vulnerable:**
```javascript
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Credentials', 'true');
  next();
});
```

**Danger:** Wildcard origin with credentials lets any website make authenticated requests, stealing user data or performing actions on their behalf.

**How to recognize:**
- CORS middleware reflecting `Origin` without validation
- Wildcard combined with credentials
- Overly broad allowed origin list
- CORS headers set in multiple places (middleware + routes)

**Remediation:**
- Explicit allowlist of trusted origins:
  ```javascript
  const allowedOrigins = ['https://app.example.com', 'https://admin.example.com'];
  app.use((req, res, next) => {
    const origin = req.headers.origin;
    if (allowedOrigins.includes(origin)) {
      res.header('Access-Control-Allow-Origin', origin);
      res.header('Access-Control-Allow-Credentials', 'true');
    }
    next();
  });
  ```
- Never use wildcard with credentials

---

### JWT Issues

**Search for:** `jwt.verify` with `none` algorithm, weak secrets, `jwt.decode` used for auth

**Vulnerable:**
- Accepting `none` algorithm in jwt.verify
- Weak/short JWT secrets (dictionary words, short strings)
- Using `jwt.decode` instead of `jwt.verify` for authentication

**Danger:**
- `none` algorithm bypass: forge tokens without knowing secret
- Weak secrets: brute-forceable
- Decode instead of verify: accepts any token without validation

**How to recognize:**
- JWT libraries accepting `none` algorithm
- Short or common JWT secrets
- Decode used for auth instead of verify
- Missing expiration/issuer/audience claim validation
- Sensitive data in JWT payload (passwords, PII)

**Remediation:**
- Specify allowed algorithms explicitly:
  ```javascript
  const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
  ```
- Strong random secrets (32+ bytes for HS256)
- Prefer asymmetric algorithms (RS256, ES256) for distributed systems
- Always use verify, never decode for auth
- Validate all claims: expiration, issuer, audience
- JWT payloads are readable by anyone with the token -- keep them minimal

---

### Session Fixation

**Search for:** session not regenerated after login, session ID in URLs

**Vulnerable:**
```javascript
app.post('/login', (req, res) => {
  if (authenticate(req.body.username, req.body.password)) {
    req.session.userId = user.id;  // Sets user on existing session
    res.redirect('/dashboard');
  }
});
```

**Danger:** Attacker obtains session ID, tricks victim into using it. When victim logs in, attacker's session is now authenticated.

**How to recognize:**
- Login sets auth state without regenerating session ID
- Session IDs in URL query parameters
- Accepting session IDs from both cookies and URL params
- Old sessions not invalidated on logout

**Remediation:**
- Regenerate session ID after authentication:
  ```javascript
  req.session.regenerate(() => {
    req.session.userId = user.id;
    res.redirect('/dashboard');
  });
  ```
- Never put session IDs in URLs
- Only accept session IDs from cookies
- Invalidate sessions on logout and password change

---

### Open Redirect

**Search for:** `res.redirect(req.query`, params named `redirect`, `url`, `next`

**Vulnerable:**
```javascript
app.get('/redirect', (req, res) => {
  res.redirect(req.query.url);
});
```

**Danger:** URL like `https://yoursite.com/redirect?url=https://evil.com` appears from your domain but redirects to malicious site. Used for phishing.

**How to recognize:**
- Redirect endpoints using user input directly
- URL params named `redirect`, `url`, `next`, `return_to`, `continue`
- OAuth/callback URLs redirecting to user-specified locations

**Remediation:**
- Validate against allowlist:
  ```javascript
  const allowedHosts = ['yoursite.com', 'app.yoursite.com'];
  const url = new URL(req.query.url, 'https://yoursite.com');
  if (!allowedHosts.includes(url.hostname)) {
    return res.status(400).send('Invalid redirect');
  }
  res.redirect(req.query.url);
  ```
- Prefer relative paths over absolute URLs
- Flexible redirects: ensure starts with `/`, not `//`

---

### Server-Side Request Forgery (SSRF)

**Search for:** HTTP client calls with user-controlled URLs, `requests.get(user_url)`

**Vulnerable:**
```python
import requests
url = request.args.get('url')
response = requests.get(url)
return response.content
```

**Danger:** Server requests user-specified URL. Can access internal services (metadata endpoints, internal APIs, databases) not exposed to the internet.

**How to recognize:**
- HTTP client calls with user-controlled URLs
- URL fetch/proxy endpoints
- Webhook testing with user-specified URLs
- Image/document import from URLs
- PDF generation from URLs

**Remediation:**
- Allowlist permitted domains/URLs
- Block internal IP ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16
- Block cloud metadata: 169.254.169.254 (AWS/GCP/Azure)
- Separate network segment for outbound requests
- Validate URL scheme (https:// only)

---

## How to Use This Reference During Code Review

### Step-by-Step Approach

1. Identify language and framework
2. Scan for patterns above using targeted searches
3. Trace user input from entry points to dangerous sinks
4. For each match, determine if input is truly user-controlled and untrusted
5. Assess exploitation impact
6. Document findings with pattern name, location, and remediation

### Common Entry Points

- HTTP request params, query strings, headers
- Request body (JSON, form data, multipart uploads)
- URL path segments
- Cookie values
- File uploads (filename and content)
- WebSocket messages
- Externally influenceable environment variables

### Common Dangerous Sinks

- Database queries (SQL, NoSQL, ORM raw)
- Shell command execution
- HTML output (rendering, DOM manipulation)
- File system operations (read, write, delete)
- Network requests (HTTP clients, sockets)
- Deserialization functions
- Template rendering engines
- Authentication and authorization logic
