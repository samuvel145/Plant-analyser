"""
Pydantic request schemas for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Request schema for POST /api/chat — conversational follow-up."""
    session_id: str = Field(..., description="UUID v4 session identifier")
    message: str = Field(..., min_length=1, max_length=2000, description="User's text message")


class AnalyseRequest(BaseModel):
    """
    Request schema for POST /api/analyse.
    Note: The actual request is multipart/form-data.
    This model is used for validation of the non-file fields.
    """
    session_id: str = Field(..., description="UUID v4 session identifier")
    message: Optional[str] = Field(None, max_length=2000, description="Optional accompanying note")
