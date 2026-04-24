"""
Gemini Vision API wrapper for plant disease image analysis.
"""

import logging
from typing import Dict, Any, Optional

import google.generativeai as genai

from config import settings
from prompts import VISION_ANALYSIS_PROMPT, VISION_ANALYSIS_WITH_MESSAGE_PROMPT
from utils.response_formatter import extract_json_from_response, format_diagnosis_response

logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_vision_model():
    """Get a configured Gemini Vision model instance."""
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.2,
            "top_p": 0.8,
            "max_output_tokens": 2048,
        }
    )


async def analyse_plant_image(
    image_bytes: bytes,
    mime_type: str,
    user_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyse a plant image using Gemini Vision API.

    Args:
        image_bytes: Raw image file bytes
        mime_type: MIME type of the image
        user_message: Optional user description accompanying the image

    Returns:
        Formatted diagnosis dict or error dict

    Raises:
        Exception: If the Gemini API call fails
    """
    model = get_vision_model()

    # Build the prompt
    if user_message:
        prompt = VISION_ANALYSIS_WITH_MESSAGE_PROMPT.format(user_message=user_message)
    else:
        prompt = VISION_ANALYSIS_PROMPT

    # Build the image part
    image_part = {
        "inline_data": {
            "mime_type": mime_type,
            "data": __import__("base64").b64encode(image_bytes).decode("utf-8")
        }
    }

    try:
        logger.info("Sending image to Gemini Vision API for analysis...")

        # Generate content with image + prompt and fallback support
        from utils.gemini_client import execute_with_fallback
        response = execute_with_fallback(
            model.generate_content,
            [prompt, image_part],
            request_options={"timeout": 30}
        )

        # Check for safety blocks
        if not response.text:
            logger.warning("Gemini Vision returned empty response (possible safety block)")
            return {"error": "safety_blocked"}

        logger.debug(f"Gemini Vision raw response: {response.text[:300]}")

        # Parse the JSON response
        parsed = extract_json_from_response(response.text)

        if parsed is None:
            logger.error("Failed to parse Gemini Vision response as JSON")
            return {"error": "parse_error"}

        # Format and return the diagnosis
        return format_diagnosis_response(parsed)

    except Exception as e:
        logger.error(f"Gemini Vision API error: {str(e)}")
        raise
