"""
API route for health check — GET /api/health
"""

import logging

from fastapi import APIRouter

from models.response_models import HealthResponse
from services.session_manager import session_manager
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    Returns server status, active session count, and Gemini API reachability.
    """
    gemini_status = "unknown"

    # Quick Gemini API check
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Just verify the key is configured — don't make an actual API call
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            gemini_status = "configured"
        else:
            gemini_status = "not_configured"
    except Exception:
        gemini_status = "error"

    return HealthResponse(
        status="ok",
        active_sessions=session_manager.get_active_count(),
        gemini_api=gemini_status,
    )
