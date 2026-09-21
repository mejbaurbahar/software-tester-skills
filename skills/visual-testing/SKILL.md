---
name: visual-testing
description: Use when checking visual/layout correctness — screenshot/visual regression testing, design-system and Figma-to-production validation, responsive layout, dark mode/theming, typography and spacing consistency. Distinct from functional correctness or accessibility (though related).
---

# Visual & UX Testing

## Visual regression testing
- Capture baseline screenshots of key screens/components at known states (empty, populated, error, loading) and compare against new builds pixel-by-pixel or via perceptual diff.
- Set a **sensible diff threshold** — pixel-perfect comparison breaks on anti-aliasing/font-rendering noise across environments; use a perceptual diff tolerance instead of exact match.
- Mask/ignore known-dynamic regions (timestamps, ads, randomized content, animations) so they don't cause false-positive diffs every run.
- Run against a **consistent rendering environment** (same OS/browser/font set, typically headless Chrome in CI) — cross-machine font rendering differences are the #1 source of visual-regression flakiness.
- Triage every flagged diff as: intentional change (update baseline), real regression (file it), or noise/flake (fix the test's stability, don't just approve blindly).

## Playwright visual testing
```
await expect(page).toHaveScreenshot('checkout.png', { maxDiffPixelRatio: 0.01 });
```
Store baselines in version control alongside the test; review baseline updates in PR diffs like code changes, since an unreviewed baseline update can silently hide a real regression.

## Design-system / Figma-to-production validation
- Compare implemented spacing, typography scale, color tokens, and component states (hover/focus/disabled/error) against the design system spec, not just "looks about right."
- Check that design tokens (colors, spacing, radii) are actually consumed from the shared token source in code, not hardcoded ad hoc values that will drift over time.
- Verify every documented component state was actually implemented — hover/focus/active/disabled/loading/error are each a separate thing to check, not just the default state.

## Responsive & layout testing
- Test at real breakpoints, not just "resize until it looks broken" — use the design's documented breakpoints if specified.
- Check for horizontal scroll/clipped content at each breakpoint, especially with long/translated text (a string that fits in English can overflow in German or Bangla — see localization note below).
- Test with browser text-size zoom (not just viewport resize) since some users zoom text independently.

## Dark mode / theming
- Every themed surface — not just top-level pages — check modals, tooltips, charts, and third-party embedded widgets, which commonly get missed in a dark-mode pass.
- Check contrast in *both* themes independently — a combination that passes contrast in light mode can fail in dark mode with the same relative colors.
- Verify theme persists correctly across navigation/reload and doesn't flash the wrong theme on load (FOUC).

## Localization/internationalization visual impact
- Text expansion: German/Finnish/Russian strings run 30-50% longer than English on average — verify UI doesn't clip/overlap.
- RTL languages (Arabic, Hebrew/Bangla context-dependent) — verify layout actually mirrors, not just text direction, and that icons/directional cues (arrows, progress indicators) are appropriately flipped or intentionally not flipped.
- Verify date/number/currency formatting matches locale, not hardcoded to one format.

## Tools
- Playwright/Cypress built-in screenshot comparison, Percy, Chromatic (Storybook-integrated), Applitools (AI-assisted visual diffing with more tolerance for legitimate rendering noise).
- Chrome DevTools MCP / Claude in Chrome `take_screenshot` + `resize_page`/`emulate` for ad hoc manual checks without a full visual-regression pipeline.

## Reporting
Attach both the baseline and the diff image, not just the new screenshot — see [[bug-reporting]]. For contrast/ARIA-adjacent findings, cross-file with [[accessibility-testing]] rather than duplicating.
