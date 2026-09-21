---
name: payment-ecommerce-testing
description: Use when testing checkout, payments, carts, coupons, taxes, inventory, orders, refunds, and subscriptions — Stripe/PayPal/Adyen sandboxes, test cards, 3-D Secure, webhooks, idempotency, rounding, PCI scope, and WooCommerce/Shopify flows.
license: MIT
metadata:
  category: domain
  version: "2.0"
  tags: payments, ecommerce, checkout, stripe, paypal, woocommerce, shopify, refunds, subscriptions, pci
---

# Payment & E-commerce Testing

Money paths need the highest rigor: bugs cost revenue, trust and compliance. **Sandbox only — never real cards or live keys in tests.**

## Journey map
Browse → search/filter → PDP (variants, stock) → cart (qty, merge guest→user) → coupon → shipping & tax → payment → confirmation/email → fulfillment → returns/refund → invoices/reports.

## Test-card & sandbox cheat-sheet (Stripe test mode)
| Scenario | Card |
| :--- | :--- |
| Success | `4242 4242 4242 4242` |
| Decline (generic) | `4000 0000 0000 0002` |
| Insufficient funds | `4000 0000 0000 9995` |
| 3-D Secure required | `4000 0027 6000 3184` |
| Fails after 3DS | `4000 0000 0000 3220` (auth fails) |
| Dispute | `4000 0000 0000 0259` |
Use any future expiry/CVC. PayPal: sandbox buyer/seller accounts. Adyen/Braintree: their published test numbers. `stripe listen --forward-to localhost:3000/webhook` + `stripe trigger payment_intent.succeeded` for webhooks.

## Must-cover cases
- **Cart & pricing**: qty limits, out-of-stock race, price changes mid-checkout, rounding (bankers vs half-up, per-line vs total tax), multi-currency & FX, zero-decimal currencies (JPY), free items, bundles.
- **Coupons**: expired, single-use, per-user, stacking rules, min-spend, excluded items, case sensitivity, removal recalculation, race on last redemption (`concurrency-race-condition-testing`).
- **Tax/shipping**: address-based tax, VAT ID B2B exemption, shipping zones/rates, free-shipping threshold, PO boxes.
- **Payment**: success, decline, SCA/3DS, timeout, browser closed mid-payment, back button, double-click Pay → **one charge** (idempotency key), async methods (bank transfer, BNPL, wallets Apple/Google Pay).
- **Webhooks**: signature verified; duplicate/out-of-order events; order state derived from webhook not redirect; missed webhook recovery (reconcile job).
- **Order state machine**: created → paid → fulfilled → refunded/partially refunded/cancelled; illegal transitions rejected (`test-design-techniques`).
- **Refunds/chargebacks**: full/partial, coupon proration, restock, ledger entries balance, email sent.
- **Subscriptions**: trial, proration on upgrade/downgrade, dunning/retries, cancel at period end, pause, card expiry, tax changes.
- **Guest checkout & accounts**: saved cards (tokens only), address book, order history authz (`authn-authz-testing`).
- **Data & compliance**: PAN never logged/stored (PCI SAQ-A via hosted fields/Elements), PII handling, invoices numbering gapless, audit trail (`compliance-testing`).
- **UX**: form validation, autofill, mobile wallets, error messages that let users recover, accessibility of checkout (`accessibility-testing`).
- **Analytics parity**: revenue in analytics = orders DB (`analytics-tracking-testing`).

## Reconciliation (daily)
Payments provider report ↔ orders ↔ ledger ↔ bank: counts and totals per day/currency must tie out; any delta → ticket.

## WooCommerce/Shopify notes
Test with `WP-CLI` seeded products, gateway in test mode, plugin conflicts (cache, security, page-builder) at checkout, block vs classic checkout, webhooks via `wc-api`; Shopify: dev store, checkout extensibility, Functions/discounts, Storefront API rate limits.

## Related
`e2e-testing`, `api-testing`, `security-testing`, `analytics-tracking-testing`, `compliance-testing`
