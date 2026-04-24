"""
Helper for Gemini API interactions with fallback support.
"""
import logging
import google.generativeai as genai
from config import settings

logger = logging.getLogger(__name__)

# Track which key is currently active globally
_current_key_is_primary = True

def execute_with_fallback(func, *args, **kwargs):
    """
    Executes a synchronous Gemini API call. If it fails and a fallback key is available,
    it switches the global configuration to the fallback key and retries once.
    """
    global _current_key_is_primary

    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Gemini API call failed: {str(e)}")
        
        if settings.GEMINI_API_KEY_FALLBACK and _current_key_is_primary:
            logger.warning("Switching to GEMINI_API_KEY_FALLBACK globally...")
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY_FALLBACK)
                _current_key_is_primary = False
                
                logger.info("Retrying API call with fallback key...")
                return func(*args, **kwargs)
            except Exception as fallback_e:
                logger.error(f"Fallback Gemini API call also failed: {str(fallback_e)}")
                raise
        else:
            raise
