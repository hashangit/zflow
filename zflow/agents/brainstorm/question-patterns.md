# Question Patterns — Multiple-Choice Templates & Examples

Templates and examples for the Socratic interviewer agent's brainstorm dimensions.

---

## Plain Language Rules

1. **Use everyday words.** "Database table" not "Prisma model." "Error message shown to the user" not "centralized error handler with toast notification pattern." "Checking user input" not "Zod validation."
2. **Explain terms in context.** "API endpoint (a URL your app calls to get or send data)" or "WebSocket (a way to push updates to the browser instantly)."
3. **Say why a choice matters.** "This determines how fast users see updates" vs. assuming they know why real-time matters.
4. **Describe outcomes, not implementations.** "Users see a small red dot when they have new notifications" vs. "In-app notification badge with session-based persistence."
5. **Keep recommendations short.** "I'd go with (A) because your project already handles this — no new tools needed."

---

## Core Pattern: Multiple-Choice with Explanations

Default format. Every option includes meaning, appropriateness, trade-offs, and grounded recommendation.

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
- Every option references actual project context (file names, existing patterns, tech choices)
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
How will we know this feature is a success? Your app already tracks user
actions with PostHog (your analytics tool), so we can measure things easily.

  A) **People actually use it**
     Users open this new feature at least 3 times per week on average.
     → Recommended: easy to measure with your existing setup, no extra work.

  B) **People get things done faster**
     Users complete their task 30% faster than they do today.
     → Consider if: you can measure how long things take today for comparison.

  C) **Fewer support requests**
     Support tickets related to {area} drop by 50% within a month.
     → Consider if: you already have a ticket category for this problem.

  D) **Something else**
     How would you measure success?

My recommendation: (A) — your analytics tool already tracks what users do,
so we can measure this right away without adding anything new.
```

### Dimension 3: Constraints

**Format**: Multiple-choice with trade-offs

```
Are there any rules or limits we should keep in mind? Based on what your
project uses (Next.js, a PostgreSQL database, and deployed on Vercel):

  A) **No new tools or packages**
     Use only what's already installed. No adding new libraries or services.
     → Recommended: your current setup is solid and well-tested.

  B) **Don't break anything that exists today**
     Everything that works now must keep working. Other apps or systems that
     talk to your app shouldn't notice a change.
     → Consider if: other teams or external apps depend on your app.

  C) **Need it done by a certain date**
     There's a deadline — {N} days. Simplify the first version to meet it.
     → Consider if: there's a specific date or event driving this.

  D) **Something else**
     What constraints do you have?

My recommendation: (A) + (C) — your current tools handle this without
adding anything new, and shipping a simple first version avoids building too
much before getting feedback.
```

### Dimension 4: Scope Boundaries

**Format**: Multiple-choice with MVP cut recommendation

```
What should we include in this first version?

Here are the pieces this feature could have:

  [1] Storing the data (database)
  [2] The behind-the-scenes connections (API)
  [3] An admin page to manage things
  [4] Users actually seeing/using it
  [5] Reports and analytics
  [6] A log of who did what and when

  A) **[1] + [2] only — Just the foundation**
     Set up the data storage and connections. No user-facing parts yet.
     → Recommended: everything else builds on this, so get it right first.

  B) **[1] + [2] + [4] — Users can see it**
     Data storage, connections, and the part users interact with.
     → Consider if: the feature isn't useful unless users can see it.

  C) **[1] + [2] + [3] + [4] — Full feature**
     Everything except reports and the activity log.
     → Consider if: you need an admin page for someone to manage this.

  D) **Something else**
     Pick what you need.

My recommendation: (B) — users need to see and use this for it to have
value. Admin pages and reports can come later.
```

### Dimension 5: Simplest Viable Version

**Format**: Multiple-choice with effort tiers

```
How much should we build in the first version?

  A) **Small — A few days of work**
     Just the basics: a small indicator showing new notifications, and a
     simple list. Notifications disappear when the user closes the browser.
     → Recommended: build the minimum to see if people find it useful,
       then add more later if they do.

  B) **Medium — About a week**
     Notifications stick around between visits (saved in your database).
     Users can mark them as read or unread. A simple notifications page.
     → Consider if: users need to see old notifications when they come back.

  C) **Full — A few weeks**
     Everything: notification preferences, email digests, instant
     delivery (using WebSocket), and a full notification center with
     search and filters.
     → Consider if: this is a core part of your product, not a nice-to-have.

