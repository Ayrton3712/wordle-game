# wordle_gui.py

import tkinter as tk
from tkinter import messagebox
import os, sys
from cpp_bridge import CppBridge

ROWS, COLS = 6, 5  # Number of guesses (rows) and letters per word (columns)

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle")
        self.bridge = CppBridge() # Start the C++ backend engine

        # Game state variables
        self.grid_widgets = []    # Stores label widgets for the grid
        self.row          = 0     # Current guess row
        self.game_over    = False # Game over flag

        # Build the UI
        self._build_grid()
        self._build_input()
        self._center_window()
        self._show_intro()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------- UI builders ----------
    def _build_grid(self):
        # Create a grid of labels for guesses and feedback
        for r in range(ROWS):
            row=[]
            for c in range(COLS):
                lbl = tk.Label(self.root, width=4, height=2,
                               font=("Consolas", 24), relief="solid")
                lbl.grid(row=r, column=c, padx=3, pady=3)
                row.append(lbl)
            self.grid_widgets.append(row)

    def _build_input(self):
        # Entry widget for user input
        self.entry = tk.Entry(self.root, font=("Consolas", 16))
        self.entry.grid(row=ROWS, column=0, columnspan=COLS-1,
                        padx=5, pady=10)
        self.entry.bind("<Return>", lambda _e: self.submit())

        # Submit button
        self.submit_btn = tk.Button(self.root, text="Submit",
                                    command=self.submit)
        self.submit_btn.grid(row=ROWS, column=COLS-1, padx=5)

    # ---------- main turn ----------
    def submit(self):
        # Handle guess submission
        if self.game_over:
            return
        
        guess = self.entry.get().lower()
        
        # Validate input length
        if len(guess) != 5:
            messagebox.showerror("Error", "Enter 5 letters")
            return
        
        # Validate input characters
        if not guess.isalpha():
            messagebox.showerror("Error", "Only A-Z characters are allowed")
            return

        self.entry.delete(0, tk.END)

        # Send guess to C++ backend and get feedback
        digits = self.bridge.send_guess(guess)
        if not (len(digits)==5 and all(ch in "012" for ch in digits)):
            messagebox.showerror("Error", f"Unexpected reply: {digits}"); return

        # Paint feedback row
        if self.row < ROWS:
            self._paint_row(guess, [int(x) for x in digits])
            self.row += 1

        # Check for win or lose
        status = ""
        if digits == "22222":
            status = self.bridge.read_status()      # WIN
        elif self.row == ROWS:
            status = self.bridge.read_status()      # LOSE:<word>

        if status == "WIN":
            self._game_end("You guessed the word!")
        elif status.startswith("LOSE"):
            tgt = status.split(":",1)[1]
            self._game_end(f"Out of attempts!\nThe word was: {tgt}")

    # ---------- helpers ----------
    def _paint_row(self, word, fb):
        # Color the row based on feedback
        for i,(ch,val) in enumerate(zip(word, fb)):
            lbl = self.grid_widgets[self.row][i]
            lbl["text"] = ch.upper()
            if   val==2: lbl.config(bg="green",  fg="white")   # Correct letter and position
            elif val==1: lbl.config(bg="yellow", fg="black")   # Correct letter, wrong position
            else:        lbl.config(bg="red",    fg="white")   # Incorrect letter

    def _game_end(self, msg):
        # End the game and show message
        self.game_over = True
        messagebox.showinfo("Game Over", msg)
        self.entry.grid_remove()
        self.submit_btn.grid_remove()

        # Show play again button
        self.play_btn = tk.Button(self.root, text="Play Again",
                                  command=self._reset)
        self.play_btn.grid(row=ROWS, column=0, columnspan=COLS, pady=8)

    def _reset(self):
        # Reset the game state and UI for a new game
        for row in self.grid_widgets:
            for lbl in row:
                lbl.config(text="", bg=self.root["bg"])
        self.row = 0
        self.game_over = False

        self.play_btn.destroy()
        self.entry.grid(row=ROWS, column=0, columnspan=COLS-1, padx=5, pady=10)
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.submit_btn.grid(row=ROWS, column=COLS-1, padx=5)

        self.bridge.reset_game()
        self.entry.focus_set()

    # ---------- misc ----------
    def _show_intro(self):
        # Show instructions at the start
        messagebox.showinfo(
            "Welcome to Wordle!",
            "You have to guess a five-letter word.\n\n"
            "Feedback for each guess:\n"
            "  • Green  - correct letter & position\n"
            "  • Yellow - letter in word but wrong spot\n"
            "  • Red    - letter not in the word\n\n"
            "Good luck!"
        )

    def _on_close(self):
        # Handle window close event
        try: self.bridge.close()
        except: pass
        self.root.destroy()

    def _center_window(self):
        # Center the window on the screen
        self.root.update_idletasks()
        w,h = self.root.winfo_width(), self.root.winfo_height()
        sw,sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x,y = (sw-w)//2, (sh-h)//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

# ---------- launch ----------
if __name__ == "__main__":
    root = tk.Tk()
    WordleGUI(root)
    root.mainloop()