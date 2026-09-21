---
name: localization-testing
description: Use when verifying internationalization (i18n) and localization (l10n) — string truncation, pseudo-localization, Right-to-Left (RTL) layout rendering, date/time/currency formatting, and UTF-8 encoding.
---

# Localization (l10n) & Internationalization (i18n) Testing

## Overview
Localization (l10n) testing ensures that software adapts seamlessly to different languages, cultures, and geographic regions without functional breakage, visual truncation, or data corruption.

## Core Verification Areas
1. **Visual Layout & Text Expansion**:
   - Translations frequently expand by 30% to 50% compared to English (e.g. German, French, Finnish).
   - Verify buttons, cards, table columns, and navigation bars do not clip or wrap awkwardly.
2. **Bidirectional & Right-to-Left (RTL) Support**:
   - Test RTL languages (Arabic, Hebrew, Persian, Urdu).
   - Layouts must flip horizontally (`dir="rtl"`): navigation, icons with directionality, chevrons, and alignment.
   - Text with mixed LTR/RTL (e.g. English brand name in an Arabic sentence) must render in correct reading order.
3. **Character Encoding & Multi-Byte Support**:
   - Verify UTF-8 end-to-end (database, API headers, frontend rendering).
   - Test with non-Latin scripts (Chinese, Japanese, Korean, Cyrillic, Greek), accented characters (é, ü, ñ, ø), and emojis.
4. **Locale-Specific Formatting**:
   - **Dates**: `MM/DD/YYYY` (US) vs `DD/MM/YYYY` (UK/EU) vs `YYYY-MM-DD` (ISO/Asia).
   - **Numbers & Currencies**: `$1,234.56` (US) vs `1.234,56 €` (DE/FR).
   - **Timezones**: Verify correct calculation across daylight saving transitions and UTC conversions.
5. **Pseudo-Localization (Pseudo-loc)**:
   - Use pseudo-localization tools to replace English characters with accented versions and expand length:
     - Example: `[!!! Ṗřǿḓŭƈťş !!!]`
   - Instantly exposes hardcoded strings (untranslated) and layout truncation before translations arrive.
