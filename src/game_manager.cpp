#include <iostream>                      // For I/O
#include <vector>                        // For vectors
#include <string>                        // For strings
#include <limits>                        // For input stream handling

#include "../include/game_manager.h"	 // Contains class declaration
#include "../include/word_comparison.h"  // To use evaluateGuess
#include "../include/word_management.h" // To use the WordManager class

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
    WordManager manager;
    if (!manager.loadValidWords()) {
        std::cerr << "Could not load word list.\n";
        return;
    }

    std::string target = manager.chooseTargetWord();

    for (int i = 0; i < 6; i++) {
        std::cout << "\nAttempt " << (i + 1) << " of 6" << std::endl;

        std::string guess = getUserGuess();
        std::vector<int> evaluation = evaluateGuess(guess, target);

        // GUI will use this later
        // displayFeedback(guess, evaluation);

        if (evaluation == std::vector<int>{2, 2, 2, 2, 2}) {
            std::cout << "You have won the game!" << std::endl;
            return;
        }
    }

    std::cout << "You are out of tries! Try again? (Y/N): ";
    char choice;
    std::cin >> choice;
    if (choice == 'Y' || choice == 'y') {
        gameLoop();
    } else {
        std::cout << "Thanks for playing!" << std::endl;
    }
}
