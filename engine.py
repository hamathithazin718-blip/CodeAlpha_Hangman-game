"""
Core runtime application engine managing colored loop configurations.
"""
import random
from hangman_app.config import WORD_CATEGORIES, DIFFICULTY_MODES, ASCII_GALLOWS
from hangman_app.utils import (
    clear_screen, render_header, 
    COLOR_CYAN, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_RESET
)

class HangmanEngine:
    def __init__(self):
        self.score_tracker = {"wins": 0, "losses": 0}

    def _select_game_parameters(self) -> tuple[str, str, int]:
        clear_screen()
        render_header(f"📊 LIVE SCORE: {self.score_tracker['wins']} WINS | {self.score_tracker['losses']} LOSSES", color=COLOR_CYAN)
        
        print(f"\n{COLOR_CYAN}[STEP 1]{COLOR_RESET} Select Your Secret Word Category:")
        categories = list(WORD_CATEGORIES.keys())
        for idx, cat in enumerate(categories, 1):
            print(f"  [{idx}] {cat}")
        print(f"  [{len(categories) + 1}] Random Mystery Mix")
        
        while True:
            choice = input("\nEnter Category Number: ").strip()
            if choice.isdigit():
                val = int(choice)
                if 1 <= val <= len(categories):
                    chosen_cat = categories[val - 1]
                    break
                elif val == len(categories) + 1:
                    chosen_cat = random.choice(categories)
                    break
            print(f"{COLOR_RED}❌ Selection error. Type a valid option index.{COLOR_RESET}")

        print(f"\n{COLOR_CYAN}[STEP 2]{COLOR_RESET} Select Core Game Difficulty:")
        for key, conf in DIFFICULTY_MODES.items():
            print(f"  [{key}] {conf['name']} Mode — Allow {conf['lives']} Misses")
            
        while True:
            diff_input = input("\nChoose Level (E/M/H): ").strip().upper()
            if diff_input in DIFFICULTY_MODES:
                max_lives = DIFFICULTY_MODES[diff_input]["lives"]
                break
            print(f"{COLOR_RED}❌ Selection error. Input must match [E], [M], or [H].{COLOR_RESET}")

        return random.choice(WORD_CATEGORIES[chosen_cat]), chosen_cat, max_lives

    def _get_ascii_visuals(self, current_lives: int) -> str:
        if current_lives >= 6:
            return f"{COLOR_CYAN}{ASCII_GALLOWS[-1]}{COLOR_RESET}"
        if current_lives <= 0:
            return f"{COLOR_RED}{ASCII_GALLOWS[0]}{COLOR_RESET}"
        return f"{COLOR_YELLOW}{ASCII_GALLOWS[current_lives]}{COLOR_RESET}"

    def execute_session(self):
        while True:
            secret_word, category, lives_left = self._select_game_parameters()
            guessed_tokens = []
            status_msg = f"{COLOR_GREEN}Game initialization complete. Type a letter!{COLOR_RESET}"
            
            while lives_left > 0:
                clear_screen()
                render_header(f"🎯 FIELD CATEGORY: {category.upper()}", color=COLOR_CYAN)
                
                print(self._get_ascii_visuals(lives_left))
                
                mask_display = [char if char in guessed_tokens else "_" for char in secret_word]
                print(f"\nWord Visual status:  {COLOR_GREEN}{' '.join(mask_display)}{COLOR_RESET}\n")
                print(f"Remaining Misses Allowed: {COLOR_RED}{lives_left}{COLOR_RESET}")
                print(f"Utilized Inputs Log: {COLOR_YELLOW}{', '.join(sorted(guessed_tokens)) if guessed_tokens else 'None'}{COLOR_RESET}")
                print("-" * 50)
                print(f"System Broadcast: {status_msg}")
                print("-" * 50)
                
                if "_" not in mask_display:
                    print(f"\n{COLOR_GREEN}🎉 EXCELLENT! Success victory achieved! Word was: {secret_word.upper()}{COLOR_RESET}\n")
                    self.score_tracker["wins"] += 1
                    break
                    
                user_guess = input("Submit Letter: ").strip().lower()
                
                if len(user_guess) != 1 or not user_guess.isalpha():
                    status_msg = f"{COLOR_RED}⚠️ Error: Entry requires a single alphabetic character.{COLOR_RESET}"
                    continue
                    
                if user_guess in guessed_tokens:
                    status_msg = f"{COLOR_YELLOW}⚠️ Warning: '{user_guess.upper()}' was already processed.{COLOR_RESET}"
                    continue
                    
                guessed_tokens.append(user_guess)
                
                if user_guess in secret_word:
                    status_msg = f"{COLOR_GREEN}✅ Target Found! '{user_guess.upper()}' maps inside the sequence.{COLOR_RESET}"
                else:
                    status_msg = f"{COLOR_RED}❌ Target Miss! '{user_guess.upper()}' is incorrect.{COLOR_RESET}"
                    lives_left -= 1
                    
            if lives_left == 0:
                clear_screen()
                render_header("💀 DEFEAT DIAGNOSTIC", color=COLOR_RED)
                print(self._get_ascii_visuals(0))
                print(f"\nOut of runtime attempts. Word was: {COLOR_YELLOW}{secret_word.upper()}{COLOR_RESET}\n")
                self.score_tracker["losses"] += 1
                
            retry_prompt = input("Initiate round restart? (Y/N): ").strip().lower()
            if retry_prompt not in ["y", "yes"]:
                clear_screen()
                render_header("🏁 SESSION CLOSED SUCCESSFULLY", color=COLOR_CYAN)
                print(f"Final Record: {self.score_tracker['wins']} Wins | {self.score_tracker['losses']} Losses\n")
                break
