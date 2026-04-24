# Security Reference: Injection & Exception Handling

Covers OWASP A05 (Injection) and A10 (Mishandling of Exceptional Conditions). Load this when auditing input handling, output encoding, command execution, and error-handling paths.

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
   - JS: `dangerouslySetInnerHTML`, `innerHTML`, `eval()`, `Function()`, `document.write`
   - Python: `eval()`, `exec()`, subprocess with `shell=True`
   - Java: `Runtime.exec()`, `ProcessBuilder` with unsanitized input
   - PHP: `eval()`, shell execution, backtick operator

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
