# Question Patterns — Multiple-Choice Templates & Examples

Templates and examples for the Socratic interviewer agent's brainstorm dimensions.

---

## Plain Language Rules

1. **Use everyday words.** "Database table" not "Prisma model." "Error message" not "centralized error handler with toast notification pattern."
2. **Explain terms in context.** "API endpoint (a URL your app calls to get or send data)" or "WebSocket (a way to push updates to the browser instantly)."
3. **Say why a choice matters.** "This determines how fast users see updates" vs. assuming they know.
4. **Describe outcomes, not implementations.** "Small red dot for new notifications" vs. "notification badge with session-based persistence."
5. **Keep recommendations short.** "I'd go with (A) — your project already handles this, no new tools needed."

---

## Core Pattern: Multiple-Choice with Explanations

Default format. Every option includes meaning, trade-offs, and grounded recommendation.

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
- Every option references actual project context (file names, patterns, tech choices)
- Recommendation always has reasoning; user always decides
- "Something else" escape hatch always included
- Options ordered by recommendation strength (recommended first)

---

## Open-Ended Pattern (Use Sparingly)

Only when genuinely open — no reasonable option set covers likely answers.

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

**Format**: Open-ended

```
Who are the primary users of this feature, and what problem does it solve for them?

Context: Your app has a dashboard showing all orders in a flat table. Users can
filter by date range but can't see order trends over time.

Some possibilities to consider:
- Operations managers who need to spot anomalies in order volume
- Sales reps tracking their individual performance
- Execs who want a high-level summary for reporting

What's the main pain point this feature addresses?
```

### Dimension 2: Success Criteria

**Format**: Multiple-choice with measurable options

```
How will we know this feature is a success? Your app tracks user actions with
PostHog (your analytics tool), so we can measure things easily.

  A) **People actually use it**
     Users open this new feature at least 3 times per week on average.
     → Recommended: easy to measure with existing setup, no extra work.

  B) **People get things done faster**
     Users complete their task 30% faster than today.
     → Consider if: you can measure how long things take today for comparison.

  C) **Fewer support requests**
     Support tickets related to {area} drop by 50% within a month.
     → Consider if: you already have a ticket category for this problem.

  D) **Something else**
     How would you measure success?

My recommendation: (A) — your analytics already tracks what users do, so we can
measure this right away without adding anything new.
```

### Dimension 3: Constraints

**Format**: Multiple-choice with trade-offs

```
Any rules or limits to keep in mind? Your project uses Next.js, PostgreSQL,
and is deployed on Vercel:

  A) **No new tools or packages**
     Use only what's already installed. No new libraries or services.
     → Recommended: current setup is solid and well-tested.

  B) **Don't break anything existing**
     Everything that works now must keep working. External apps shouldn't notice.
     → Consider if: other teams or external apps depend on your app.

  C) **Need it done by a certain date**
     Deadline — {N} days. Simplify first version to meet it.
     → Consider if: a specific date or event is driving this.

  D) **Something else**
     What constraints do you have?

My recommendation: (A) + (C) — current tools handle this, and shipping a simple
first version avoids building too much before getting feedback.
```

### Dimension 4: Scope Boundaries

**Format**: Multiple-choice with MVP cut recommendation

```
What should we include in this first version? Possible pieces:

  [1] Storing the data (database)
  [2] Behind-the-scenes connections (API)
  [3] Admin page to manage things
  [4] Users seeing/using it
  [5] Reports and analytics
  [6] Log of who did what and when

  A) **[1] + [2] — Just the foundation**
     Data storage and connections. No user-facing parts.
     → Recommended: everything else builds on this.

  B) **[1] + [2] + [4] — Users can see it**
     Storage, connections, and user-facing parts.
     → Consider if: feature isn't useful unless users can see it.

  C) **[1] + [2] + [3] + [4] — Full feature**
     Everything except reports and activity log.
     → Consider if: you need an admin page to manage this.

  D) **Something else**
     Pick what you need.

My recommendation: (B) — users need to see and use this for value. Admin and
reports can come later.
```

### Dimension 5: Simplest Viable Version

**Format**: Multiple-choice with effort tiers

```
How much should we build in the first version?

  A) **Small — A few days**
     Basics: small indicator for new notifications, simple list. Disappear on
     browser close.
     → Recommended: minimum to test if people find it useful, add more later.

  B) **Medium — About a week**
     Notifications persist between visits (database). Read/unread states.
     Simple notifications page.
     → Consider if: users need to see old notifications when they return.

  C) **Full — A few weeks**
     Everything: preferences, email digests, instant delivery (WebSocket),
     full notification center with search and filters.
     → Consider if: this is a core product feature, not a nice-to-have.

My recommendation: (A) — start small, ship simple version, see if people use it,
then invest in bigger version.
```

