---
name: cross-browser-testing
description: Use when testing across multiple browser engines, operating systems, and viewport dimensions — Chromium, Gecko (Firefox), WebKit (Safari), responsive breakpoints, and engine-specific CSS/JS quirks.
---

# Cross-Browser & Cross-Platform Testing

## Overview
Cross-browser testing verifies that web applications render, function, and perform consistently across different browser rendering engines, operating systems, and device form factors.

## The Core Engine Matrix
Always test across the three fundamental rendering engines:
1. **Blink / V8 (Chromium)**: Google Chrome, Microsoft Edge, Brave, Opera.
2. **Gecko / SpiderMonkey**: Mozilla Firefox.
3. **WebKit / JavaScriptCore**: Apple Safari (macOS & iOS).

## High-Risk Cross-Engine Quirks to Check
- **Safari / WebKit Quirks**:
  - Date parsing: Safari fails on `YYYY-MM-DD HH:MM:SS` (requires ISO-8601 `YYYY-MM-DDTHH:MM:SSZ`).
  - Flexbox & Grid min-height / scroll calculation differences.
  - Form controls styling, datepicker picker popups, and select elements.
  - Audio/Video auto-play restrictions and video codecs (HEVC vs WebM).
- **Firefox / Gecko Quirks**:
  - Scrollbar styling (`scrollbar-width` vs `::-webkit-scrollbar`).
  - SVG sizing inside flex containers.
  - CSS subgrid behavior and font smoothing differences.
- **Mobile Viewport & Touch Quirks**:
  - `100vh` vs dynamic address bar expansion (use `100dvh` / `100svh`).
  - Touch event delays (300ms click delay), pinch-to-zoom scaling bounds.
  - Virtual keyboard appearance pushing layouts or hiding inputs.

## Responsive Breakpoint Matrix
- **Mobile**: 320px (iPhone SE), 375px (iPhone standard), 390px, 412px (Android standard).
- **Tablet**: 768px (iPad portrait), 820px, 1024px (iPad landscape).
- **Desktop**: 1280px (MacBook standard), 1440px, 1920px (Full HD), 2560px (4K/Ultrawide).

## Automation
- Configure Playwright projects to run suites across `chromium`, `firefox`, and `webkit`.
- Use mobile emulation presets: `devices['iPhone 14']`, `devices['Pixel 7']`.
