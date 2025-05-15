#ifndef GAME_MANAGER_H
#define GAME_MANAGER_H

#include <string>

class GameManager{
	public:
		void gameLoop();

	private:
		std::string getUserGuess();
};

#endif