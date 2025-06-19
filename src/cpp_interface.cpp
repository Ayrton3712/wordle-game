#include <iostream>                     // std::cin, std::cout, std::flush
#include <string>                       // std::string (lines, tags)
#include <vector>                       // To use the vector returned by processGuess

#include "../include/game_manager.h"    // To use GameManager's reset and processGuess)
#include "../include/word_management.h" // To use loadValidWords and chooseTargetWord

int main(){
    WordManager wm;                                         // Instantiating WordManager
    if (!wm.loadValidWords()){                              // Loading word file via loadValidWords()
        std::cout << "ERROR:init\n";                        // Sending ERROR via cout if load was unsuccessful
        return 1;
    }

    GameManager gm;                                         // Instantiating GameManager
    gm.reset(wm.chooseTargetWord());                        // Randomly choosing a target word with chooseTargetWord()

    std::string line;
    while (std::getline(std::cin, line)){                   // Loop to read messages from Python via getline and cin
        if (line=="EXIT") break;                            // If the incoming message is EXIT, break the loop
        if (line=="RESET"){                                 // If the incoming message is RESET, choose a new random word, send READY and restart the loop
            gm.reset(wm.chooseTargetWord());
            std::cout << "READY\n";
            continue;
        }

        std::string tag;
        std::vector<int> fb = gm.processGuess(line, tag);   // Store feedback vector for the guess from Python (stored in "line") and communication tag in "tag"

        for(int v : fb){                                    // Send each feedback digit to Python via cout
            std::cout << v;
        }
        std::cout << std::flush;                            // To ensure all 5 digits leave the pipe immediately
        std::cout << '\n';                                  // Terminating newline

        if(tag=="WIN"){                                     // If the tag is WIN, send it to Python via cout and restart the loop
            std::cout << "WIN\n";
            continue;
        }
        if(tag=="LOSE"){                                    // If the tag is LOSE, send it together with the target word to Python via cout and restart the loop
            std::cout << "LOSE:" << gm.getTarget() << "\n";
            continue;
        }
    }
    return 0;
}