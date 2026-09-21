---
name: serverless-testing
description: Use when testing serverless and cloud-function architectures — AWS Lambda, Azure Functions, Cloud Functions/Run, event sources, cold starts, timeouts and retries, IAM least privilege, idempotency, local emulation (SAM, LocalStack, Functions Core Tools), and testing in the cloud.
license: MIT
metadata:
  category: platform
  version: "2.0"
  tags: serverless, lambda, azure-functions, cloud-functions, cold-start, localstack, sam, idempotency, event-sources, iam
---

# Serverless Testing

Business logic is small; the risk lives in **configuration, permissions, events and integrations**. Emulators never fully match the cloud, so test at more than one level.

## Strategy
| Level | What | Tooling |
| :--- | :--- | :--- |
| Unit | Handler logic with the event as plain data; ports/adapters keep SDK calls behind interfaces | Jest/pytest, `aws-sdk-client-mock`, `moto` |
| Local integration | Function + emulated services | LocalStack, SAM CLI (`sam local invoke`), Azure Functions Core Tools + Azurite, Firebase Emulator Suite |
| **Cloud integration** | Deploy an ephemeral stack per PR, hit real services | CDK/SAM/Serverless Framework/Terraform, unique stack name per branch, destroy afterwards |
| Contract | Event and API schemas between producers and consumers | JSON Schema, EventBridge schema registry, Pact (`contract-testing`) |
| E2E / synthetic | Full flow via the public entry point | `production-monitoring-synthetic-testing` |

```bash
sam local invoke OrderFn -e events/order-created.json
sam local start-api & curl localhost:3000/orders
awslocal lambda invoke --function-name OrderFn --payload fileb://event.json out.json
```
```python
def test_handler_is_idempotent(dynamodb_table):
    evt = load("sqs_order_created.json")
    handler(evt, None); handler(evt, None)          # SQS may deliver twice
    assert dynamodb_table.scan()["Count"] == 1
```

## Checklist
- **Events**: one test event per trigger shape (API Gateway, SQS, SNS, S3, EventBridge, Kinesis, Blob/Queue). Batch events with partial failures (`batchItemFailures`); malformed/oversized payloads; duplicate and out-of-order delivery (`event-driven-messaging-testing`).
- **Idempotency & retries**: at-least-once delivery means duplicates. Use idempotency keys (Powertools idempotency), DLQs with alarms, retry/backoff limits; poison messages don't loop forever.
- **Timeouts & limits**: function timeout < upstream timeout (API Gateway 29 s), visibility timeout ≥ 6× function timeout for SQS, memory sizing, payload limits (6 MB sync), `/tmp` size, concurrency limits and throttling behaviour (429s).
- **Cold starts**: measure p95/p99 with and without provisioned concurrency; init code outside the handler; package size; VPC/ENI impact; test after deploy and after idle.
- **IAM least privilege**: each function's role allows only required actions/resources — test that a denied action really fails (negative tests) and scan policies (`iac-container-security-testing`).
- **Config & secrets**: env vars validated at init; secrets from Secrets Manager/Key Vault with caching; no secrets in logs.
- **State**: functions are stateless — no reliance on in-memory or `/tmp` state across invocations; connection reuse and pool exhaustion on databases (use RDS Proxy/pooling).
- **Observability**: structured logs with correlation IDs, X-Ray/OpenTelemetry traces across async hops, metrics and alarms on errors, throttles, iterator age, DLQ depth (`observability-testing`).
- **Cost guards**: recursive-invocation protection, concurrency caps, budget alarms; load test for cost per 1k invocations (`scalability-capacity-testing`).
- **Deploy safety**: aliases + weighted traffic shifting (CodeDeploy canary), rollback on alarm, backward-compatible event schemas.

## Pitfalls
Only mocking the cloud SDK (misses IAM, permissions, resource config) · testing only the handler, not trigger configuration · ignoring duplicate deliveries · assuming ordering · not testing throttling.

## Related
`microservices-testing`, `event-driven-messaging-testing`, `cloud-infrastructure-testing`, `api-testing`, `chaos-resilience-testing`
