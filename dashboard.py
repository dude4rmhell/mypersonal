"""
Helios Dashboard Service

Collects structured system information for the Helios browser UI.
This module does not replace the existing CLI system commands.
"""

from __future__ import annotations

import platform
import shutil
import socket

import psutil

from config.version import VERSION
from plugins.plugin_manager import get_plugin_manager


def _gib(value: int) -> float:
    """Convert bytes to GiB."""
    return round(value / (1024 ** 3), 1)


def get_cpu() -> dict:
    """Return CPU information."""

    return {
        "percent": round(psutil.cpu_percent(interval=0.2)),
        "cores": psutil.cpu_count(logical=True) or 0,
    }


def get_memory() -> dict:
    """Return memory information."""

    info = psutil.virtual_memory()

    return {
        "percent": round(info.percent),
        "used_gb": _gib(info.used),
        "total_gb": _gib(info.total),
    }


def get_disk() -> dict:
    """Return disk information."""

    info = shutil.disk_usage("/")

    percent = (info.used / info.total) * 100

    return {
        "percent": round(percent),
        "used_gb": _gib(info.used),
        "total_gb": _gib(info.total),
    }


def get_battery() -> dict:
    """Return battery information."""

    status = psutil.sensors_battery()

    if status is None:
        return {
            "available": False,
            "percent": None,
            "charging": False,
        }

    return {
        "available": True,
        "percent": round(status.percent),
        "charging": status.power_plugged,
    }


def get_ip() -> str:
    """Return the local IP address."""

    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return "Unavailable"


def get_system() -> dict:
    """Return operating-system information."""

    return {
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }


def get_plugins() -> dict:
    """Return loaded plugin information."""

    manager = get_plugin_manager()

    plugins = getattr(manager, "plugins", None)

    if isinstance(plugins, dict):
        return {
            "count": len(plugins),
        }

    return {
        "count": 0,
    }


def get_dashboard_data() -> dict:
    """Return all dashboard information."""

    return {
        "status": "online",
        "version": VERSION,
        "cpu": get_cpu(),
        "memory": get_memory(),
        "disk": get_disk(),
        "battery": get_battery(),
        "network": {
            "ip": get_ip(),
        },
        "system": get_system(),
        "plugins": get_plugins(),
    }