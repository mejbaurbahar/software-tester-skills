---
name: exploratory-testing
description: Use when conducting exploratory testing, unscripted bug hunting, and session-based test management — test charters, heuristics (SFDIPOT, Tours), timeboxed sessions, and exploratory debriefing.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: exploratory, sbtm, heuristics, tours, charters
---

# Exploratory Testing

## Overview
Exploratory testing is simultaneous learning, test design, and test execution. It discovers edge-case bugs, usability flaws, and unexpected state combinations that predefined automated tests miss.

## Session-Based Test Management (SBTM)
Conduct exploratory testing in structured, timeboxed sessions (45-90 minutes):
1. **Charter**: Clear scope defining what to explore, with what tools, to discover what risks.
   - Formula: `Explore [target/feature] with [tools/data/methods] to discover [risks/vulnerabilities/bugs]`.
2. **Timebox**: Focus strictly on the charter without distractions.
3. **Session Notes**: Log bugs found, areas covered, questions raised, and test ideas.
4. **Debrief**: Review findings with developers or product managers.

## Proven Exploratory Heuristics
### SFDIPOT (San Francisco Depot)
- **Structure**: What is the application made of? (Files, modules, dependencies)
- **Function**: What does the software do? (Features, calculations, transformations)
- **Data**: What does it process? (Inputs, outputs, boundary values, corrupted data)
- **Interfaces**: How does it interact? (UI, APIs, CLI, webhooks, exports)
- **Platform**: What does it rely on? (OS, browser, hardware, network speed)
- **Operations**: How is it used? (User personas, unusual habits, peak usage)
- **Time**: When does timing matter? (Timeouts, race conditions, concurrency, timezones)

### Testing Tours
- **The Guidebook Tour**: Follow user documentation step-by-step; verify reality matches docs.
- **The Saboteur Tour**: Deliberately disrupt inputs, kill network connections mid-request, supply malformed payloads.
- **The Supermodel Tour**: Focus entirely on visual layout, aesthetics, typography, alignment, and responsiveness.
- **The Intellectual Tour**: Stress the system with complex, highly intricate workflows and heavy calculations.
