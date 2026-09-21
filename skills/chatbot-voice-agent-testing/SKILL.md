---
name: chatbot-voice-agent-testing
description: Use when testing chatbots, voice assistants, or conversational AI agents specifically — multi-turn conversation flow, context/memory retention, intent recognition, STT/TTS accuracy, interrupt handling, and fallback behavior. Builds on llm-testing for the underlying model concerns.
license: MIT
metadata:
  category: ai
  version: "2.0"
  tags: chatbot, voice-agent, conversation, intent, stt, tts
---

# Chatbot / Voice / Conversational Agent Testing

## The pipeline to test end-to-end
**Input (text/speech) → intent/NLU → reasoning/planning → tool/API call → response generation → output (text/speech)**. Test each stage in isolation first (does STT transcribe correctly regardless of what the agent does with it?), then the full pipeline — isolating stages tells you *where* a failure lives instead of just *that* the conversation went wrong.

## Multi-turn conversation testing
- **Context retention**: does the agent correctly reference something said 3+ turns earlier? Test with conversations long enough to exceed casual expectations, not just 2-turn exchanges.
- **Context window / memory limits**: what happens when a conversation exceeds the model's context window — does it degrade gracefully (summarize, drop oldest turns intelligently) or does it silently lose critical earlier information (like an established user preference or constraint)?
- **Topic switching**: user abruptly changes subject — does the agent follow naturally, or does it awkwardly force the old topic?
- **Correction handling**: user says "no, I meant X not Y" — does the agent actually update its understanding, or does it repeat the same mistake?
- **Interrupt handling** (voice specifically): user starts speaking while the agent is still responding — does it stop and listen (barge-in), and does it recover the conversation state correctly after being interrupted mid-sentence?

## Intent recognition & entity extraction
- Test with paraphrases of the same intent (people don't say things the same way twice) — a brittle system that only handles the exact training phrasing will fail broadly in production.
- Test entity extraction with ambiguous/malformed input (misspelled city names, informal date references like "next Tuesday," numbers spelled out vs. digits).
- Test **out-of-scope** input explicitly — the agent should recognize when a request is outside its capability and say so, rather than confidently attempting something it can't actually do.

## Fallback & error handling
- When the agent doesn't understand, does it ask a clarifying question or escalate to a human, rather than looping the same "I didn't understand" response or guessing wrong silently?
- Test the actual escalation/handoff path (to a human agent, or a documented fallback) end-to-end, not just that a fallback message exists.
- Test recovery from a bad turn — after a misunderstanding, can the conversation get back on track, or does the whole session degrade?

## Speech-specific testing (STT/TTS)
- **STT accuracy**: test across accents, background noise levels, and domain-specific vocabulary/jargon the generic model wasn't trained on — measure word error rate (WER) on a representative sample, not just clean-studio audio.
- **TTS quality**: pronunciation of domain-specific terms/names, natural pacing, and correct handling of numbers/dates/abbreviations (does it say "dot" or "point" for a decimal appropriately in context?).
- **Latency**: for voice, response latency has a much stricter human-perceptible threshold than text chat — measure time-to-first-audio, not just full-response time.
- **Barge-in and silence handling**: does the system correctly detect end-of-utterance (not cutting the user off mid-sentence, but also not waiting too long after they've finished)?

## Tool-calling / backend integration
Same discipline as [[llm-testing]]'s agent/tool-use section — verify the agent calls the right backend action with correct arguments and handles tool failures without hallucinating a fake success. For a booking/support bot, always verify the claimed backend action (an order placed, a ticket created) actually happened in the system of record, not just that the agent said it did.

## Safety
- Test that the agent refuses/deflects appropriately for out-of-policy requests (medical/legal/financial advice beyond scope, harmful content) consistently across many phrasings, not just the obvious direct ask.
- Test that PII shared mid-conversation (by the user) isn't inappropriately echoed back, logged in plaintext, or leaked to a downstream integration beyond what's necessary.

## Reporting
Log the full conversation transcript (not just the final failing turn) as evidence — conversational bugs are almost always about what happened earlier in the session. See [[bug-reporting]].
