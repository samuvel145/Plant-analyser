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
# Static Frontend Serving
# ─────────────────────────────────────────────
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Determine path to the frontend dist directory
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

@app.get("/api")
async def api_root():
    """API Root endpoint"""
    return {
        "app": "PlantMD API",
        "version": "1.0.0",
        "status": "active"
    }

if os.path.exists(frontend_dist):
    logger.info(f"Serving frontend from {frontend_dist}")
    
    # Serve assets directory directly
    assets_path = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
        
    # Catch-all route for SPA and root static files
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Allow requests to /api to fall through to FastAPI routes (if not already handled)
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
            
        file_path = os.path.join(frontend_dist, full_path)
        
        # If the file exists in dist (e.g. favicon.svg), serve it directly
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Otherwise, fall back to index.html for React SPA routing
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.isfile(index_path):
            return FileResponse(index_path)
            
        return {"error": "Frontend build not found. Please run 'npm run build' in the frontend directory."}
else:
    logger.warning(f"Frontend dist directory not found at {frontend_dist}. API only mode.")
    
    @app.get("/")
    async def root():
        return {
            "app": "PlantMD",
            "message": "API is running, but frontend is not built. Run 'npm run build' in the frontend folder."
        }
