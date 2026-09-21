---
name: e2e-testing
description: Use when automating end-to-end user journeys through the browser or UI — Playwright, Cypress, user critical paths, resilient locators, session storage, network stubbing, and visual artifacts.
---

# End-to-End (E2E) Testing

## Overview
End-to-End (E2E) testing validates complete user journeys from frontend UI through backend APIs to data storage, simulating real human interactions across realistic browser environments.

## Golden Rules for Resilient E2E Tests
1. **User-Centric Locators**:
   - Priority 1: User-visible roles and text (`getByRole('button', { name: 'Submit' })`, `getByLabel('Email')`).
   - Priority 2: Explicit test IDs (`getByTestId('checkout-total')`).
   - Avoid: Brittle CSS selectors (`div > span:nth-child(3)`), XPath, and class names tied to styling.
2. **Auto-Waiting Over Hard Sleeps**:
   - Never use `sleep(5000)` or arbitrary timeouts.
   - Rely on Playwright/Cypress built-in auto-waiting for element visibility, enablement, and network idle.
3. **Independent Test States**:
   - Every E2E test must start with a clean session. Authenticate via direct API injection (storage state / cookies) rather than logging in through the UI before every single test.
4. **Capture Diagnostic Artifacts on Failure**:
   - Automatically save screenshots, DOM snapshots, video recordings, and browser console/network traces on failure.

## Critical User Paths to Cover
- **Authentication**: Sign up, sign in, OAuth redirects, session expiration, logout.
- **Revenue/Conversion Flows**: Product search, add to cart, checkout, payment processing, invoice confirmation.
- **Data Mutation**: Create resource, edit fields, save, verify persistence after page reload.
- **Error Recovery**: Form validation errors, network failure banner, retry button functionality.

## Tooling
- **Primary**: Playwright (fastest, native multi-tab/multi-context, built-in tracing).
- **Secondary**: Cypress, Selenium WebDriver, Puppeteer.
