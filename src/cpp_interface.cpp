#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "../include/game_manager.h"
#include "../include/word_management.h"
#include "../include/word_comparison.h"

// ───────────────────────────────────────────
// Protocol  (one line per response)
//
// 01201          <- 5 digits of feedback
// WIN            <- guess == target
// LOSE:<word>    <- ran out of tries
// ERROR:<reason> <- bad length, etc.
// READY          <- after RESET, engine ready
// (Engine never quits until it receives EXIT)
// ───────────────────────────────────────────

int main() {
    WordManager wm;
    if (!wm.loadValidWords()){
        std::cout << "ERROR:init\n";
        return 1;
    }

    GameManager gm;
    gm.reset(wm.chooseTargetWord());

    std::string line;
    while (std::getline(std::cin, line)){
        if (line=="EXIT") break;
        if (line=="RESET"){
            gm.reset(wm.chooseTargetWord());
            std::cout<<"READY\n";
            continue;
        }

        std::string tag;
        auto fb = gm.processGuess(line, tag);

        for(int v : fb){
            std::cout << v;
        }
        std::cout << std::flush; // To ensure all 5 digits leave the pipe
        std::cout << '\n';

        if(tag=="WIN"){
            std::cout << "WIN\n";
            continue;
        }
        if(tag=="LOSE"){
            std::cout << "LOSE:" << gm.getTarget() << "\n";
            continue;
        }
    }
    return 0;
}