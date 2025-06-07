import subprocess, os, sys

SCRIPT_DIR = os.path.dirname(__file__)
CPP_PATH   = os.path.join(SCRIPT_DIR, "../wordle_cpp_bridge.exe")

class CppBridge:
    """Starts the C++ engine and offers send()/close() helpers."""

    def __init__(self):
        if not os.path.exists(CPP_PATH):
            sys.exit(f"Bridge executable not found: {CPP_PATH}")
        self.proc = subprocess.Popen(
            [CPP_PATH],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
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