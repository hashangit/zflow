# Vulnerability Patterns: JavaScript & TypeScript

Code-level vulnerability patterns for JS/TS ecosystems. Load this when auditing JavaScript or TypeScript codebases.

Each pattern includes: what to search for, why it is dangerous, how to recognize it, and how to fix it.

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
