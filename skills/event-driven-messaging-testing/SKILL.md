---
name: event-driven-messaging-testing
description: Use when testing message queues and event streams — Kafka, RabbitMQ, SQS/SNS, Pub/Sub, NATS, webhooks — covering schema evolution, ordering, at-least-once delivery, idempotent consumers, dead-letter queues, replay, and eventual consistency.
license: MIT
metadata:
  category: api-backend
  version: "2.0"
  tags: kafka, rabbitmq, sqs, event-driven, dlq, idempotency, schema-registry, webhooks, outbox
---

# Event-Driven & Messaging Testing

Async systems fail **quietly**: messages get lost, duplicated, reordered or poisoned, and the effect shows up minutes later somewhere else.

## Properties to test
| Property | Test |
| :--- | :--- |
| Delivery semantics | Kill consumer mid-processing → message redelivered (at-least-once); no loss |
| **Idempotency** | Deliver same message 2–5× → same end state (dedupe key / upsert) |
| Ordering | Per-partition/key order preserved; consumer tolerant when cross-key order isn't guaranteed |
| Schema evolution | Old consumer + new producer and vice versa (Avro/Protobuf/JSON Schema compat: BACKWARD/FORWARD/FULL) |
| Poison message | Malformed message → retry N → **DLQ**, main flow continues; alert fires |
| Retry/backoff | Transient failure retried with backoff; permanent failure not retried forever |
| Backpressure | Slow consumer → lag metric grows, producers throttled, no OOM |
| Replay | Reprocessing a topic from offset 0 yields same result; side effects guarded |
| Transactional outbox | DB write + event publish atomic (no dual-write gap) |
| Eventual consistency | Read-your-writes UX; poll-until with timeout, never `sleep` |

## Tooling
```bash
docker compose up -d kafka schema-registry            # or Testcontainers
kcat -b localhost:9092 -t orders -P <<< '{"id":1}'     # produce
kcat -b localhost:9092 -t orders -C -o beginning -e    # consume
kafka-consumer-groups --bootstrap-server :9092 --describe --group billing   # lag
rabbitmqadmin list queues name messages_ready messages_unacknowledged
awslocal sqs receive-message --queue-url $Q --max-number-of-messages 10     # LocalStack
```
```java
// Testcontainers Kafka in JUnit 5
@Container static KafkaContainer k = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.6.0"));
```
```python
# wait for effect — never sleep
from tenacity import retry, stop_after_delay, wait_fixed
@retry(stop=stop_after_delay(10), wait=wait_fixed(0.2))
def order_is_shipped(): assert db.get(order_id).status == "SHIPPED"
```

## Contract & schema
Register schemas; CI check `curl -X POST .../compatibility/subjects/orders-value/versions/latest`; consumer-driven contracts for messages (Pact message pacts, `contract-testing`); never remove/rename fields, only add optional ones.

## Webhooks
Signature verification (HMAC), replay window/timestamps, retries with 5xx, out-of-order & duplicate delivery, 2xx-fast + async processing, endpoint idempotency, delivery logs.

## Failure injection
Broker restart · partition rebalance during processing · network partition (`toxiproxy`) · consumer crash after side-effect before ack · duplicate producers · clock skew — see `chaos-resilience-testing`.

## Related
`microservices-testing`, `contract-testing`, `integration-testing`, `observability-testing`, `concurrency-race-condition-testing`
