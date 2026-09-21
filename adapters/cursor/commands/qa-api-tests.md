<!-- Generated from commands/api-tests.md by scripts/build_adapters.py - do not edit by hand. -->
# Build an API test suite from an endpoint, OpenAPI spec, or running service

Create API tests for: the text the user typed after this command (ask if none)

Use the `api-testing`, `contract-testing` and `authn-authz-testing` skills (and `graphql-testing` if the API is GraphQL).

1. Locate the spec (OpenAPI/GraphQL schema) or explore the endpoint. Only send requests to systems the user owns or has told you to test; prefer staging.
2. For each operation cover: success, validation errors, auth missing/invalid/expired, authorization per role and object ownership, pagination, filtering, idempotency, rate limits and error format.
3. Validate responses against the schema, not only the status code.
4. Generate runnable tests in the project's existing stack (pytest+requests, Jest+supertest, Playwright request, or Postman/Newman) and run them.
5. Report failures as bugs using the `bug-reporting` skill format.
