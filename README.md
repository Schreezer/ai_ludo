# Ludo Game Enhancement (ai_ludo)

This project is an enhanced version of a classic Ludo game implemented in Python using Tkinter for the graphical user interface.

## Current Features

*   Classic Ludo gameplay for 2-4 players.
*   Option to play against an "Easy" level AI opponent (controls the Red player).
*   Graphical Ludo board and pieces.
*   Dice rolling mechanism.
*   Basic win/runner-up detection.

## Technologies Used

*   **Python 3.x**
*   **Tkinter:** For the graphical user interface.
*   **Pillow (PIL):** For handling dice images.
*   **Standard Libraries:** `time`, `random`, `enum`.

## How to Run

1.  **Prerequisites:**
    *   Ensure you have Python 3 installed.
    *   Install the Pillow library:
        ```bash
        pip install Pillow
        ```
2.  **Run the Game:**
    Execute the main game file from your terminal in the project directory:
    ```bash
    python first.py
    ```
3.  **Gameplay:**
    *   A window will pop up asking for the number of players (2-4) or if you want to play against the computer.
    *   Follow the on-screen prompts and use the "Predict" buttons and numbered coin buttons to play your turn.

## Future Enhancements (Planned)

*   Implement Medium/Hard AI difficulty levels.
*   Add a feature to save and load game progress.
*   Improve the user interface (potentially using a different framework like Pygame).
*   Refactor the codebase for better modularity and maintainability.
*   Add comprehensive testing.

## Memory Bank

Internal project documentation, plans, and context can be found in the `memory-bank/` directory.
