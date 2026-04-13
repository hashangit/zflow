# Common Vulnerability Patterns by Language/Ecosystem

Reference for recognizing and remediating vulnerability patterns during code review and security audit.

---

## Overview

This document catalogs common vulnerability patterns organized by language and ecosystem. The `security-auditor.md` agent uses this reference during Phase 5 (QA) to recognize known patterns in the code being audited. Each pattern includes what to look for, why it is dangerous, and how to fix it.

**Note:** Code examples in this document illustrate vulnerable patterns for educational purposes. They are not meant to be used in production.

---

## JavaScript / TypeScript Patterns

### XSS via dangerouslySetInnerHTML

**Pattern to search for:** `dangerouslySetInnerHTML`

**Vulnerable code:**
```jsx
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

**Why it is dangerous:** React's `dangerouslySetInnerHTML` bypasses React's built-in XSS protection. If `userInput` contains a script tag or event handler attribute, it will execute in the user's browser.

**How to recognize it:**
- Search for `dangerouslySetInnerHTML` across all JSX/TSX files
- Check whether the content being rendered comes from user input or an untrusted source
- Check if the content is sanitized before rendering (using DOMPurify or similar)

**Remediation:**
- If the content is plain text, use React's default text rendering: `<div>{userInput}</div>`
- If rich HTML is genuinely needed, sanitize with DOMPurify:
  ```jsx
  import DOMPurify from 'dompurify';
  <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
  ```
- If rendering markdown, use a markdown library that sanitizes output

---

### Prototype Pollution

**Pattern to search for:** recursive merge functions, `Object.assign` with user data

**Vulnerable code:**
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

**Why it is dangerous:** If `userInput` contains `__proto__`, `constructor`, or `prototype` as keys, the merge function can modify `Object.prototype`, affecting all objects in the application. This can lead to authentication bypass, privilege escalation, or RCE.

**How to recognize it:**
- Recursive merge/deep clone functions that iterate over object keys
- `Object.assign()` with user-controlled source objects
- JSON parsing where the result is used as a config object
- Any pattern that copies user-controlled properties onto existing objects

**Remediation:**
- Use safe merge utilities (lodash `_.merge` with recent versions that have prototype pollution fixes)
- Validate that keys do not include `__proto__`, `constructor`, or `prototype`
- Use `Object.create(null)` for objects that receive user properties
- Use `Map` instead of plain objects for user-controlled key-value data

---

### Regex DoS (ReDoS)

**Pattern to search for:** complex regex with nested quantifiers

**Vulnerable code:**
```javascript
const emailRegex = /^([a-zA-Z0-9]+)*@([a-zA-Z0-9]+)*\.([a-zA-Z0-9]+)*$/;
emailRegex.test(userInput);
```

**Why it is dangerous:** Nested quantifiers (like `(a+)+` or `(a*)*`) can cause catastrophic backtracking on certain inputs. A carefully crafted input can cause the regex engine to take exponential time, freezing the Node.js event loop.

**How to recognize it:**
- Regex patterns with nested quantifiers: `(x+)+`, `(x*)*`, `(x+)*`
- Regex with alternating groups and quantifiers: `(a|b)+` where both alternatives can match the same input
- User input tested against complex regex patterns

**Remediation:**
- Simplify regex patterns to avoid nested quantifiers
- Use atomic groups or possessive quantifiers where supported
- Set a timeout on regex matching (e.g., using `re2` library which has bounded execution time)
- For email validation, use a simple pattern or a dedicated validation library rather than complex regex

---

### Path Traversal

**Pattern to search for:** `fs.readFile`, `fs.writeFileSync`, `path.join` with user input

**Vulnerable code:**
```javascript
const filePath = path.join(__dirname, 'uploads', req.params.filename);
fs.readFile(filePath, (err, data) => { ... });
```

**Why it is dangerous:** If `req.params.filename` contains `../../etc/passwd`, the resolved path escapes the intended `uploads` directory and reads arbitrary files from the server.

**How to recognize it:**
- File system operations that use user input in the path
- `path.join()` or string concatenation with user-controlled segments
- Static file serving where the file path is derived from user input
- Image/file upload handlers that use the original filename

**Remediation:**
- Validate that the resolved path is within the intended directory:
  ```javascript
  const resolved = path.resolve(__dirname, 'uploads', req.params.filename);
  if (!resolved.startsWith(path.resolve(__dirname, 'uploads'))) {
    throw new Error('Path traversal detected');
  }
  ```
- Use generated filenames instead of user-provided ones
- Use a whitelist of allowed file extensions
- Sanitize filenames: remove path separators, null bytes, and `..` sequences

---

### Dynamic Code Execution

**Pattern to search for:** `eval(`, `new Function(`, `setTimeout(string`, `setInterval(string`

**Vulnerable code:** Passing user-controlled strings to JavaScript code execution functions.

**Why it is dangerous:** Functions that evaluate strings as code (the built-in code evaluation function, the Function constructor, setTimeout/setInterval with string arguments) execute arbitrary JavaScript. If the input comes from a user, this is remote code execution.

**How to recognize it:**
- Any code evaluation function with user-controlled input
- `setTimeout()` and `setInterval()` with string arguments (not function references)
- `vm.runInContext()`, `vm.runInNewContext()`, `vm.compileFunction()`
- Dynamic `import()` with user-controlled paths

**Remediation:**
- Never pass user input to code execution functions
- Use `setTimeout(() => { ... }, 0)` (function reference, not string)
- Use `JSON.parse` for data instead of code evaluation
- For dynamic calculations, use a safe expression evaluator library

---

## Python Patterns

### SQL Injection via f-strings

**Pattern to search for:** f-strings in SQL queries, `.format()` in SQL, `%` formatting in SQL

**Vulnerable code:**
```python
query = f"SELECT * FROM users WHERE email = '{email}' AND status = '{status}'"
cursor.execute(query)
```

**Why it is dangerous:** User input is directly interpolated into the SQL query. An attacker can inject SQL by entering something like `' OR '1'='1' --` as the email field, bypassing authentication.

**How to recognize it:**
- f-strings, `.format()`, or `%` string formatting in SQL queries
- Any SQL query built by concatenating user input
- Raw SQL in Django's `raw()`, SQLAlchemy's `text()`, or cursor `execute()` with string formatting

**Remediation:**
- Use parameterized queries:
  ```python
  cursor.execute("SELECT * FROM users WHERE email = %s AND status = %s", (email, status))
  ```
- Use ORM methods that handle parameterization automatically:
  ```python
  User.objects.filter(email=email, status=status)
  ```
- If raw SQL is necessary, always use parameterized placeholders

---

### Pickle Deserialization

**Pattern to search for:** `pickle.loads`, `pickle.load`, `yaml.load` without SafeLoader

**Vulnerable code:**
```python
import pickle
data = pickle.loads(request.data)
```

**Why it is dangerous:** `pickle.loads()` can execute arbitrary Python code during deserialization. An attacker can craft a pickle payload that executes system commands, reads files, or establishes a reverse shell.

**How to recognize it:**
- `pickle.loads()`, `pickle.load()` with data from untrusted sources
- `cPickle.loads()` (Python 2)
- `shelve.open()` (uses pickle internally)
- `marshal.loads()` (less dangerous but still risky)
- `yaml.load()` without `Loader=yaml.SafeLoader`

**Remediation:**
- Use JSON for data interchange (no code execution during parsing):
  ```python
  data = json.loads(request.data)
  ```
- If you must deserialize, use `yaml.safe_load()` instead of `yaml.load()`
- For pickle specifically: only unpickle data from trusted sources, never from user input
- Consider using alternatives like `msgpack`, `protobuf`, or `JSON`

---

### Template Injection (SSTI)

**Pattern to search for:** `Template(user_input)`, `render_template_string`

**Vulnerable code:**
```python
from jinja2 import Template
template = Template(user_input)
result = template.render()
```

**Why it is dangerous:** If user input is treated as a template, it can contain template directives that execute code. In Jinja2, `{{ config }}` leaks Flask config, and accessing the MRO chain can lead to RCE.

**How to recognize it:**
- User input passed directly to template engines as the template string (not as a variable)
- `Template(user_input).render()`
- `render_template_string(user_input)` in Flask
- Mako templates with user-controlled content
- Django templates with `mark_safe` on user input

**Remediation:**
- Pass user input as template variables, not as the template itself:
  ```python
  template = Template("Hello {{ name }}!")
  result = template.render(name=user_input)  # Safe: user_input is a variable
  ```
- Use sandboxed template environments if user-defined templates are required
- Enable Jinja2's autoescaping: `Environment(autoescape=True)`
- Never use `render_template_string` with user input

---

### Command Injection

**Pattern to search for:** `os.system`, `subprocess` with `shell=True`, `os.popen`

**Vulnerable code:**
```python
import os
os.system(f"ping {user_ip}")
subprocess.call(f"convert {user_filename} output.png", shell=True)
```

**Why it is dangerous:** When `shell=True` is used or `os.system()` is called, the command string is passed to the system shell. User input containing shell metacharacters like semicolons or command substitution syntax will be executed.

**How to recognize it:**
- `os.system()`, `os.popen()` with user input
- `subprocess.call()`, `subprocess.run()`, `subprocess.Popen()` with `shell=True`
- String formatting or concatenation in command strings

**Remediation:**
- Use `subprocess.run()` without `shell=True`, passing arguments as a list:
  ```python
  subprocess.run(["ping", "-c", "3", user_ip], capture_output=True)
  ```
- If shell features are truly needed, sanitize input rigorously using `shlex.quote()`
- Validate input against a strict allowlist (e.g., IP addresses must match a regex)

---

## General Web Patterns

### CORS Misconfiguration

**Pattern to search for:** `Access-Control-Allow-Origin` with wildcard or dynamic origin

**Vulnerable code:**
```javascript
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Credentials', 'true');
  next();
});
```

**Why it is dangerous:** Setting wildcard origin with credentials allows any website to make authenticated requests to your API, stealing user data or performing actions on their behalf.

**How to recognize it:**
- CORS middleware that reflects the `Origin` header without validation
- Wildcard origin combined with credentials
- A static list of allowed origins that includes overly broad domains
- CORS headers set in multiple places (middleware + individual routes)

**Remediation:**
- Maintain an explicit allowlist of trusted origins
- Validate the `Origin` header against the allowlist before setting CORS headers:
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
- Never use wildcard when credentials are involved

---

### JWT Issues

**Pattern to search for:** `jwt.verify` with `none` algorithm, weak secrets, `jwt.decode` used for auth

**Vulnerable code:**
- Accepting the `none` algorithm in jwt.verify
- Using weak or short JWT secrets (dictionary words, short strings)
- Using `jwt.decode` instead of `jwt.verify` for authentication

**Why it is dangerous:**
- The `none` algorithm bypass allows attackers to forge tokens without knowing the secret
- Weak secrets can be brute-forced
- Using decode instead of verify accepts any token without validation

**How to recognize it:**
- JWT libraries configured to accept the `none` algorithm
- Short or common JWT secrets
- Using decode instead of verify for authentication
- Missing validation of expiration, issuer, or audience claims
- JWT payload containing sensitive data (passwords, PII)

**Remediation:**
- Always specify allowed algorithms explicitly:
  ```javascript
  const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
  ```
- Use strong, randomly generated secrets (32+ bytes for HS256)
- Prefer asymmetric algorithms (RS256, ES256) for distributed systems
- Always use verify, never decode for authentication
- Validate all relevant claims: expiration, issuer, audience
- Keep JWT payloads minimal -- they are readable by anyone who has the token

---

### Session Fixation

**Pattern to search for:** session not regenerated after login, session ID in URLs

**Vulnerable code:**
```javascript
app.post('/login', (req, res) => {
  if (authenticate(req.body.username, req.body.password)) {
    req.session.userId = user.id;  // Sets user on existing session without regeneration
    res.redirect('/dashboard');
  }
});
```

**Why it is dangerous:** An attacker can obtain a session ID (e.g., by visiting the site), then trick a victim into using that session ID (via a link or cookie injection). When the victim logs in, the attacker's session ID is now authenticated, and the attacker can access the victim's account.

**How to recognize it:**
- Login handlers that set authentication state on the existing session without regenerating the session ID
- Session IDs in URLs (query parameters)
- Accepting session IDs from both cookies and URL parameters
- Not invalidating old sessions on logout

**Remediation:**
- Regenerate the session ID after successful authentication:
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

**Pattern to search for:** `res.redirect(req.query`, `redirect`, `url`, `next` parameters

**Vulnerable code:**
```javascript
app.get('/redirect', (req, res) => {
  res.redirect(req.query.url);
});
```

**Why it is dangerous:** An attacker can craft a URL like `https://yoursite.com/redirect?url=https://evil.com` that appears to be from your domain but redirects to a malicious site. This is used for phishing attacks.

**How to recognize it:**
- Redirect endpoints that use user input directly
- URL parameters named `redirect`, `url`, `next`, `return_to`, `continue`
- OAuth/callback URLs that redirect to user-specified locations

**Remediation:**
- Validate the redirect target against an allowlist:
  ```javascript
  const allowedHosts = ['yoursite.com', 'app.yoursite.com'];
  const url = new URL(req.query.url, 'https://yoursite.com');
  if (!allowedHosts.includes(url.hostname)) {
    return res.status(400).send('Invalid redirect');
  }
  res.redirect(req.query.url);
  ```
- Use relative paths instead of absolute URLs when possible
- If the redirect URL must be flexible, ensure it starts with `/` and does not start with `//`

---

### Server-Side Request Forgery (SSRF)

**Pattern to search for:** HTTP client calls with user-controlled URLs, `requests.get(user_url)`

**Vulnerable code:**
```python
import requests
url = request.args.get('url')
response = requests.get(url)
return response.content
```

**Why it is dangerous:** The server makes an HTTP request to a user-specified URL. This can be used to access internal services (metadata endpoints, internal APIs, databases) that are not exposed to the internet.

**How to recognize it:**
- HTTP client calls with user-controlled URLs
- URL fetch/fetch proxy endpoints
- Webhook testing tools that make requests to user-specified URLs
- Image/document import from URLs
- PDF generation from URLs

**Remediation:**
- Use an allowlist of permitted domains/URLs
- Block requests to internal IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16)
- Block cloud metadata endpoints (169.254.169.254 for AWS/GCP/Azure)
- Use a separate network segment for outbound requests
- Validate URL scheme (only allow https://, not other protocols)

---

## How to Use This Reference During Code Review

### Step-by-Step Approach

1. **Identify the language and framework** of the code being audited
2. **Scan for the patterns listed above** using targeted searches
3. **Trace user input** from entry points (request parameters, headers, body, files) to dangerous sinks (queries, commands, HTML output, file paths)
4. **For each match**, determine if the input is truly user-controlled and untrusted
5. **Assess the impact** of successful exploitation
6. **Document findings** with the pattern name, location, and remediation

### Common Entry Points to Trace

- HTTP request parameters, query strings, and headers
- Request body (JSON, form data, multipart uploads)
- URL path segments
- Cookie values
- File uploads (filename and content)
- WebSocket messages
- Environment variables that can be influenced by external input

### Common Dangerous Sinks

- Database queries (SQL, NoSQL, ORM raw queries)
- Shell command execution
- HTML output (rendering, DOM manipulation)
- File system operations (read, write, delete)
- Network requests (HTTP clients, socket connections)
- Deserialization functions
- Template rendering engines
- Authentication and authorization logic
