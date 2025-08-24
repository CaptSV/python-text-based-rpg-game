# Text-Based RPG Game

A classic command-line, text-based Role-Playing Game demonstrating fundamental programming concepts and game development principles.

---

## Description

This project is a fully interactive text-based RPG designed to run in a terminal environment. It showcases a **modular design**, structuring core game mechanics such as player actions, combat encounters, inventory management, and narrative progression into distinct, manageable functions and logical blocks. The game emphasizes **clear input/output handling** to provide an engaging player experience through textual interactions. Through its implementation, it demonstrates foundational computer science concepts like **state management**, **conditional logic**, and iterative **game loop** design. It's a foundational exercise in creating interactive systems and managing application flow in a command-line interface (CLI).

---

## Getting Started

### Dependencies

* **Python 3.x:** (Tested with Python 3.8+)
* No external libraries are strictly required; the game is built using standard Python modules.
* **Operating System:** Cross-platform (Windows, macOS, Linux).

### Installing

1.  **Clone the Repository:**
    Download or clone this repository to your local machine.
    ```bash
    git clone [https://github.com/CaptSV/text-based-rpg.git](https://github.com/CaptSV/text-based-rpg.git)
    cd text-based-rpg
    ```
2.  No specific modifications to files or folders are needed for initial setup.

### Executing program

1.  **Open your terminal or command prompt.**
2.  **Navigate to the project directory** where the main game script (e.g., `game.py` or `main.py`) is located.
    ```bash
    cd /path/to/your/text-based-rpg-folder
    ```
3.  **Run the game script:**
    ```bash
    python game.py
    ```
    (Replace `game.py` with the actual name of your main game file if different.)
4.  Follow the on-screen prompts to interact with the game.

---

## Help

* **Invalid Input:** If the game doesn't recognize your command, it will usually prompt you again or provide a list of valid actions. Pay attention to the exact wording required (e.g., "attack" vs. "Attack").
* **Game Not Starting:** Ensure you are in the correct directory where the `game.py` file resides when running `python game.py`.
* **`SyntaxError` or `IndentationError`:** These are common Python errors. Double-check your code for correct syntax and consistent indentation, especially if you've made any modifications.

---

## Authors

Simon Valenzuela  
[GitHub](https://github.com/CaptSV)  
[LinkedIn](https://www.linkedin.com/in/simonrpvalenzuela/)

---
## License

This project is licensed under the [MIT License](https://opensource.org/license/mit)  - see the LICENSE.md file for details

---

## Version History

* 0.2
    * Implemented enhanced game loop and state management.
    * Improved player input parsing and response logic.
    * Expanded basic combat system.
* 0.1
    * Initial Release: Core game loop with basic player movement and story introduction.

---

## Future Enhancements

* **Save/Load Game Functionality:** Implement a system to save player progress and load existing games.
* **Expanded World Map:** Introduce a more complex world map with distinct regions and random encounters.
* **Non-Player Characters (NPCs):** Add basic NPC interactions, quests, and dialogues.
* **More Diverse Combat Mechanics:** Introduce special abilities, status effects, and enemy types.
* **Inventory Management:** Develop a robust system for collecting, using, and managing items.
* **Simple Graphical Interface:** Explore using libraries like `curses` or `PyGame` for a more visually engaging terminal or basic windowed experience.
* **Unit Testing:** Implement automated

---
## Known Issues

* **Enemy List Corruption After Defeat:** Currently, attempting to remove a defeated enemy from the location's enemy list results in the list being set to `None`. This will cause errors when the game attempts to access or iterate over the enemy list again. This is a high-priority bug that needs to be resolved.
* **Single Turn Combat:** The combat loop currently performs one player attack and one enemy retaliation, then exits the `_handle_attack_input` function without checking if more enemies remain or if combat should continue.
* **Incomplete Player Death Logic:** If the player's health drops to zero, the game does not currently trigger a "Game Over" state or exit gracefully.
* **Limited Input Validation:** User input for menu choices (`int(input(...))`) does not yet handle non-integer input and will cause a `ValueError`.
