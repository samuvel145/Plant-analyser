"""
PlantMD — AI Plant Disease Detection Chat Agent
FastAPI Application Entry Point

Main application configuration including:
- CORS middleware
- Request size limits
- Route registration
- Logging setup
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from routes import analyse, chat, session, health


# ─────────────────────────────────────────────
# Logging Configuration
# ─────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# App Lifespan
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("🌿 PlantMD server starting...")
    logger.info(f"   Debug mode: {settings.DEBUG}")
    logger.info(f"   Allowed origins: {settings.allowed_origins_list}")
    logger.info(f"   Max sessions: {settings.MAX_SESSIONS}")
    logger.info(f"   Session TTL: {settings.SESSION_TTL_MINUTES} min")
    yield
    logger.info("🌿 PlantMD server shutting down...")


# ─────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────
app = FastAPI(
    title="PlantMD — AI Plant Disease Detection",
    description="Chat-based plant disease diagnosis powered by Google Gemini",
    version="1.0.0",
    lifespan=lifespan,
)


# ─────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request size limiter middleware
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    """Limit request body size to prevent abuse (12 MB max)."""
    max_size = 12 * 1024 * 1024  # 12 MB

    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > max_size:
        return JSONResponse(
            status_code=413,
            content={
                "error": "payload_too_large",
                "message": "Request body exceeds the 12 MB limit."
            }
        )

    return await call_next(request)


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
app.include_router(analyse.router, tags=["Analysis"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(session.router, tags=["Session"])
app.include_router(health.router, tags=["Health"])


# ─────────────────────────────────────────────
# Root
# ─────────────────────────────────────────────
@app.get("/")
async def root():
    """Root endpoint — API info."""
    return {
        "app": "PlantMD",
        "version": "1.0.0",
        "description": "AI Plant Disease Detection Chat Agent",
        "docs": "/docs",
    }
