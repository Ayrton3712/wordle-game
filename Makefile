# Builds two executables from the same C++ engine:
# wordle                - CLI version (main.cpp), runs in the terminal
# gui/wordle_cpp_bridge	- Subprocess used by the Python GUI (cpp_interface.cpp)

CXX      := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -O2 -Iinclude

# Shared engine sources used by both binaries
CORE_SRC := src/game_manager.cpp src/word_comparison.cpp src/word_management.cpp

# Platform-appropriate executable extension (.exe on Windows, empty elsewhere)
ifeq ($(OS),Windows_NT)
    EXE_EXT := .exe
else
    EXE_EXT :=
endif

CLI_BIN    := wordle$(EXE_EXT)
BRIDGE_BIN := wordle_cpp_bridge$(EXE_EXT)

.PHONY: all cli bridge run-cli run-gui clean

# Default target: build everything the GUI needs plus the CLI
all: $(CLI_BIN) gui/$(BRIDGE_BIN) gui/words.txt

# Build targets

# CLI version
$(CLI_BIN): main.cpp $(CORE_SRC)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Bridge version
gui/$(BRIDGE_BIN): src/cpp_interface.cpp $(CORE_SRC)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Stage the word list next to the bridge (child process's cwd is gui/)
gui/words.txt: words.txt
	cp $< $@

# Convenience aliases

cli:    $(CLI_BIN)
bridge: gui/$(BRIDGE_BIN) gui/words.txt

# Run helpers

run-cli: $(CLI_BIN)
	./$(CLI_BIN)

run-gui: bridge
	cd gui && python3 wordle_gui.py

# Cleanup

clean:
	rm -f $(CLI_BIN) gui/$(BRIDGE_BIN) gui/words.txt
	rm -rf gui/__pycache__