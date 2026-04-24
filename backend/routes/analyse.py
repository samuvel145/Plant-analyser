"""
API route for plant image analysis — POST /api/analyse
"""

import asyncio
import logging
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from models.response_models import DiagnosisResponse, DiagnosisData, GuardrailResponse
from services.session_manager import session_manager
from services.gemini_vision import analyse_plant_image
from utils.image_utils import validate_image
from prompts import NON_PLANT_IMAGE_MESSAGE, IMAGE_SAFETY_MESSAGE

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/analyse")
@router.post("/analyse")
async def analyse_image(
    image: UploadFile = File(..., description="Plant/leaf image (JPEG, PNG, WEBP)"),
    session_id: str = Form(..., description="UUID v4 session identifier"),
    message: Optional[str] = Form(None, description="Optional accompanying note"),
):
    """
    Upload a plant image for AI-powered disease detection.
    Returns a structured diagnosis with plant, disease, confidence, symptoms, and treatment.
    """
    # Get or create session
    session = session_manager.get_or_create_session(session_id)

    # Rate limit check
    if not session.check_rate_limit():
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment before trying again."
        )

    # Image upload limit check
    if not session.can_upload_image():
        raise HTTPException(
            status_code=429,
            detail="Maximum image uploads per session reached. Please start a new session."
        )

    # Read image content
    image_content = await image.read()
    content_type = image.content_type or "application/octet-stream"

    # Validate image
    is_valid, error_msg = validate_image(image_content, content_type)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Add user message to chat history
    if message:
        session.add_message("user", f"[Uploaded an image] {message}")
    else:
        session.add_message("user", "[Uploaded an image for analysis]")

    # Increment image count
    session.increment_image_count()

    try:
        # Call Gemini Vision API with timeout
        result = await asyncio.wait_for(
            analyse_plant_image(image_content, content_type, message),
            timeout=30
        )
    except asyncio.TimeoutError:
        logger.error(f"Gemini Vision API timed out for session {session_id}")
        raise HTTPException(
            status_code=504,
            detail="Analysis is taking longer than usual. Please try again."
        )
    except Exception as e:
        logger.error(f"Gemini Vision API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"DEBUG ERROR: {str(e)} | Type: {type(e).__name__}"
        )

    # Handle non-plant image
    if result.get("error") == "not_a_plant":
        session.add_message("assistant", NON_PLANT_IMAGE_MESSAGE)
        return GuardrailResponse(
            session_id=session_id,
            message=NON_PLANT_IMAGE_MESSAGE
        )

    # Handle safety block
    if result.get("error") == "safety_blocked":
        session.add_message("assistant", IMAGE_SAFETY_MESSAGE)
        return GuardrailResponse(
            session_id=session_id,
            message=IMAGE_SAFETY_MESSAGE
        )

    # Handle parse error
    if result.get("error") == "parse_error":
        error_msg = "Could not parse the AI response. Please try uploading again."
        session.add_message("assistant", error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

    # Store diagnosis in session
    session.set_diagnosis(result)

    # Build diagnosis summary for chat history
    diagnosis_summary = (
        f"**Diagnosis Complete**\n"
        f"🌱 Plant: {result['plant']}\n"
        f"🦠 Disease: {result['disease']}\n"
        f"📊 Confidence: {result['confidence']} ({result.get('confidence_tier', '')})\n"
        f"Symptoms: {', '.join(result.get('symptoms', []))}\n"
        f"Treatment: {'; '.join(result.get('treatment', []))}"
    )
    session.add_message("assistant", diagnosis_summary)

    # Return structured response
    return DiagnosisResponse(
        session_id=session_id,
        data=DiagnosisData(
            plant=result["plant"],
            disease=result["disease"],
            confidence=result["confidence"],
            symptoms=result.get("symptoms", []),
            treatment=result.get("treatment", []),
        )
    )
