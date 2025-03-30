from random import choice, random
from enum import Enum

class AIState(Enum):
    RANDOM = "random"  # Make random valid moves
    BASIC = "basic"    # Follow simple strategy
    SAFE = "safe"     # Try to stay safe

class EasyAI:
    def __init__(self):
        # Store active coins (equivalent to Store_Robo in original)
        self.active_coins = []
        
        # Track coin positions (will be updated by main game)
        self.red_positions = [-1, -1, -1, -1]  # -1 means in home
        self.blue_positions = [-1, -1, -1, -1] # opponent positions
        
        # Safe spots on board
        self.safe_spots = [1, 9, 14, 22, 27, 35, 40, 48]
        
        # Current state
        self.current_state = AIState.BASIC
        
        # Current dice value
        self.current_roll = 0

    def decide_state(self):
        """Randomly choose a state based on weightings"""
        rand = random()
        if rand < 0.4:  # 40% chance
            return AIState.RANDOM
        elif rand < 0.8:  # 40% chance
            return AIState.BASIC
        else:  # 20% chance
            return AIState.SAFE

    def get_valid_moves(self):
        """Get list of coins that can legally move"""
        valid_coins = []
        
        # If all coins are home and roll isn't 6, no valid moves
        if all(pos == -1 for pos in self.red_positions) and self.current_roll != 6:
            return []

        # Check each coin
        for coin_num in range(4):
            pos = self.red_positions[coin_num]
            
            # If coin is home, only valid with a 6
            if pos == -1 and self.current_roll == 6:
                valid_coins.append(coin_num + 1)
                
            # If coin is on board, check if move would be valid
            elif pos != -1:
                if pos + self.current_roll <= 106:  # Check won't overshoot end
                    valid_coins.append(coin_num + 1)
                    
        return valid_coins

    def will_capture(self, coin_num, new_pos):
        """Check if moving coin_num will capture an opponent"""
        if new_pos in self.blue_positions and new_pos not in self.safe_spots:
            return True
        return False

    def is_in_danger(self, coin_num):
        """Check if coin is at risk of being captured"""
        pos = self.red_positions[coin_num - 1]
        if pos == -1 or pos in self.safe_spots:
            return False
            
        # Check if any opponent coin is 1-6 spaces behind
        for opp_pos in self.blue_positions:
            if opp_pos != -1:  # If opponent coin is on board
                distance = pos - opp_pos
                if 0 < distance <= 6:  # Opponent is 1-6 spaces behind
                    return True
        return False

    def random_strategy(self):
        """Simply choose a random valid move"""
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None
        return choice(valid_moves)

    def basic_strategy(self):
        """Follow basic priorities"""
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None

        # Priority 1: If roll is 6 and have coins at home, bring one out
        if self.current_roll == 6:
            for coin in valid_moves:
                if self.red_positions[coin - 1] == -1:
                    return coin

        # Priority 2: If can capture, do it
        for coin in valid_moves:
            new_pos = self.red_positions[coin - 1] + self.current_roll
            if self.will_capture(coin, new_pos):
                return coin

        # Priority 3: Just move furthest coin
        furthest_coin = valid_moves[0]
        for coin in valid_moves[1:]:
            if self.red_positions[coin - 1] > self.red_positions[furthest_coin - 1]:
                furthest_coin = coin
        return furthest_coin

    def safe_strategy(self):
        """Try to make safe moves"""
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None

        # Priority 1: If any coin in danger, move it
        for coin in valid_moves:
            if self.is_in_danger(coin):
                new_pos = self.red_positions[coin - 1] + self.current_roll
                if new_pos in self.safe_spots:  # Even better if can reach safe spot
                    return coin

        # Priority 2: Move to a safe spot if possible
        for coin in valid_moves:
            new_pos = self.red_positions[coin - 1] + self.current_roll
            if new_pos in self.safe_spots:
                return coin

        # Priority 3: Don't move coins that are already safe
        safe_moves = [coin for coin in valid_moves 
                     if self.red_positions[coin - 1] in self.safe_spots]
        if len(valid_moves) > len(safe_moves):  # If have unsafe coins
            unsafe_moves = [coin for coin in valid_moves 
                          if coin not in safe_moves]
            return choice(unsafe_moves)

        return choice(valid_moves)  # If all else fails, move randomly

    def make_move(self, dice_value, red_positions, blue_positions):
        """Main method called by game to get AI's move"""
        # Update current game state
        self.current_roll = dice_value
        self.red_positions = red_positions.copy()
        self.blue_positions = blue_positions.copy()

        # Choose state for this move
        self.current_state = self.decide_state()

        # Make move based on current state
        if self.current_state == AIState.RANDOM:
            return self.random_strategy()
        elif self.current_state == AIState.BASIC:
            return self.basic_strategy()
        else:  # SAFE state
            return self.safe_strategy()