# Question Patterns — Multiple-Choice Templates & Examples

Reference document for the Socratic interviewer agent. Contains question format
templates and realistic examples for each brainstorm dimension.

---

## Core Pattern: Multiple-Choice with Explanations

Use this format by default. Every option includes what it means, when it's
appropriate, trade-offs, and a grounded recommendation.

```
{Context sentence tying the question to the codebase}

{Question}

  A) **{Option Name}**
     {What this means — 1-2 sentences}
     → Recommended: {why, tied to project context}

  B) **{Option Name}**
     {What this means — 1-2 sentences}
     → Consider if: {when this is the better choice}

  C) **{Option Name}**
     {What this means — 1-2 sentences}
     → Consider if: {when this is the better choice}

  D) **Something else**
     Describe your preferred approach.

My recommendation: ({letter}) — {one-sentence reasoning grounded in codebase}
```

**Rules:**
- Every option references actual project context (file names, existing patterns,
  tech choices already made)
- The recommendation always has reasoning, but the user always decides
- The "Something else" escape hatch is always included
- Options are ordered by recommendation strength (recommended first)

---

## Open-Ended Pattern (Use Sparingly)

Use only when the topic is genuinely open — no reasonable set of options covers
the likely answers.

```
{Question}

Context: {1-2 sentences connecting to the codebase}

Some possibilities to consider:
- {possibility 1 — what it would mean}
- {possibility 2 — what it would mean}
- {possibility 3 — what it would mean}

{Focused follow-up question}
```

---

## Examples by Dimension

### Dimension 1: Problem & Users

**Format**: Open-ended (genuinely different per project)

```
Who are the primary users of this feature, and what problem does it solve for
them?

Context: Your app currently has a dashboard that shows all orders in a flat
table. Users can filter by date range but can't see order trends over time.

Some possibilities to consider:
- Operations managers who need to spot anomalies in order volume
- Sales reps tracking their individual performance
- Execs who want a high-level summary for reporting

What's the main pain point this feature addresses?
```

### Dimension 2: Success Criteria

**Format**: Multiple-choice with measurable options

```
How will we know this feature is successful? Based on your current analytics
setup (PostHog events on order actions):

  A) **Engagement metric**
     Users view the new feature at least 3x per week on average.
     → Recommended: measurable via existing PostHog tracking, no new infra.

  B) **Task completion metric**
     Users complete their intended action 30% faster than with the current
     interface.
     → Consider if: you can establish a baseline from current usage data.

  C) **Error reduction metric**
     Support tickets related to {area} drop by 50% within 30 days.
     → Consider if: there's an existing ticket category for this pain point.

  D) **Something else**
     Describe your success criteria.

My recommendation: (A) — you already have PostHog integrated and it gives us
a clear, falsifiable signal without adding tracking overhead.
```

### Dimension 3: Constraints

**Format**: Multiple-choice with trade-offs

```
What constraints should guide this work? Based on your current setup (Next.js 14,
Prisma, PostgreSQL, deployed on Vercel):

  A) **Minimal dependency addition**
     No new packages or infrastructure. Work within existing tech stack.
     → Recommended: your Prisma/PostgreSQL setup is solid and well-tested.

  B) **Backward compatible**
     Must not break any existing API contracts or data formats. Existing
     consumers continue to work unchanged.
     → Consider if: external systems consume your API.

  C) **Timeline-driven**
     Need this shipped within {N} days. Willing to accept a simpler first
     version to meet the deadline.
     → Consider if: there's a business deadline or event driving urgency.

  D) **Something else**
     Describe your constraints.

My recommendation: (A) + (C) — your stack is mature enough to handle this
without new deps, and shipping a focused first version avoids scope creep.
```

### Dimension 4: Scope Boundaries

**Format**: Multiple-choice with MVP cut recommendation

```
Which of these are in scope for this iteration?

Based on the feature description, here are the potential pieces:

  [1] Core data model and storage
  [2] API endpoints for CRUD operations
  [3] Admin dashboard for management
  [4] End-user notification delivery
  [5] Analytics and reporting
  [6] Audit logging

  A) **[1] + [2] only — Bare minimum**
     Data layer and API. No UI, no notifications, no reporting.
     → Recommended: foundation that everything else builds on.

  B) **[1] + [2] + [4] — User-facing MVP**
     Core data, API, and the user notification experience.
     → Consider if: the feature isn't useful without user-facing delivery.

  C) **[1] + [2] + [3] + [4] — Full feature**
     Everything except analytics and audit logging.
     → Consider if: admin management is required for launch.

  D) **Something else**
     Pick your own combination.

My recommendation: (B) — your users need to receive notifications for this
to have value, but admin tooling and analytics can follow in the next iteration.
```

### Dimension 5: Simplest Viable Version

**Format**: Multiple-choice with effort tiers

```
What level of scope feels right for this feature?

  A) **Minimal — Days of work**
     In-app notification badge with a simple dropdown list. No persistence
     beyond session. No read/unread state.
     → Recommended: validates the feature has value before investing in
       infrastructure.

  B) **Standard — Week of work**
     Persistent notifications with read/unread state, stored in your existing
     PostgreSQL database via Prisma. Basic notification list page.
     → Consider if: users need notification history across sessions.

  C) **Full — Multiple weeks**
     Notification preferences, email digest integration, real-time WebSocket
     delivery, and a notification center with filtering.
     → Consider if: this is a core product feature, not a nice-to-have.

My recommendation: (A) — your existing session storage (NextAuth session)
can hold a notification count. Ship a badge first, measure engagement, then
decide whether to invest in persistence. (Karpathy: Simplicity First)
```

