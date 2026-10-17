"""
Hangman - a simple text-based game.
Guess the secret word one letter at a time. You get 6 incorrect guesses.
"""

import random  # standard library module used to pick a random word

# Predefined word pool (exactly 5 simple words)
WORDS = ["python", "coding", "program", "laptop", "screen"]

MAX_WRONG_GUESSES = 6


def display_word(secret_word, guessed_letters):
    """Return the word as a string like 'a _ _ l _', showing only guessed letters."""
    shown = []
    for letter in secret_word:
        if letter in guessed_letters:
            shown.append(letter)
        else:
            shown.append("_")
    return " ".join(shown)


def play_hangman():
    # Randomly select one word from the list
    secret_word = random.choice(WORDS)

    guessed_letters = []   # every letter the player has tried (right or wrong)
    wrong_guesses = 0      # number of incorrect guesses so far

    print("=== Welcome to Hangman! ===")
    print(f"I'm thinking of a {len(secret_word)}-letter word.")
    print(f"You can make up to {MAX_WRONG_GUESSES} incorrect guesses.\n")

    # Keep the game running until the player wins or runs out of guesses
    while wrong_guesses < MAX_WRONG_GUESSES:
        # Show the current game state
        print("Word:", display_word(secret_word, guessed_letters))
        print("Guessed letters:", ", ".join(sorted(guessed_letters)) if guessed_letters else "none yet")
        print(f"Incorrect guesses left: {MAX_WRONG_GUESSES - wrong_guesses}")

        # Get input and normalize it (strip spaces, convert to lowercase)
        guess = input("Enter a letter: ").strip().lower()

        # --- Input validation ---
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).\n")
        elif guess in guessed_letters:
            # Repeated guess: warn the player, but don't cost them a turn
            print(f"You already guessed '{guess}'. Try a different letter.\n")
        else:
            # Valid new guess: record it
            guessed_letters.append(guess)

            if guess in secret_word:
                print(f"Good job! '{guess}' is in the word.\n")
            else:
                wrong_guesses += 1
                print(f"Sorry, '{guess}' is not in the word.\n")

            # Win check: are all letters of the secret word guessed?
            all_found = True
            for letter in secret_word:
                if letter not in guessed_letters:
                    all_found = False
                    break

            if all_found:
                print("Word:", display_word(secret_word, guessed_letters))
                print(f"Congratulations, you won! The word was '{secret_word}'.")
                return  # end the game early

    # If the loop ends without a win, the player has lost
    print(f"Game over! You ran out of guesses. The word was '{secret_word}'.")


# Run the game only when this file is executed directly
if __name__ == "__main__":
    try:
        play_hangman()
    except KeyboardInterrupt:
        print("\nGame cancelled. Thanks for playing!")
