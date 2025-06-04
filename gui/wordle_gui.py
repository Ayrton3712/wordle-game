import tkinter as tk
from tkinter import messagebox
import subprocess, os, sys

ROWS, COLS = 6, 5
SCRIPT_DIR   = os.path.dirname(__file__)
CPP_PATH     = os.path.join(SCRIPT_DIR, "../wordle_cpp_bridge.exe")

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle")
        self.grid  = []
        self.row   = 0
        self.game_over = False
        self._build_grid()
        self._build_input()
        self._start_cpp()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._center_window()

    # ───────────────────── C++ process ─────────────────────
    def _start_cpp(self):
        self.cpp = subprocess.Popen([CPP_PATH], text=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

    def _send(self, line:str) -> str:
        """Send a line to C++ and return a single response line."""
        self.cpp.stdin.write(line + "\n")
        self.cpp.stdin.flush()
        return self.cpp.stdout.readline().strip()

    # ───────────────────── GUI widgets ─────────────────────
    def _build_grid(self):
        for r in range(ROWS):
            row=[]
            for c in range(COLS):
                lbl = tk.Label(self.root, width=4, height=2,
                               font=("Consolas", 24), relief="solid")
                lbl.grid(row=r, column=c, padx=3, pady=3)
                row.append(lbl)
            self.grid.append(row)

    def _build_input(self):
        self.entry = tk.Entry(self.root, font=("Consolas", 16))
        self.entry.grid(row=ROWS, column=0, columnspan=COLS-1, padx=5, pady=10)
        self.entry.bind("<Return>", lambda e: self.submit())
        tk.Button(self.root, text="Submit", command=self.submit
                  ).grid(row=ROWS, column=COLS-1, padx=5)

    # ───────────────────── game flow ─────────────────────
    def submit(self):
        if self.game_over: return
        guess = self.entry.get().lower()
        if len(guess)!=5:
            messagebox.showerror("Error","Enter 5 letters"); return
        self.entry.delete(0, tk.END)

        while True:
            line = self._send(guess)
            if len(line) == 5 and all(ch in "012" for ch in line):
                break                       # got full feedback
            # otherwise loop again (it might be a partial flush)
        if line.startswith("ERROR"):
            messagebox.showerror("Error", line); return

        if all(ch in "012" for ch in line):          # feedback digits
            self._paint_row(guess, [int(x) for x in line])
            self.row += 1
            if self.row==ROWS:                       # fell off grid
                line = self._send("RESET")           # force C++ reset
        if line=="WIN":
            self._game_end("You guessed the word!")
        elif line.startswith("LOSE"):
            tgt = line.split(":",1)[1]
            self._game_end(f"Out of attempts!\nThe word was: {tgt}")

    def _paint_row(self, word, fb):
        for i,(ch,val) in enumerate(zip(word,fb)):
            lbl = self.grid[self.row][i]
            lbl["text"]=ch.upper()
            if val==2: lbl["bg"]="green";  lbl["fg"]="white"
            elif val==1: lbl["bg"]="yellow"
            else: lbl["bg"]="red";        lbl["fg"]="white"

    def _game_end(self, msg):
        self.game_over=True
        messagebox.showinfo("Game Over", msg)
        tk.Button(self.root, text="Play Again", command=self._reset
                  ).grid(row=ROWS+1,column=0,columnspan=COLS, pady=8)

    def _reset(self):
        # clear board
        for row in self.grid:
            for lbl in row: lbl.config(text="", bg=self.root["bg"])
        self.row=0; self.game_over=False; self.entry.config(state="normal")
        self._send("RESET")

    def _on_close(self):
        try: self._send("EXIT")
        except: pass
        self.root.destroy()

    def _center_window(self):
        # Ask Tk to center the toplevel on the screen
        try:
            self.root.tk.call('tk', 'scaling')          # ensures Tk has initialized
            self.root.eval('tk::PlaceWindow . center')
        except tk.TclError:
            # Fallback to manual math if older Tcl
            self._center_manual()

# ────────────────────────── run ──────────────────────────
if __name__ == "__main__":
    if not os.path.exists(CPP_PATH):
        sys.exit(f"❌ {CPP_PATH} not found. Compile C++ first.")
    root = tk.Tk()
    WordleGUI(root)
    root.mainloop()
