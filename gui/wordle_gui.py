import tkinter as tk
from tkinter import messagebox
import subprocess, os, sys

ROWS, COLS = 6, 5
SCRIPT_DIR = os.path.dirname(__file__)
CPP_PATH   = os.path.join(SCRIPT_DIR, "../wordle_cpp_bridge.exe")

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle")

        # state
        self.grid_widgets = []
        self.row          = 0
        self.game_over    = False

        # build ui
        self._build_grid()
        self._build_input()
        self._start_cpp()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._center_window()

        # ────────── show welcome instructions ──────────
        messagebox.showinfo(
            "Welcome to Wordle!",
            "You have to guess a five-letter word.\n\n"
            "Feedback for each guess:\n"
            "  • Green  – letter is in the word and in the correct position\n"
            "  • Yellow – letter is in the word but in the wrong position\n"
            "  • Red    – letter is nowhere in the word\n\n"
            "Good luck!"
        )

    # ────────── C++ helpers ──────────
    def _start_cpp(self):
        self.cpp = subprocess.Popen([CPP_PATH],
                                    text=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

    def _send(self, line:str) -> str:
        self.cpp.stdin.write(line + "\n")
        self.cpp.stdin.flush()
        return self.cpp.stdout.readline().strip()   # exactly 1 line

    # ────────── build ui ──────────
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

    # ────────── main turn ──────────
    def submit(self):
        if self.game_over: return
        guess = self.entry.get().lower()
        if len(guess)!=5:
            messagebox.showerror("Error","Enter 5 letters")
            return
        self.entry.delete(0, tk.END)

        # first reply = 5 digits
        digits = self._send(guess)
        if digits.startswith("ERROR"):
            messagebox.showerror("Error", digits); return
        if not (len(digits)==5 and all(ch in "012" for ch in digits)):
            messagebox.showerror("Error", f"Unexpected reply: {digits}"); return

        # paint
        if self.row < ROWS:
            self._paint_row(guess, [int(x) for x in digits])
            self.row += 1

        # check if game should be over and read 2nd line only then
        status = ""
        if digits == "22222":
            status = self.cpp.stdout.readline().strip()   # expect WIN
        elif self.row == ROWS:        # used all rows -> expect LOSE
            status = self.cpp.stdout.readline().strip()

        if status == "WIN":
            self._game_end("You guessed the word!")
        elif status.startswith("LOSE"):
            tgt = status.split(":",1)[1]
            self._game_end(f"Out of attempts!\nThe word was: {tgt}")

    # ────────── helpers ──────────
    def _paint_row(self, word, fb):
        for i,(ch,val) in enumerate(zip(word, fb)):
            lbl = self.grid_widgets[self.row][i]
            lbl["text"]=ch.upper()
            if   val==2: lbl.config(bg="green",  fg="white")
            elif val==1: lbl.config(bg="yellow", fg="black")
            else:        lbl.config(bg="red",    fg="white")

    def _game_end(self, msg):
        self.game_over = True
        messagebox.showinfo("Game Over", msg)

        # disable & hide entry + submit
        self.entry.config(state="disabled")
        self.entry.grid_remove()
        self.submit_btn.grid_remove()

        # show Play-Again button in the same row
        self.play_btn = tk.Button(self.root, text="Play Again",
                                  command=self._reset)
        self.play_btn.grid(row=ROWS, column=0, columnspan=COLS, pady=8)

    def _reset(self):
        # clear grid
        for row in self.grid_widgets:
            for lbl in row:
                lbl.config(text="", bg=self.root["bg"])
        self.row = 0
        self.game_over = False

        # remove Play-Again, restore entry+submit
        self.play_btn.destroy()
        self.entry.grid(row=ROWS, column=0, columnspan=COLS-1, padx=5, pady=10)
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.submit_btn.grid(row=ROWS, column=COLS-1, padx=5)

        # tell engine to pick new word, consume "READY"
        self._send("RESET")
        self.entry.focus_set() # give focus to the field

    # ────────── housekeeping ──────────
    def _on_close(self):
        try: self._send("EXIT")
        except: pass
        self.root.destroy()

    def _center_window(self):
        self.root.update_idletasks()
        w,h = self.root.winfo_width(), self.root.winfo_height()
        sw,sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x,y = (sw-w)//2, (sh-h)//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

# ────────── launch ──────────
if __name__ == "__main__":
    if not os.path.exists(CPP_PATH):
        sys.exit("Compile C++ bridge first.")
    root = tk.Tk()
    WordleGUI(root)
    root.mainloop()