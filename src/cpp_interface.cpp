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

    std::string guess;
    std::string target = manager.chooseTargetWord();
    int attempts = 0;
    const int max_attempts = 6;

    while (true) {
        std::getline(std::cin, guess);

        if (guess == "EXIT") break;
        if (guess == "RESET") {
            target = manager.chooseTargetWord();
            attempts = 0;
            continue;
        }

        std::transform(guess.begin(), guess.end(), guess.begin(), ::tolower);
        std::transform(target.begin(), target.end(), target.begin(), ::tolower);

        if (guess.length() != 5) {
            std::cout << "ERROR:INVALID_LENGTH" << std::endl;
            continue;
        }

        std::vector<int> result = evaluateGuess(guess, target);

        for (int val : result) std::cout << val;
        std::cout << std::endl;

        if (result == std::vector<int>{2, 2, 2, 2, 2}) {
            std::cout << "WIN" << std::endl;
            std::cout.flush();
            continue;
        }

        attempts++;
        if (attempts == max_attempts) {
            std::cout << "LOSE:" << target << std::endl;
            std::cout.flush();
            continue;
        }
    }

    return 0;
}