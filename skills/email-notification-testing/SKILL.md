---
name: email-notification-testing
description: Use when testing transactional/marketing email, SMS, push and in-app notifications — capture inboxes (Mailpit, MailHog, Mailosaur), rendering across clients, links/tokens, SPF/DKIM/DMARC deliverability, unsubscribe/consent, timing, retries, and localization.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: email, notifications, sms, push, mailpit, deliverability, dkim, spf, dmarc, unsubscribe
---

# Email, SMS & Notification Testing

Notifications are user-visible, legally regulated, and easy to break silently. Never test against real customers' addresses.

## Capture, don't send
| Need | Tool |
| :--- | :--- |
| Local SMTP sink + UI/API | **Mailpit** (`docker run -p 8025:8025 -p 1025:1025 axllent/mailpit`), MailHog |
| Hosted, CI-friendly inboxes | Mailosaur, Mailtrap, Testmail, Ethereal |
| SMS | Twilio test credentials/magic numbers, provider sandbox |
| Push | Firebase/APNs sandbox; emulator/simulator receipts |
```bash
curl -s localhost:8025/api/v1/messages | jq '.messages[0] | {Subject, To, Created}'
curl -s localhost:8025/api/v1/search?query="subject:Reset" | jq '.messages_count'
```
```ts
// Playwright: request reset, read link from Mailpit, complete flow
await page.getByRole('button', {name:'Send reset link'}).click();
const msg = await (await request.get('http://localhost:8025/api/v1/message/latest')).json();
const link = msg.Text.match(/https?:\/\/\S+\/reset\S+/)[0];
await page.goto(link);
```

## What to verify
- **Trigger**: sent once per event (no duplicates, no missing); correct recipient (To/Cc/Bcc); sender name/address; reply-to.
- **Content**: subject/preheader, personalization tokens (no `{{name}}` leaks; fallback when missing), currency/date/locale formatting, plain-text alternative, RTL, long names, emoji.
- **Links & tokens**: correct environment domain; tracking params; magic links single-use, expire, bound to user; unsubscribe works without login and is honored within 10 days (CAN-SPAM) — immediately is better.
- **Rendering**: Litmus/Email on Acid or Playwright screenshots; dark mode; Outlook (Word engine) tables; image blocking + alt text; mobile width ≤ 600px; size < 102 KB (Gmail clipping).
- **Deliverability**: SPF, DKIM, DMARC pass (`dig TXT`, mail-tester.com, Google Postmaster); `List-Unsubscribe` + One-Click header; bounce/complaint webhooks suppress addresses; warm-up; no spammy content.
- **Timing & retries**: send delay SLA; queue outage → retried, not lost; time-zone aware scheduling; quiet hours; rate limits/digest batching.
- **Preferences & consent**: opt-in/out per channel/category, double opt-in, GDPR/PECR consent records; transactional mail still sent to unsubscribed users only if truly transactional.
- **Security**: no secrets/passwords in email; header injection (`\r\n` in name/subject); HTML injection; account-existence not leaked by "we sent an email" messaging.
- **Multi-channel**: SMS length/segments (GSM-7 vs UCS-2), opt-out keywords (STOP/HELP), short-code compliance; push permissions denied path, deep-link routing, badge counts.

## Related
`functional-testing`, `localization-testing`, `security-testing`, `compliance-testing`, `test-data-engineering`
