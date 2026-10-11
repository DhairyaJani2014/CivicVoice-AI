"""
CivicVoice AI - Civic Issue Reporting Assistant (Core Prototype)
-----------------------------------------------------------------
A citizen provides a photo (or a text description) of a civic issue.
The app classifies the issue with the Gemini API, identifies the
responsible municipal department, and drafts a formal complaint that
the citizen can REVIEW and then submit manually (no auto-submission).

Flow: User -> Application -> Python -> Gemini API -> Processing -> Output

Week 10 - Friday Hands-on Activity - Davine Technologies
Author: Dhairya Jani
"""

import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

from input_handler import validate_input
from prompt_builder import build_prompt
from department_mapper import map_department
from response_parser import parse_response

# ---------------------------------------------------------
# Configuration (API key loaded securely from environment)
# ---------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.6-flash"
MAX_ATTEMPTS = 3
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs", "civic_reports_log.json")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found. Please check your .env file.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)


# ---------------------------------------------------------
# Call the AI model (with retry for temporary API errors)
# ---------------------------------------------------------
def call_gemini(validated: dict) -> dict:
    """Sends the prompt (and image, if any) to Gemini. Returns raw text or an error."""
    if validated["mode"] == "image":
        contents = [
            types.Part.from_bytes(data=validated["image_bytes"], mime_type=validated["mime_type"]),
            build_prompt(),
        ]
    else:
        contents = build_prompt(text_description=validated["text"])

    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=contents)
            return {"ok": True, "text": response.text}
        except Exception as e:
            last_error = str(e)
            # Retry only for temporary overload / rate-limit style errors
            if ("503" in last_error or "429" in last_error) and attempt < MAX_ATTEMPTS:
                print(f"  (AI service busy, retrying attempt {attempt + 1}/{MAX_ATTEMPTS}...)")
                time.sleep(5)
                continue
            break
    return {"ok": False, "error": last_error}


# ---------------------------------------------------------
# Full pipeline for ONE report
# ---------------------------------------------------------
def process_report(user_input: str) -> dict:
    """Validate -> AI call -> parse -> map department. Never raises; always returns a result dict."""
    result = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "input": user_input, "model": MODEL_NAME}

    validated = validate_input(user_input)
    if not validated["valid"]:
        result.update({"status": "invalid_input", "error_message": validated["error"]})
        return result

    ai = call_gemini(validated)
    if not ai["ok"]:
        result.update({"status": "api_error", "error_message": ai["error"]})
        return result

    parsed = parse_response(ai["text"])
    if not parsed["ok"]:
        result.update({"status": "parse_error", "error_message": parsed["error"], "raw_response": parsed["raw"]})
        return result

    data = parsed["data"]
    result.update({
        "status": "success",
        "input_mode": validated["mode"],
        "analysis": data,
        "department": map_department(data["issue_type"]),
        "human_review_required": True,
    })
    return result


# ---------------------------------------------------------
# Logging + display helpers
# ---------------------------------------------------------
def save_to_log(result: dict):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    existing = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = []
    existing.append(result)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)


def display_result(result: dict):
    print("\n" + "-" * 62)
    if result["status"] == "success":
        a = result["analysis"]
        print(f"Issue Type   : {a['issue_type']}  (confidence {a['confidence']}%)")
        print(f"Description  : {a['description']}")
        print(f"Urgency      : {a['urgency']}")
        print(f"Safety Risk  : {a['safety_risk']}")
        print(f"Department   : {result['department']}")
        if a["issue_type"] == "Not a Civic Issue":
            print("\nNo civic issue detected, so no complaint was drafted.")
        else:
            print(f"\nDRAFT COMPLAINT\nSubject: {a['complaint_subject']}\n\n{a['complaint_body']}")
            print("\n>> HUMAN REVIEW REQUIRED: check the draft, fill in [LOCATION], [DATE],")
            print(">> [YOUR NAME], then submit it yourself via your municipal portal/email.")
    elif result["status"] == "invalid_input":
        print(f"Invalid input: {result['error_message']}")
    elif result["status"] == "api_error":
        print("Sorry, the AI service could not be reached right now. Please try again shortly.")
        print(f"(Technical detail: {result['error_message'][:150]})")
    else:
        print(f"Could not understand the AI response: {result['error_message']}")
    print("-" * 62)


# ---------------------------------------------------------
# Main interactive loop
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=" * 62)
    print("CivicVoice AI - Civic Issue Reporting Assistant")
    print("=" * 62)
    print("Enter the path to a photo (e.g. sample_inputs/pothole.jpg)")
    print("OR describe the issue in text. Type 'exit' to quit.\n")

    while True:
        user_input = input("Photo path / description: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        result = process_report(user_input)
        display_result(result)
        save_to_log(result)
        print()