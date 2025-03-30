# Easy Level AI Implementation Details (`easy_ai.py`)

## Overview
This document describes the implementation of the easy level AI (`EasyAI`) for the Ludo game, as found in `easy_ai.py`. This AI uses a state-based heuristic approach, switching between simple strategies based on random chance to provide varied gameplay suitable for beginners.

## Architecture (`EasyAI` Class)

```mermaid
graph TD
    A[EasyAI Class] --> B{Current State}
    A --> C[Red Positions]
    A --> D[Blue Positions]
    A --> E[Current Roll]
    A --> F[Safe Spots List]

    B --> G[Decide State (Random %)]

    G --> H[RANDOM State (40%)]
    G --> I[BASIC State (40%)]
    G --> J[SAFE State (20%)]

    H --> K[Random Strategy: Pick any valid move]
    I --> L[Basic Strategy: Simple Priorities]
    J --> M[Safe Strategy: Prioritize Safety]

    L --> N[1. Get Piece Out (Roll=6)]
    L --> O[2. Capture Opponent]
    L --> P[3. Move Furthest Piece]

    M --> Q[1. Move to Safe Spot]
    M --> R[2. Avoid Moving Already-Safe Pieces]
    M --> S[3. Random Valid Move (Fallback)]

    K & L & M --> T[Get Valid Moves]
    T --> U[Check: Home & Roll=6]
    T --> V[Check: On Board & Roll <= 106]

    L & M --> W[Helper: will_capture]
    M --> X[Helper: is_in_danger]

    A -.-> Y[make_move Method: Entry Point]
    Y --> G
    Y --> T
    Y --> K/L/M
    Y --> Z[Return Chosen Coin (1-4) or None]

```

## Implementation Details (`easy_ai.py`)

### 1. `EasyAI` Class Structure
- Contains methods for state management, move validation, strategy execution, and helper checks.
- Tracks `red_positions`, `blue_positions`, `current_roll`, and predefined `safe_spots`.

### 2. State Machine (`AIState` Enum & `decide_state`)
- Defines three states: `RANDOM`, `BASIC`, `SAFE`.
- `decide_state()` method uses `random.random()` to select the active state for the current move based on probabilities: RANDOM (40%), BASIC (40%), SAFE (20%).

### 3. State Behaviors (Strategy Methods)

#### `random_strategy`
- Selects any valid move randomly using `choice(self.get_valid_moves())`.

#### `basic_strategy`
- Implements simple priorities:
  1.  **Bring Out:** If roll is 6 and a coin is at home (`-1`), return that coin number.
  2.  **Capture:** Check if any valid move results in a capture (`will_capture`). If yes, return that coin number.
  3.  **Move Furthest:** Otherwise, return the valid coin number corresponding to the piece furthest along the track (highest position value).

#### `safe_strategy`
- Focuses on minimizing risk:
  1.  **Move to Safety:** Check if any valid move lands the piece on a `safe_spot`. If yes, return that coin number.
  2.  **Prioritize Unsafe Pieces:** If moves exist for pieces *not* currently on safe spots, choose randomly from those moves. Avoid moving pieces already safe if other options exist.
  3.  **Fallback:** If only safe pieces can move, or no other priority applies, choose a random valid move.
  - Uses `is_in_danger` helper, but primarily focuses on moving *to* safe spots rather than explicitly moving endangered pieces unless that move leads to safety.

### 4. Helper Methods
- **`get_valid_moves()`:** Returns a list of coin numbers (1-4) that can legally move based on `current_roll` and `red_positions`.
- **`will_capture(coin_num, new_pos)`:** Checks if moving `coin_num` to `new_pos` would land on an opponent's piece (`blue_positions`) that is not on a `safe_spot`.
- **`is_in_danger(coin_num)`:** Checks if the piece `coin_num` (which must be on the board and not on a safe spot) has an opponent piece 1-6 steps behind it.

### 5. Integration (`first.py`)
- `Ludo_Game` initializes `self.ai = EasyAI()` if `self.Robo == 1`.
- The `Robo_Judge(ind)` method was updated:
    - `ind="predict"` calls `Prediction_Maker("red")`.
    - `ind="give"` calls `self.ai.make_move(self.move_Red, self.Position_Red_coin, self.Position_Blue_coin)` to get the `chosen_coin`.
    - If `chosen_coin` is not `None`, it calls `self.Main_Controller("red", chosen_coin)` to execute the move.
- The previous complex heuristic logic within `Robo_Judge` was removed.

## Comparison with Previous AI (`Robo_Judge` Heuristics)

1.  **Simplicity & Fairness:** `EasyAI` removes the complex, sometimes hard-to-follow conditional logic and potential "cheating" mechanics (like forced sixes) of the old `Robo_Judge`. It relies on clearer state-based rules and standard game mechanics.
2.  **Randomization & Predictability:** `EasyAI` introduces significant randomness through state selection and choices within states, making it less predictable than the mostly deterministic old AI.
3.  **Strategy:** Replaces complex distance calculations (`Positive_Distance`, `Negative_Distance`) with simpler, state-dependent priorities (capturing, safety, bringing pieces out).
4.  **Maintainability:** The logic is encapsulated within the `EasyAI` class, improving separation of concerns compared to the large `Robo_Judge` method in `first.py`.

## Outcome
- The `EasyAI` implementation provides a functional "easy" level opponent.
- Its behavior is varied due to the state machine and randomness.
- It offers a fair challenge without artificial advantages.
- The code is more modular and easier to understand than the previous implementation.
