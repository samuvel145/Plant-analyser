"""
API route for session management — DELETE /api/session/{session_id}
"""

import logging

from fastapi import APIRouter

from models.response_models import SessionResetResponse
from services.session_manager import session_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.delete("/api/session/{session_id}")
async def reset_session(session_id: str):
    """
    Clear/reset a session from memory.
    All chat history and diagnosis data for the session is purged.
    """
    deleted = session_manager.delete_session(session_id)

    if deleted:
        logger.info(f"Session {session_id} cleared by user request")
    else:
        logger.info(f"Session {session_id} not found (may have already expired)")

    return SessionResetResponse(
        message=f"Session {session_id} has been cleared successfully."
    )