### Dimension 6: UI Work Detection

**Format**: Multiple-choice — always asked

```
Does this feature involve any user interface changes?

  A) **New UI components**
     New pages, sections, or interactive elements the user will see and interact
     with.
     → If yes, we'll flag this for design-first development (Pencil.dev).

  B) **Modifications to existing UI**
     Changes to existing components — new fields, layout adjustments, state
     changes.
     → Smaller scope but still benefits from visual design review.

  C) **No UI — backend only**
     API changes, data processing, background jobs, or internal tooling.
     → No design phase needed. Implementation can be more direct.

  D) **Not sure**
     Describe what the user will experience, and I'll assess.

My recommendation: based on your description, this looks like (B) — the
existing {ComponentName} will need updates. If there are also new visual
elements, we should flag for design review.
```

### Dimension 7: Data Model

**Format**: Multiple-choice grounded in existing DB patterns

```
How should this feature's data be stored? Based on your current Prisma schema
(14 models, PostgreSQL with soft-delete pattern on all models):

  A) **New Prisma model**
     Add a dedicated {ModelName} table following your existing model conventions
     (id, createdAt, updatedAt, deletedAt).
     → Recommended: clean separation, follows your established pattern.

  B) **Extend existing model**
     Add fields to your existing {ExistingModel} (e.g., a JSON column for
     metadata or a status enum).
     → Consider if: the new data is a natural extension of an existing entity.

  C) **Separate storage**
     Use a different storage mechanism (Redis cache, file storage, external
     service).
     → Consider if: this data has different access or retention patterns.

  D) **Something else**
     Describe your preferred data approach.

My recommendation: (A) — your codebase consistently uses one model per domain
concept, and the new data has its own lifecycle separate from existing models.
```

### Dimension 8: API Design

**Format**: Multiple-choice grounded in existing API patterns

```
What API approach fits this feature? Your project currently has 12 REST
endpoints following the pattern `/api/v1/{resource}`, all using Next.js Route
Handlers with Zod validation.

  A) **REST — Match existing pattern**
     Add new `/api/v1/{resource}` endpoints with Zod validation. Consistent
     with your 12 existing routes.
     → Recommended: no new patterns for the team to learn.

  B) **Extend existing endpoint**
     Add query parameters or response fields to an existing endpoint.
     → Consider if: the new functionality is a natural extension of an
       existing API surface.

  C) **WebSocket / SSE for real-time**
     Add a WebSocket connection or Server-Sent Events stream for live updates.
     → Consider if: the feature requires sub-second updates. Note: your project
       currently has no WebSocket infrastructure.

  D) **Something else**
     Describe your preferred API approach.

My recommendation: (A) — your existing REST pattern with Zod validation is
well-established. Unless there's a specific need for real-time delivery, stick
with what's already working.
```

### Dimension 9: Error Handling

**Format**: Multiple-choice with UX implications

```
How should errors in this feature be handled? Your project currently uses a
centralized error handler that returns `{ error: string, code: string }` with
toast notifications on the frontend.

  A) **Match existing error pattern**
     Use the same centralized error handler and toast notifications. Users see
     a brief error message with a retry option.
     → Recommended: consistent with the rest of your application.

  B) **Inline validation**
     Validate before submission and show errors next to the relevant fields.
     Prevents submissions with invalid data.
     → Consider if: this feature has form inputs where per-field feedback
       would help users correct mistakes.

  C) **Silent retry with fallback**
     Automatically retry failed operations (1-2 times) before showing the
     error to the user. Show a degraded experience if retries exhaust.
     → Consider if: this involves network operations that may fail
       intermittently.

  D) **Something else**
     Describe your preferred error handling approach.

My recommendation: (A) — your users are already familiar with the toast
notification pattern. Add inline validation (B) only if the feature has
complex form inputs.
```

### Dimension 10: Migration / Compatibility

**Format**: Multiple-choice with risk assessment (conditional — only when modifying existing features)

```
Your feature modifies the existing {ExistingFeature}. How should we handle the
transition?

  A) **Non-breaking — Additive only**
     Add new functionality alongside existing behavior. Nothing changes for
     current users until they opt in.
     → Recommended: zero risk of regression. Safest approach.

  B) **Feature flag rollout**
     Ship changes behind a feature flag. Gradually enable for users while
     monitoring for issues.
     → Consider if: the change affects critical user workflows and you need
       a rollback plan.

  C) **Direct replacement**
     Replace the existing implementation. All users get the new behavior
     immediately.
     → Consider if: the old behavior is buggy or actively harmful, and a
       clean break is warranted.

  D) **Something else**
     Describe your migration strategy.

My recommendation: (A) — your codebase already supports additive changes
without breaking consumers. Reserve direct replacement for when the old
behavior is causing active problems.
```
```

---

## Usage Guidelines

- **Don't ask all dimensions** — select the 6-8 most relevant ones
- **Skip dimensions the user already answered** in their initial description
- **Adapt the examples** — these are templates, not scripts. Replace the
  hypothetical project context with the actual project's details
- **Order matters** — Problem & Users first, Migration last
- **If a question feels forced**, skip it. Better 6 great questions than
  10 mediocre ones
- **Track question count** — after 8 questions, start wrapping up. If critical
  gaps remain, ask at most 2 more
