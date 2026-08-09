from core.registry import COMMANDS


def execute(command: str):
    """Execute a command entered by the user."""
    command = command.strip()
    if not command:
        return
    name, _, args = command.partition(" ")
    name = name.lower()
    handler = COMMANDS.get(name)
    if handler:
        handler(args.strip())
    else:
        print(f"\nUnknown command: {name}")
        print("Type 'help' to see available commands.\n")
