# Karpathy Guidelines with ZFlow Annotations

Full text of Andrej Karpathy's LLM coding guidelines as applied to ZFlow, with enforcement mechanisms and anti-patterns.

---

## Overview

The Karpathy guidelines are not a separate phase in ZFlow -- they are behavioral constraints baked into every agent across every phase. They are injected via a shared preamble file (`agents/_shared/karpathy-preamble.md`) and enforced at three levels: agent prompts, review agents, and QA agents.

---

## Guideline 1: Think Before Coding

### Original Principle

Before writing any code, state your assumptions explicitly. If multiple interpretations exist, present them. If something is unclear, name what is confusing. Do not guess.

### ZFlow Application

Every agent must articulate its assumptions before taking action. In ZFlow, this manifests as:

- **Brainstorm agent (Phase 0):** Restates the user's idea before asking clarifying questions. If the request is ambiguous, surfaces the ambiguity with multiple interpretations rather than picking one.
- **Research agents (Phase 1):** State what they expect to find before exploring. If the codebase contradicts their expectations, they flag it.
- **Design agent (Phase 2):** Lists design assumptions before proposing approaches. Identifies assumptions that need user validation.
- **Review agents (Phase 3):** State their review criteria before examining the solution. Identify assumptions baked into the design.
- **Implementation agents (Phase 4):** Define success criteria before writing code. If a task description is ambiguous, they surface the ambiguity rather than guessing.
- **QA agents (Phase 5):** State what they expect to find before auditing. Unexpected findings get elevated.
- **Debug agents (Phase D2):** State assumptions about what is happening before analyzing. Low-confidence root causes are flagged explicitly.

### When Agents Should Stop and Ask

An agent MUST stop and ask (via the coordinator, which surfaces to the user) when:

1. The task description has multiple valid interpretations
2. Required context is missing and cannot be inferred from available documents
3. The agent discovers that the scope is larger or different than documented
4. A simpler approach exists but contradicts the design
5. The agent is unsure whether a change is in scope

### Anti-Patterns and Red Flags

- **Silent assumption:** The agent proceeds with an unstated assumption. "I assumed you meant X" should never appear after the fact.
- **Guessing on ambiguity:** The agent picks one interpretation of an ambiguous requirement without surfacing the alternatives.
- **Assumption cascading:** One wrong assumption leads to a chain of downstream decisions, all built on a faulty foundation.
- **Confidence without evidence:** The agent expresses high confidence without stating the basis for that confidence.

---

## Guideline 2: Simplicity First

### Original Principle

Minimum code that solves the problem. No features beyond what was asked. No abstractions for single-use code. No speculative "flexibility" or "configurability." If 200 lines could be 50, rewrite it. Every agent asks: "Would a senior engineer say this is overcomplicated?"

### ZFlow Application

Simplicity First is enforced throughout the workflow:

