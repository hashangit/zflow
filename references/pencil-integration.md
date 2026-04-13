# Pencil.dev Integration Reference

How Pencil.dev fits into ZFlow for design-first UI development.

---

## Overview

Pencil.dev provides a visual design canvas that integrates with ZFlow through MCP tools. When a project involves UI work, ZFlow can use Pencil.dev to design, review, and approve interfaces before writing implementation code. This "design-first" approach prevents the common failure mode of agents writing CSS and markup without seeing the result.

Key integration characteristics:
- `.pen` files are JSON and live in the repo (version-controlled like code)
- MCP tools give agents full read/write access to the design canvas
- Design tokens (variables) can be extracted and injected into implementation code
- Screenshots provide visual verification at every stage

---

## How Pencil.dev Fits into ZFlow

Pencil.dev operates as a conditional phase (Phase 3.5) between Review and Implementation. It is triggered only when:
1. The scope includes UI work (`scope.md` has `ui_work: true`)
2. Pencil.dev MCP tools are available (detected at runtime)
3. The user wants to use the design-first flow

Pencil.dev also has touchpoints in the Research phase (surveying existing design systems) and QA phase (visual comparison against designs).

---

## Decision Flow

```
scope.md has ui_work: true?
    |
    +-- No --> Skip to Phase 4 (Implementation)
    |
    +-- Yes --> Check: Pencil.dev MCP tools available?
                |
                +-- Yes --> Full Pencil.dev UI design flow (Phase 3.5)
                |
                +-- No  --> Ask user:
                            "Your scope includes UI work. Pencil.dev enables
                             design-first development with a visual canvas.
                             Would you like to:"
                            [A] Install Pencil.dev and use design-first flow
                            [B] Proceed without it (standard code-first UI)
                            |
                            +-- [A] --> Guide installation --> Full Pencil.dev flow
                            +-- [B] --> Skip Phase 3.5, standard implementation
```

### Availability Detection

The orchestrator detects Pencil.dev availability by checking for `mcp__pencil__` prefixed tools at runtime. The `scripts/check-pencil-availability.sh` script provides a quick check.

If tools like `batch_design`, `get_screenshot`, `set_variables`, `open_document` are present, Pencil.dev is considered available.

---

## MCP Tool Usage Map

### Research Phase

| Tool | Purpose |
|------|---------|
| `get_variables` | Read existing design tokens from `.pen` files |
| `get_guidelines` | Load style archetypes and component guidelines |

### UI Design Phase (Phase 3.5)

| Tool | Sub-Phase | Purpose |
|------|-----------|---------|
| `open_document` | 3.5b Canvas Design | Open or create `.pen` file for the feature |
| `find_empty_space_on_canvas` | 3.5b Canvas Design | Find space on the canvas for new screens/components |
| `batch_design` | 3.5b Canvas Design | Create screens and components on the canvas |
| `set_variables` | 3.5a Design System | Set or update design tokens (colors, typography, spacing) |
| `get_screenshot` | 3.5b/3.5c Design/Review | Present designs to user; review for accessibility |
| `snapshot_layout` | 3.5c Review | Validate layout structure, check for overlaps/clipping |
| `export_nodes` | 3.5c Review | Export approved designs as images for implementation reference |
| `get_guidelines` | 3.5a Design System | Load style archetypes for the project |
| `batch_get` | 3.5c Review | Read design specs for detailed component review |

### QA Phase

| Tool | Purpose |
|------|---------|
| `get_screenshot` | Compare implemented UI against Pencil.dev designs |
| `batch_get` | Read design specs for pixel-level comparison |
| `snapshot_layout` | Check for layout issues in the design reference |

---

## The 3 Sub-Phases of UI Design

### Sub-Phase 3.5a: Design System Setup

**Agent:** `design-system-builder.md`

This sub-phase establishes the design foundation. It runs first, before any canvas design begins.

