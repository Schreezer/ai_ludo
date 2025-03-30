# AI Decision Making in Ludo Game (EasyAI Implementation)

## Overview
The computer player (Red) in the Ludo game now uses the `EasyAI` class for its decision-making. This AI employs a state-based heuristic approach, switching between different strategies to provide varied and less predictable gameplay suitable for an "easy" difficulty level.

## Key Components (`easy_ai.py`)

### 1. `EasyAI` Class
- Manages the AI's state and decision logic.
- Tracks its own positions (`red_positions`) and opponent positions (`blue_positions`).
- Knows the `safe_spots` on the board: `[1, 9, 14, 22, 27, 35, 40, 48]`.
- Maintains a `current_roll` value provided by the game.

### 2. AI States (`AIState` Enum)
The AI operates in one of three states, chosen randomly with weightings for each move:
- **`RANDOM` (40% chance):** Makes a random valid move.
- **`BASIC` (40% chance):** Follows a simple, predefined strategy.
- **`SAFE` (20% chance):** Prioritizes keeping its pieces safe.

### 3. State Selection (`decide_state` method)
- Uses `random.random()` to pick a state based on the probabilities mentioned above before each move decision.

### 4. Identifying Valid Moves (`get_valid_moves` method)
- Determines which of the AI's coins (1-4) can legally move based on the `current_roll`.
- Considers:
    - If a coin is at home (`-1`), it can only move out on a roll of 6.
    - If a coin is on the board, the move must not overshoot the final position (<= 106).
- Returns a list of valid coin numbers (e.g., `[1, 3]`). Returns an empty list if no moves are possible.

### 5. Core Decision Logic (`make_move` method)
- This is the main entry point called by the game (`first.py`).
- It receives the `dice_value`, current `red_positions`, and `blue_positions`.
- Updates its internal state (`self.current_roll`, `self.red_positions`, `self.blue_positions`).
- Calls `decide_state()` to choose the strategy for the current turn.
- Calls the appropriate strategy method (`random_strategy`, `basic_strategy`, or `safe_strategy`).
- Returns the chosen coin number (1-4) to move, or `None` if no valid move exists.

### 6. Strategy Implementations

#### a) `random_strategy`
- Gets the list of valid moves using `get_valid_moves()`.
- If valid moves exist, returns a random choice from the list using `random.choice()`.

#### b) `basic_strategy`
- Gets valid moves.
- **Priority 1:** If the roll is 6 and a coin is at home, choose that coin to bring out.
- **Priority 2:** Check if any valid move results in capturing an opponent piece (`will_capture` helper method checks if the `new_pos` matches a `blue_position` and is not a `safe_spot`). If yes, choose that capturing move.
- **Priority 3:** If no capture or bringing-out move is made, choose the valid coin that is currently furthest along the board (highest position number).

#### c) `safe_strategy`
- Gets valid moves.
- **Priority 1:** Check if any currently owned pieces are "in danger" (`is_in_danger` helper method checks if an opponent piece is 1-6 steps behind the AI piece on a non-safe spot). If a piece is in danger, check if moving it leads to a `safe_spot`. If yes, move that piece. (Note: The current implementation checks *if* a piece is in danger, but the primary action is to move *to* a safe spot if possible, not necessarily moving the endangered piece first unless that move leads to safety).
- **Priority 2:** Check if any valid move lands the piece on a `safe_spot`. If yes, choose such a move.
- **Priority 3:** Avoid moving pieces that are *already* on a `safe_spot` if other valid moves exist for pieces *not* on safe spots. Choose randomly among the non-safe pieces.
- **Priority 4:** If all valid moves involve pieces already on safe spots, or if no other priority applies, choose a random valid move.

## Integration with `first.py`
- The `Ludo_Game` class initializes `self.ai = EasyAI()` when playing against the computer (`self.Robo = 1`).
- The `Robo_Judge` method in `first.py` now acts as a simple wrapper:
    - If called with `ind="predict"`, it calls `self.Prediction_Maker("red")`.
    - If called with `ind="give"`, it calls `self.ai.make_move(...)` with the current game state and dice roll, then calls `self.Main_Controller("red", chosen_coin)` if the AI returns a valid move.
