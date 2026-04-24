"""
API route for conversational follow-up — POST /api/chat
"""

import asyncio
import logging

from fastapi import APIRouter, HTTPException

from models.request_models import ChatRequest
from models.response_models import ChatResponse, GuardrailResponse
from services.session_manager import session_manager
from services.guardrail import is_allowed_topic
from services.gemini_llm import chat_followup
from prompts import GUARDRAIL_REFUSAL_MESSAGE

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/chat")
@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Send a follow-up text message in an existing session.
    The AI responds with context from the last diagnosis.
    """
    session = session_manager.get_or_create_session(request.session_id)

    # Rate limit check
    if not session.check_rate_limit():
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment before trying again."
        )

    # Run guardrail check (pre-LLM filter)
    try:
        allowed = await asyncio.wait_for(
            is_allowed_topic(request.message),
            timeout=10
        )
    except asyncio.TimeoutError:
        # If guardrail times out, allow the message through
        logger.warning("Guardrail timed out, allowing message through")
        allowed = True
    except Exception as e:
        logger.error(f"Guardrail error: {str(e)}, allowing message through")
        allowed = True

    if not allowed:
        logger.info(f"Guardrail BLOCKED message in session {request.session_id}")
        session.add_message("user", request.message)
        session.add_message("assistant", GUARDRAIL_REFUSAL_MESSAGE)
        return GuardrailResponse(
            session_id=request.session_id,
            message=GUARDRAIL_REFUSAL_MESSAGE
        )

    # Add user message to history
    session.add_message("user", request.message)

    # Generate follow-up response
    try:
        response_text = await asyncio.wait_for(
            chat_followup(
                user_message=request.message,
                chat_history=session.chat_history[:-1],  # Exclude the message we just added
                last_diagnosis=session.last_diagnosis,
            ),
            timeout=20
        )
    except asyncio.TimeoutError:
        logger.error(f"Gemini LLM timed out for session {request.session_id}")
        raise HTTPException(
            status_code=504,
            detail="Response is taking longer than usual. Please try again."
        )
    except Exception as e:
        logger.error(f"Gemini LLM error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"DEBUG ERROR: {str(e)} | Type: {type(e).__name__}"
        )

    # Add AI response to history
    session.add_message("assistant", response_text)

    return ChatResponse(
        session_id=request.session_id,
        message=response_text
    )
