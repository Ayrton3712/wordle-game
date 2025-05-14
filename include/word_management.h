#ifndef WORD_MANAGEMENT_H
#define WORD_MANAGEMENT_H

#include <string>           // To use strings
#include <unordered_set>    // To use unordered_set

using namespace std;

class WordManager{
private:
    unordered_set<string> validWords;

public:
    bool loadValidWords(); // Loads valid 5-letter words from a file

    bool isValidWord(const string& word); // Checks if a word is in the set

    string chooseTargetWord(); // Chooses a random word from the set
};

#endif