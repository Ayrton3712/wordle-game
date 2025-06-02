#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "../include/word_management.h"
#include "../include/word_comparison.h"

// ───────────────────────────────────────────
// Protocol  (one line per response)
//
// 01201          ← 5 digits of feedback
// WIN            ← guess == target
// LOSE:<word>    ← ran out of tries
// ERROR:<reason> ← bad length, etc.
// READY          ← after RESET, engine ready
// (Engine never quits until it receives EXIT)
// ───────────────────────────────────────────

int main() {
    WordManager wm;
    if (!wm.loadValidWords()) {
        std::cout << "ERROR:wordlist" << std::endl;
        return 1;
    }

    std::string target = wm.chooseTargetWord();
    int tries = 0;
    const int MAX_TRIES = 6;

    for (std::string line; std::getline(std::cin, line); ) {

        // Special commands from GUI
        if (line == "EXIT") break;
        if (line == "RESET") {
            target = wm.chooseTargetWord();
            tries  = 0;
            std::cout << "READY" << std::endl;
            continue;
        }

        // Normalize guess
        std::string guess = line;
        std::transform(guess.begin(), guess.end(), guess.begin(), ::tolower);

        if (!wm.isValidWord(guess)) {                  // from word management
        std::cout << "ERROR:invalid" << std::endl;
        continue;
        }

        if (guess.size() != 5) {                       // wrong length
            std::cout << "ERROR:length" << std::endl;
            continue;
        }

        // Produce feedback
        std::vector<int> fb = evaluateGuess(guess, target);
        for (int v : fb) std::cout << v;
        std::cout << std::endl;

        if (fb == std::vector<int>{2,2,2,2,2}) {      // WIN!
            std::cout << "WIN" << std::endl;
            continue;                                 // wait for RESET / EXIT
        }

        ++tries;
        if (tries >= MAX_TRIES) {                     // out of attempts
            std::cout << "LOSE:" << target << std::endl;
            continue;                                 // wait for RESET / EXIT
        }
    }
    return 0;
}