# ----------------------------------------------
# --------------- module imports ---------------
# ----------------------------------------------
import subprocess           # To create and control the child C++ process
import os, sys, platform    # To handle paths, program-exit, and OS detection

# ---------------------------------------------------------------------
# --------------- helper function to resolve data files ---------------
# ---------------------------------------------------------------------
# Returns an absolute path to rel for use with PyInstaller-generated .exe
def resource_path(rel):
    if getattr(sys, 'frozen', False):       # PyInstaller sets sys.frozen = True
        base = sys._MEIPASS                 # _MEIPASS: Temporary PyInstaller directory that holds bundled files
    else:
        base = os.path.dirname(__file__)    # Directory where this script resides
        
    return os.path.abspath(os.path.join(base, rel)) # Returns the absolute path

# Full path to the bundled C++ engine and its directory
_exe_name = "wordle_cpp_bridge.exe" if sys.platform == "win32" else "wordle_cpp_bridge"
CPP_PATH = resource_path(_exe_name)
CPP_DIR  = os.path.dirname(CPP_PATH)

# -----------------------------------------------
# --------------- CppBridge class ---------------
# -----------------------------------------------
class CppBridge:
    # -----------------------
    # ----- constructor -----
    # -----------------------
    def __init__(self):
        # Checking if the bridge .exe exists
        if not os.path.exists(CPP_PATH):
            sys.exit(f"Bridge executable not found: {CPP_PATH}")

        kwargs = {"cwd": CPP_DIR} # Run child in the folder that also contains words.txt

        # On Windows, stop the child from opening its own console window
        if platform.system() == "Windows":
            import subprocess as sp
            kwargs["creationflags"] = sp.CREATE_NO_WINDOW

        # Launching the child process with pipes for stdin and stdout
        self.proc = subprocess.Popen(
            [CPP_PATH],
            text=True,              # Communication with strings instead of bytes
            stdin=subprocess.PIPE,  # stdin pipe, parent keeps write end
            stdout=subprocess.PIPE, # stdout pipe, parent keeps read end
            **kwargs
        )

    # ------------------------------------
    # -------- high-level helpers --------
    # ------------------------------------
    def send_guess(self, word:str) -> str:
        """Send a 5-letter guess and return feedback digits (always 5 characterss)"""
        self._writeline(word)
        return self._readline()

    def read_status(self) -> str:
        """Read the next line (WIN / LOSE:<word> / READY)."""
        return self._readline()

    def reset_game(self):
        self._writeline("RESET")    # Sending RESET to child
        _ = self._readline()        # Consuming READY through dummy variable

    def close(self):
        try:  self._writeline("EXIT")   # Send EXIT to child
        except BrokenPipeError:         # If the BrokenPipeError exception occurs, terminate the program from the parent
            pass
        self.proc.terminate()

    # -----------------------------------
    # ---------- low-level I/O ----------
    # -----------------------------------
    def _writeline(self, s:str):
        """Write one line and flush"""
        self.proc.stdin.write(s + "\n")
        self.proc.stdin.flush()

    def _readline(self) -> str:
        """Read one full line and strip trailing newline"""
        return self.proc.stdout.readline().strip()