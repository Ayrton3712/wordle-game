#include <string>           // To use strings
#include <cstdlib>          // To use rand(), srand()
#include <ctime>            // To use time()
#include <fstream>          // To read words.txt
#include <unordered_set>    // To use unordered_set

#include <iostream>         // I/O header file

#include <vector>           // To use vectors
#include <algorithm>        // To use transform

// Path: Go up one level from the src/ folder (with ..), then enter the include/ folder and find word_management.h.
#include "../include/word_management.h"

using namespace std;

// Returns true if it successfully loads words from the file, false otherwise
bool WordManager::loadValidWords(){
    ifstream file("words.txt"); // Reading words.txt

    // Checking if file could be opened, if not, return false immediately
    if (!file.is_open()){
        return false;
    }
	
    // Reading each word from the file
    string word;
    while (file >> word){
        // Converting each word to lowercase
        transform(word.begin(), word.end(), word.begin(),::tolower);
        // Inserting each word into validWords
        validWords.insert(word);
    }

    // Closing the file and returning true for successful loading
    file.close();
    return true;
}

bool WordManager::isValidWord(const string& word){
    return validWords.find(word) != validWords.end();
}

string WordManager::chooseTargetWord(){
    // Convert unordered_set to vector for indexing
    vector<string> words(validWords.begin(), validWords.end());

    // Seed random once
    srand(static_cast<unsigned int>(time(nullptr)));

    int index;
    index = rand() % words.size(); // Obtaining the index of the word randomly

    return words[index]; // Returning the word at index
}

/*// main function to test the WordManager class
int main(){
    WordManager manager;
    
    if (!manager.loadValidWords()){
        cerr << "Failed to load words.";
        return 1;
    }
    
    string target = manager.chooseTargetWord();
    cout << "Target word (for testing): " << target << "\n";

    string input;
    cout << "Enter a 5-letter word: ";
    cin >> input;

    if (manager.isValidWord(input)){
        cout << "Valid word!";
    }
    else{
        cout << "Invalid word.";
    }

    return 0;
}*/