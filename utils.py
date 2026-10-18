"""
"""
Utility module handling CLI view configurations and premium color layouts.
"""
import os

# Professional ANSI color constants
COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

def clear_screen():
    """Clears the terminal workspace dynamically across operating systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def render_header(title: str, size: int = 50, color: str = COLOR_CYAN):
    """Draws a premium styled dashboard panel border block."""
    print(f"{color}" + "=" * size)
    print(f"{title.center(size)}")
    print("=" * size + f"{COLOR_RESET}")
