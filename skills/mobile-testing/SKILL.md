---
name: mobile-testing
description: Use when testing mobile apps (iOS/Android native, or responsive/mobile-web) — device/viewport matrices, touch gesture testing, mobile-specific network and lifecycle conditions, and app-store readiness checks.
license: MIT
metadata:
  category: platform
  version: "2.0"
  tags: mobile, ios, android, touch, viewport, responsive
---

# Mobile Testing

Covers **mobile web** (responsive sites, PWAs) and **native/hybrid apps** (iOS, Android, React Native, Flutter). Mobile bugs are often device-, OS- and network-specific: always record them precisely.

## 1. Responsive / mobile-web
- Test key widths: 360–375 (small phone), 390–430 (modern phone), 768 (tablet portrait), 1024 (tablet landscape), plus the design's real breakpoints. Both orientations.
- Emulate real devices (DevTools device mode, Playwright `devices['iPhone 15']`, BrowserStack/Sauce/LambdaTest real devices) including **user agent, touch events, DPR and CPU/network throttling**, not just a resized window.
- Touch targets ≥ 44×44 pt (Apple) / 48×48 dp (Material); WCAG 2.2 minimum 24×24 CSS px (`accessibility-testing`).
- No hover-only functionality; virtual keyboard doesn't cover fields (`visualViewport`), correct `inputmode`/`autocomplete`/`type` for keyboards; sticky bars vs dynamic address bar (`dvh` units); safe-area insets/notches; pull-to-refresh and scroll-lock behavior.
- Performance on mid-range Android over throttled 4G (`web-performance-testing`); offline/PWA behavior (`pwa-offline-testing`).

## 2. Native app test matrix
Pick a representative spread rather than "everything": oldest supported OS, latest OS, one low-end device (RAM/CPU-constrained), one flagship, a foldable/tablet if supported, small and large screens, and the top devices from your analytics. Use real devices for sensors, camera, biometrics, push, Bluetooth, GPS, thermal and battery behavior; emulators/simulators for fast functional runs.

## 3. What to test
| Area | Cases |
| :--- | :--- |
| **Lifecycle** | Background mid-flow (payment, upload) and resume · force-quit and relaunch (state restore) · low-memory kill · rotation · split-screen/multi-window · app switcher snapshot hides sensitive data |
| **Interruptions** | Incoming call, SMS, notification, alarm, low-battery dialog, OS permission popups, Do Not Disturb, Bluetooth/headphone connect |
| **Network** | Airplane mode mid-request, slow/lossy 3G, Wi-Fi ↔ cellular handover, captive portal, offline queue and sync, timeouts and retry UX (`chaos-resilience-testing`) |
| **Permissions** | Grant **and deny** (and "only this time", approximate location) for camera, mic, location, notifications, contacts, photos; "don't ask again" recovery path via Settings |
| **Push & deep links** | Delivery in foreground/background/killed state, tap routing, badge counts, universal/app links, cold vs warm start |
| **Gestures** | Tap, long-press, swipe, pinch, drag-reorder; accidental-gesture resistance; edge-swipe back gesture conflicts |
| **Install/update** | Fresh install, upgrade from previous **and** older versions (data migration), reinstall, uninstall cleanup, background app refresh |
| **Data & storage** | Local DB migrations, secure storage (Keychain/Keystore), backup/restore, low-disk behavior, logout clears data |
| **Security** | Certificate pinning behavior, no secrets in logs/binaries, jailbreak/root handling, screenshot/recording protection where required, deep-link input validation (`security-testing`) |
| **Accessibility** | VoiceOver/TalkBack, dynamic type/font scaling, contrast, reduced motion, switch control |
| **Localization** | RTL, long strings, locale formats (`localization-testing`) |
| **Battery/perf** | Cold start time, frame rate/jank, memory growth, battery drain, thermal throttling (`memory-leak-resource-testing`) |
| **Payments/IAP** | Store sandbox, restore purchases, refunds, receipt validation (`payment-ecommerce-testing`) |

## 4. Automation
| Tool | Notes |
| :--- | :--- |
| **Appium** (UiAutomator2/XCUITest drivers) | Cross-platform, WebDriver-based |
| **Maestro** | Simple YAML flows, fast to author, good for smoke |
| **XCUITest / Espresso** | Native, fastest and most stable per platform |
| **Detox** | React Native gray-box E2E |
| **Flutter `integration_test`** | Flutter apps |
| Device clouds | BrowserStack, Sauce Labs, AWS Device Farm, Firebase Test Lab |
```yaml
# Maestro flow
appId: com.example.shop
---
- launchApp: { clearState: true }
- tapOn: "Sign in"
- inputText: "qa@example.com"
- assertVisible: "Welcome"
```
```bash
adb shell settings put global airplane_mode_on 1          # Android network toggles
xcrun simctl status_bar booted override --time 9:41       # deterministic iOS screenshots
adb logcat -b crash ; xcrun simctl spawn booted log stream --predicate 'process == "MyApp"'
```

## 5. Release readiness for stores
Store screenshots and metadata match the current UI · privacy labels/data-safety form match real data collection · crash-free sessions ≥ 99.5% on a beta/TestFlight/internal track · staged rollout with halt criteria · store policy checks (permissions justification, IAP rules, background modes) (`release-readiness-testing`).

## Reporting
Always include **device model, OS version, app version/build, network condition, locale, and whether it reproduces on other devices**, plus logs (`adb logcat`, Xcode device logs), screen recording and crash stack. Format: `bug-reporting`.

## Related
`e2e-testing`, `accessibility-testing`, `pwa-offline-testing`, `web-performance-testing`, `compatibility-testing`, `game-testing`
