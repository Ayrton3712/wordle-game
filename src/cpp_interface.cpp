#include <iostream>
#include <string>
#include <vector>
#include "../include/word_comparison.h"
#include "../include/word_management.h"

int main() {
    std::string guess;
    std::string target;

    // Read guess and target word from stdin
    std::cin >> guess >> target;

    // Validate length
    if (guess.length() != 5 || target.length() != 5) {
        std::cerr << "ERROR: Both guess and target must be 5-letter words." << std::endl;
        return 1;
    }

    // Evaluate the guess against the target
    std::vector<int> result = evaluateGuess(guess, target);

    // Output feedback as a string of digits (e.g. "20110")
    for (int val : result) {
        std::cout << val;
    }
    std::cout << std::endl;

    return 0;
}