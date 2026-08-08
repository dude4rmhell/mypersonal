"""
Helios Personal AI Assistant
Version 0.6.0
"""

from app.banner import show_banner
from app.console import get_user_input
from core.router import execute


def main():
    show_banner()

    try:
        while True:
            command = get_user_input()
            execute(command)
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye from Helios.\n")


if __name__ == "__main__":
    main()
