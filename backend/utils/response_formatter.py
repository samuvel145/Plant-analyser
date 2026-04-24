"""
Structured output parser for Gemini API responses.
Handles JSON extraction and confidence tier mapping.
"""

import json
import re
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


# Confidence tier mapping
CONFIDENCE_TIERS = [
    (90, "Very High", "green"),
    (75, "High", "light-green"),
    (55, "Moderate", "amber"),
    (35, "Low", "orange"),
    (0, "Very Low", "red"),
]

LOW_CONFIDENCE_DISCLAIMER = (
    "This result has low confidence. Please consult a local "
    "agricultural extension officer for confirmation."
)


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from a Gemini API response.
    Handles cases where JSON is embedded in markdown code blocks or plain text.

    Args:
        response_text: Raw text response from Gemini

    Returns:
        Parsed JSON dict or None if parsing fails
    """
    if not response_text:
        return None

    # Try direct JSON parse first
    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block ```json ... ```
    json_block_pattern = r"```(?:json)?\s*\n?(.*?)\n?\s*```"
    matches = re.findall(json_block_pattern, response_text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue

    # Try finding JSON object pattern { ... }
    brace_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
    matches = re.findall(brace_pattern, response_text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue

    logger.error(f"Failed to parse JSON from response: {response_text[:200]}")
    return None


def parse_confidence(confidence_str: str) -> int:
    """
    Parse confidence percentage string to integer.
    Handles formats like '91%', '91', '~91%'.

    Args:
        confidence_str: Confidence string from Gemini

    Returns:
        Integer percentage (0-100)
    """
    try:
        # Extract digits from the string
        numbers = re.findall(r"\d+", confidence_str)
        if numbers:
            value = int(numbers[0])
            return max(0, min(100, value))
    except (ValueError, IndexError):
        pass
    return 0


def get_confidence_tier(confidence_percent: int) -> Tuple[str, str]:
    """
    Map a confidence percentage to its display tier.

    Args:
        confidence_percent: Integer 0-100

    Returns:
        Tuple of (tier_label, colour)
    """
    for threshold, label, colour in CONFIDENCE_TIERS:
        if confidence_percent >= threshold:
            return label, colour
    return "Very Low", "red"


def format_diagnosis_response(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format raw Gemini vision output into a structured diagnosis response.

    Args:
        raw_data: Parsed JSON from Gemini Vision API

    Returns:
        Formatted diagnosis dict with tier information
    """
    # Check for non-plant error
    if raw_data.get("error") == "not_a_plant":
        return {"error": "not_a_plant"}

    confidence_str = raw_data.get("confidence", "0%")
    confidence_int = parse_confidence(confidence_str)
    tier_label, tier_colour = get_confidence_tier(confidence_int)

    formatted = {
        "plant": raw_data.get("plant", "Unknown"),
        "disease": raw_data.get("disease", "Unable to determine"),
        "confidence": confidence_str,
        "confidence_percent": confidence_int,
        "confidence_tier": tier_label,
        "confidence_colour": tier_colour,
        "symptoms": raw_data.get("symptoms", []),
        "treatment": raw_data.get("treatment", []),
    }

    # Add disclaimer for low confidence
    if confidence_int < 35:
        formatted["disclaimer"] = LOW_CONFIDENCE_DISCLAIMER

    return formatted
