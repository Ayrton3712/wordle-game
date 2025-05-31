import tkinter as tk
from tkinter import messagebox
import subprocess
import os

ROWS = 6
COLS = 5

# Get the directory of this script (gui/)
SCRIPT_DIR = os.path.dirname(__file__)
CPP_EXEC_PATH = os.path.join(SCRIPT_DIR, "../wordle_cpp_bridge.exe")

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle GUI")
        self.grid = []
        self.current_row = 0
        self.play_again_btn = None

        self.setup_grid()
        self.setup_input()
        self.cpp_process = subprocess.Popen([
            CPP_EXEC_PATH
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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

        try:
            self.cpp_process.stdin.write(guess + "\n")
            self.cpp_process.stdin.flush()

            feedback_line = self.cpp_process.stdout.readline().strip()

            if feedback_line.startswith("ERROR"):
                if "INVALID_WORD" in feedback_line:
                    messagebox.showerror("Error", "That word is not in the list.")
                elif "INVALID_LENGTH" in feedback_line:
                    messagebox.showerror("Error", "Word must be 5 letters.")
                return

            if feedback_line == "WIN":
                self.play_again_prompt("Congratulations! You guessed the word!")
                return
            elif feedback_line.startswith("LOSE"):
                target = feedback_line.split(":")[1]
                self.play_again_prompt(f"Out of attempts! The word was: {target}")
                return

            feedback = [int(c) for c in feedback_line if c.isdigit()]

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

        except Exception as e:
            messagebox.showerror("Error", f"Subprocess communication failed: {e}")

    def reset_game(self):
        self.current_row = 0
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.play_again_btn.grid_forget()

        for row in self.grid:
            for label in row:
                label.config(text="", bg=self.root.cget('bg'), fg="black")

        # Restart subprocess
        self.cpp_process.kill()
        self.cpp_process = subprocess.Popen([
            CPP_EXEC_PATH
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def play_again_prompt(self, message):
        messagebox.showinfo("Game Over", message)
        self.entry.config(state=tk.DISABLED)
        self.play_again_btn = tk.Button(self.root, text="Play Again", command=self.reset_game, font=("Helvetica", 14))
        self.play_again_btn.grid(row=ROWS + 1, column=0, columnspan=COLS, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()
