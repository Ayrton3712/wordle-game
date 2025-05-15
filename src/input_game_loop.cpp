#include <iostream>                     // To use I/O objects
#include <vector>                       // To use vectors
#include <conio.h>                      // I/O functions, non-standard
#include "../include/word_comparison.h" // To use the evaluateGuess method
#include "../include/display.h"

using namespace std;  

//- Prompt user
//- Ensure input is 5 letters. 
//- Loop until valid, return input. 

string getUserGuess(){
	vector<char> word_vector; 
	char inputCharacter = 'o'; 
	int i = 0; 
	cout<<"Enter a 5 letter word: "; 
	
	do{ 
		inputCharacter = _getch(); 
		cout<<inputCharacter; 
		word_vector.insert(word_vector.begin() + i, inputCharacter); 
		i++; 
	}while (word_vector.size()!=5);										 
	
	return string(word_vector.begin(), word_vector.end());
}

//- Loop through attempts
//- Call getUserGuess(), evaluateGuess(), displayFeedback()
//- End game on win or out of tries

void gameLoop(){
	for (int i = 0; i < 6; i++){
		cout<<"Attempt number "<<i+1<<endl; 
		string word = getUserGuess(); 
		vector<int> evaluation = evaluateGuess(word); 
		displayFeedback();
		if (evaluation == {2,2,2,2,2}){
			"You have won the game!"; 
			break; 
		}
		if (evaluation != {2,2,2,2,2}){
			cout<<"You are out of tries! Try again? Y/N"; 
		}
	}

}

int main (){
	return 0; 
}