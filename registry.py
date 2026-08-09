from app.commands.help import execute as help_cmd
from app.commands.about import execute as about_cmd
from app.commands.version import execute as version_cmd
from app.commands.clear import execute as clear_cmd
from app.commands.exit import execute as exit_cmd
from app.commands.ai_chat import ask as ask_cmd
from app.commands.ai_chat import chat as chat_cmd
from app.commands.ai_chat import clear_history as clear_history_cmd
from app.commands.ai_chat import history as history_cmd
from app.commands.config import execute as config_cmd
from app.commands.disable import execute as disable_cmd
from app.commands.enable import execute as enable_cmd
from app.commands.export_history import execute as export_history_cmd
from app.commands.health import execute as health_cmd
from app.commands.load import execute as load_cmd
from app.commands.model import execute as model_cmd
from app.commands.models import execute as models_cmd
from app.commands.plugin import execute as plugin_cmd
from app.commands.plugins import execute as plugins_cmd
from app.commands.provider import execute as provider_cmd
from app.commands.reload import execute as reload_cmd
from app.commands.stats import execute as stats_cmd
from app.commands.unload import execute as unload_cmd
from app.commands.system_info import battery, cpu, date, disk, ip, memory, system, time
from plugins.plugin_manager import get_plugin_manager

COMMANDS = {
    "help": lambda _args="": help_cmd(),
    "about": lambda _args="": about_cmd(),
    "version": lambda _args="": version_cmd(),
    "clear": lambda _args="": clear_cmd(),
    "exit": lambda _args="": exit_cmd(),
    "time": lambda _args="": time(),
    "date": lambda _args="": date(),
    "system": lambda _args="": system(),
    "battery": lambda _args="": battery(),
    "ip": lambda _args="": ip(),
    "cpu": lambda _args="": cpu(),
    "memory": lambda _args="": memory(),
    "disk": lambda _args="": disk(),
    "ask": ask_cmd,
    "chat": lambda _args="": chat_cmd(),
    "history": lambda _args="": history_cmd(),
    "clear_history": lambda _args="": clear_history_cmd(),
    "export_history": export_history_cmd,
    "provider": provider_cmd,
    "models": models_cmd,
    "model": model_cmd,
    "config": config_cmd,
    "health": health_cmd,
    "stats": stats_cmd,
    "plugins": plugins_cmd,
    "plugin": plugin_cmd,
    "load": load_cmd,
    "unload": unload_cmd,
    "reload": reload_cmd,
    "disable": disable_cmd,
    "enable": enable_cmd,
}

_PLUGIN_MANAGER = get_plugin_manager()
_PLUGIN_COMMANDS: set[str] = set()


def refresh_plugin_commands() -> None:
    global _PLUGIN_COMMANDS
    for command_name in list(_PLUGIN_COMMANDS):
        COMMANDS.pop(command_name, None)
    plugin_commands = _PLUGIN_MANAGER.get_command_map()
    COMMANDS.update(plugin_commands)
    _PLUGIN_COMMANDS = set(plugin_commands.keys())


refresh_plugin_commands()
