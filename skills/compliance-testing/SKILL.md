---
name: compliance-testing
description: Use when testing for regulatory and standards compliance — GDPR/CCPA privacy rights, HIPAA, PCI-DSS, SOC 2, ISO 27001, WCAG/ADA/EAA, audit logging, data retention/deletion, consent, and generating verifiable audit evidence.
license: MIT
metadata:
  category: compliance
  version: "2.0"
  tags: compliance, gdpr, hipaa, pci-dss, soc2, iso27001, privacy, audit-trail, consent, retention, ada
---

# Compliance & Privacy Testing

Compliance = **controls that work + evidence that they worked.** Test the controls; save the proof. (This is engineering testing guidance, not legal advice.)

## Map obligations → testable controls
| Regime | Testable controls |
| :--- | :--- |
| **GDPR / UK GDPR / CCPA-CPRA** | Lawful basis & consent capture; **data-subject rights** (access/export, rectification, erasure, restriction, portability, objection) work end-to-end within 30 days; retention limits; DPA/sub-processor list; breach-notification runbook (72 h); cross-border transfer controls; privacy by default |
| **HIPAA** | PHI encryption at rest/in transit; access controls & unique IDs; audit logs of PHI access; minimum-necessary; BAAs; session timeout; backup/DR (`disaster-recovery-backup-testing`) |
| **PCI DSS 4.0** | No PAN/CVV stored or logged; TLS 1.2+; network segmentation; MFA to CDE; vuln scans/pen tests; logging & retention; secure SDLC |
| **SOC 2 / ISO 27001** | Access reviews, change management evidence (PR + approval + CI), MFA, encryption, logging/monitoring, backups, incident response, vendor mgmt, vulnerability mgmt SLAs |
| **Accessibility (WCAG 2.2 AA, ADA, EN 301 549, EAA)** | Automated + manual + assistive tech audits, VPAT/ACR (`accessibility-testing`) |
| **Sector** | SOX (financial reporting controls), FERPA, COPPA (child data & consent), PSD2 SCA, FDA 21 CFR Part 11 (e-signatures/audit trail) |

## Privacy tests to automate
```text
DSAR export   : create user + data across services → request export → verify ALL stores (DB, search, analytics, backups policy, logs) included, machine-readable
Erasure       : delete user → verify removed/anonymized in DB, search index, cache, object storage, analytics, 3rd-party processors; tombstones for backups; legal-hold exceptions
Consent       : no non-essential cookies/tags before opt-in; withdrawal honored everywhere (analytics-tracking-testing); consent stored with timestamp/version/text
Retention     : records older than policy are purged by job (assert with time travel, date-time-timezone-testing)
Minimization  : API responses & logs contain no unnecessary PII; masking in non-prod (test-data-engineering)
Access logging: every read of sensitive record produces immutable audit entry (who/what/when/why/from where)
```

## Audit-trail testing
Events captured for auth, permission changes, data export/delete, admin actions, config changes; **tamper-evident** (append-only/WORM/hash chain); time-synced (NTP, UTC); include actor, action, target, result, source IP, request ID; retention per regulation; queryable; no secrets in logs.

## Evidence pack (make audits boring)
Automated test run IDs + timestamps · screenshots/exports · config snapshots (`terraform show`) · access-review records · pen-test reports · policy → control → test mapping table (traceability, `test-planning-documentation`) · CI as evidence (branch protection, required reviews, signed commits).

## Continuous compliance
Policy-as-code (OPA/Conftest, Checkov, Cloud Custodian, AWS Config/Security Hub) in CI & runtime; drift alerts; quarterly control tests; track exceptions with expiry.

## Related
`security-testing`, `accessibility-testing`, `authn-authz-testing`, `analytics-tracking-testing`, `disaster-recovery-backup-testing`
