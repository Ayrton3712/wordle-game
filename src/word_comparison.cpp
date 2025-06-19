#include "../include/word_comparison.h" // To define evaluateGuess
#include <vector>                       // To use vectors
#include <string>                       // To use strings
#include <iostream>                     // Only used in the test main

// Compares the guess with the target and gives you feedback
// 2 = correct letter in correct position (GREEN)
// 1 = correct letter in wrong position (YELLOW)
// 0 = incorrect letter (RED)
std::vector<int> evaluateGuess(const std::string& guess, const std::string& target) {
    const int GREEN = 2;    // Code for Green: correct letter, correct position
    const int YELLOW = 1;   // Code for Yellow: correct letter, wrong position
    const int RED = 0;     // Code for Red: wrong letter

    std::vector<int> feedback(5, RED); // Creates a vector with 5 elements, all set to RED (0). This holds the feedback.
    std::vector<bool> usedInTarget(5, false); // Keeps track of which letters in the target word have been used (matched) during comparison.

    // First pass: Verify all correct letters are in correct position (GREEN)
    for (int i = 0; i < 5; ++i) {
        if (guess[i] == target[i]) {
            feedback[i] = GREEN;
            usedInTarget[i] = true;
        }
    }

    // Second pass: Verify correct letters are in the wrong position (YELLOW)
    for (int i = 0; i < 5; ++i) {
        if (feedback[i] == GREEN) continue; // Only check letters not already marked green

        for (int j = 0; j < 5; ++j) {
            if (!usedInTarget[j] && guess[i] == target[j]) {
                feedback[i] = YELLOW;
                usedInTarget[j] = true; // Mark the letter as used
                break;
            }
        }
    }

    return feedback;
}

/*// main function to test evaluateGuess
int main(){ 
    std::string guess = "crane";

    std::vector<int> feedback = evaluateGuess(guess, "apple");

    for (int i = 0; i < feedback.size(); i++){
        std::cout << feedback[i] << " ";
    }

    return 0;
}*/