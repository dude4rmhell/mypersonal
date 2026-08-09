"""
Helios API Routes

HTTP endpoints used by the Helios browser UI.
"""

import io
from contextlib import redirect_stdout

from fastapi import APIRouter, HTTPException

from api.dashboard import get_dashboard_data
from api.schemas import CommandRequest, CommandResponse


router = APIRouter(prefix="/api", tags=["Helios"])


@router.get("/dashboard")
def dashboard():
    """
    Return structured data for the Helios dashboard.
    """

    return get_dashboard_data()


@router.post("/command", response_model=CommandResponse)
def execute_command(request: CommandRequest):
    """
    Execute an existing Helios CLI command through the core router.

    The existing command system writes its output to stdout.
    We capture that output and return it to the browser UI.
    """

    command = request.command.strip()

    if not command:
        raise HTTPException(
            status_code=400,
            detail="Command cannot be empty.",
        )

    output = io.StringIO()

    try:
        from core.router import execute

        with redirect_stdout(output):
            execute(command)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    return CommandResponse(
        command=command,
        output=output.getvalue(),
    )