**Steps:**

1. **Check for existing design system**
   - Read the `ui-system-scout` report from Phase 1 research
   - If the project already has a `.pen` file with design tokens: extract them via `get_variables`
   - If no existing design system: proceed to establish one

2. **Establish design tokens (if new)**
   Work with the user to define:
   - **Color palette:** Primary, secondary, neutral, semantic (success, warning, error, info)
   - **Typography scale:** Font families, sizes (heading levels, body, caption), weights
   - **Spacing system:** 4px/8px grid with named tokens (xs, sm, md, lg, xl)
   - **Component library choice:** Shadcn, custom components, or mixed
   - **Responsive breakpoints:** Mobile, tablet, desktop widths

3. **Set tokens in Pencil.dev**
   - Use `set_variables` to define all design tokens in the `.pen` file
   - Use `get_guidelines` to load style archetypes that match the project's aesthetic
   - Tokens become the source of truth for all subsequent design work

**Output:** Design tokens stored in the `.pen` file, documented in `ui-design-report.md`

### Sub-Phase 3.5b: UI Design on Canvas

**Agent:** `pencil-designer.md`

This sub-phase creates the actual UI designs on the Pencil canvas.

**Steps:**

1. **Open the `.pen` file** via `open_document` (create new if needed)

2. **For each screen/component in the reviewed solution:**
   - Find empty canvas space via `find_empty_space_on_canvas`
   - Design the component using `batch_design` with the established tokens
   - Use design system components (reusable instances via `ref` nodes)
   - Follow the component hierarchy from the reviewed solution

3. **Present to user** via `get_screenshot` for each screen
   - User reviews and provides feedback
   - Agent iterates on the design based on feedback
   - Repeat until the user approves

4. **Capture final layouts** via `snapshot_layout` to verify no overlaps or clipping issues

**Design principles enforced:**
- All values use design tokens (no hardcoded colors or spacing)
- Components are reusable where possible (use `ref` instances)
- Responsive behavior is considered (flexbox patterns, breakpoints)
- Accessibility is considered (contrast ratios, touch targets, text sizing)

**Output:** Screens and components designed on the Pencil canvas

### Sub-Phase 3.5c: Design Review

**Agent:** `ui-review-agent.md`

This sub-phase reviews the designs for quality before they are handed off to implementation.

**Steps:**

1. **Take screenshots** of all designed screens via `get_screenshot`

2. **Review against accessibility criteria:**
   - Contrast ratios meet WCAG 2.1 AA (4.5:1 for text, 3:1 for large text)
   - Touch targets are at least 44x44px
   - Screen reader flow is logical (heading hierarchy, landmark regions)
   - Color is not the only indicator of state

3. **Review against responsiveness:**
   - Layout logic works at all breakpoints
   - No fixed widths that would break on mobile
   - Text truncation is handled gracefully
   - Navigation collapses appropriately

4. **Review against consistency:**
   - All screens use the same tokens
   - Component patterns are consistent across screens
   - No off-system values (colors, sizes, fonts not in the design tokens)

5. **Check for layout issues** via `snapshot_layout`
   - No overlapping elements
   - No clipped content
   - Proper spacing between components

6. **Export approved designs** via `export_nodes`
   - Export as PNG for implementation reference
   - These images are included in the handoff documentation

**Output:** `ui-design-report.md` with design tokens, component specs, screen descriptions, exported images, accessibility requirements, and implementation notes.

---

## Handoff to Implementation

The `ui-design-report.md` serves as the bridge between design and implementation. It contains:

### Design Tokens
All tokens defined in the design system, in a format ready for CSS/implementation:
```json
{
  "colors": {
    "primary": "#3B82F6",
    "primary-hover": "#2563EB",
    "neutral-100": "#F3F4F6",
    "error": "#EF4444"
  },
  "typography": {
    "heading-1": { "font": "Inter", "size": 32, "weight": "bold" },
    "body": { "font": "Inter", "size": 16, "weight": "regular" }
  },
  "spacing": {
    "xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32
  }
}
```