My recommendation: (A) — start small. Ship a simple version first, see if
people use it, then invest in the bigger version if they do.
```

### Dimension 6: UI Work Detection

**Format**: Multiple-choice — always asked

```
Does this feature involve any user interface changes?

  A) **New UI components**
     New pages, sections, or interactive elements the user will see and
     interact with.
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
Where should this feature's data live? Your project stores data in
PostgreSQL (your database) using Prisma (a tool that talks to the database).
You have 14 different data types already.

  A) **Add a new data type**
     Create a new table specifically for this feature, following the same
     pattern your other data uses (with created date, updated date, etc.).
     → Recommended: keeps things clean and organized, like your other data.

  B) **Add to an existing data type**
     Add new fields to something that already exists. For example, adding a
     "status" field to an existing record type.
     → Consider if: the new information is naturally part of something that
       already exists.

  C) **Use a different kind of storage**
     Store it somewhere else — like a fast cache (Redis), files, or an
     external service.
     → Consider if: this data needs to be accessed differently than your
       main data (e.g., it expires quickly or is very temporary).

  D) **Something else**
     How would you like to store the data?

My recommendation: (A) — your project keeps each type of data in its own
table, and this new data has its own lifecycle separate from what exists.
```

### Dimension 8: API Design

**Format**: Multiple-choice grounded in existing API patterns

```
How should the different parts of your app talk to each other about this
feature? Your app has 12 API endpoints (URLs that your frontend calls to
get or send data) — all following the same pattern.

  A) **Add new endpoints — same pattern as the rest**
     Create new URLs for this feature, following the same style as your
     existing 12 endpoints. Includes the same input checking your other
     endpoints use.
     → Recommended: consistent with everything else — nothing new to learn.

  B) **Add to an existing endpoint**
     Extend an existing URL to also handle this feature's data.
     → Consider if: this feature is closely related to something that already
       has an endpoint.

  C) **Real-time updates (WebSocket or SSE)**
     Set up a live connection so updates appear instantly without refreshing.
     WebSocket and SSE are two technologies that push updates to the browser
     as they happen.
     → Consider if: users need to see changes the moment they happen. Note:
       your project doesn't currently use this, so it's a new pattern.

  D) **Something else**
     How should the app handle this?

My recommendation: (A) — your existing pattern works well and the team
already knows it. Unless users specifically need instant real-time updates,
stick with what works.
```

### Dimension 9: Error Handling

**Format**: Multiple-choice with UX implications

```
What should happen when something goes wrong in this feature? Right now,
your app shows a small pop-up message (toast) when there's an error, with
a retry button.

  A) **Same as the rest of the app**
     Show a pop-up error message with a retry button. Same way other parts
     of your app handle errors.
     → Recommended: users already know how this works in your app.

  B) **Show errors next to the relevant field**
     Before the user even submits, check their input and highlight what's
     wrong right next to the field.
     → Consider if: this feature has a form where users type in information,
       and seeing what's wrong immediately would help them fix it faster.

  C) **Try again automatically before showing the error**
     If something fails, quietly try again 1-2 times. Only show the error
     if it keeps failing. Show a simpler version of the page if it can't
     recover.
     → Consider if: this involves internet requests that sometimes fail
       for no good reason (like a flaky connection).

  D) **Something else**
     How would you like errors handled?

My recommendation: (A) — users already know how errors work in your app.
Add the per-field checking (B) only if this feature has a complex form.
```

### Dimension 10: Migration / Compatibility

**Format**: Multiple-choice with risk assessment (conditional — only when modifying existing features)

```
This feature changes something that already exists ({ExistingFeature}).
How should we handle the switch?

  A) **Add the new stuff without changing the old**
     Build the new feature alongside what's there. Users keep using the old
     version until they choose to use the new one.
     → Recommended: safest option. Nothing breaks for existing users.

  B) **Gradual rollout with a toggle**
     Build the new version but hide it behind a switch. Turn it on for
     a few users at a time while watching for problems. Can turn it off
     instantly if something goes wrong.
     → Consider if: this change affects something important that many users
       rely on daily.

  C) **Replace the old version directly**
     Remove the old version and replace it. Everyone gets the new version
     right away.
     → Consider if: the old version has known bugs or causes problems, and
       a clean start makes sense.

  D) **Something else**
     How would you like to handle the transition?

My recommendation: (A) — safest approach. Only use direct replacement if the
old version is actively causing problems.
```

---

## Usage Guidelines

- **Select 6-8 most relevant dimensions** — don't ask all 10
- **Skip dimensions the user already answered** in their initial description
- **Adapt examples** — these are templates, not scripts. Replace hypothetical context with actual project details
- **Order matters** — Problem & Users first, Migration last
- **Skip forced questions** — better 6 great questions than 10 mediocre ones
- **Track question count** — after 8, start wrapping up. If critical gaps remain, ask at most 2 more
