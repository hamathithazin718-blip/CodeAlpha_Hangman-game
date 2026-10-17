# Python Text-Based Hangman Game

A clean, beginner-friendly, text-based **Hangman** game implemented in pure Python. The player must guess a randomly selected secret word one letter at a time via the console before running out of turns.

## 🚀 Features
- **Random Selection:** Picks a word dynamically from a predefined 5-word pool.
- **Input Validation:** Gracefully handles uppercase/lowercase text and rejects invalid inputs (numbers, symbols, or multi-letter words).
- **Duplicate Prevention:** Warns the player if they guess a letter they've already tried without penalizing their score.
- **Pure Python:** Built entirely with standard libraries (`random`)—no external dependencies or installations required.

## 🧠 Concepts Demonstrated
This project is an excellent demonstration of foundational Python coding paradigms:
* Module imports (`random`)
* Control flow using `while` loops and nested `if-else` conditionals
* Dynamic state tracking via lists and strings
* Clean terminal input/output management

## 🛠️ How to Run

1. Make sure you have **Python 3** installed.
2. Clone or download this repository.
3. Open your terminal or VS Code, navigate to the project folder, and run:
   ```bash
   python hangman.py
   ```

## 🎮 Game Rules
- You start with exactly **6 incorrect guesses**.
- Correct guesses fill in the corresponding blanks.
- Incorrect guesses reduce your remaining turns.
- Win by revealing the full word; lose if your incorrect guesses hit zero!
