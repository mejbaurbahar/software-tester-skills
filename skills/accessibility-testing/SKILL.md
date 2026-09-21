---
name: accessibility-testing
description: Use when auditing a web app for accessibility (a11y) — WCAG compliance, screen reader compatibility, keyboard navigation, color contrast, and semantic HTML/ARIA correctness.
license: MIT
metadata:
  category: web
  version: "2.0"
  tags: accessibility, wcag, axe-core, screen-reader, keyboard, a11y
---

# Accessibility Testing

Target **WCAG 2.2 Level AA** (the basis of most laws: ADA/Section 508, EN 301 549, European Accessibility Act). Automated tools find roughly a third of issues; the rest need keyboard and assistive-technology checks and human judgment.

## Organize by POUR
- **Perceivable:** text alternatives, captions/transcripts, contrast, not color-only, resize/reflow, orientation.
- **Operable:** everything keyboard-operable, no traps, visible and unobscured focus, skip links, adequate target size, no seizure-inducing flashing, alternatives to drag gestures.
- **Understandable:** clear labels and instructions, consistent navigation, helpful errors, no cognitive-test-only authentication.
- **Robust:** valid semantics, correct ARIA (no ARIA is better than wrong ARIA), name/role/value exposed, status messages announced.

**New in WCAG 2.2 (AA):** 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (Minimum, 24×24 CSS px), 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication.

## Audit procedure
1. **Automated scan** on every key page and state (open menus, dialogs, error states):
   ```bash
   npx @axe-core/cli https://staging.example.com --exit
   npx pa11y https://staging.example.com --standard WCAG2AA
   npx lighthouse https://staging.example.com --only-categories=accessibility --output=json
   ```
   ```ts
   // Playwright + axe in CI
   import AxeBuilder from '@axe-core/playwright';
   const results = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag22aa']).analyze();
   expect(results.violations).toEqual([]);
   ```
2. **Keyboard-only pass:** Tab/Shift+Tab through the full page. Everything reachable in a logical order with a **visible** focus indicator; menus/dialogs operable with Enter/Space/Arrows/Esc; modals trap focus and return it on close; no hover-only or drag-only actions; focus not hidden behind sticky headers.
3. **Screen-reader pass** on the primary flow: VoiceOver (macOS/iOS), NVDA or JAWS (Windows), TalkBack (Android). Check that names/roles/states are announced, headings and landmarks give structure, dynamic changes use `aria-live`/`role="status"`, icon buttons have accessible names, and focus moves sensibly after route changes in SPAs.
4. **Visual checks:** contrast 4.5:1 text, 3:1 large text and UI components/focus rings; 200% zoom and 400% reflow without horizontal scroll or clipping; text spacing overrides; Windows High Contrast/forced colors; `prefers-reduced-motion` respected; dark mode contrast.
5. **Forms:** each input has a programmatically associated `<label>`; required state exposed (not just an asterisk); errors are text, associated via `aria-describedby`, and summarized/focused; `autocomplete` tokens set; no placeholder-only labels.
6. **Media & documents:** captions, transcripts, audio descriptions where needed; accessible PDFs (tags, reading order).
7. **Mobile/native:** touch target size, screen-reader gestures, orientation, dynamic type (`mobile-testing`).

## Real bugs to hunt
`<div onclick>` instead of `<button>` · missing/`alt=""` misuse on meaningful images · custom dropdown/modal/tabs without roles/states/keyboard model (follow WAI-ARIA Authoring Practices) · placeholder as only label · disabled-looking clickable controls · focus lost after dynamic updates · positive `tabindex` · reading order differing from visual order · links named "click here" · time limits with no extension · CAPTCHA with no alternative · error messages not announced.

## Reporting and CI
File each issue with the failing **WCAG success criterion** (for example 1.4.3 Contrast), element/selector, user impact, and a code-level fix; severity follows impact on task completion. Add automated checks to CI (axe in E2E, Lighthouse CI budget) and require zero new violations; keep a manual checklist for releases. Produce an accessibility conformance report (VPAT/ACR) when customers ask (`compliance-testing`).

## Related
`usability-testing`, `e2e-testing`, `mobile-testing`, `localization-testing`, `visual-testing`, `compliance-testing`
