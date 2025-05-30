import tkinter as tk
from tkinter import messagebox
import subprocess
import random
import os

ROWS = 6
COLS = 5
# hola test
# test edna
# Get the directory of this script (gui/)
SCRIPT_DIR = os.path.dirname(__file__)
WORDS_PATH = os.path.join(SCRIPT_DIR, "../words.txt")
CPP_EXEC_PATH = os.path.join(SCRIPT_DIR, "../wordle_cpp_bridge.exe")

# Load valid words from words.txt
with open(WORDS_PATH, "r") as f:
    VALID_WORDS = [word.strip().lower() for word in f if len(word.strip()) == 5]

# Randomly choose a target word
TARGET_WORD = random.choice(VALID_WORDS)

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle GUI")
        self.grid = []
        self.current_row = 0

        self.setup_grid()
        self.setup_input()

    def setup_grid(self):
        for row in range(ROWS):
            row_cells = []
            for col in range(COLS):
                label = tk.Label(self.root, text="", width=4, height=2,
                                 font=("Helvetica", 24), relief="solid", borderwidth=1)
                label.grid(row=row, column=col, padx=5, pady=5)
                row_cells.append(label)
            self.grid.append(row_cells)

    def setup_input(self):
        self.entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.entry.grid(row=ROWS, column=0, columnspan=COLS-1, padx=5, pady=10)
        self.entry.bind("<Return>", lambda event: self.submit_guess())

        submit_btn = tk.Button(self.root, text="Submit", command=self.submit_guess, font=("Helvetica", 14))
        submit_btn.grid(row=ROWS, column=COLS-1, padx=5)

    def submit_guess(self):
        guess = self.entry.get().lower()
        if len(guess) != 5:
            messagebox.showerror("Error", "Please enter a 5-letter word.")
            return

        feedback = self.get_feedback_from_cpp(guess, TARGET_WORD)
        if feedback is None:
            messagebox.showerror("Error", "Something went wrong with the C++ logic.")
            return

        for i, val in enumerate(feedback):
            label = self.grid[self.current_row][i]
            label.config(text=guess[i].upper())
            if val == 2:
                label.config(bg="green", fg="white")
            elif val == 1:
                label.config(bg="yellow", fg="black")
            else:
                label.config(bg="gray", fg="white")

        self.entry.delete(0, tk.END)
        self.current_row += 1

        if feedback == [2, 2, 2, 2, 2]:
            messagebox.showinfo("Congratulations!", "You guessed the word!")
            self.root.quit()
        elif self.current_row >= ROWS:
            messagebox.showinfo("Game Over", f"Out of attempts! The word was: {TARGET_WORD}")
            self.root.quit()

    def get_feedback_from_cpp(self, guess, target):
        try:
            process = subprocess.Popen([
                CPP_EXEC_PATH
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)

            input_data = f"{guess} {target}\n"
            stdout, stderr = process.communicate(input=input_data)

            if stderr:
                print("C++ Error:", stderr)
                return None

            return [int(c) for c in stdout.strip() if c.isdigit()]

        except Exception as e:
            print("Error running subprocess:", e)
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()