# Helios

Helios is a modular local desktop-assistant foundation written in Python. It provides an interactive command console, local system diagnostics, a stabilized AI provider layer, a plugin architecture, and a Windows desktop automation plugin.

## Run

```powershell
cd C:\AIProjects\Helios
python -m pip install -r requirements.txt
python main.py
```

Type `help` in Helios to list all available commands.

AI commands:

- `ask <prompt>`
- `chat`
- `history`
- `clear_history`
- `export_history`
- `provider [groq|openrouter|openai|local]`
- `models`
- `model [name]`
- `config`
- `health`
- `stats`

Plugin commands:

- `plugins`
- `plugin info <name>`
- `load <name>`
- `unload <name>`
- `reload <name>`
- `disable <name>`
- `enable <name>`

Automation commands:

- `open <target>`
- `close <target>`
- `windows`
- `active`
- `switch <target>`
- `minimize <target>`
- `maximize <target>`
- `restore <target>`
- `processes`
- `clipboard`
- `copy <text>`
- `paste`
- `volume`
- `mute`
- `unmute`
- `set volume <n>`
- `screenshot`
- `capture active`
- `file <action>`
- `google <query>`
- `youtube <query>`
- `github`
- `gmail`
- `servicenow`
- `shutdown`
- `restart`
- `sleep`
- `hibernate`
- `lock`

The `weather` command is now provided by the Weather plugin and still uses the public wttr.in endpoint.
