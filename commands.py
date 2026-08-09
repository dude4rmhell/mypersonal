"""
Helios Command Module

This module is kept only for backward compatibility.

All command processing is now handled by:

    core/router.py
    core/registry.py
"""

from core.router import execute


def process_command(command: str) -> bool:
    """
    Compatibility wrapper.

    Existing code can still call process_command(),
    but internally the new command router is used.
    """

    try:
        execute(command)
        return True

    except SystemExit:
        return False