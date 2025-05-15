#ifndef DISPLAY_H
#define DISPLAY_H

#include <vector>
#include <string>

class Display{
    public:
        void displayFeedback(const std::vector<int>&, const std::string&);
        void displayGameState();
};

#endif