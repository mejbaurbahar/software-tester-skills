---
name: desktop-app-testing
description: Use when testing desktop applications — Electron, Tauri, WPF/WinForms, Qt, macOS/Cocoa, GTK — covering UI automation (Playwright for Electron, WinAppDriver, pywinauto, Appium Mac2), installers/auto-update, OS integration, permissions, multi-monitor/DPI, and crash reporting.
license: MIT
metadata:
  category: platform
  version: "2.0"
  tags: desktop, electron, tauri, wpf, qt, macos, windows, installer, auto-update, ui-automation
---

# Desktop Application Testing

## Automation options
| App type | Tool |
| :--- | :--- |
| Electron | Playwright `_electron.launch()`, Spectron (deprecated) → Playwright/WebdriverIO |
| Tauri | `tauri-driver` + WebDriver, WebdriverIO |
| Windows (WPF/WinForms/UWP/Win32) | WinAppDriver, FlaUI, **pywinauto**, Appium Windows driver, UI Automation |
| macOS native | XCUITest, Appium Mac2 driver, AppleScript/`osascript` + Accessibility API |
| Qt | Squish, Qt Test / QtQuickTest (`qt-qml-test`) |
| Cross-platform image-based fallback | SikuliX / pyautogui (brittle — last resort) |

```ts
// Playwright + Electron
import { _electron as electron } from '@playwright/test';
const app = await electron.launch({ args: ['.'], env: { ...process.env, APP_ENV: 'test' } });
const win = await app.firstWindow();
await expect(win.getByRole('heading', {name: 'Projects'})).toBeVisible();
const isPackaged = await app.evaluate(({ app }) => app.isPackaged);
await app.close();
```

## Desktop-specific checklist
- **Install / upgrade / uninstall**: clean VM snapshot; per-user vs all-users; silent flags (`/S`, `msiexec /qn`); PATH/registry/launch-agent entries; **leftover files after uninstall**; upgrade preserves settings; downgrade blocked or safe (`installation-upgrade-testing`).
- **Signing & security**: code-signed + notarized (macOS Gatekeeper `spctl -a -vv`), SmartScreen reputation, hardened runtime/entitlements; Electron: `contextIsolation`, `nodeIntegration:false`, CSP, no remote content w/ Node access, safe `shell.openExternal`.
- **Auto-update**: staged rollout, signature verification, rollback on failure, offline/blocked update server, delta updates, update while app running.
- **OS integration**: file associations, deep links/URI schemes, drag-and-drop, clipboard, tray/menu bar, notifications, autostart, single-instance lock, sleep/wake, lock screen, network change.
- **Permissions**: macOS TCC prompts (camera, mic, files, accessibility), Windows UAC/firewall, sandbox/entitlements; graceful denial.
- **Display**: HiDPI/scaling 100–300%, multi-monitor, dock/undock, window restore position, dark/light theme, high-contrast, font scaling.
- **Filesystem**: paths with spaces/unicode/long paths (>260 on Windows), network drives, read-only dirs, case sensitivity, permission denied, disk full, file locking, atomic saves & crash recovery (autosave).
- **Performance/resources**: cold start time, idle CPU/RAM (Electron baseline), memory growth over hours (`memory-leak-resource-testing`), battery impact, GPU fallback.
- **Crash & telemetry**: crash reporter (Sentry/Crashpad) uploads symbolicated dumps with consent; safe mode on repeated crash.
- **Accessibility**: screen readers (Narrator/NVDA/VoiceOver), keyboard-only, UIA/AX properties (`accessibility-testing`).
- **Compat matrix**: OS versions × architectures (x64/arm64/universal) × locales.

## CI
Windows/macOS runners; xvfb on Linux (`xvfb-run -a npm test`); record video/trace on failure; test packaged build, not just dev mode.

## Related
`test-automation`, `installation-upgrade-testing`, `compatibility-testing`, `accessibility-testing`, `security-testing`
