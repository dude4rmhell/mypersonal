from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from app.logger import get_logger
from config import settings
from plugins.plugin_api import PluginContext, PluginDefinition
from plugins.plugin_loader import extract_definition, load_plugin_metadata, load_plugin_module


@dataclass
class PluginState:
    definition: PluginDefinition
    loaded: bool = False
    enabled: bool = True


@dataclass
class PluginManager:
    root: Path = settings.PLUGIN_ROOT
    context: PluginContext | None = None
    logger_name: str = "helios.plugins"
    _plugins: dict[str, PluginState] = field(default_factory=dict)
    _commands: dict[str, callable] = field(default_factory=dict)
    _owners: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.logger = get_logger(self.logger_name)
        self.root.mkdir(parents=True, exist_ok=True)

    def set_context(self, context: PluginContext) -> None:
        self.context = context

    def discover(self) -> list[str]:
        loaded: list[str] = []
        for plugin_dir in sorted(self.root.iterdir()):
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
                continue
            if (plugin_dir / "plugin.json").exists() and (plugin_dir / "plugin.py").exists():
                try:
                    self.load_plugin(plugin_dir.name)
                    loaded.append(plugin_dir.name)
                except Exception as exc:
                    self.logger.info("Skipped plugin %s: %s", plugin_dir.name, exc)
        return loaded

    def load_plugin(self, name: str) -> PluginState:
        plugin_dir = self.root / name
        metadata = load_plugin_metadata(plugin_dir)
        module = load_plugin_module(plugin_dir)
        definition = extract_definition(module, metadata, plugin_dir)
        key = definition.name.lower()
        existing = self._plugins.get(key)
        if existing:
            self._unregister_commands(existing.definition)
        state = PluginState(definition=definition, loaded=True, enabled=True)
        self._plugins[key] = state
        self._register_commands(definition)
        if callable(definition.initialize) and self.context is not None:
            definition.initialize(self.context)
        self.logger.info("Loaded plugin %s", definition.name)
        return state

    def unload_plugin(self, name: str) -> bool:
        key = self._resolve_key(name)
        state = self._plugins.get(key)
        if not state:
            return False
        self._unregister_commands(state.definition)
        if callable(state.definition.shutdown):
            state.definition.shutdown()
        del self._plugins[key]
        self.logger.info("Unloaded plugin %s", state.definition.name)
        return True

    def reload_plugin(self, name: str) -> PluginState:
        key = self._resolve_key(name)
        state = self._plugins.get(key)
        if state:
            self.unload_plugin(state.definition.name)
        return self.load_plugin(name)

    def disable_plugin(self, name: str) -> bool:
        key = self._resolve_key(name)
        state = self._plugins.get(key)
        if not state:
            return False
        state.enabled = False
        self._unregister_commands(state.definition)
        self.logger.info("Disabled plugin %s", state.definition.name)
        return True

    def enable_plugin(self, name: str) -> bool:
        key = self._resolve_key(name)
        state = self._plugins.get(key)
        if not state:
            return False
        state.enabled = True
        self._register_commands(state.definition)
        self.logger.info("Enabled plugin %s", state.definition.name)
        return True

    def list_plugins(self) -> list[PluginState]:
        return sorted(self._plugins.values(), key=lambda item: item.definition.name.lower())

    def get_plugin(self, name: str) -> PluginState | None:
        return self._plugins.get(self._resolve_key(name))

    def plugins_text(self) -> str:
        lines = ["\nPlugins", "-" * 7]
        for state in self.list_plugins():
            status = "Enabled" if state.enabled else "Disabled"
            lines.append(f"{state.definition.name} ({state.definition.version}) - {status}")
        if len(lines) == 2:
            lines.append("No plugins loaded.")
        lines.append("")
        return "\n".join(lines)

    def plugin_info_lines(self, name: str) -> list[str]:
        state = self.get_plugin(name)
        if not state:
            return [f"Plugin '{name}' is not loaded."]
        definition = state.definition
        commands = ", ".join(command.name for command in definition.commands) or "None"
        return [
            f"Name        : {definition.name}",
            f"Version     : {definition.version}",
            f"Author      : {definition.author}",
            f"Description : {definition.description}",
            f"Enabled     : {state.enabled}",
            f"Commands    : {commands}",
        ]

    def get_command_map(self) -> dict[str, callable]:
        return dict(self._commands)

    def _register_commands(self, definition: PluginDefinition) -> None:
        for command in definition.commands:
            command_name = command.name.lower()
            owner = self._owners.get(command_name)
            if owner and owner != definition.name.lower():
                raise ValueError(f"Command '{command.name}' is already registered by '{owner}'.")
            self._commands[command_name] = command.handler
            self._owners[command_name] = definition.name.lower()

    def _unregister_commands(self, definition: PluginDefinition) -> None:
        for command in definition.commands:
            command_name = command.name.lower()
            if self._owners.get(command_name) == definition.name.lower():
                self._commands.pop(command_name, None)
                self._owners.pop(command_name, None)

    def _resolve_key(self, name: str) -> str:
        return name.strip().lower()


_MANAGER: PluginManager | None = None


def get_plugin_manager() -> PluginManager:
    global _MANAGER
    if _MANAGER is None:
        _MANAGER = PluginManager()
        _MANAGER.discover()
    return _MANAGER
