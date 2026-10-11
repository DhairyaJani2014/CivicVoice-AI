"""
response_parser.py
Parses and validates the JSON returned by the AI model. Models do not
always follow the format perfectly, so every step has a safe fallback.
"""

import json

REQUIRED_KEYS = ["issue_type", "description", "urgency", "safety_risk",
                 "confidence", "complaint_subject", "complaint_body"]


def clean_json_text(raw_text: str) -> str:
    """Removes markdown code fences (```json ... ```) if the model added them."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return text.strip()


def parse_response(raw_text: str) -> dict:
    """
    Returns {"ok": True, "data": {...}} on success, or
            {"ok": False, "error": "...", "raw": raw_text} on failure.
    """
    try:
        data = json.loads(clean_json_text(raw_text))
    except (json.JSONDecodeError, TypeError):
        return {"ok": False, "error": "AI response was not valid JSON.", "raw": raw_text}

    if not isinstance(data, dict):
        return {"ok": False, "error": "AI response JSON had an unexpected structure.", "raw": raw_text}

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        return {"ok": False, "error": f"AI response is missing fields: {', '.join(missing)}", "raw": raw_text}

    return {"ok": True, "data": data}