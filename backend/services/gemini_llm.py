"""
Gemini LLM wrapper for conversational follow-up Q&A.
"""

import logging
from typing import Dict, Any, List, Optional

import google.generativeai as genai

from config import settings
from prompts import CHAT_SYSTEM_PROMPT, CHAT_SYSTEM_PROMPT_NO_CONTEXT

logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_chat_model(system_instruction: Optional[str] = None):
    """Get a configured Gemini LLM model instance for chat."""
    kwargs = {
        "model_name": "gemini-2.5-flash",
        "generation_config": {
            "temperature": 0.6,
            "top_p": 0.9,
            "max_output_tokens": 1024,
        }
    }
    if system_instruction:
        kwargs["system_instruction"] = system_instruction
        
    return genai.GenerativeModel(**kwargs)


def build_system_prompt(last_diagnosis: Optional[Dict[str, Any]] = None) -> str:
    """
    Build the system prompt with diagnosis context if available.

    Args:
        last_diagnosis: The last diagnosis result from the session

    Returns:
        Formatted system prompt string
    """
    if last_diagnosis and "plant" in last_diagnosis:
        return CHAT_SYSTEM_PROMPT.format(
            plant=last_diagnosis.get("plant", "Unknown"),
            disease=last_diagnosis.get("disease", "Unknown"),
            confidence=last_diagnosis.get("confidence", "Unknown"),
        )
    return CHAT_SYSTEM_PROMPT_NO_CONTEXT


async def chat_followup(
    user_message: str,
    chat_history: List[Dict[str, str]],
    last_diagnosis: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a conversational follow-up response using Gemini LLM.

    Args:
        user_message: The user's new message
        chat_history: Previous messages in the session
        last_diagnosis: Last diagnosis result for context

    Returns:
        AI-generated response text

    Raises:
        Exception: If the Gemini API call fails
    """
    system_prompt = build_system_prompt(last_diagnosis)
    model = get_chat_model(system_instruction=system_prompt)

    # Build the conversation history for Gemini
    contents = []

    # Add chat history
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    # Add the new user message
    contents.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    try:
        logger.info(f"Sending follow-up chat to Gemini LLM ({len(contents)} messages)")

        from utils.gemini_client import execute_with_fallback
        response = execute_with_fallback(
            model.generate_content,
            contents,
            request_options={"timeout": 20}
        )

        if not response.text:
            logger.warning("Gemini LLM returned empty response")
            return "I'm sorry, I couldn't generate a response. Please try asking again."

        logger.debug(f"Gemini LLM response: {response.text[:200]}")
        return response.text

    except Exception as e:
        logger.error(f"Gemini LLM API error: {str(e)}")
        raise
