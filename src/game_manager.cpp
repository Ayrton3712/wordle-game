#include <iostream>                      // For I/O
#include <vector>                        // For vectors
#include <string>                        // For strings
#include <limits>                        // For input stream handling

#include "../include/game_manager.h"	 // Contains class declaration
#include "../include/word_comparison.h"  // To use evaluateGuess
#include "../include/word_management.h" // To use the WordManager class

std::string GameManager::getUserGuess(){
    std::string guess;
	
    while (true) {
        std::cout << "Enter a 5-letter word: ";
        std::cin >> guess;

        if (guess.length() != 5) {
            std::cout << "Invalid input. Please enter exactly 5 letters.\n";
            // Clear input state and discard bad input
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
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

// Resets target and attempts for a new round
void GameManager::reset(const std::string& newTarget){
    target = newTarget;
    attempts = 0;
}

// Processes the guess, encodes it into resultTag, and returns feedback vector
std::vector<int> GameManager::processGuess(const std::string& guess, std::string& resultTag){
    std::vector<int> feedback = evaluateGuess(guess, target);
    attempts++;
    resultTag.clear(); // Clears the string

    // resultTag = ""     -> normal turn
    // resultTag = "WIN"  -> guessed it
    // resultTag = "LOSE" -> out of tries

    if (feedback == std::vector<int>{2, 2, 2, 2, 2}){
        resultTag = "WIN";
    }
    else if (attempts >= 6){
        resultTag = "LOSE";
    }

    return feedback;
}

// Getter for the target
const std::string& GameManager::getTarget() const{
    return target;
}