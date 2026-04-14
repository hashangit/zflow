# Karpathy Guidelines with ZFlow Annotations

Behavioral constraints baked into every ZFlow agent via `agents/_shared/karpathy-preamble.md`.

---

## Guideline 1: Think Before Coding

**Principle:** State assumptions explicitly. Present multiple interpretations. Name what's confusing. Don't guess.

**ZFlow enforcement:**
- Every agent articulates assumptions before acting
- Agents MUST stop and ask when: task has multiple interpretations, required context is missing, scope is larger than documented, a simpler approach contradicts the design

**Anti-patterns:** Silent assumptions, guessing on ambiguity, assumption cascading, confidence without evidence.

---

## Guideline 2: Simplicity First

**Principle:** Minimum code that solves the problem. No speculative features or abstractions. If 200 lines could be 50, rewrite it.

**ZFlow enforcement:**
- Brainstorm: presents "simplest viable version" as a scope tier
- Design: prefers simplest approach unless complexity is justified with concrete reasons
- Review: `overengineering-critic` audits for YAGNI, unnecessary complexity, single-use abstractions
- QA: `code-quality-auditor` checks for speculative features and unnecessary abstractions

### Code Examples

**Unnecessary abstraction:**
```javascript
// BAD: Interface for a single implementation
interface IUserRepository {
  findById(id: string): Promise<User>;
}
class UserRepository implements IUserRepository { ... }

// GOOD: Just the class, add interface when you have a second implementation
class UserRepository {
  findById(id: string): Promise<User> { ... }
}
```

**Speculative configuration:**
```python
# BAD: Configurable for scenarios that don't exist yet
def process_data(data, strategy="default", batch_size=100, retry_count=3):
    ...

# GOOD: Only what is needed now
def process_data(data):
    ...
```

**Premature optimization:**
```typescript
// BAD: Caching layer with no performance requirements
const cache = new Map<string, User>();
async function getUser(id: string): Promise<User> {
  if (cache.has(id)) return cache.get(id)!;
  const user = await db.users.findById(id);
  cache.set(id, user);
  return user;
}

// GOOD: Direct call until performance is actually a problem
async function getUser(id: string): Promise<User> {
  return db.users.findById(id);
}
```

**Anti-patterns:** "In case we need it later", config for single values, abstraction with one implementation, event systems for two events, plugin architecture for fixed features.

---

## Guideline 3: Surgical Changes

**Principle:** Touch only what you must. Don't "improve" adjacent code. Match existing style. Remove only what YOUR changes made unused. Every changed line traces to the user's request.

**ZFlow enforcement:**
- Implementation agents receive explicit file paths and scope boundaries
- Debug fix agents: fix design scopes what to change; deviations must be justified
- QA: `code-quality-auditor` verifies every changed line traces to scope

### Code Examples

**Tangential refactoring:**
```typescript
// Task: Add email validation to the registration form
// BAD: Also refactored password validation, renamed variables, reorganized component
// GOOD: Only add email validation, leave everything else alone
```

**Style "improvements":**
```python
// Task: Fix off-by-one error in process_items()
// BAD: Also reformatted file, changed quotes, added type hints to unrelated functions
// GOOD: Only fix the bug
```

**Anti-patterns:** "While I'm here...", formatting-only changes, dead code removal beyond scope, style unification, dependency upgrades, comment improvements on unchanged code.

---

## Guideline 4: Goal-Driven Execution

**Principle:** Transform tasks into verifiable goals. Every task has success criteria upfront. Strong criteria enable autonomous loops; weak criteria require human clarification.

**ZFlow enforcement:**
- Brainstorm: defines measurable success criteria in scope.md
- Design: every task has explicit success criteria; tasks without them are flagged
- Implementation: each agent receives criteria, plans as `Step -> verify: check`
- QA: each dimension has a verifiable checklist

### Success Criteria Format

```markdown
### Task T3: CreateUserService
- **Complexity:** M
- **Dependencies:** T1 (User model)
- **Success criteria:**
  - [ ] `createUser(validData)` returns 201 with created user
  - [ ] `createUser(invalidEmail)` returns 400 "Invalid email format"
  - [ ] `createUser(duplicateEmail)` returns 409 "Email already exists"
  - [ ] All operations require valid JWT, return 401 without
```

**Anti-patterns:** Vague criteria ("works correctly"), missing negative cases, unmeasurable criteria ("feels fast"), missing criteria entirely.

---

## Enforcement Mechanisms

| Level | Mechanism | Effect |
|-------|-----------|--------|
| Agent preamble | `karpathy-preamble.md` injected into every agent | Baseline behavioral expectations |
| Review phase | `overengineering-critic` + `alignment-checker` | Catches over-engineering before implementation |
| QA phase | `code-quality-auditor` verifies on actual code | Catches violations in implementation |

---

## Quick Reference Card

| Guideline | Agent Asks | Red Flag |
|-----------|-----------|----------|
| Think Before Coding | "What are my assumptions?" | Proceeding without stating assumptions |
| Simplicity First | "Is this the minimum that solves it?" | Code for scenarios not in scope |
| Surgical Changes | "Does every change trace to scope?" | "While I'm here..." improvements |
| Goal-Driven | "How do I verify this works?" | Vague or missing success criteria |
