import tkinter as tk
from tkinter import messagebox
import random

# --- CORE DATA MATRIX ---
WORD_CATEGORIES = {
    "Animals": ["elephant", "giraffe", "dolphin", "penguin", "leopard"],
    "Programming": ["python", "variable", "compiler", "function", "database"],
    "Countries": ["brazil", "germany", "vietnam", "morocco", "australia"]
}

# 7-stage visual canvas rendering matrix based on remaining lives
HANGMAN_STAGES = [
    # 0 Lives: Head, Torso, Both Arms, Both Legs (Final Game Over)
    lambda c: (c.create_line(50, 180, 150, 180, width=3), c.create_line(100, 180, 100, 20, width=3),
               c.create_line(100, 20, 160, 20, width=3), c.create_line(160, 20, 160, 40, width=3),
               c.create_oval(145, 40, 175, 70, width=3), c.create_line(160, 70, 160, 120, width=3),
               c.create_line(160, 85, 135, 100, width=3), c.create_line(160, 85, 185, 100, width=3),
               c.create_line(160, 120, 135, 150, width=3), c.create_line(160, 120, 185, 150, width=3)),
    # 1 Life: Left Leg missing
    lambda c: (c.create_line(50, 180, 150, 180, width=3), c.create_line(100, 180, 100, 20, width=3),
               c.create_line(100, 20, 160, 20, width=3), c.create_line(160, 20, 160, 40, width=3),
               c.create_oval(145, 40, 175, 70, width=3), c.create_line(160, 70, 160, 120, width=3),
               c.create_line(160, 85, 135, 100, width=3), c.create_line(160, 85, 185, 100, width=3),
               c.create_line(160, 120, 135, 150, width=3)),
    # 2 Lives: Right Arm missing
    lambda c: (c.create_line(50, 180, 150, 180, width=3), c.create_line(100, 180, 100, 20, width=3),
               c.create_line(100, 20, 160, 20, width=3), c.create_line(160, 20, 160, 40, width=3),
               c.create_oval(145, 40, 175, 70, width=3), c.create_line(160, 70, 160, 120, width=3),
               c.create_line(160, 85, 135, 100, width=3), c.create_line(160, 85, 185, 100, width=3)),
    # 3 Lives: Left Arm missing
    lambda c: (c.create_line(50, 180, 150, 180, width=3), c.create_line(100, 180, 100, 20, width=3),
               c.create_line(100, 20, 160, 20, width=3), c.create_line(160, 20, 160, 40, width=3),
               c.create_oval(145, 40, 175, 70, width=3), c.create_line(160, 70, 160, 120, width=3),
               c.create_line(160, 85, 135, 100, width=3)),
    # 4 Lives: Torso missing
    lambda c: (c.create_line(50, 180, 150, 180, width=3), c.create_line(100, 180, 100, 20, width=3),
               c.create_line(100, 20, 160, 20, width=3), c.create_line(160, 20, 160, 40, width=3),
               c.create_oval(145, 40, 175, 70, width=3), c.create_line(160, 70, 160, 120, width=3)),
    # 5 Lives: Head missing
    lambda c: (c.create_line(50, 180, 150, 180, width=3), c.create_line(100, 180, 100, 20, width=3),
               c.create_line(100, 20, 160, 20, width=3), c.create_line(160, 20, 160, 40, width=3),
               c.create_oval(145, 40, 175, 70, width=3)),
    # 6 Lives: Base Stand Only (Initial State)
    lambda c: (c.create_line(50, 180, 150, 180, width=3), c.create_line(100, 180, 100, 20, width=3),
               c.create_line(100, 20, 160, 20, width=3), c.create_line(160, 20, 160, 40, width=3))
]

class DesktopHangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha Premium Hangman Console")
        self.root.geometry("620x500")
        self.root.configure(bg="#1e1e2e") # Modern dark workspace theme
        
        # Session Trackers
        self.wins = 0
        self.losses = 0
        self.lives = 6
        self.secret_word = ""
        self.guessed_letters = set()
        
        self._build_interface_layout()
        self.restart_game_round()

    def _build_interface_layout(self):
        # 1. Top Control Panel Dashboard
        self.top_frame = tk.Frame(self.root, bg="#252538", pady=10)
        self.top_frame.pack(fill="x", side="top")
        
        self.score_label = tk.Label(self.top_frame, text="WINS: 0 | LOSSES: 0", font=("Helvetica", 12, "bold"), fg="#a6e3a1", bg="#252538")
        self.score_label.pack(side="left", padx=20)
        
        # Category Selector Widget
        tk.Label(self.top_frame, text="Category:", fg="#cdd6f4", bg="#252538", font=("Helvetica", 10)).pack(side="left", padx=5)
        self.category_var = tk.StringVar(value="Animals")
        self.category_menu = tk.OptionMenu(self.top_frame, self.category_var, *WORD_CATEGORIES.keys(), command=lambda _: self.restart_game_round())
        self.category_menu.config(bg="#11111b", fg="#cdd6f4", highlightthickness=0)
        self.category_menu.pack(side="left", padx=5)

        # 2. Main Gameplay Split Panel Frame Layout
        self.main_pane = tk.Frame(self.root, bg="#1e1e2e")
        self.main_pane.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Drawing Canvas Layer (Left Side)
        self.canvas = tk.Canvas(self.main_pane, width=220, height=220, bg="#11111b", highlightthickness=1, highlightbackground="#45475a")
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        # Target Displays Frame Layer (Right Side)
        self.right_frame = tk.Frame(self.main_pane, bg="#1e1e2e")
        self.right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nw")
        
        self.word_display_lbl = tk.Label(self.right_frame, text="_ _ _ _ _", font=("Courier New", 26, "bold"), fg="#89b4fa", bg="#1e1e2e")
        self.word_display_lbl.pack(anchor="w", pady=10)
        
        self.lives_label = tk.Label(self.right_frame, text="Remaining Attempts: 6", font=("Helvetica", 11), fg="#f38ba8", bg="#1e1e2e")
        self.lives_label.pack(anchor="w", pady=5)
        
        self.status_label = tk.Label(self.right_frame, text="Choose a letter below to play!", font=("Helvetica", 10, "italic"), fg="#a6adc8", bg="#1e1e2e")
        self.status_label.pack(anchor="w", pady=5)

        # 3. Alphabet Graphical Input Matrix Button Layout
        self.keyboard_frame = tk.Frame(self.root, bg="#1e1e2e", pady=10)
        self.keyboard_frame.pack(fill="x", side="bottom", padx=20)
        
        self.button_references = {}
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for index, letter in enumerate(alphabet):
            btn = tk.Button(self.keyboard_frame, text=letter, width=3, height=1, font=("Helvetica", 10, "bold"),
                            bg="#313244", fg="#cdd6f4", activebackground="#89b4fa", relief="flat",
                            command=lambda l=letter: self.process_letter_entry(l))
            # Form grid coordinates safely inside layout matrix
            btn.grid(row=index // 13, column=index % 13, padx=3, pady=3)
            self.button_references[letter] = btn

    def restart_game_round(self):
        """Clears states and resets the dashboard layout for a new match round."""
        category = self.category_var.get()
        self.secret_word = random.choice(WORD_CATEGORIES[category]).upper()
        self.guessed_letters.clear()
        self.lives = 6
        
        # Reset visual labels
        self.lives_label.config(text=f"Remaining Attempts: {self.lives}")
        self.status_label.config(text="New round started! Make a guess.", fg="#a6adc8")
        self.score_label.config(text=f"WINS: {self.wins} | LOSSES: {self.losses}")
        
        # Refresh the drawing canvas frame matrix
        self.canvas.delete("all")
        HANGMAN_STAGES[-1](self.canvas)
        
        # Re-enable all matrix entry keyboard buttons
        for btn in self.button_references.values():
            btn.config(state="normal", bg="#313244", fg="#cdd6f4")
            
        self._refresh_word_mask_view()

    def _refresh_word_mask_view(self):
        """Dynamically builds the obscured target underline map template."""
        mask = [char if char in self.guessed_letters else "_" for char in self.secret_word]
        self.word_display_lbl.config(text=" ".join(mask))
        
        # Check Win state parameters
        if "_" not in mask:
            self.wins += 1
            self.score_label.config(text=f"WINS: {self.wins} | LOSSES: {self.losses}")
            messagebox.showinfo("🎉 Victory!", f"Excellent work! You guessed the word: {self.secret_word}")
            self.restart_game_round()

    def process_letter_entry(self, character):
        """Processes the state engine loop triggers when a user interacts with a GUI button."""
        self.guessed_letters.add(character)
        self.button_references[character].config(state="disabled", bg="#11111b", fg="#45475a") # Block reuse
        
        if character in self.secret_word:
            self.status_label.config(text=f"✅ Accurate! Letter '{character}' is inside the target string sequence.", fg="#a6e3a1")
            self._refresh_word_mask_view()
        else:
            self.lives -= 1
            self.lives_label.config(text=f"Remaining Attempts: {self.lives}")
            self.status_label.config(text=f"❌ Miss! Letter '{character}' is incorrect.", fg="#f38ba8")
            
            # Re-draw hangman parts dynamically
            self.canvas.delete("all")
            HANGMAN_STAGES[self.lives](self.canvas)
            
            # Check Defeat state parameters
            if self.lives <= 0:
                self.losses += 1
                self.score_label.config(text=f"WINS: {self.wins} | LOSSES: {self.losses}")
                messagebox.showerror("💀 Defeat!", f"Out of turns! The target answer was: {self.secret_word}")
                self.restart_game_round()

if __name__ == "__main__":
    app_window = tk.Tk()
    desktop_engine = DesktopHangmanApp(app_window)
    app_window.mainloop()
