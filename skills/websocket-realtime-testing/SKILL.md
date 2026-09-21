---
name: websocket-realtime-testing
description: Use when testing WebSockets, Server-Sent Events, Socket.IO, WebRTC signaling, push/live-update features, chat, presence, and collaborative editing — connection lifecycle, reconnect, ordering, backpressure, auth, and scale.
license: MIT
metadata:
  category: api-backend
  version: "2.0"
  tags: websocket, sse, socket.io, realtime, reconnect, backpressure, presence, collaboration
---

# WebSocket & Real-Time Testing

Long-lived, stateful, bidirectional connections break the assumptions of request/response testing.

## Lifecycle checklist
| Phase | Verify |
| :--- | :--- |
| Handshake | Upgrade succeeds; `Origin` validated (CSWSH); auth via token/cookie; wrong/expired token → close code 1008/4401 |
| Open | Server hello/ack; subscribe to channel; permissions per channel |
| Messages | Schema validation; max frame size; binary/text; unicode; ordering per key; duplicates |
| Heartbeat | Ping/pong; idle timeout; proxy/LB timeout (60s traps) |
| Reconnect | Exponential backoff + jitter; resume with last-event-id/offset; no duplicate or lost messages |
| Close | Graceful close codes; server-initiated close; resource cleanup |
| Errors | Malformed JSON; oversized frame; unknown event; flood → rate limit, not crash |

## Tools & snippets
```bash
npx wscat -c wss://stg.example.com/ws -H "Authorization: Bearer $T"
websocat -H="Authorization: Bearer $T" wss://stg.example.com/ws
curl -N -H "Accept: text/event-stream" $URL/events          # SSE
```
```python
# pytest-asyncio + websockets
async def test_echo():
    async with websockets.connect(URL, extra_headers=H) as ws:
        await ws.send(json.dumps({"type":"ping","id":1}))
        msg = json.loads(await asyncio.wait_for(ws.recv(), 2))
        assert msg == {"type":"pong","id":1}
```
Playwright: `page.on('websocket', ws => ws.on('framereceived', ...))` to assert UI reacts to frames; `context.setOffline(true/false)` to test reconnect UX.

## Two-client scenarios (the real bugs)
Client A edits → Client B sees within SLA · presence join/leave · typing indicators · message ordering with concurrent senders · conflict resolution (CRDT/OT: converge to same state) · A goes offline, edits, reconnects → merge · same user, 2 tabs · permissions revoked mid-session → server closes/filters.

## Load & resilience
k6 `ws` module / Artillery: N thousand concurrent sockets, message fan-out latency p95, memory per connection, slow-consumer/backpressure (server buffers bounded?), LB sticky sessions, rolling deploy (drain + reconnect storm), network flaps (`toxiproxy`, `tc netem`).

## Security
Validate Origin; auth on connect *and* on subscribe; per-message authorization; rate-limit; no sensitive data broadcast to wrong rooms (IDOR on channel names); TLS `wss://` only; input sanitization before rendering (XSS via chat).

## Related
`api-testing`, `performance-testing`, `chaos-resilience-testing`, `security-testing`, `e2e-testing`
