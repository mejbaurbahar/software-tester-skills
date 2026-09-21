---
name: installation-upgrade-testing
description: Use when testing software installation, upgrade, downgrade, uninstall and packaging — installers (MSI/DMG/DEB/RPM/Docker/Helm/npm/pip), silent installs, permission and disk edge cases, data/config preservation across versions, rollback, and version-skew.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: installation, upgrade, uninstall, packaging, rollback, docker, helm, msi, deb, version-skew
---

# Installation, Upgrade & Uninstall Testing

First and last impressions of your product happen in the installer. Use **clean VMs/containers with snapshots** for every run.

## Matrix
Fresh install · upgrade N-1→N (and N-2, LTS→latest) · **skip-version upgrade** · downgrade/rollback · repair/reinstall · uninstall/purge · side-by-side versions · per-user vs system-wide · air-gapped/offline · silent/unattended · interrupted install (kill, power loss) · re-run same installer (idempotent).

## Checklist
| Area | Verify |
| :--- | :--- |
| Prereqs | Missing/old runtime (JRE/.NET/glibc/OpenSSL) → clear error; disk space check; OS/arch support (x64/arm64) |
| Permissions | Non-admin/non-root behavior, UAC/sudo prompts, SELinux/AppArmor, file ownership & modes (no world-writable) |
| Paths | Spaces/unicode/long paths, custom install dir, network drive, read-only FS |
| Integrity | Checksums/signatures verified (`sha256sum -c`, `gpg --verify`, `cosign verify`), SBOM shipped, no debug symbols/secrets |
| Config & data | Existing config preserved (three-way merge), migrations run once & atomically, backup created before upgrade, user data untouched |
| Services | Daemon/service registered, starts on boot, ports free/conflict handling, health check passes |
| Upgrade | In-flight jobs/connections drained; DB schema forward + **backward compatible during rolling update**; cache/session invalidation; rollback path tested |
| Uninstall | Removes binaries, services, PATH/registry, shortcuts; **keeps or prompts on user data**; no orphan processes |
| Docs & UX | Install guide commands actually work copy-paste; progress, errors and logs actionable; exit codes (`cli-testing`) |

## Automation recipes
```bash
# Debian package in a clean container
docker run --rm -v $PWD:/pkg debian:12 bash -c 'apt-get update -qq && apt-get install -y /pkg/app_2.0.0_amd64.deb && app --version && apt-get purge -y app && test ! -e /usr/bin/app'
# Upgrade path matrix
for from in 1.8.0 1.9.3 2.0.0-rc1; do ./install.sh $from && seed_data && ./install.sh 2.0.0 && ./verify_data.sh; done
# Helm
helm lint chart/ && helm template chart/ | kubeconform -strict -summary
helm upgrade --install app chart/ --atomic --wait --timeout 5m && helm rollback app 1
# Windows silent
msiexec /i App.msi /qn /l*v install.log ; msiexec /x App.msi /qn
# npm/pip package sanity
npm pack && npm i -g ./pkg-1.0.0.tgz && pkg --version ; python -m venv v && v/bin/pip install dist/*.whl && v/bin/python -c "import pkg"
```
Docker image: non-root user, minimal base, healthcheck, reproducible tags, `docker run` with read-only FS, multi-arch manifests, image scan (`iac-container-security-testing`).

## Failure injection
Kill installer at 10/50/90%, fill disk, revoke network mid-download, corrupt package, expire cert, pre-existing conflicting version, locked files/running app → expect **atomic result: fully old or fully new**, never half-installed.

## Related
`compatibility-testing`, `desktop-app-testing`, `data-migration-testing`, `cloud-infrastructure-testing`, `release-readiness-testing`
