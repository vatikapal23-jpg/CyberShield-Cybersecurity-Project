"""Transparent educational message-risk screening. Heuristic scores are not probabilities."""
import re
from urllib.parse import urlparse

RULES = [
    ("Urgency or threat", 2, r"\b(urgent|immediately|within \d+ hours?|account will be blocked|final warning|act now|last chance|legal action)\b"),
    ("Credential or OTP request", 4, r"\b(password|passcode|otp|one[- ]time password|pin|cvv|card number|login credentials)\b"),
    ("Money transfer or payment pressure", 3, r"\b(transfer money|send money|pay now|processing fee|release fee|pay a fee|upi pin|refund fee|gift card)\b"),
    ("Impersonation / authority pressure", 3, r"\b(police|cbi|customs|court|digital arrest|arrest warrant|income tax officer|bank officer|government officer)\b"),
    ("Prize / too-good-to-be-true claim", 2, r"\b(you have won|winner|prize money|guaranteed returns|double your money|free iphone|lottery)\b"),
    ("Remote access request", 4, r"\b(anydesk|teamviewer|remote access|screen sharing app|install this app to fix)\b"),
    ("Suspicious attachment language", 2, r"\b(enable macros|invoice\.exe|open the attached|urgent invoice|unknown attachment|install this apk)\b"),
    ("Suspicious link wording", 2, r"\b(click here|verify your account|update kyc|suspended account|reset your password here|claim refund)\b"),
    ("Secrecy / anti-verification", 3, r"\b(do not tell anyone|keep this confidential|don't disconnect|do not contact your bank|do not call the police)\b"),
    ("Sensitive identity information request", 3, r"\b(aadhaar|social security number|passport number|date of birth|bank details|identity document)\b"),
    ("Recruitment / job fee", 2, r"\b(job offer|work from home|registration fee|training fee|recruitment fee|pay to get hired)\b"),
    ("Crypto / investment lure", 2, r"\b(crypto investment|trading signal|guaranteed profit|risk-free investment|wallet seed phrase|recovery phrase)\b"),
]

def _extract_urls(text: str):
    # This extracts text-shaped URLs only; it does not visit or reputation-check them.
    found = re.findall(r"(?i)\b(?:https?://|www\.)[^\s<>'\"]+", text or "")
    return [u.rstrip(".,);!?]") for u in found]

def analyze_message(text: str):
    text = text or ""
    lowered = text.lower()
    score = 0
    signals = []
    for name, weight, pattern in RULES:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            score += weight
            signals.append({"signal": name, "points": weight})
    urls = _extract_urls(text)
    for url in urls:
        candidate = url if url.lower().startswith(("http://", "https://")) else "http://" + url
        try:
            host = urlparse(candidate).hostname or ""
        except ValueError:
            host = ""
        if host and (host.replace(".", "").isdigit() or host.startswith("xn--") or host.count("-") >= 2):
            score += 2
            signals.append({"signal": "URL has an unusual textual host pattern (manual review needed)", "points": 2})
            break
    score = min(score, 20)
    if score >= 9:
        level = "High"
        advice = "Do not click links, open attachments, pay, or share information. Verify independently using an official app/site or a known phone number."
    elif score >= 4:
        level = "Elevated"
        advice = "Pause and verify the sender through a separate trusted channel. Never share OTPs, PINs, passwords, or recovery phrases."
    elif score >= 1:
        level = "Caution"
        advice = "Review the message carefully. The score is only a heuristic; legitimate messages can trigger rules and scams can avoid them."
    else:
        level = "No rule triggered"
        advice = "No configured text rule matched. This does not mean the message is safe; verify unexpected requests independently."
    return {
        "score": score,
        "level": level,
        "signals": signals,
        "urls_found": urls,
        "advice": advice,
        "disclaimer": "Heuristic indicator score, not a probability or a definitive verdict. No links are opened and no external lookup is performed."
    }
