import subprocess, os, sys, platform

def resource_path(rel):
    """Return absolute path to resource, for use with PyInstaller"""
    if getattr(sys, 'frozen', False):             # running as exe
        base = sys._MEIPASS                       # temp dir created by PyInstaller
    else:
        base = os.path.dirname(__file__)          # folder of this .py
    return os.path.abspath(os.path.join(base, rel))

CPP_PATH = resource_path("wordle_cpp_bridge.exe")

class CppBridge:
    def __init__(self):
        if not os.path.exists(CPP_PATH):
            sys.exit(f"Bridge executable not found: {CPP_PATH}")

        kw = {}
        if platform.system() == "Windows":
            kw["creationflags"] = subprocess.CREATE_NO_WINDOW  # hide console

        self.proc = subprocess.Popen(
            [CPP_PATH],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            **kw
        )

    # -------- high-level protocol helpers --------
    def send_guess(self, word:str) -> str:
        """Send a 5-letter guess - return feedback digits (always 5 chars)."""
        self._writeline(word)
        return self._readline()

    def read_status(self) -> str:
        """Read the next line (WIN / LOSE:<word> / READY)."""
        return self._readline()

    def reset_game(self):
        self._writeline("RESET")
        _ = self._readline()      # consumes READY

    def close(self):
        try:  self._writeline("EXIT")
        except BrokenPipeError:
            pass
        self.proc.terminate()

    # -------- low-level ----------
    def _writeline(self, s:str):
        self.proc.stdin.write(s + "\n")
        self.proc.stdin.flush()

    def _readline(self) -> str:
        return self.proc.stdout.readline().strip()