---
name: accessibility-testing
description: Use when auditing a web app for accessibility (a11y) — WCAG compliance, screen reader compatibility, keyboard navigation, color contrast, and semantic HTML/ARIA correctness.
---

# Accessibility Testing

## Baseline: WCAG 2.1/2.2 AA
Most legal/compliance requirements target AA. Structure the audit around the four POUR principles:
- **Perceivable** — alt text on images, captions on video, sufficient color contrast, content not conveyed by color alone.
- **Operable** — full keyboard operability, no keyboard traps, visible focus indicators, skip-to-content link, no seizure-inducing flashing.
- **Understandable** — clear labels, consistent navigation, error messages that say how to fix the problem (not just "invalid input").
- **Robust** — valid semantic HTML, correct ARIA usage (or none — wrong ARIA is worse than no ARIA), works across assistive tech.

## Practical audit pass
1. **Automated scan first** (fast, catches ~30-40% of issues): axe-core via browser extension, or Lighthouse's accessibility category (`lighthouse_audit` in Chrome DevTools MCP covers this).
2. **Keyboard-only pass**: unplug the mouse mentally — Tab through the entire page. Every interactive element must be reachable, in a logical order, with a visible focus ring. Modals must trap focus while open and return it on close. Nothing should require a mouse-only gesture (hover-only menus, drag-and-drop with no keyboard alternative).
3. **Screen reader spot-check**: VoiceOver on macOS (Cmd+F5) for at least the primary flow — does it announce meaningful labels, form errors, and dynamic content changes (`aria-live` regions)? Icon-only buttons must have accessible names.
4. **Color contrast**: 4.5:1 for normal text, 3:1 for large text/UI components (AA). Check via browser DevTools contrast checker, not eyeballing.
5. **Forms**: every input has a programmatically associated `<label>`, required fields are announced as required (not just visually marked with an asterisk), errors are associated with their field via `aria-describedby`.
6. **Zoom/reflow**: page usable at 200% browser zoom without horizontal scroll or clipped content.

## Common real bugs to specifically hunt for
- `<div onclick>` instead of `<button>` — not keyboard-focusable, no accessible role.
- Images with `alt=""` on content images (decorative-only pattern misapplied) vs. missing `alt` entirely on meaningful images.
- Custom dropdowns/modals built without ARIA roles/states (`role="dialog"`, `aria-modal`, `aria-expanded`) — screen readers can't tell they exist.
- Placeholder text used as the only label — disappears on focus, not a real label.
- Low-contrast disabled-looking buttons that are actually clickable, or vice versa.

## Reporting
File via [[bug-reporting]], citing the specific WCAG success criterion violated (e.g. "1.4.3 Contrast (Minimum)") — this makes severity/priority unambiguous and ties directly to compliance requirements when they apply.
