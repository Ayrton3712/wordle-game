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
    	std::vector<int> processGuess(const std::string& guess, std::string& resultTag);  
		const std::string& getTarget() const;
};

#endif