---
name: game-testing
description: Use when testing video games — gameplay/balance, playtesting, performance (FPS, frame pacing, memory), input devices, save/load integrity, multiplayer/netcode, platform certification (TRC/TCR), localization, anti-cheat, monetization, and Unity/Unreal automation.
license: MIT
metadata:
  category: platform
  version: "2.0"
  tags: game-testing, gameplay, playtesting, fps, netcode, multiplayer, unity, unreal, certification, soak
---

# Game Testing

Games combine software correctness with **feel, fairness and fun**. Blend scripted checks, exploratory play and telemetry.

## Test areas
| Area | Focus |
| :--- | :--- |
| **Functionality** | Core loop, progression, quests/scripting triggers, UI/menus, achievements, tutorials, edge-of-map/out-of-bounds, sequence breaks, softlocks |
| **Compatibility** | GPU/driver/OS matrix, consoles/handhelds, controllers, resolutions/aspect ratios (ultrawide), HDR, refresh rates, cloud saves |
| **Performance** | Avg FPS **and 1%/0.1% lows**, frame-time spikes/stutter (shader compile, streaming), load times, VRAM/RAM, thermals on mobile/Deck, battery; soak 4–24 h for leaks (`memory-leak-resource-testing`) |
| **Multiplayer/netcode** | Latency/jitter/packet loss (`clumsy`, `tc netem`), rollback/prediction correctness, desync detection, host migration, matchmaking, lobby/party, NAT traversal, server load, cheating/exploits |
| **Save/load** | Save at every state, corrupt/partial save, versions/migration, cloud conflict, disk full, quit during save |
| **Economy/balance** | Currency sinks/sources, dupe exploits, drop rates statistics, difficulty curve (telemetry), progression pacing |
| **Monetization** | IAP purchase/restore/refund, entitlement sync, parental controls, loot-box odds disclosure (`payment-ecommerce-testing`) |
| **Localization** | Text expansion, fonts/glyph coverage (CJK, Arabic RTL), VO sync, culturally sensitive content, age ratings (`localization-testing`) |
| **Accessibility** | Remappable controls, subtitles, colorblind modes, difficulty options, motion/photosensitivity (Game Accessibility Guidelines; `accessibility-testing`) |
| **Certification** | Platform requirements (Sony TRC, Xbox XR, Nintendo Lotcheck, Steam Deck Verified, Apple/Google store policies): suspend/resume, controller disconnect, account switching, trophies |
| **Audio/visual** | Clipping, z-fighting, LOD pop-in, shader errors, audio ducking/desync (`visual-testing`) |

## Automation
- **Unity**: Test Framework (Edit/Play mode), Unity Test Runner CLI `-runTests -testPlatform PlayMode`, Performance Testing package, AltTester. **Unreal**: Automation System/Gauntlet, Functional Tests, `stat fps/unit`, Unreal Insights. **Godot**: GUT/GdUnit4.
- **Bots/monkey**: random-input agents crawling levels, navmesh-coverage bots, replay-input determinism (record inputs + seed → replay), screenshot diff of known camera points.
- **Smoke per build**: boot → main menu → load level → 60 s play → quit; fail on crash/hang/assert/log-error thresholds, track perf vs baseline.
- **Telemetry & crash**: Sentry/Backtrace symbolicated crashes, funnel and heatmap analytics to find where players quit or die.

## Playtest process
Define goals & questions · recruit target players · observe (don't coach) · think-aloud · capture video+telemetry · rate severity by *player impact*, not code cause · retest fixes; use structured bug titles (`[Level 3][Boss] Player falls through floor after dodge-roll on ramp` + repro save file).

## Bug report extras
Build/CL number, platform/SKU, save file, video clip, coordinates/level, repro rate, network conditions, log & dump (`bug-reporting`).

## Related
`performance-testing`, `compatibility-testing`, `exploratory-testing`, `mobile-testing`, `chaos-resilience-testing`
