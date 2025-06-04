#ifndef GAME_MANAGER_H
#define GAME_MANAGER_H

#include <string>

class GameManager{
	private:
		std::string getUserGuess();
		std::string target;
		int attempts = 0;
	
	public:
		void gameLoop();
		void reset(const std::string& newTarget);
    	std::vector<int> processGuess(const std::string& guess,std::string& resultTag);  
			// resultTag = ""     -> normal turn
			// resultTag = "WIN"  -> guessed it
			// resultTag = "LOSE" -> out of tries
		const std::string& getTarget() const;
};

#endif