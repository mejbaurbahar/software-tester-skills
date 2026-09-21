---
name: iac-container-security-testing
description: Use when testing Infrastructure-as-Code and container configuration — Terraform/CloudFormation/Helm/Kubernetes scanning (Checkov, tfsec, KICS, kube-linter), policy-as-code (OPA/Conftest/Kyverno), Dockerfile lint (hadolint), image scanning (Trivy), CIS benchmarks, and drift detection.
license: MIT
metadata:
  category: security
  version: "2.0"
  tags: iac, terraform, kubernetes, docker, helm, opa, conftest, kyverno, checkov, trivy, cis-benchmark, policy-as-code
---

# IaC & Container Configuration Testing

Misconfiguration is a leading cause of cloud incidents. Shift it left: **test infrastructure definitions like code, before they are applied.**

## Pipeline: lint → scan → policy → plan-test → runtime
```bash
terraform fmt -check && terraform validate && tflint
checkov -d . --framework terraform,kubernetes,dockerfile,helm
trivy config --severity HIGH,CRITICAL .
terraform plan -out tf.plan && terraform show -json tf.plan > plan.json
conftest test plan.json -p policy/                     # OPA/Rego on the plan
helm template chart | kubeconform -strict -            # schema validation
kube-linter lint k8s/ ; kubescape scan framework nsa k8s/
hadolint Dockerfile
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 myapp:1.2.3
```

## Checklist by layer
| Layer | Verify |
| :--- | :--- |
| Cloud IAM | No wildcard actions/principals, root protected with MFA, roles over users, short-lived credentials |
| Network | No world-open admin/DB ports, data in private subnets, restricted egress, TLS everywhere |
| Storage & DB | Encryption at rest, public access blocked, versioning, backups (`disaster-recovery-backup-testing`), access logging |
| Secrets | Not in Terraform variables/state/env in plain text; secret manager in use; state backend encrypted and locked |
| Logging | Audit logs enabled, immutable, alerting on IAM/root changes |
| Kubernetes | Non-root, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop capabilities, no privileged/hostPath/hostNetwork, resource limits, default-deny NetworkPolicy, Pod Security `restricted`, least-privilege RBAC |
| Images | Minimal/distroless base, pinned digest, non-root `USER`, no secrets in layers, multi-stage build, SBOM + signature (`supply-chain-dependency-testing`) |
| Dockerfile | No `latest`, `COPY` over `ADD`, `HEALTHCHECK`, no `sudo`/ssh |

## Policy-as-code example (Rego)
```rego
package terraform.s3
deny[msg] {
  r := input.resource_changes[_]
  r.type == "aws_s3_bucket_public_access_block"
  r.change.after.block_public_acls == false
  msg := sprintf("%s must block public ACLs", [r.address])
}
```
Enforce the same rules at admission with Kyverno or Gatekeeper (`require-non-root`, `disallow-latest-tag`, `require-resource-limits`). **Test the policies too:** `opa test policy/ -v`, `kyverno test .`.

## Test infrastructure behaviour, not just config
Terratest, `terraform test` or Pulumi tests: create ephemeral infra, assert outputs and reachability, destroy. Add **drift detection** (`terraform plan -detailed-exitcode` nightly) and idempotency (second apply = no changes).

## Triage
Suppress only with an inline reason, owner and expiry (`#checkov:skip=CKV_AWS_18:reason`). Prioritise internet-exposed, data-bearing, privileged resources.

## Related
`cloud-infrastructure-testing`, `supply-chain-dependency-testing`, `security-hardening`, `compliance-testing`, `configuration-feature-flag-testing`
