# Wordle Game Project

This project implements the game Wordle using C++ for the core game logic and Python (Tkinter) for the graphical user interface.

## Structure
- `src/`: Contains all C++ source files
- `include/`: Header files for sharing functions across modules
- `gui/`: Python interface built with Tkinter

## How to Compile
```bash
g++ -std=c++17 -Iinclude src/*.cpp -o wordle
```

## How to Run GUI
```bash
python gui/wordle_gui.py
```
