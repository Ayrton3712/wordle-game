//Edna:  Display & Output
#include <iostream> // For input/output (cout, endl)
#include <vector> // For dynamic arrays (vector)
#include <string> // For string manipulation
#include <algorithm> // For transform/toupper (case conversion)
#ifdef _WIN32 // Check if compiling on Windows
#include <windows.h> // Windows-specific console functions
#endif

using namespace std;

class Display {
    private:
    // Console color codes (platform-dependent)
    #ifdef _WIN32   // Windows-specific color codes
        const int DEFAULT = 7;  // Default console color (gray)
        const int GREEN = 10;   //Light Green
        const int YELLOW = 14;  //Yellow
        const int RED = 12;     //Red
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE); // Windows console handle
    #else // ANSI color codes (Linux/Mac)
        const int DEFAULT = 7;  // Reset color
        const int GREEN = 10;   // Green ANSI code
        const int YELLOW = 14;  // Yellow ANSI code
        const int RED = 12;     // Red ANSI code
    #endif

    /**
     * Sets the console text color (platform-specific).
     * @param color - The color code to apply.
     */
    void setConsoleColor(int color){
        #ifdef _WIN32
            SetConsoleTextAttribute(hConsole, color); // Windows API call
        #else
            cout << "\033[" << color << "m"; // ANSI escape code
        #endif
    }

    //Resets the console color to default.
    void resetConsoleColor(){
        #ifdef _WIN32
            SetConsoleTextAttribute(hConsole, DEFAULT); // Windows reset
        #else
            cout << "\033[" << DEFAULT << "m";  // ANSI reset
        #endif
    }


    public:
    // Constants for feedback codes (used to represent letter states)
    static const int CORRECT = 2;   //Green - correct letter and position
    static const int PRESENT = 1;   //Yellow - correct letter but wrong position
    static const int ABSENT = 0;    //Red - letter not in word

    /**
     * Displays feedback for each letter in a guessed word.
     * @param feedback - Vector of feedback codes (0=ABSENT, 1=PRESENT, 2=CORRECT)
     * @param guess - The guessed word
     */

    void displayFeedback(const vector<int>& feedback, const string& guess){
        // Loop through each letter in the guessed word
        for (size_t i=0; i<guess.length(); i++){
            char upperChar = toupper(guess[i]);

            // Apply color/symbol based on feedback
            switch (feedback[i]) {
                case CORRECT:                           // Correct letter & position (Green)
                    setConsoleColor(GREEN);             // Set console color to green 
                    cout << "[" << upperChar << "]";    // Display as [X]  
                    break;
                case PRESENT:                           // Correct letter, wrong position (Yellow)   
                    setConsoleColor(YELLOW);            // Set console color to yellow
                    cout << "{" << upperChar << "}";    // Display as {X}
                    break;
                case ABSENT:                            // Letter not in word (Red)
                    setConsoleColor(RED);               // Set console color to red
                    cout << " " << upperChar << " ";    // Display as  X 
                    break;
                default:                                // Fallback (shouldn't happen)
                    setConsoleColor(DEFAULT);           // Reset to default color
                    cout << " " << upperChar << " ";
            }
            resetConsoleColor();   // Reset color after each letter
            cout << " ";           // Space between letters 
        }
        cout << endl; // Move to next line after displaying the word
    };

    /**
     * Shows the game state (all previous guesses and their feedback).
     * @param guessHistory - A vector of pairs: {guessed_word, feedback_vector}
     */

    void displayGameState(const vector <pair<string, vector<int>>> & guessHistory){
        cout << "\n----- Game State -----\n";   // Header for game state display
        
        if (guessHistory.empty()){              // If no guesses made yet
            cout << "No guesses made yet.\n";
            return;
        }

        //Loop through all past guesses and display them
        for (const auto& [guess, feedback] : guessHistory) {
            displayFeedback(feedback, guess);
        }
        cout << "------------------\n";         // Footer for game state display
    };
};