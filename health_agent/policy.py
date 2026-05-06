from dataclasses import dataclass


CRISIS_KEYWORDS = {
    "suicide",
    "kill myself",
    "hurt myself",
    "end my life",
    "self harm",
    "overdose",
}


@dataclass
class PolicyResult:
    safe_reply: str


def classify_input_risk(text):
    lowered = (text or "").lower()
    return "crisis" if any(k in lowered for k in CRISIS_KEYWORDS) else "normal"


def crisis_response_template():
    return (
        "I am really glad you told me. If you might act on these thoughts, "
        "please call 988 right now in the U.S., or your local emergency number. "
        "If possible, move to a safer place and reach out to someone you trust nearby."
    )


def enforce_response_policy(text):
    cleaned = (text or "").strip()
    if not cleaned:
        cleaned = "I am here with you. We can take one slow breath together."
    return PolicyResult(safe_reply=cleaned)
