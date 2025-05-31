#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "../include/word_management.h"
#include "../include/word_comparison.h"

int main() {
    WordManager manager;
    if (!manager.loadValidWords()) {
        std::cout << "ERROR: Could not load word list." << std::endl;
        return 1;
    }

    std::string target = manager.chooseTargetWord();
    int attempts = 0;
    const int max_attempts = 6;

    while (attempts < max_attempts) {
        std::string guess;
        std::getline(std::cin, guess);

        // Clean input
        std::transform(guess.begin(), guess.end(), guess.begin(), ::tolower);

        if (guess.length() != 5) {
            std::cout << "ERROR:INVALID_LENGTH" << std::endl;
            continue;
        }

        if (!manager.isValidWord(guess)) {
            std::cout << "00000" << std::endl;  // All gray
            attempts++;  // ✅ Count the guess
            if (attempts == max_attempts) {
                std::cout << "LOSE:" << target << std::endl;
            }
            continue;
        }

        std::vector<int> result = evaluateGuess(guess, target);

        // Output feedback digits as string
        for (int val : result) {
            std::cout << val;
        }
        std::cout << std::endl;

        if (result == std::vector<int>{2, 2, 2, 2, 2}) {
            std::cout << "WIN" << std::endl;
            break;
        }

        attempts++;

        if (attempts == max_attempts) {
            std::cout << "LOSE:" << target << std::endl;
            break;
        }
    }

    return 0;
}