# Vulnerability Patterns: Python

Code-level vulnerability patterns for Python ecosystems. Load this when auditing Python codebases.

Each pattern includes: what to search for, why it is dangerous, how to recognize it, and how to fix it.

**Note:** Code examples illustrate vulnerable patterns for educational purposes only.

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