### Component Specifications
For each component, the report includes:
- Name and purpose
- Props/variants
- Layout structure (with Pencil node IDs for reference)
- Design token usage (which tokens are used where)
- Interaction states (hover, focus, active, disabled)
- Responsive behavior

### Screen Descriptions
For each screen:
- Component composition (which components, in what order)
- Layout direction and spacing
- Navigation and flow
- Edge case states (empty, loading, error)

### Implementation Notes
- Priority order for implementation (which components are dependencies)
- Accessibility requirements (ARIA labels, keyboard navigation)
- Animation/transition specifications
- Integration points with non-UI code

---

## UI-Specific Implementation

When Pencil.dev designs exist, the `ui-implementer.md` agent is used instead of the generic `focused-implementer.md`. This agent:

1. Receives the exported screenshots from Phase 3.5
2. Receives the component specifications with exact token values
3. Implements pixel-perfect to the design, using the exact design tokens
4. Uses CSS variables (or equivalent) mapped to the design tokens
5. Implements responsive behavior as specified
6. Implements accessibility requirements as specified

The agent has access to the `.pen` file via MCP tools for reference during implementation.

---

## Graceful Degradation When Pencil.dev Is Not Available

When Pencil.dev is not available and the user declines to install it:

### What Changes

| Aspect | With Pencil.dev | Without Pencil.dev |
|--------|----------------|-------------------|
| Phase 3.5 | Full visual design flow | Skipped entirely |
| Research | ui-system-scout surveys design system | ui-system-scout surveys CSS/component patterns |
| Design (Phase 2) | Standard text-based component specs | Enhanced text-based specs with more detail |
| Implementation | ui-implementer works from visual designs | ui-implementer works from text descriptions |
| QA | ui-visual-qa compares against designs | ui-visual-qa skipped; ux-reviewer covers basics |

### What Stays the Same

- The brainstorm agent still asks about UI requirements
- The design agent still includes interface design in the section-by-section approval
- Implementation agents still receive component specifications (text-based)
- QA still includes UX review and accessibility checks

### Compensating Adjustments

When Phase 3.5 is skipped, the system makes these adjustments:

1. **Design agent (Phase 2)** includes more detailed text-based component specifications:
   - Explicit CSS values (colors, spacing, typography) in the solution document
   - Component hierarchy diagrams (ASCII art)
   - State transition descriptions for interactive components

2. **ux-reviewer (Phase 5)** gets expanded scope:
   - Basic visual consistency checks (consistent spacing, alignment)
   - Accessibility checks (contrast, semantic HTML, keyboard navigation)
   - Responsive behavior verification

3. **ui-visual-qa** is skipped (no design reference to compare against)

---

## Tips for Getting the Best Results with Pencil.dev

1. **Invest time in the design system setup (Sub-Phase 3.5a).** Well-defined tokens make everything downstream smoother. Rush this and you will fight inconsistencies during implementation.

2. **Iterate on designs before approving.** It is much cheaper to change a design on the canvas than to change it in code. Use the review-iterate cycle in Sub-Phase 3.5b fully.

3. **Review the exported screenshots carefully.** These are what the implementation agent will reference. If something looks off in the screenshot, fix it before handoff.

4. **Use design system components (ref nodes) consistently.** This ensures that changes to a component propagate across all screens, just like in code.

5. **Think about responsive behavior during design.** The Pencil canvas can represent layout logic (flexbox directions, wrapping, gaps). Use these features so the implementation agent has clear responsive guidance.

6. **Check the snapshot_layout output.** Layout issues (overlaps, clipping) are much easier to fix in the design phase than in implementation.

7. **Version the `.pen` files.** Since they are JSON, they work with git. If a design needs to change after implementation, you can track the evolution.
