#ifndef WORD_MANAGEMENT_H
#define WORD_MANAGEMENT_H

#include <string>           // To use strings
#include <unordered_set>    // To use unordered_set

class WordManager{
private:
    std::unordered_set<std::string> validWords;

public:
    bool loadValidWords(); // Loads valid 5-letter words from a file

    bool isValidWord(const std::string& word); // Checks if a word is in the set

    std::string chooseTargetWord(); // Chooses a random word from the set
};

#endif