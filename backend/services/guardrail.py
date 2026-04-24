"""
Domain guardrail service using Gemini Flash for topic classification.
Ensures only plant/agriculture-related queries reach the main LLM.
"""

import logging

import google.generativeai as genai

from config import settings
from prompts import GUARDRAIL_PROMPT

logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_guardrail_model():
    """Get a configured Gemini Flash model for fast classification."""
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config={
            "temperature": 0.0,
            "max_output_tokens": 10,
        }
    )


async def is_allowed_topic(user_message: str) -> bool:
    """
    Classify whether a user message is within the allowed agricultural domain.

    Args:
        user_message: The user's text message to classify

    Returns:
        True if the message is plant/agriculture-related (ALLOWED),
        False if it's off-topic (BLOCKED)
    """
    # Allow very short messages like 'hi', 'hello', 'thanks' automatically
    if len(user_message.strip()) <= 15:
        return True

    model = get_guardrail_model()
    prompt = GUARDRAIL_PROMPT.format(user_message=user_message)

    try:
        response = model.generate_content(
            prompt,
            request_options={"timeout": 10}
        )

        if not response.text:
            # If guardrail fails, default to ALLOWED to avoid blocking legitimate queries
            logger.warning("Guardrail returned empty response, defaulting to ALLOWED")
            return True

        result = response.text.strip().upper()
        logger.debug(f"Guardrail classification: '{user_message[:50]}' → {result}")

        return "ALLOWED" in result

    except Exception as e:
        # If the guardrail service fails, default to ALLOWED
        # to prevent blocking users due to API issues
        logger.error(f"Guardrail service error: {str(e)}, defaulting to ALLOWED")
        return True
