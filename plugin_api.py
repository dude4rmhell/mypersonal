from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Protocol


CommandHandler = Callable[[str], None]


class LoggerLike(Protocol):
    def info(self, *args, **kwargs) -> None: ...


@dataclass
class PluginContext:
    logger: LoggerLike
    ai_manager: object
    memory_path: Path
    config: object
    settings: object
    utils: dict[str, object] = field(default_factory=dict)


@dataclass
class PluginCommand:
    name: str
    handler: CommandHandler
    description: str = ""


@dataclass
class PluginDefinition:
    name: str
    version: str
    author: str
    description: str
    commands: list[PluginCommand]
    initialize: Callable[[PluginContext], None] | None = None
    shutdown: Callable[[], None] | None = None
    enabled: bool = True
    path: Path | None = None
    metadata: dict[str, object] = field(default_factory=dict)
