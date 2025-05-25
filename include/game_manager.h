#ifndef GAME_MANAGER_H
#define GAME_MANAGER_H

#include <string>

class GameManager{
	private:
		std::string getUserGuess();
	
	public:
		void gameLoop();
};

#endif