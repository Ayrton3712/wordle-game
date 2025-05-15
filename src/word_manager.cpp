#include <iostream>                      // For I/O
#include <vector>                        // For vectors
#include <string>                        // For strings
#include <limits>                        // For input stream handling

#include "../include/game_manager.h"	 // Contains class declaration
#include "../include/word_comparison.h"  // Custom header
#include "../include/display.h"          // Custom header

using namespace std;

string GameManager::getUserGuess() {
    string guess;
	
    while (true) {
        cout << "Enter a 5-letter word: ";
        cin >> guess;

        if (guess.length() != 5) {
            cout << "Invalid input. Please enter exactly 5 letters.\n";
            // Clear input state and discard bad input
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }
        break;
    }
    return guess;
}

void GameManager::gameLoop() {
    for (int i = 0; i < 6; i++) {
        cout << "\nAttempt " << (i + 1) << " of 6" << endl;

        string guess = getUserGuess();
        vector<int> evaluation = evaluateGuess(guess); // Assume this takes a guess and returns feedback

        displayFeedback(); // You'll probably want to pass guess & evaluation here for a real display

        if (evaluation == vector<int>{2, 2, 2, 2, 2}) {
            cout << "You have won the game!" << endl;
            return;
        }
    }
    cout << "You are out of tries! Try again? (Y/N): ";
    char choice;
    cin >> choice;
    if (choice == 'Y' || choice == 'y') {
        gameLoop();
    } else {
        cout << "Thanks for playing!" << endl;
    }
}
