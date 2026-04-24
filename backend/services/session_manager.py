"""
In-memory session store with TTL enforcement, FIFO history management,
and per-session rate limiting.
"""

import time
import uuid
import logging
from typing import Dict, List, Optional, Any

from config import settings

logger = logging.getLogger(__name__)


class SessionData:
    """Holds all data for a single user session."""

    def __init__(self, session_id: str):
        self.session_id: str = session_id
        self.chat_history: List[Dict[str, str]] = []
        self.last_diagnosis: Optional[Dict[str, Any]] = None
        self.image_upload_count: int = 0
        self.created_at: float = time.time()
        self.last_active: float = time.time()
        self.request_timestamps: List[float] = []

    def touch(self) -> None:
        """Update the last active timestamp."""
        self.last_active = time.time()

    def is_expired(self) -> bool:
        """Check if the session has exceeded the TTL."""
        ttl_seconds = settings.SESSION_TTL_MINUTES * 60
        return (time.time() - self.last_active) > ttl_seconds

    def add_message(self, role: str, content: str) -> None:
        """Add a message to chat history with FIFO enforcement."""
        self.chat_history.append({"role": role, "content": content})
        self.touch()

        # FIFO: if history exceeds max turns (each turn = 2 messages),
        # drop the oldest 4 messages (2 turns)
        max_messages = settings.MAX_TURNS_PER_SESSION * 2
        if len(self.chat_history) > max_messages:
            self.chat_history = self.chat_history[4:]
            logger.debug(f"Session {self.session_id}: FIFO trimmed oldest 2 turns")

    def set_diagnosis(self, diagnosis: Dict[str, Any]) -> None:
        """Store the latest diagnosis result."""
        self.last_diagnosis = diagnosis
        self.touch()

    def can_upload_image(self) -> bool:
        """Check if the session hasn't exceeded image upload limit."""
        return self.image_upload_count < settings.MAX_IMAGES_PER_SESSION

    def increment_image_count(self) -> None:
        """Track an image upload."""
        self.image_upload_count += 1

    def check_rate_limit(self) -> bool:
        """
        Check if the session is within rate limits.
        Returns True if the request is allowed, False if rate-limited.
        """
        now = time.time()
        window = 60  # 1 minute window

        # Remove timestamps older than the window
        self.request_timestamps = [
            ts for ts in self.request_timestamps if (now - ts) < window
        ]

        if len(self.request_timestamps) >= settings.RATE_LIMIT_RPM:
            return False

        self.request_timestamps.append(now)
        return True


class SessionManager:
    """Manages all active sessions in-memory."""

    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}

    def get_or_create_session(self, session_id: str) -> SessionData:
        """
        Get an existing session or create a new one.
        Also runs cleanup of expired sessions.
        """
        self._cleanup_expired()

        if session_id in self._sessions:
            session = self._sessions[session_id]
            if session.is_expired():
                logger.info(f"Session {session_id} expired, creating new one")
                del self._sessions[session_id]
            else:
                session.touch()
                return session

        # Check max sessions limit
        if len(self._sessions) >= settings.MAX_SESSIONS:
            self._evict_oldest()

        session = SessionData(session_id)
        self._sessions[session_id] = session
        logger.info(f"Created new session: {session_id}")
        return session

    def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get a session by ID, returns None if not found or expired."""
        if session_id not in self._sessions:
            return None

        session = self._sessions[session_id]
        if session.is_expired():
            del self._sessions[session_id]
            return None

        return session

    def delete_session(self, session_id: str) -> bool:
        """Delete a session. Returns True if it existed."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False

    def get_active_count(self) -> int:
        """Get the count of active (non-expired) sessions."""
        self._cleanup_expired()
        return len(self._sessions)

    def _cleanup_expired(self) -> None:
        """Remove all expired sessions."""
        expired = [
            sid for sid, session in self._sessions.items()
            if session.is_expired()
        ]
        for sid in expired:
            del self._sessions[sid]
            logger.debug(f"Cleaned up expired session: {sid}")

    def _evict_oldest(self) -> None:
        """Evict the oldest session when at capacity."""
        if not self._sessions:
            return
        oldest_id = min(
            self._sessions,
            key=lambda sid: self._sessions[sid].last_active
        )
        del self._sessions[oldest_id]
        logger.info(f"Evicted oldest session: {oldest_id}")


# Singleton instance
session_manager = SessionManager()
