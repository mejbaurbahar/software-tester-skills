---
name: iot-embedded-testing
description: Use when testing IoT devices, firmware and embedded systems — hardware-in-the-loop, simulators/emulators, MQTT/BLE/Zigbee/LoRa protocols, OTA updates, power/battery, sensor edge cases, constrained resources, connectivity loss, and device fleet security.
license: MIT
metadata:
  category: platform
  version: "2.0"
  tags: iot, embedded, firmware, hil, mqtt, ble, ota, edge, fleet, real-time
---

# IoT & Embedded Systems Testing

Constraints (memory, power, connectivity, real-time deadlines) and the physical world make failure modes different — and recall costly. Test on **host → emulator → hardware-in-the-loop → field.**

## Test levels
| Level | What | Tools |
| :--- | :--- | :--- |
| Host unit (x86) | Business logic compiled natively, HAL mocked | Unity/CMock, Ceedling, GoogleTest, CppUTest, Rust `#[test]` |
| Simulation/emulation | Firmware on virtual MCU/board | QEMU, Renode, Wokwi, Zephyr `native_sim`, Arm FVP |
| **HIL** | Real board + rigs (relays, signal generators, sensors) | pytest + pyserial/`pyocd`, Robot Framework, Labgrid, OpenOCD/JTAG, Saleae logic analyzer |
| Integration | Device ↔ gateway ↔ cloud | MQTT broker (Mosquitto), device shadow/twin tests, LocalStack IoT |
| System/field | Real environment, fleet pilots | Staged OTA rings, telemetry dashboards |

## Behavior checklist
- **Sensors**: out-of-range, stuck-at, noise/spikes, drift, calibration, missing sensor, debouncing, sampling jitter, ADC saturation.
- **Real-time**: deadlines met under worst-case load; interrupt latency; priority inversion; watchdog resets & recovery; stack/heap high-water marks (`memory-leak-resource-testing`).
- **State & power**: cold boot, warm reset, brownout, power loss mid-flash-write (config not corrupted), sleep/wake current (µA budget), battery curve at temperature, low-battery behavior.
- **Connectivity**: offline buffering & backpressure, reconnect with backoff, QoS 0/1/2 semantics, retained/LWT messages, clock without NTP, NAT/firewall, cellular roaming, BLE pairing/bonding & range, Wi-Fi provisioning failure paths.
- **OTA updates**: signed images verified; A/B partitions with **automatic rollback** on failed boot; power cut mid-update; downgrade protection; delta updates; staged rollout; version skew between device and cloud API.
- **Protocols**: fuzz parsers (`fuzz-testing`), malformed frames, MTU limits, endianness, CRC failures, duplicate/out-of-order packets.
- **Security**: secure boot chain, debug ports (JTAG/UART) locked, unique device identity/keys (no shared secrets), TLS with cert pinning/rotation, encrypted flash/secrets, least-privilege services; supply-chain SBOM (`supply-chain-dependency-testing`); aligned to ETSI EN 303 645 / IEC 62443 / OWASP IoT Top 10.
- **Environmental**: temperature/humidity, EMI, vibration (lab/certification).
- **Fleet**: 1 → 10k devices: registration storms, thundering-herd reconnect after outage, config drift, telemetry cost, remote diagnostics, decommission & data wipe.

## Example: HIL test with pytest
```python
def test_bootloader_rolls_back_on_bad_image(dut, relay, fw_bad):
    dut.flash(fw_bad); relay.power_cycle()
    dut.wait_for("Rollback to slot A", timeout=20)
    assert dut.version() == "1.4.2"
```
MQTT smoke: `mosquitto_sub -h $B -t 'dev/+/telemetry' -v` while `mosquitto_pub` simulates commands.

## Related
`chaos-resilience-testing`, `security-testing`, `performance-testing`, `event-driven-messaging-testing`, `installation-upgrade-testing`
