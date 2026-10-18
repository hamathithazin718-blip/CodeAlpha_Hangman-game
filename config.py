"""
Configuration module holding application-wide static assets and data dictionaries.
"""

WORD_CATEGORIES = {
    "Animals": ["elephant", "giraffe", "dolphin", "penguin", "leopard"],
    "Programming": ["python", "variable", "compiler", "function", "database"],
    "Countries": ["brazil", "germany", "vietnam", "morocco", "australia"]
}

DIFFICULTY_MODES = {
    "E": {"name": "Easy", "lives": 8},
    "M": {"name": "Medium", "lives": 6},
    "H": {"name": "Hard", "lives": 4}
}

ASCII_GALLOWS = [
    "\n   +---+\n   |   |\n   O   |\n  /|\\  |\n  / \\  |\n       |\n =========",  # 0 lives left
    "\n   +---+\n   |   |\n   O   |\n  /|\\  |\n  /    |\n       |\n =========",  # 1 life left
    "\n   +---+\n   |   |\n   O   |\n  /|\\  |\n       |\n       |\n =========",  # 2 lives left
    "\n   +---+\n   |   |\n   O   |\n  /|   |\n       |\n       |\n =========",  # 3 lives left
    "\n   +---+\n   |   |\n   O   |\n   |   |\n       |\n       |\n =========",  # 4 lives left
    "\n   +---+\n   |   |\n   O   |\n       |\n       |\n       |\n =========",  # 5 lives left
    "\n   +---+\n   |   |\n       |\n       |\n       |\n       |\n ========="   # 6+ lives left
]
