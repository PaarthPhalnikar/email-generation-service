# guardrails.py
from typing import Tuple, List
from email_schemas import EmailRequest, EmailResponse


class GuardrailError(Exception):
    """Hard failure – stop pipeline."""


class GuardrailWarning(Warning):
    """Soft warning – you may log or flag but still continue."""


def check_input_guardrails(req: EmailRequest) -> List[str]:
    """
    Returns list of warnings. Raises GuardrailError if input is invalid.
    """
    warnings: List[str] = []

    # 1. Length check
    if len(req.user_input.strip()) < 10:
        raise GuardrailError("Input too short. Please provide more context.")

    text = req.user_input.lower()

    # 2. Disallowed content (very simple example; you can expand)
    blocked_keywords = ["kill", "suicide", "bomb"]
    if any(k in text for k in blocked_keywords):
        raise GuardrailError("Input contains disallowed or unsafe content.")

    # 3. Soft warnings
    if "refund" in text:
        warnings.append("Refund-related emails should be reviewed manually.")
    if "legal advice" in text or "lawsuit" in text:
        warnings.append("Legal topics should be reviewed by a qualified professional.")

    return warnings


def check_output_guardrails(email: EmailResponse) -> List[str]:
    """
    Returns list of warnings. Raises GuardrailError if output is invalid.
    """
    warnings: List[str] = []
    body_l = email.body.lower()

    # 1. Basic sanity
    if len(email.body) < 30:
        warnings.append("Email body is very short; check if it has enough detail.")

    # 2. Avoid hard guarantees
    risky_phrases = ["guarantee", "100% certain", "no risk"]
    if any(p in body_l for p in risky_phrases):
        warnings.append("Avoid hard guarantees; may cause compliance issues.")

    # 3. Legal/compliance category stricter
    if email.category == "legal":
        if "this is legal advice" in body_l:
            warnings.append("Remove explicit legal advice wording; add disclaimer.")

    return warnings
