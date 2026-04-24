"""
Image utility functions for Base64 encoding and MIME type validation.
"""

import base64
import logging
from typing import Tuple, Optional

from config import settings

logger = logging.getLogger(__name__)

# Allowed MIME types for plant image uploads
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

# Magic bytes for file type detection
MAGIC_BYTES = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG": "image/png",
    b"RIFF": "image/webp",  # WebP starts with RIFF
}


def validate_image(file_content: bytes, content_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an uploaded image file.

    Args:
        file_content: Raw file bytes
        content_type: MIME type from the upload header

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size
    if len(file_content) > settings.max_image_size_bytes:
        return False, f"Image too large. Maximum size is {settings.MAX_IMAGE_SIZE_MB} MB."

    # Check MIME type
    if content_type not in ALLOWED_MIME_TYPES:
        return False, "Unsupported file type. Please upload a JPEG, PNG, or WEBP image."

    # Check empty file
    if len(file_content) == 0:
        return False, "The uploaded file is empty."

    # Verify magic bytes match declared MIME type
    detected_type = detect_mime_type(file_content)
    if detected_type and detected_type != content_type:
        logger.warning(
            f"MIME mismatch: declared={content_type}, detected={detected_type}"
        )
        # Allow it if the detected type is still in allowed list
        if detected_type not in ALLOWED_MIME_TYPES:
            return False, "File content does not match the declared image type."

    return True, None


def detect_mime_type(file_content: bytes) -> Optional[str]:
    """Detect MIME type from file magic bytes."""
    for magic, mime in MAGIC_BYTES.items():
        if file_content[:len(magic)] == magic:
            return mime
    return None


def encode_image_to_base64(file_content: bytes) -> str:
    """Encode raw image bytes to a Base64 string."""
    return base64.b64encode(file_content).decode("utf-8")


def get_gemini_image_part(file_content: bytes, mime_type: str) -> dict:
    """
    Create a Gemini API-compatible image part from raw bytes.

    Args:
        file_content: Raw image bytes
        mime_type: MIME type of the image

    Returns:
        Dict formatted for Gemini API inline_data
    """
    b64_data = encode_image_to_base64(file_content)
    return {
        "inline_data": {
            "mime_type": mime_type,
            "data": b64_data
        }
    }