### Dimension 6: UI Work Detection

**Format**: Multiple-choice — always asked

```
Does this feature involve user interface changes?

  A) **New UI components**
     New pages, sections, or interactive elements.
     → Flagged for design-first development (Pencil.dev).

  B) **Modifications to existing UI**
     Changes to existing components — new fields, layout, state changes.
     → Smaller scope but benefits from visual design review.

  C) **No UI — backend only**
     API changes, data processing, background jobs, internal tooling.
     → No design phase. More direct implementation.

  D) **Not sure**
     Describe what the user will experience and I'll assess.

My recommendation: based on your description, (B) — existing {ComponentName}
needs updates. Flag for design review if new visual elements too.
```

### Dimension 7: Data Model

**Format**: Multiple-choice grounded in existing DB patterns

```
Where should this feature's data live? Your project uses PostgreSQL (database)
via Prisma (database tool). You have 14 data types already.

  A) **Add a new data type**
     New table for this feature, same pattern as other data (created/updated dates).
     → Recommended: keeps things organized like your other data.

  B) **Add to an existing data type**
     New fields on something existing. E.g., "status" field on existing record.
     → Consider if: new info is naturally part of something that already exists.

  C) **Different storage**
     Fast cache (Redis), files, or external service.
     → Consider if: data has different access patterns (expires quickly, temporary).

  D) **Something else**
     How would you like to store the data?

My recommendation: (A) — your project keeps each data type in its own table,
and this data has its own lifecycle separate from what exists.
```

### Dimension 8: API Design

**Format**: Multiple-choice grounded in existing API patterns

```
How should app parts communicate about this feature? You have 12 API endpoints
(URLs the frontend calls) — all following the same pattern.

  A) **New endpoints — same pattern**
     New URLs matching your existing 12-endpoint style, with same input checking.
     → Recommended: consistent, nothing new to learn.

  B) **Add to existing endpoint**
     Extend an existing URL to also handle this feature's data.
     → Consider if: feature is closely related to something with an endpoint.

  C) **Real-time updates (WebSocket or SSE)**
     Live connection for instant updates without refreshing.
     → Consider if: users need changes the moment they happen. Note: new pattern
       for your project.

  D) **Something else**
     How should the app handle this?

My recommendation: (A) — existing pattern works well and team knows it. Unless
users need instant updates, stick with what works.
```

### Dimension 9: Error Handling

**Format**: Multiple-choice with UX implications

```
What should happen when something goes wrong? Your app shows a pop-up (toast)
error with a retry button currently.

  A) **Same as the rest of the app**
     Pop-up error message with retry button, matching other parts of the app.
     → Recommended: users already know how this works.

  B) **Show errors next to the field**
     Check input before submit, highlight what's wrong right next to the field.
     → Consider if: feature has a form where immediate feedback helps fix errors.

  C) **Auto-retry before showing error**
     Quietly retry 1-2 times, only show error if it keeps failing. Show simpler
     page version if unrecoverable.
     → Consider if: involves requests that fail randomly (flaky connection).

  D) **Something else**
     How would you like errors handled?

My recommendation: (A) — consistent with your app. Add per-field checking (B)
only if this has a complex form.
```

### Dimension 10: Migration / Compatibility

**Format**: Multiple-choice with risk assessment (conditional — only when modifying existing features)

```
This changes something that already exists ({ExistingFeature}). How to handle
the switch?

  A) **Add new without changing old**
     Build alongside existing. Users keep old version until they opt into new.
     → Recommended: safest option, nothing breaks for existing users.

  B) **Gradual rollout with toggle**
     Hide behind a switch, enable for small user groups while watching for
     problems. Can turn off instantly if something goes wrong.
     → Consider if: change affects something many users rely on daily.

  C) **Replace old version directly**
     Remove old, everyone gets new version immediately.
     → Consider if: old version has known bugs, clean start makes sense.

  D) **Something else**
     How would you like to handle the transition?

My recommendation: (A) — safest. Only use direct replacement if old version is
actively causing problems.
```

---

## Usage Guidelines

- **Select 6-8 most relevant dimensions** — don't ask all 10
- **Skip dimensions the user already answered** in their initial description
- **Adapt examples** — templates, not scripts. Replace hypothetical context with actual project details
- **Order matters** — Problem & Users first, Migration last
- **Skip forced questions** — better 6 great questions than 10 mediocre ones
- **Track question count** — after 8, start wrapping up; at most 2 more if critical gaps remain
