from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
from types import ModuleType

from plugins.plugin_api import PluginCommand, PluginDefinition


@dataclass
class LoadedPlugin:
    definition: PluginDefinition
    module: ModuleType
    source_path: Path


def load_plugin_metadata(plugin_dir: Path) -> dict[str, object]:
    metadata_path = plugin_dir / "plugin.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing plugin.json in {plugin_dir.name}")
    payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("plugin.json must contain a JSON object.")
    return payload


def load_plugin_module(plugin_dir: Path) -> ModuleType:
    plugin_file = plugin_dir / "plugin.py"
    if not plugin_file.exists():
        raise FileNotFoundError(f"Missing plugin.py in {plugin_dir.name}")
    spec = importlib.util.spec_from_file_location(f"helios_plugin_{plugin_dir.name}", plugin_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load plugin module from {plugin_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_definition(module: ModuleType, metadata: dict[str, object], source_path: Path) -> PluginDefinition:
    factory = getattr(module, "create_plugin", None)
    if callable(factory):
        definition = factory(metadata)
        if not isinstance(definition, PluginDefinition):
            raise TypeError("create_plugin() must return a PluginDefinition.")
        definition.path = source_path
        definition.metadata = metadata
        return definition

    command_names = metadata.get("commands", [])
    if not isinstance(command_names, list):
        raise TypeError("plugin metadata commands must be a list.")

    commands: list[PluginCommand] = []
    command_map = getattr(module, "COMMANDS", {})
    for command_name in command_names:
        handler = None
        if isinstance(command_map, dict):
            handler = command_map.get(command_name)
        if handler is None:
            handler = getattr(module, command_name, None)
        if not callable(handler):
            raise TypeError(f"Plugin command '{command_name}' is not callable.")
        commands.append(PluginCommand(name=str(command_name), handler=handler))

    return PluginDefinition(
        name=str(metadata.get("name", source_path.name.title())),
        version=str(metadata.get("version", "1.0.0")),
        author=str(metadata.get("author", "Helios")),
        description=str(metadata.get("description", "")),
        commands=commands,
        initialize=getattr(module, "initialize", None),
        shutdown=getattr(module, "shutdown", None),
        path=source_path,
        metadata=metadata,
    )
