"""
prompt_builder.py
Builds the reusable prompt template sent to the AI model.
The model is told to pick from a FIXED list of issue types so the
department mapper can work deterministically.
"""

ISSUE_TYPES = [
    "Pothole",
    "Garbage",
    "Streetlight",
    "Drainage",
    "Water Leakage",
    "Other Civic Issue",
    "Not a Civic Issue",
]


def build_prompt(text_description: str = None) -> str:
    """
    Builds the instruction prompt. If a text description is given it is
    included; otherwise the model is told to analyze the attached image.
    """
    if text_description:
        source_block = f'The citizen described the issue in text:\n"""\n{text_description}\n"""'
    else:
        source_block = "The citizen attached a photo of the issue. Analyze the photo."

    issue_list = ", ".join(f'"{t}"' for t in ISSUE_TYPES)

    return f"""
You are CivicVoice AI, an assistant that helps citizens report civic issues
(like potholes, garbage, broken streetlights, drainage problems) to the
correct municipal authority.

{source_block}

Tasks:
1. Classify the issue. "issue_type" MUST be exactly one of: [{issue_list}].
   If the input is not a civic problem (e.g. a selfie, food, a pet), use "Not a Civic Issue".
2. Briefly describe what is visible or described (do not invent details).
3. Rate urgency as "Low", "Medium" or "High" based on public safety risk.
4. Give a confidence score from 0 to 100 for your classification.
5. Draft a formal, polite complaint. IMPORTANT: do NOT invent specific facts
   such as the exact location, date, or the citizen's name. Use the
   placeholders [LOCATION], [DATE] and [YOUR NAME] instead.

Respond ONLY with valid JSON in exactly this format, and nothing else:
{{
  "issue_type": "<one of the allowed values>",
  "description": "<1-2 sentence factual description>",
  "urgency": "<Low | Medium | High>",
  "safety_risk": "<short note on the public safety risk>",
  "confidence": <number 0-100>,
  "complaint_subject": "<one-line subject for the complaint>",
  "complaint_body": "<formal complaint letter body, 4-6 sentences, using the placeholders>"
}}
"""