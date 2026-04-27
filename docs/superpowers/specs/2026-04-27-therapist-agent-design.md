# Therapist-Style Agent Design (Jetson Orin Nano, Fully Local)

Date: 2026-04-27
Project: be-more-agent

## 1. Scope and Goal
Build a fully local, voice-only supportive companion for Jetson Orin Nano (8GB) that:
- Listens after wake word `melvin`
- Holds supportive conversations
- Guides users with safe self-help techniques
- Preserves context only within the active session

Out of scope for v1:
- Clinical diagnosis
- Medication/prescription guidance
- Cross-session personal memory
- Cloud inference

## 2. Target Hardware and I/O
- Device: Jetson Orin Nano 8GB
- I/O: microphone + speaker only
- Interaction mode: wake-word triggered, turn-based voice conversation

## 3. Model and Runtime Stack
- Wake word: local wake-word model configured for `melvin`
- VAD: local voice activity detection for turn boundaries
- STT: `Systran/faster-whisper-small`
- LLM: `naomipeng/gemma2-2b-therapy`
- TTS: Piper (`OHF-Voice/piper1-gpl` runtime)
- Memory: in-RAM session context only

## 4. Conversation and Safety Policy
Allowed behaviors:
- Reflective listening
- Emotional validation
- Gentle reframing
- Grounding and breathing prompts
- Journaling prompts

Disallowed behaviors:
- Diagnosis
- Prescription/medication advice
- Instructions that increase harm

Crisis handling:
- Detect crisis/self-harm language
- Switch to crisis-safe response template
- Encourage immediate contact with local emergency resources/hotline

## 5. End-to-End Data Flow
1. Wake detector listens for `melvin`
2. VAD opens capture window
3. STT transcribes user speech
4. Safety pre-check classifies risk and policy boundaries
5. LLM generates supportive response candidate
6. Safety post-check validates/edits/blocks unsafe response
7. TTS speaks final response
8. Session memory appends turn context in RAM

## 6. Session Memory Rules
- Memory lasts only during the active chat session
- New session starts with empty context
- No disk persistence of user emotional history by default
- Optional manual transcript logging can be added later as explicit opt-in

## 7. Error Handling and Recovery
- STT no-speech/low-confidence: reprompt with short clarification
- LLM failure/timeout: fallback supportive template response
- Safety block: replace output with safe template and continue
- Audio device failure: retry initialization; if still failing, announce error and pause conversation

## 8. v1 Acceptance Criteria
Functional:
- Wake word reliably triggers listening state
- Voice turn loop works fully offline
- Session context influences follow-up answers within a chat
- New chat has no previous context

Safety:
- No diagnosis or prescription output on policy test prompts
- Crisis prompts always produce crisis-safe response template

Performance:
- End-to-end voice turn latency acceptable for natural conversation on Orin Nano 8GB
- Stable operation over extended sessions without memory leaks/crashes

## 9. Validation Plan
Test categories:
- Support quality: empathy, clarity, actionable self-help guidance
- Policy compliance: diagnosis/prescription refusal correctness
- Crisis robustness: consistent safe redirection
- Runtime metrics: transcription time, generation time, total turn latency

Suggested eval set:
- 30 supportive prompts
- 20 boundary/policy prompts
- 10 crisis prompts

Pass/fail:
- 100% pass on policy + crisis gates
- Majority pass on conversational quality rubric
- Latency stays within acceptable interactive threshold for device

## 10. Implementation Notes
- Start with smallest reliable runtime settings to protect latency
- Tune STT chunking/VAD thresholds on live mic data
- Keep responses concise to reduce perceived delay
- Maintain strict separation between policy checks and generation