- **Brainstorm agent:** Presents a "simplest viable version" as one of the scope tiers. Recommends the simplest approach unless complexity is justified.
- **Design agent:** For each approach proposed, assesses which is simplest. Prefers the simplest approach unless complexity is justified with concrete reasons. Includes an "Alternatives Considered" section with rejection rationale for more complex options.
- **Review phase:** The `overengineering-critic` agent specifically audits against Simplicity First. It asks: What can be simplified? What is YAGNI (You Ain't Gonna Need It)? What adds complexity without value? Are there abstractions for single-use code?
- **Implementation agents:** Instructed to write minimum code. No speculative features. No "flexibility" for future use cases not in scope.
- **QA phase:** The `code-quality-auditor` checks that no speculative features were added and no unnecessary abstractions exist.

### Examples of Overengineering to Avoid

**Unnecessary abstraction layer:**
```javascript
// BAD: Interface for a single implementation
interface IUserRepository {
  findById(id: string): Promise<User>;
  create(data: CreateUserDTO): Promise<User>;
}
class UserRepository implements IUserRepository { ... }

// GOOD: Just the class, add interface when you have a second implementation
class UserRepository {
  findById(id: string): Promise<User> { ... }
  create(data: CreateUserDTO): Promise<User> { ... }
}
```

**Speculative configuration:**
```python
# BAD: Configurable for scenarios that do not exist yet
def process_data(data, strategy="default", batch_size=100, retry_count=3, timeout=30):
    ...

# GOOD: Only what is needed now
def process_data(data):
    ...
```

**Premature optimization:**
```typescript
// BAD: Caching layer for a feature with no performance requirements
const cache = new Map<string, User>();
async function getUser(id: string): Promise<User> {
  if (cache.has(id)) return cache.get(id)!;
  const user = await db.users.findById(id);
  cache.set(id, user);
  return user;
}

// GOOD: Direct database call until performance is actually a problem
async function getUser(id: string): Promise<User> {
  return db.users.findById(id);
}
```

**Overly generic solution:**
```python
# BAD: Generic event system for a single notification type
class EventBus:
    def subscribe(self, event_type: str, handler: Callable): ...
    def publish(self, event_type: str, data: Any): ...

# GOOD: Direct function call
def send_notification(user_id: str, message: str): ...
```

### Anti-Patterns and Red Flags

- **"In case we need it later":** Any code justified by future needs rather than current requirements.
- **Configuration for single values:** A config system for values that are only set once.
- **Abstraction with one implementation:** An interface, abstract class, or strategy pattern with a single concrete implementation.
- **Event systems for two events:** A pub/sub system when two direct function calls would suffice.
- **Plugin architecture for a fixed feature set:** Extensibility hooks for features that are known and finite.

---

## Guideline 3: Surgical Changes

### Original Principle

Touch only what you must. Don't "improve" adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style. Remove only imports/variables/functions that YOUR changes made unused. Every changed line must trace directly to the user's request.

### ZFlow Application

Surgical Changes is the most strictly enforced guideline in ZFlow because agents have a tendency to "improve" things outside their scope:

- **Implementation agents:** Receive explicit file paths and scope boundaries. Their agent prompt includes: "Every changed line must trace directly to the scope requirements."
- **Debug fix agents:** The fix design explicitly scopes what files and functions to change. The implementation agent must justify any deviation.
- **Review phase:** The `overengineering-critic` checks for scope creep in the design. The `alignment-checker` ensures changes align with existing patterns.
- **QA phase:** The `code-quality-auditor` verifies that every changed line traces to the scope. Lines that do not trace to scope are flagged as violations.

### Examples of Scope Creep to Resist

**Tangential refactoring:**
```typescript
// Task: Add email validation to the registration form

// BAD: Also refactored the password validation, renamed variables,
// and reorganized the form component structure
export function RegistrationForm() {
  // renamed all variables from camelCase to snake_case
  // refactored password validation into a separate module
  // reorganized component structure
  const email_error = validateEmail(email); // <-- the actual task
}

// GOOD: Only add email validation, leave everything else alone
export function RegistrationForm() {
  const emailError = validateEmail(email); // <-- added
  // ... rest unchanged
}
```

**Style "improvements":**
```python
# Task: Fix the off-by-one error in process_items()

# BAD: Also reformatted the file, changed quotes from single to double,
# added type hints to unrelated functions, and "improved" variable names
def process_items(items: List[Item]) -> List[Result]:
    """Process a list of items and return results."""  # added docstring
    results: List[Result] = []  # added type hint
    for item in items:  # fixed the range bug (actual fix)
        results.append(transform(item))
    return results

# GOOD: Only fix the bug
def process_items(items):
    results = []
    for i in range(len(items)):  # changed range(1, len(items))
        results.append(transform(items[i]))  # <-- fixed
    return results
```

**Unnecessary cleanup:**
```javascript
// Task: Add a loading state to the button component

// BAD: Also removed "unused" imports (that are used in another branch),
// cleaned up comments, and reorganized the CSS

// GOOD: Only add the loading state prop and its conditional rendering
function Button({ children, loading }) {
  return (
    <button disabled={loading}>
      {loading ? <Spinner /> : children}
    </button>
  );
}
```

### Anti-Patterns and Red Flags

- **"While I'm here...":** Any change justified by proximity rather than scope.
- **Formatting-only changes:** Reformatting code that is not related to the task.
- **Dead code removal beyond scope:** Removing imports/variables/functions that the task did not make unused.
- **Style unification:** Changing code style to match personal preference when the existing style is consistent within itself.
- **Dependency upgrades:** Upgrading packages that are not related to the task.
- **Comment improvements:** Rewriting or adding comments to code that is not being changed by the task.

---

## Guideline 4: Goal-Driven Execution

### Original Principle

Transform tasks into verifiable goals. Every implementation task has success criteria defined upfront. Each step has a verification check. Strong success criteria let agents loop independently; weak criteria require human clarification.

### ZFlow Application

Goal-driven execution is how ZFlow enables autonomous agent loops:

- **Brainstorm agent:** Defines measurable success criteria in `scope.md`. "Users can complete the flow" is weak; "Users can complete the registration flow in under 30 seconds with a 95% success rate" is strong.
- **Design agent:** Every task in the task breakdown has explicit success criteria. Tasks without measurable success criteria are flagged as ambiguous.
- **Implementation agents:** Each agent receives success criteria for its task. The agent defines its plan as: Step 1 -> verify: check. Step 2 -> verify: check.
- **Debug agents:** The root cause analysis has a confidence level. The fix verification confirms success against the original reproduction steps.
- **QA agents:** Each QA dimension has a checklist of verifiable items.

### How Success Criteria Work in ZFlow Tasks

Every task in the solution's task breakdown includes success criteria in this format:

```markdown
### Task T3: Create UserService
- **Complexity:** M
- **Dependencies:** T1 (User model)
- **Success criteria:**
  - [ ] `createUser(validData)` returns the created user with status 201
  - [ ] `createUser(invalidEmail)` returns 400 with error message "Invalid email format"
  - [ ] `createUser(duplicateEmail)` returns 409 with error message "Email already exists"
  - [ ] `getUser(existingId)` returns the user with status 200
  - [ ] `getUser(nonexistentId)` returns 404 with error message "User not found"
  - [ ] `updateUser(validData)` returns the updated user with status 200
  - [ ] `deleteUser(existingId)` returns 204 with empty body
  - [ ] All operations require valid JWT, return 401 without
```

### Why This Matters

Strong success criteria enable:
1. **Autonomous verification:** Implementation agents can verify their own work against the criteria
2. **Independent QA:** QA agents have a clear checklist to audit against
3. **Reduced human intervention:** Fewer "does this look right?" questions to the user
4. **Debugging efficiency:** When a fix attempt fails, the failure is specific ("criterion 3 not met" rather than "something went wrong")

### Anti-Patterns and Red Flags

- **Vague criteria:** "Works correctly" or "handles edge cases" without specifying which edge cases.
- **Missing negative cases:** Only defining what should work, not what should fail.
- **Unmeasurable criteria:** "Feels fast" instead of "responds in under 200ms at p95."
- **Missing criteria entirely:** A task that lists what to implement but not how to verify it.

---

## Enforcement Mechanisms

### Level 1: Agent Prompt Preamble

Every agent template starts with the Karpathy preamble (`agents/_shared/karpathy-preamble.md`). This is a behavioral rules section that is injected before the agent's specific instructions. It covers all four guidelines with concrete "do" and "don't" items.

**Effect:** Sets the baseline behavioral expectation for every agent.

### Level 2: Review Phase (Phase 3)

The `overengineering-critic` agent is specifically tasked with auditing the solution against Simplicity First and Surgical Changes. It asks:

- What can be simplified?
- What is YAGNI?
- What adds complexity without value?
- Would a senior engineer say this is overcomplicated?
- Are there abstractions for single-use code?

The `alignment-checker` agent verifies that the proposed changes match existing patterns and do not introduce unnecessary new patterns.

**Effect:** Catches over-engineering before implementation begins.

### Level 3: QA Phase (Phase 5)

The `code-quality-auditor` agent enforces Karpathy guidelines on the actual implementation:

- **Simplicity:** No speculative features, no unnecessary abstractions
- **Surgical:** Every changed line traces to scope; no tangential changes
- **Goal-driven:** All success criteria are met

Lines that violate Surgical Changes (changed without tracing to scope) are flagged as QA issues.

**Effect:** Catches violations in the actual code, after implementation.

---

## Quick Reference Card

| Guideline | Agent Asks | Red Flag |
|-----------|-----------|----------|
| Think Before Coding | "What are my assumptions?" | Proceeding without stating assumptions |
| Simplicity First | "Is this the minimum that solves it?" | Code that handles scenarios not in scope |
| Surgical Changes | "Does every change trace to scope?" | "While I'm here..." improvements |
| Goal-Driven Execution | "How do I verify this works?" | Success criteria that are vague or missing |
