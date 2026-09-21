---
name: seo-testing
description: Use when auditing technical SEO and search visibility — crawlability, indexation, robots.txt, sitemaps, canonical/hreflang, meta and Open Graph tags, structured data (JSON-LD), Core Web Vitals, JS-rendering, redirects, and automating SEO regression checks in CI.
license: MIT
metadata:
  category: web
  version: "2.0"
  tags: seo, technical-seo, structured-data, sitemap, robots, canonical, hreflang, lighthouse, indexing
---

# SEO Testing (Technical SEO QA)

Ship-blocking SEO bugs are cheap to catch pre-release (accidental `noindex`, broken canonicals, blocked JS) and brutal in production. Automate them.

## Crawl & index basics
| Check | Pass condition | How |
| :--- | :--- | :--- |
| `robots.txt` | 200, doesn't block CSS/JS/important paths; lists sitemap; staging blocked by **auth**, not just robots | `curl -s site/robots.txt` |
| XML sitemap | Valid, ≤50k URLs/50 MB, only 200-status canonical indexable URLs, `lastmod` accurate | `xmllint --noout sitemap.xml` |
| Status codes | Indexable pages 200; moved = single-hop 301; removed = 410/404; no soft-404s; no redirect chains/loops | `curl -sI -L -o /dev/null -w "%{http_code} %{num_redirects}\n" URL` |
| Meta robots | No stray `noindex/nofollow` (also `X-Robots-Tag` header) | `curl -sI URL \| grep -i robots` |
| Canonical | Self-referencing absolute URL on indexable pages; consistent with sitemap & hreflang | view-source / crawler |
| Rendering | Critical content & links present in **rendered** DOM (not only after user action); SSR/SSG/prerender for JS apps | Search Console URL Inspection, Playwright `page.content()` |

## On-page
Unique `<title>` (≈50–60 chars) & meta description (≈120–155) · single `<h1>` · logical heading order · descriptive anchor text · image `alt` + width/height + modern formats + lazy-load below fold · internal links ≤3 clicks deep · pagination via crawlable links · faceted URLs controlled (canonical/noindex/robots).

## International
`hreflang` reciprocal (each page lists all alternates + self), valid ISO codes, `x-default`; one language per URL; no auto-redirect by IP that blocks crawlers.

## Social & rich results
Open Graph (`og:title/description/image 1200×630/url/type`), Twitter card, **JSON-LD** structured data valid: `Organization`, `WebSite` + SearchAction, `BreadcrumbList`, `Article`, `Product`, `FAQPage`, `SoftwareSourceCode`. Validate with Google Rich Results Test / Schema.org validator; keep markup matching visible content.

## Performance & UX signals
Core Web Vitals (LCP ≤2.5s, INP ≤200ms, CLS ≤0.1) via Lighthouse/CrUX (`web-performance-testing`) · HTTPS + HSTS · mobile-friendly, no intrusive interstitials · accessibility overlaps (`accessibility-testing`).

## Automation
```bash
npx lighthouse https://example.com --only-categories=seo,performance --output=json --output-path=lh.json --chrome-flags="--headless"
npx unlighthouse --site https://example.com            # whole-site crawl report
screamingfrogseospider --crawl https://example.com --headless --export-tabs "Internal:All"   # if licensed
```
```python
# CI guard: no noindex on prod, canonical present
import requests, re
h = requests.get(URL).text
assert 'noindex' not in re.findall(r'<meta[^>]+robots[^>]*>', h, re.I).__str__()
assert re.search(r'<link[^>]+rel="canonical"', h)
```
Playwright/pytest checks per template: title length, one h1, canonical, JSON-LD parses (`JSON.parse`), OG image 200. Diff sitemap URL count release-over-release.

## Release checklist
Staging `noindex` removed at launch · redirects map tested (old→new, 100% of top URLs) · analytics still firing · robots/sitemap updated · Search Console property verified & sitemap submitted · monitor coverage & CWV for 4 weeks.

## Related
`web-performance-testing`, `accessibility-testing`, `analytics-tracking-testing`, `cross-browser-testing`, `localization-testing`
