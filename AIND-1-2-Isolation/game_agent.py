"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    # get a bonus at the center position
    center_bonus = 2
    if located_center(game, game.get_player_location(player)):
        own_moves += center_bonus
    
    return float(own_moves - opp_moves)
    
    def located_center(game, player_location):
        center = [(4,4)]
        return player_location in center


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.This should be the best heuristic function for your project submission.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(own_moves - 2 * opp_moves)

    raise NotImplementedError


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    # set a landmine at some locations
    trap_position = 2
    if located_trap(game, game.get_player_location(player)):
        opp_moves -= trap_position
        
    return float(own_moves - opp_moves)
   
    def located_trap(game, player_location):
        landmine_area = [(3,3),(5,3),(3,5)(5,5)]
        return player_location in landmine_area

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        
         function MINIMAX-DECISION(state) returns an action
         return arg max a ∈ ACTIONS(s) MIN-VALUE(RESULT(state, a))

        function MAX-VALUE(state) returns a utility value
         if TERMINAL-TEST(state) then return UTILITY(state)
         v ← −∞
         for each a in ACTIONS(state) do
           v ← MAX(v, MIN-VALUE(RESULT(state, a)))
         return v

        function MIN-VALUE(state) returns a utility value
         if TERMINAL-TEST(state) then return UTILITY(state)
         v ← ∞
         for each a in ACTIONS(state) do
           v ← MIN(v, MAX-VALUE(RESULT(state, a)))
         return v
         
         An algorithm for calculating minimax decisions. It returns the action corre- sponding to the best possible move, that is, the move that leads to the outcome with the best utility, under the assumption that the opponent plays to minimize utility. The functions MAX-VALUE and MIN-VALUE go through the whole game tree, all the way to the leaves, to determine the backed-up value of a state. The notation argmaxa ∈ S f (a) computes the element a of set S that has the maximum value of f (a).
         
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        best_move, best_value = self.max_value(game, depth)
        return best_move
    
        def max_value(self, game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
                
            if depth==0 or game.utility(game.inactive_player) != 0.:
                return game.get_player_location(game.inactive_player),self.score(game,self)
            
            bestValue = float('-inf')
            bestMove  = (-1, -1)
            for forecast_move in game.get_legal_moves():
                move, value = self.min_value(game.forecast_move(forecast_move), depth-1)
                if value > bestValue:
                    bestValue = value
                    bestMove  = move
                    
            return bestMove, bestValue

        def min_value(self, game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
                
            if depth==0 or game.utility(game.inactive_player) != 0.:
                return game.get_player_location(game.inactive_player),self.score(game,self)
            
            minValue = float('inf')
            minValue  = (-1, -1)
            for forecast_move in game.get_legal_moves():
                move, value = self.min_value(game.forecast_move(forecast_move), depth-1)
                if value < minValue:
                    minValue = value
                    minMove  = move
                    
            return minMove, minValue

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        
        --- Iterative deepening psuedocode ---
        
        function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution, or failure
         for depth = 0 to ∞ do
           result ← DEPTH-LIMITED-SEARCH(problem,depth)
           if result ≠ cutoff then return result
        
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        """        
        self.time_left = time_left
        
        best_move = (-1, -1)
        upcoming_best = best_move

        try:
            search_depth = 1
            
            while True:
                on_move = self.alphabeta(game, self.search_depth)
                if on_move != best_move:
                    best_move = (-1, -1)
                    upcoming_best = on_move
                else:
                    best_move = upcoming_best
            search_depth += 1
            
        except SearchTimeout:
            pass
        
        return best_move

        # TODO: finish this function!
        raise NotImplementedError

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        
        function ALPHA-BETA-SEARCH(state) returns an action
         v ← MAX-VALUE(state, −∞, +∞)
         return the action in ACTIONS(state) with value v

        function MAX-VALUE(state, α, β) returns a utility value
         if TERMINAL-TEST(state) the return UTILITY(state)
         v ← −∞
         for each a in ACTIONS(state) do
           v ← MAX(v, MIN-VALUE(RESULT(state, a), α, β))
           if v ≥ β then return v
           α ← MAX(α, v)
         return v

        function MIN-VALUE(state, α, β) returns a utility value
         if TERMINAL-TEST(state) the return UTILITY(state)
         v ← +∞
         for each a in ACTIONS(state) do
           v ← MIN(v, MAX-VALUE(RESULT(state, a), α, β))
           if v ≤ α then return v
           β ← MIN(β, v)
         return v
         
         The alpha–beta search algorithm. Notice that these routines are the same as the MINIMAX functions in Figure 5.3, except for the two lines in each of MIN-VALUE and MAX-VALUE that maintain α and β (and the bookkeeping to pass these parameters along).
         
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        best_move, best_value = self.max_value(game, depth)
        return best_move
                                           
        # TODO: finish this function!
        def max_value(self, game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
                       
            if depth == 0 or game.utility(game.inactive_player) != 0:
                return game.get_player_location(game.inactive_player), self.score(game, self)
            
            best_value = float('-inf')
            best_move = (-1,-1)
            
            for forecast_move in game.get_legal_moves():
                move, value = self.min_value(game.forecast_move, depth-1, alpha, beta)
                if best_value >= beta:
                    return best_value
                alpha = max(alpha, best_value)
                
            return best_move, best_value
        
        def min_value(self, game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
                       
            if depth == 0 or game.utility(game.inactive_player) != 0:
                return game.get_player_location(game.inactive_player), self.score(game, self)
            
            min_value = float('inf')
            min_move = (-1,-1) 
            for forecast_move in game.get_legal_moves():
                move, value = self.min_value(game.forecast_move, depth-1, alpha, beta)
                if min_value < alpha:
                    return min_value
                beta = min(beta, min_value)
                
            return min_move, min_value
                        
        raise NotImplementedError
