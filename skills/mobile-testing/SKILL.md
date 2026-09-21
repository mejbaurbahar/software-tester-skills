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

## Responsive/mobile-web testing (most common in this harness)
- Use Chrome DevTools MCP `emulate`/`resize_page` or Claude in Chrome to test key breakpoints: 375px (small phone), 414px (large phone), 768px (tablet), plus the actual design breakpoints if known.
- Check touch target size (min ~44×44px) — mouse-precision UI often ships touch targets too small to tap reliably.
- Check for hover-dependent functionality that has no touch equivalent (tooltips, hover menus).
- Test both orientations (portrait/landscape) if the app doesn't lock orientation.
- Test with the mobile viewport's actual user-agent, not just a resized desktop window — some sites serve different code paths by UA.

## Native app testing (iOS/Android)
- **Device/OS matrix**: pick a representative spread — oldest supported OS version, newest, one low-end device (perf-constrained), one high-end. Don't test only on the simulator/emulator; real-device testing catches sensor, permissions-dialog, and performance issues simulators miss.
- **Lifecycle testing**: backgrounding mid-flow (payment, upload) and resuming, force-quit and relaunch (state restore correctness), low-memory termination behavior, incoming call/notification interruption.
- **Network conditions**: airplane mode mid-request, flaky/slow 3G simulation, switching wifi→cellular mid-session — does the app recover gracefully or lose state/crash?
- **Permissions**: test both grant and deny paths for every permission (camera, location, notifications, contacts) — deny path is the one that gets skipped and ships broken.
- **Push notifications**: delivery, deep-linking from a notification tap, badge count accuracy.
- **App update path**: test upgrading from the previous released version (migrations, cached data compatibility), not just fresh installs.

## Touch gesture testing
- Tap, long-press, swipe (all directions where relevant), pinch-zoom, double-tap-zoom, drag-and-drop reorder.
- Accidental-gesture resistance: does a scroll accidentally trigger a swipe-to-delete? Does a slightly-off tap on an adjacent element misfire?

## App store readiness (if shipping to stores)
- Screenshots/metadata match current UI (stale store screenshots are a common rejection/complaint source).
- Privacy manifest / data-collection disclosures match what the app actually collects.
- Crash-free session rate from a beta/TestFlight build before submitting.

## Reporting
Always include exact device model, OS version, app version/build number, and network condition in the report — mobile bugs are frequently device/OS-specific and unreproducible without this. Use [[bug-reporting]].
