"""
input_handler.py
Validates user input (image path or text description) before anything is
sent to the AI API. Catching bad input here avoids wasting API requests.
"""

import os
from PIL import Image

VALID_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
MAX_IMAGE_SIZE_MB = 10
MIN_TEXT_LENGTH = 10


def looks_like_image_path(user_input: str) -> bool:
    """True if the input ends with an image-like extension."""
    return user_input.lower().endswith(VALID_IMAGE_EXTENSIONS)


def validate_input(user_input: str) -> dict:
    """
    Returns a dict:
      {"valid": True,  "mode": "image", "image_bytes": ..., "mime_type": ...}
      {"valid": True,  "mode": "text",  "text": ...}
      {"valid": False, "error": "<clear message for the user>"}
    """
    if user_input is None or not user_input.strip():
        return {"valid": False, "error": "Input is empty. Please enter an image path or describe the civic issue."}

    user_input = user_input.strip().strip('"').strip("'")

    # ---------- Image mode ----------
    if looks_like_image_path(user_input):
        if not os.path.exists(user_input):
            return {"valid": False, "error": f"Image file not found: '{user_input}'. Please check the path."}

        size_mb = os.path.getsize(user_input) / (1024 * 1024)
        if size_mb > MAX_IMAGE_SIZE_MB:
            return {"valid": False, "error": f"Image is too large ({size_mb:.1f} MB). Maximum allowed is {MAX_IMAGE_SIZE_MB} MB."}

        # Confirm the file is a genuine, readable image (not just renamed)
        try:
            with Image.open(user_input) as img:
                img.verify()
        except Exception:
            return {"valid": False, "error": "File could not be read as a valid image. It may be corrupted or not a real image."}

        ext = os.path.splitext(user_input)[1].lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}

        with open(user_input, "rb") as f:
            image_bytes = f.read()

        return {"valid": True, "mode": "image", "source": user_input,
                "image_bytes": image_bytes, "mime_type": mime_map[ext]}

    # ---------- Text mode ----------
    if len(user_input) < MIN_TEXT_LENGTH:
        return {"valid": False, "error": f"Description is too short. Please write at least {MIN_TEXT_LENGTH} characters, or provide an image path."}

    return {"valid": True, "mode": "text", "source": "text description", "text": user_input}