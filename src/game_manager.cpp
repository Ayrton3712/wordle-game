#include <iostream>                      // For I/O
#include <vector>                        // For vectors
#include <string>                        // For strings
#include <limits>                        // For input stream handling

#include "../include/game_manager.h"	 // Contains class declaration
#include "../include/word_comparison.h"  // To use evaluateGuess
#include "../include/word_management.h" // To use the WordManager class
//Defining getUserGuess method.
std::string GameManager::getUserGuess(){
    std::string guess;
//Promptinh user to enter a 5-letter word.	
    while (true) {
        std::cout << "Enter a 5-letter word: ";
        std::cin >> guess;
	//If the length of guess is not 5. 
        if (guess.length() != 5) {
	//Displaying invalid input message. 
            std::cout << "Invalid input. Please enter exactly 5 letters.\n";
            // Clear input state and discard bad input
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	//Continue to the loop's next iteration. 
            continue;
        }
	//Breaking loop if word lenght = 5. 
        break;
    }
	//Returning guess. 
    return guess;
}
//Defining gameLoop method. 
void GameManager::gameLoop() {
//Instantiating WordManager class. 
    WordManager manager;
	//Checking if word file could open. 
    if (!manager.loadValidWords()) {
        std::cerr << "Could not load word list.\n";
        return;
    }
	//Getting ramdom word from file and storing it on target string variable. 
    std::string target = manager.chooseTargetWord();
	//Loop used for each trial.
    for (int i = 0; i < 6; i++) {
	    //Printing out trial number. 
        std::cout << "\nAttempt " << (i + 1) << " of 6" << std::endl;
	//Calling guetUserGuess method which returns string with the user's guess. 
        std::string guess = getUserGuess();
	    //Calling evaluateGuess function wich returns an evaluation which is stored in a vector. 
        std::vector<int> evaluation = evaluateGuess(guess, target);
	//If the condition to win the game is met. 
        if (evaluation == std::vector<int>{2, 2, 2, 2, 2}) {
		//Display win message. 
            std::cout << "You have won the game!" << std::endl;
		//Getting out of the function. 
            return;
        }
    }
	//If the user did not guess the word after 6 tries, prompt the user to try again. 
    std::cout << "You are out of tries! Try again? (Y/N): ";
    char choice;
    std::cin >> choice;
	//If user wants to try again. 
    if (choice == 'Y' || choice == 'y') {
	    //gameLoop function is called.  
        gameLoop();
    } else {
	    //If the user does not want to play again, the game is finished. 
        std::cout << "Thanks for playing!" << std::endl;
    }
}

// Resets target and attempts for a new round
void GameManager::reset(const std::string& newTarget){
    target = newTarget;
    attempts = 0;
}

// Processes the guess, encodes it into resultTag, and returns feedback vector
std::vector<int> GameManager::processGuess(const std::string& guess, std::string& resultTag){
    std::vector<int> feedback = evaluateGuess(guess, target);
    attempts++;
    resultTag.clear(); // Clears the string

    // resultTag = ""     -> normal turn
    // resultTag = "WIN"  -> guessed it
    // resultTag = "LOSE" -> out of tries

    if (feedback == std::vector<int>{2, 2, 2, 2, 2}){
        resultTag = "WIN";
    }
    else if (attempts >= 6){
        resultTag = "LOSE";
    }

    return feedback;
}

// Getter for the target
const std::string& GameManager::getTarget() const{
    return target;
}
