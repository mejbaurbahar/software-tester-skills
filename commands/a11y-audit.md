---
description: Audit a page or component for WCAG 2.2 accessibility issues
argument-hint: "[URL or component path]"
---

Audit accessibility of: $ARGUMENTS

Use the `accessibility-testing` skill.

1. Run automated checks first (axe-core, Lighthouse) if available, then do the manual checks automation cannot do: keyboard-only flow, focus order and visibility, screen-reader names/roles, zoom/reflow, contrast, motion.
2. Map each issue to its WCAG success criterion and level.
3. Report: element/selector, issue, user impact, fix (code snippet), severity.
4. Finish with a prioritised fix list and a short list of automated tests to add to CI.
