"""
Helios API Schemas
"""

from pydantic import BaseModel, Field


class CommandRequest(BaseModel):
    """Request sent by the browser UI."""

    command: str = Field(
        ...,
        min_length=1,
        description="Helios command to execute",
    )


class CommandResponse(BaseModel):
    """Response returned to the browser UI."""

    command: str
    output: str