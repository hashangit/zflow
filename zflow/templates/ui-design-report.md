# UI Design Report

> Produced by ZFlow Phase 3.5: UI Design.
> Input: reviewed-solution.md + design tokens + Pencil canvas designs.
> This document is the visual design handoff for implementation.

## Template Guidance

This template provides a recommended structure. Sections marked **Required** must
be present — downstream phases depend on them. Sections marked **Expected** should
be present unless you note a reason for omission. Sections marked **Optional** are
suggestions — include, restructure, or omit as the task demands. Produce output
proportional to complexity.

---

---

## Design System

### Color Tokens

| Token Name | Value | Usage |
|------------|-------|-------|
| {color-primary-500} | {#hex} | Primary actions, links, branding |
| {color-primary-600} | {#hex} | Primary hover states |
| {color-secondary-500} | {#hex} | Secondary actions |
| {color-neutral-50} | {#hex} | Page backgrounds |
| {color-neutral-900} | {#hex} | Primary text |
| {color-success-500} | {#hex} | Success states |
| {color-warning-500} | {#hex} | Warning states |
| {color-error-500} | {#hex} | Error states |
| {color-info-500} | {#hex} | Info states |

{Continue for all color tokens.}

### Typography Tokens

| Token Name | Value | Usage |
|------------|-------|-------|
| {font-family-sans} | {font stack} | Body text |
| {font-family-mono} | {font stack} | Code, monospace content |
| {font-size-xs} | {12px} | Captions, labels |
| {font-size-sm} | {14px} | Secondary text |
| {font-size-base} | {16px} | Body text |
| {font-size-lg} | {18px} | Subheadings |
| {font-size-xl} | {20px} | Section titles |
| {font-size-2xl} | {24px} | Page titles |
| {font-weight-normal} | {400} | Body text |
| {font-weight-medium} | {500} | Emphasized text |
| {font-weight-semibold} | {600} | Subheadings |
| {font-weight-bold} | {700} | Headings |

{Continue for all typography tokens.}

### Spacing Tokens

| Token Name | Value | Usage |
|------------|-------|-------|
| {spacing-1} | {4px} | Tight gaps |
| {spacing-2} | {8px} | Inline element gaps |
| {spacing-4} | {16px} | Standard padding |
| {spacing-6} | {24px} | Section gaps |
| {spacing-8} | {32px} | Major section gaps |

{Continue for all spacing tokens.}

### Component Library

- **Library**: {name (e.g., Shadcn/UI, Radix, custom)}
- **Base components available**: {list}
- **Custom components defined**: {list}

---

## Component Specifications

### {Component 1 Name}

- **Description**: {What this component does}
- **Tokens used**:
  - Colors: {list token names}
  - Typography: {list token names}
  - Spacing: {list token names}
  - Radius: {list token names}
- **States**:
  - Default: {description}
  - Hover: {description}
  - Active/Pressed: {description}
  - Focus: {description}
  - Disabled: {description}
  - {Other states as needed}
- **Responsive behavior**:
  - Desktop: {layout/behavior}
  - Tablet: {layout/behavior}
  - Mobile: {layout/behavior}

### {Component 2 Name}

{Same structure as above.}

{Continue for each component.}

---

## Screen-by-Screen Layouts

### {Screen 1 Name}

- **Purpose**: {What this screen is for}
- **Route/URL**: {If applicable}
- **Layout description**: {Describe the layout structure in words.
  What is the visual hierarchy? Where do key elements sit?}

#### Desktop Layout (1440x900)
- **Canvas node ID**: {node_id}
- **Exported image**: `exports/{screen-name}-desktop.png`
- **Layout**:
  - Header: {description}
  - Main content: {description}
  - Sidebar (if any): {description}
  - Footer (if any): {description}

#### Tablet Layout (768x1024)
- **Canvas node ID**: {node_id}
- **Exported image**: `exports/{screen-name}-tablet.png`
- **Changes from desktop**: {what changes}

#### Mobile Layout (375x812)
- **Canvas node ID**: {node_id}
- **Exported image**: `exports/{screen-name}-mobile.png`
- **Changes from tablet**: {what changes}

#### Interactions
| Interaction | Trigger | Response |
|-------------|---------|----------|
| {Action} | {User does X} | {Visual/system response} |

### {Screen 2 Name}

{Same structure as above.}

{Continue for each screen.}

---

## Implementation Notes

### Per-Component Implementation Guidance

#### {Component 1 Name}
- **Code location**: {suggested file path}
- **Framework pattern**: {e.g., React functional component with hooks}
- **Design tokens to import**: {list}
- **Responsive strategy**: {CSS approach: flex, grid, media queries, container queries}
- **Animation notes**: {if any transitions or animations are designed}
- **Accessibility notes**: {ARIA roles, labels, keyboard behavior}

#### {Component 2 Name}

{Same structure.}

{Continue for each component.}

### General Implementation Guidance
- **CSS approach**: {Tailwind classes / CSS Modules / Styled Components / etc.}
- **Token import method**: {how to import and use the design tokens in code}
- **Responsive approach**: {mobile-first / desktop-first / container queries}
- **Testing recommendations**: {visual regression, accessibility testing tools}

---

## Accessibility Requirements

### Contrast Compliance
- All text meets WCAG AA (4.5:1 for normal text, 3:1 for large text)
- Known edge cases: {list any borderline contrast situations and the exact ratios}

### Keyboard Navigation
- All interactive elements are keyboard accessible
- Focus order follows visual layout order
- Focus indicators are visible (specify: {outline style})

### Screen Reader Support
- {List ARIA labels needed}
- {List landmark roles}
- {List any live regions for dynamic content}

### Touch Targets
- All interactive elements meet 44x44px minimum
- {List any exceptions with justification}

### Motion & Animation
- {Any animations defined}
- `prefers-reduced-motion`: {how animations are handled}

---

## Design Review Results

- **Screens reviewed**: {N}
- **Screens approved**: {N}
- **Issues found**: {N} (Critical: {N}, Major: {N}, Minor: {N})
- **All critical/major issues resolved**: {Yes/No}

---

## Exported Files

| Screen | Breakpoint | File |
|--------|-----------|------|
| {Screen 1} | Desktop | `exports/{screen}-desktop.png` |
| {Screen 1} | Tablet | `exports/{screen}-tablet.png` |
| {Screen 1} | Mobile | `exports/{screen}-mobile.png` |

{Continue for all screens and breakpoints.}
