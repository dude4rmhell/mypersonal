"""
Helios API Server

Provides the HTTP interface for the Helios core
and serves the local Helios browser UI.
"""
from config.version import VERSION
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router
from config.version import VERSION


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = BASE_DIR / "ui"


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Helios API",
    description="API interface for the Helios desktop AI assistant",
    version=VERSION,
)


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check():
    """
    Return the current API health status.
    """

    return {
        "status": "ok",
        "service": "Helios",
        "version": VERSION,
    }


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

app.include_router(router)


# ---------------------------------------------------------------------------
# Browser UI
# ---------------------------------------------------------------------------

if UI_DIR.exists():
    app.mount(
        "/",
        StaticFiles(
            directory=UI_DIR,
            html=True,
        ),
        name="ui",
    )