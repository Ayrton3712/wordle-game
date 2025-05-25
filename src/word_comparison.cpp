#include "../include/word_comparison.h" // To define evaluateGuess
#include "../include/word_management.h" // To use chooseTargetWord

#include <vector>
#include <string>
#include <iostream>

using namespace std;

vector<int> evaluateGuess(const string& guess) {
    const int GREEN = 2; // Code for Green: correct letter, correct position
    const int YELLOW = 1; // Code for Yellow: correct letter, wrong position
    const int GRAY = 0; // Code for Gray: wrong letter

    string targetWord = "apple"; // Change later for full integration
    vector<int> feedback(5, GRAY); // Default all to GRAY
    vector<bool> usedInTarget(5, false); // Track matched letters in target

    // First pass: Mark GREEN
    for (int i = 0; i < 5; ++i) {
        if (guess[i] == targetWord[i]) {
            feedback[i] = GREEN;
            usedInTarget[i] = true;
        }
    }

    // Second pass: Mark YELLOW
    for (int i = 0; i < 5; ++i) {
        if (feedback[i] == GREEN) continue;

        for (int j = 0; j < 5; ++j) {
            if (!usedInTarget[j] && guess[i] == targetWord[j]) {
                feedback[i] = YELLOW;
                usedInTarget[j] = true;
                break;
            }
        }
    }

    return feedback;
}

/*// main function to test evaluateGuess
int main(){ 
    string guess = "crane";

    vector<int> feedback = evaluateGuess(guess);

    for (int i = 0; i < feedback.size(); i++){
        cout << feedback[i] << " ";
    }

    return 0;
}*/