# wordle_gui.py
import tkinter as tk
from tkinter import messagebox
import os, sys
from cpp_bridge import CppBridge

ROWS, COLS = 6, 5

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle")
        self.bridge = CppBridge() # start C++ engine

        # state
        self.grid_widgets = []
        self.row          = 0
        self.game_over    = False

        # ui
        self._build_grid()
        self._build_input()
        self._center_window()
        self._show_intro()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------- UI builders ----------
    def _build_grid(self):
        for r in range(ROWS):
            row=[]
            for c in range(COLS):
                lbl = tk.Label(self.root, width=4, height=2,
                               font=("Consolas", 24), relief="solid")
                lbl.grid(row=r, column=c, padx=3, pady=3)
                row.append(lbl)
            self.grid_widgets.append(row)

    def _build_input(self):
        self.entry = tk.Entry(self.root, font=("Consolas", 16))
        self.entry.grid(row=ROWS, column=0, columnspan=COLS-1,
                        padx=5, pady=10)
        self.entry.bind("<Return>", lambda _e: self.submit())

        self.submit_btn = tk.Button(self.root, text="Submit",
                                    command=self.submit)
        self.submit_btn.grid(row=ROWS, column=COLS-1, padx=5)

    # ---------- main turn ----------
    def submit(self):
        if self.game_over:
            return
        
        guess = self.entry.get().lower()
        
        if len(guess) != 5:
            messagebox.showerror("Error", "Enter 5 letters")
            return
        
        if not guess.isalpha():
            messagebox.showerror("Error", "Only A-Z characters are allowed")
            return

        self.entry.delete(0, tk.END)

        # feedback digits
        digits = self.bridge.send_guess(guess)
        if not (len(digits)==5 and all(ch in "012" for ch in digits)):
            messagebox.showerror("Error", f"Unexpected reply: {digits}"); return

        if self.row < ROWS:
            self._paint_row(guess, [int(x) for x in digits])
            self.row += 1

        # only read status line if game over conditions met
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
        for i,(ch,val) in enumerate(zip(word, fb)):
            lbl = self.grid_widgets[self.row][i]
            lbl["text"] = ch.upper()
            if   val==2: lbl.config(bg="green",  fg="white")
            elif val==1: lbl.config(bg="yellow", fg="black")
            else:        lbl.config(bg="red",    fg="white")

    def _game_end(self, msg):
        self.game_over = True
        messagebox.showinfo("Game Over", msg)
        self.entry.grid_remove()
        self.submit_btn.grid_remove()

        self.play_btn = tk.Button(self.root, text="Play Again",
                                  command=self._reset)
        self.play_btn.grid(row=ROWS, column=0, columnspan=COLS, pady=8)

    def _reset(self):
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
        try: self.bridge.close()
        except: pass
        self.root.destroy()

    def _center_window(self):
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