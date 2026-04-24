"""
Pydantic response schemas for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class DiagnosisData(BaseModel):
    """Structured plant disease diagnosis result."""
    plant: str = Field(..., description="Identified plant species")
    disease: str = Field(..., description="Detected disease or 'None detected'")
    confidence: str = Field(..., description="Confidence percentage e.g. '91%'")
    symptoms: List[str] = Field(default_factory=list, description="List of observed symptoms")
    treatment: List[str] = Field(default_factory=list, description="Ordered treatment steps")


class DiagnosisResponse(BaseModel):
    """Response for POST /api/analyse — successful diagnosis."""
    session_id: str
    type: str = "diagnosis"
    data: DiagnosisData
    follow_up_prompt: str = (
        "You can ask me more about this disease, organic treatment "
        "alternatives, or upload another image."
    )


class ChatResponse(BaseModel):
    """Response for POST /api/chat — conversational follow-up."""
    session_id: str
    type: str = "chat"
    message: str


class GuardrailResponse(BaseModel):
    """Response when a guardrail is triggered (off-topic or non-plant image)."""
    session_id: str
    type: str = "guardrail"
    message: str


class ErrorResponse(BaseModel):
    """Generic error response."""
    error: str
    message: str


class HealthResponse(BaseModel):
    """Response for GET /api/health."""
    status: str = "ok"
    active_sessions: int = 0
    gemini_api: str = "unknown"


class SessionResetResponse(BaseModel):
    """Response for DELETE /api/session/{session_id}."""
    message: str
