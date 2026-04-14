# Common Vulnerability Patterns by Language/Ecosystem

Reference for recognizing and remediating vulnerability patterns during code review and security audit.

---

## Overview

Common vulnerability patterns organized by language/ecosystem. Used by `security-auditor.md` during Phase 5 (QA). Each pattern includes: what to search for, why it is dangerous, how to recognize it, and how to fix it.

**Note:** Code examples illustrate vulnerable patterns for educational purposes only.

---

## JavaScript / TypeScript Patterns

### XSS via dangerouslySetInnerHTML

**Search for:** `dangerouslySetInnerHTML`

**Vulnerable:**
```jsx
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

**Danger:** Bypasses React's XSS protection. If `userInput` contains script tags or event handlers, they execute in the browser.

**How to recognize:**
- `dangerouslySetInnerHTML` in any JSX/TSX
- Content from user input or untrusted source
- No sanitization (DOMPurify or similar) before rendering

**Remediation:**
- Plain text: use React's default rendering: `<div>{userInput}</div>`
- Rich HTML needed: sanitize with DOMPurify:
  ```jsx
  import DOMPurify from 'dompurify';
  <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
  ```
- Markdown: use a sanitizing markdown library

---

### Prototype Pollution

**Search for:** recursive merge functions, `Object.assign` with user data

**Vulnerable:**
```javascript
function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === 'object') {
      target[key] = target[key] || {};
      merge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
}
merge(config, userInput);
```

**Danger:** Keys like `__proto__`, `constructor`, or `prototype` modify `Object.prototype`, affecting all objects. Can lead to auth bypass, privilege escalation, or RCE.

**How to recognize:**
- Recursive merge/deep clone iterating object keys
- `Object.assign()` with user-controlled source
- JSON parsed result used as config object
- User-controlled properties copied onto existing objects

**Remediation:**
- Use safe merge utilities (lodash `_.merge` with prototype pollution fixes)
- Validate keys exclude `__proto__`, `constructor`, `prototype`
- Use `Object.create(null)` for objects receiving user properties
- Use `Map` for user-controlled key-value data

---

### Regex DoS (ReDoS)

**Search for:** complex regex with nested quantifiers

**Vulnerable:**
```javascript
const emailRegex = /^([a-zA-Z0-9]+)*@([a-zA-Z0-9]+)*\.([a-zA-Z0-9]+)*$/;
emailRegex.test(userInput);
```

**Danger:** Nested quantifiers (`(a+)+`, `(a*)*`) cause catastrophic backtracking. Crafted input causes exponential time, freezing the Node.js event loop.

**How to recognize:**
- Nested quantifiers: `(x+)+`, `(x*)*`, `(x+)*`
- Alternating groups with quantifiers: `(a|b)+` where both match same input
- User input tested against complex regex

**Remediation:**
- Simplify regex to avoid nested quantifiers
- Use atomic groups or possessive quantifiers where supported
- Set timeout on matching (e.g., `re2` library with bounded execution)
- Email validation: use simple pattern or dedicated library

---

### Path Traversal

**Search for:** `fs.readFile`, `fs.writeFileSync`, `path.join` with user input

**Vulnerable:**
```javascript
const filePath = path.join(__dirname, 'uploads', req.params.filename);
fs.readFile(filePath, (err, data) => { ... });
```

**Danger:** `req.params.filename` containing `../../etc/passwd` escapes the intended directory and reads arbitrary files.

**How to recognize:**
- File system ops using user input in path
- `path.join()` or string concat with user-controlled segments
- Static file serving with user-derived paths
- Upload handlers using original filename

**Remediation:**
- Validate resolved path within intended directory:
  ```javascript
  const resolved = path.resolve(__dirname, 'uploads', req.params.filename);
  if (!resolved.startsWith(path.resolve(__dirname, 'uploads'))) {
    throw new Error('Path traversal detected');
  }
  ```
- Use generated filenames, not user-provided
- Whitelist allowed file extensions
- Sanitize filenames: remove path separators, null bytes, `..`

---

### Dynamic Code Execution

**Search for:** `eval(`, `new Function(`, `setTimeout(string`, `setInterval(string`

**Vulnerable:** Passing user-controlled strings to code execution functions.

**Danger:** eval, Function constructor, and setTimeout/setInterval with string arguments execute arbitrary JS. User-controlled input equals remote code execution.

**How to recognize:**
- Any code eval function with user-controlled input
- setTimeout/setInterval with string arguments (not function refs)
- `vm.runInContext()`, `vm.runInNewContext()`, `vm.compileFunction()`
- Dynamic `import()` with user-controlled paths

**Remediation:**
- Never pass user input to code execution functions
- Use `setTimeout(() => { ... }, 0)` (function reference)
- Use `JSON.parse` for data, not code evaluation
- Dynamic calculations: use a safe expression evaluator library

---

## Python Patterns

### SQL Injection via f-strings

**Search for:** f-strings in SQL, `.format()` in SQL, `%` formatting in SQL

**Vulnerable:**
```python
query = f"SELECT * FROM users WHERE email = '{email}' AND status = '{status}'"
cursor.execute(query)
```

**Danger:** User input interpolated directly into SQL. Attacker injects via `' OR '1'='1' --` to bypass authentication.

**How to recognize:**
- f-strings, `.format()`, or `%` formatting in SQL queries
- SQL built by concatenating user input
- Raw SQL in Django `raw()`, SQLAlchemy `text()`, or cursor `execute()` with formatting

**Remediation:**
- Parameterized queries:
  ```python
  cursor.execute("SELECT * FROM users WHERE email = %s AND status = %s", (email, status))
  ```
- ORM methods:
  ```python
  User.objects.filter(email=email, status=status)
  ```
- Raw SQL: always use parameterized placeholders

---

### Pickle Deserialization

**Search for:** `pickle.loads`, `pickle.load`, `yaml.load` without SafeLoader

**Vulnerable:**
```python
import pickle
data = pickle.loads(request.data)
```

**Danger:** `pickle.loads()` executes arbitrary Python code during deserialization. Crafted payload can run system commands, read files, or open reverse shells.

**How to recognize:**
- `pickle.loads()`/`pickle.load()` with untrusted data
- `cPickle.loads()` (Python 2)
- `shelve.open()` (uses pickle internally)
- `marshal.loads()` (less dangerous but risky)
- `yaml.load()` without `Loader=yaml.SafeLoader`

**Remediation:**
- Use JSON for data interchange:
  ```python
  data = json.loads(request.data)
  ```
- YAML: use `yaml.safe_load()` instead of `yaml.load()`
- Pickle: only unpickle from trusted sources, never user input
- Alternatives: `msgpack`, `protobuf`, or JSON

---

### Template Injection (SSTI)

**Search for:** `Template(user_input)`, `render_template_string`

**Vulnerable:**
```python
from jinja2 import Template
template = Template(user_input)
result = template.render()
```

**Danger:** User input as template can contain directives that execute code. Jinja2 `{{ config }}` leaks Flask config; MRO chain access leads to RCE.

**How to recognize:**
- User input as template string (not as variable)
- `Template(user_input).render()`
- `render_template_string(user_input)` in Flask
- Mako templates with user-controlled content
- Django templates with `mark_safe` on user input

**Remediation:**
- Pass user input as template variables:
  ```python
  template = Template("Hello {{ name }}!")
  result = template.render(name=user_input)  # Safe: user_input is a variable
  ```
- Sandboxed environments if user-defined templates required
- Enable Jinja2 autoescaping: `Environment(autoescape=True)`
- Never use `render_template_string` with user input

---

### Command Injection

**Search for:** `os.system`, `subprocess` with `shell=True`, `os.popen`

**Vulnerable:**
```python
import os
os.system(f"ping {user_ip}")
subprocess.call(f"convert {user_filename} output.png", shell=True)
```

**Danger:** `shell=True` or `os.system()` passes command to system shell. Shell metacharacters (`;`, `$()`) in user input get executed.

**How to recognize:**
- `os.system()`, `os.popen()` with user input
- `subprocess.call/run/Popen()` with `shell=True`
- String formatting/concat in command strings

**Remediation:**
- Use `subprocess.run()` without `shell=True`, args as list:
  ```python
  subprocess.run(["ping", "-c", "3", user_ip], capture_output=True)
  ```
- Shell features truly needed: sanitize with `shlex.quote()`
- Validate input against strict allowlist (e.g., IP regex)

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
