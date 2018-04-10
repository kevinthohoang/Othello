# Kevin Hoang 76963024. ICS 32 Lab Section 11. Project 4.

import itertools
import copy


BLACK = "B"
WHITE = "W"
NONE  = " "


class InvalidOthelloMoveError(Exception):
    """ Raised whenever an invalid move is attempted to be made.
    """
    pass


class GameState:
    def __init__(self, rows: int, columns: int, first_player: str, win_style: int):
        """ Initialize this GameState object with a row count, column count, turn as the first
            player, initial looking game board, win style, and initial score of 2:2.
        """
        self._rows        = rows
        self._columns     = columns
        self._turn        = first_player
        self._game_board  = _new_game_board(rows, columns, first_player)
        self._win_style   = win_style
        self._score       = {"black score": 2, "white score": 2}

    def get_rows(self) -> int:
        """ Return the number of rows used to create the Othello game board.
        """
        return self._rows

    def get_columns(self) -> int:
        """ Return the number of columns used to create the Othello game board.
        """
        return self._columns

    def get_turn(self) -> str:
        """ Return the current player.
        """
        return self._turn
    
    def get_game_board(self) -> [[str]]:
        """ Return the current game board.
        """
        return self._game_board

    def get_white_score(self) -> int:
        """ Return white's current score.
        """
        self.determine_score()
        return self._score["white score"]

    def get_black_score(self) -> int:
        """ Return white's current score.
        """
        self.determine_score()
        return self._score["black score"]
        
    def apply_move(self, move: tuple) -> None:
        """ Given a move tuple that carries the row/column of the move, this function adds the player's piece
            to the game board, reverses the opponent's pieces, and changes the current player to the opponent.
            However, if the move is invalid, an InvalidOthelloMoveError is raised.
        """
        rows          = self.get_rows()
        columns       = self.get_columns()
        player_copy   = _copy_game_state(self)

        row = move[0]
        col = move[1]

        d = {"north":     [(row - 1, col),     (row - 1, -1, -1),     (row - 1, -1, -1) ],
             "east":      [(row, col + 1),     (col + 1, columns, 1), (col + 1, columns, 1)],
             "south":     [(row + 1, col),     (row + 1, rows, 1),    (row + 1, rows, 1)],
             "west":      [(row, col - 1),     (col - 1, -1, -1),     (col - 1, -1, -1)],
             "northeast": [(row - 1, col + 1), (row - 1, -1, -1),     (col + 1, columns, 1)],
             "southeast": [(row + 1, col + 1), (row + 1, rows, 1),   (col + 1, columns, 1)],
             "southwest": [(row + 1, col - 1), (row + 1, rows, 1),    (col - 1, -1, -1)],
             "northwest": [(row - 1, col - 1), (row - 1, -1, -1),     (col - 1, -1, -1)]}

        if move in self.possible_moves(self._turn):
            player_copy.get_game_board()[row][col] = self._turn
            self._game_board = player_copy.get_game_board()

            for key in d:
                player_copy = _copy_game_state(self)
                if player_copy.check_opponent(d[key][0][0], d[key][0][1], self._turn):
                    for subrow, subcol in zip(range(d[key][1][0], d[key][1][1], d[key][1][2]),
                                              range(d[key][2][0], d[key][2][1], d[key][2][2])):
                        if key == "north" or key == "south":
                            subcol = col
                        if key == "east" or key == "west":
                            subrow = row
                                              
                        if player_copy.check_opponent(subrow, subcol, self._turn):
                            player_copy.get_game_board()[subrow][subcol] = self._turn
                        elif player_copy.check_ally(subrow, subcol, self._turn):
                            self._game_board = player_copy.get_game_board()
                            break
                        else:
                            break
                        
            self._turn = _opposite_turn(self._turn)
        else:
            raise InvalidOthelloMoveError()

    def possible_moves(self, turn: str) -> {tuple}:
        """ This function traverses  through the entire game board looking for the current player's game pieces. With
            a given game piece, this funciton then looks in the eight compass directions for valid possible moves. A
            thorough list of possible moves is compiled and returned at the end.
        """
        rows          = self.get_rows()
        columns       = self.get_columns()
        
        possible_moves = set()

        for row in range(rows):
            for col in range(columns):
                if self._game_board[row][col] == turn:
                    
                    # NORTH SEARCH
                    if self.check_opponent(row - 1, col, turn):
                        for subrow in range(row - 1, -1, -1):
                            if self.check_opponent(subrow, col, turn):
                                if self.check_empty(subrow - 1, col):
                                    possible_moves.add((subrow - 1, col))
                                    break
                            else:
                                break
                            
                    # EAST SEARCH
                    if self.check_opponent(row, col + 1, turn):
                        for subcol in range(col + 1, columns):
                            if self.check_opponent(row, subcol, turn):
                                if self.check_empty(row, subcol + 1):
                                    possible_moves.add((row, subcol + 1))
                                    break
                            else:
                                break
                            
                    # SOUTH SEARCH
                    if self.check_opponent(row + 1, col, turn):
                        for subrow in range(row + 1, rows):
                            if self.check_opponent(subrow, col, turn):
                                if self.check_empty(subrow + 1, col):
                                    possible_moves.add((subrow + 1, col))
                                    break
                            else:
                                break
                            
                    # WEST SEARCH
                    if self.check_opponent(row, col - 1, turn):
                        for subcol in range(col - 1, -1, -1):
                            if self.check_opponent(row, subcol, turn):
                                if self.check_empty(row, subcol - 1):
                                    possible_moves.add((row, subcol - 1))
                                    break
                            else:
                                break

                    # NORTH EAST SEARCH
                    if self.check_opponent(row - 1, col + 1, turn):
                        for subrow, subcol in zip(range(row - 1, -1, -1), range(col + 1, columns)):
                            if self.check_opponent(subrow, subcol, turn):
                                if self.check_empty(subrow - 1, subcol + 1):
                                    possible_moves.add((subrow - 1, subcol + 1))
                                    break
                            else:
                                break
                            
                    # SOUTH EAST SEARCH
                    if self.check_opponent(row + 1, col + 1, turn):
                        for subrow, subcol in zip(range(row + 1, rows), range(col + 1, columns)):
                            if self.check_opponent(subrow, subcol, turn):
                                if self.check_empty(subrow + 1, subcol + 1):
                                    possible_moves.add((subrow + 1, subcol + 1))
                                    break
                            else:
                                break
                        
                    # SOUTH WEST SEARCH
                    if self.check_opponent(row + 1, col - 1, turn):
                         for subrow, subcol in zip(range(row + 1, rows), range(col - 1, -1, -1)):
                            if self.check_opponent(subrow, subcol, turn):
                                if self.check_empty(subrow + 1, subcol - 1):
                                    possible_moves.add((subrow + 1, subcol - 1))
                                    break
                            else:
                                break
                                
                    # NORTH WEST SEARCH
                    if self.check_opponent(row - 1, col - 1, turn):
                        for subrow, subcol in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
                            if self.check_opponent(subrow, subcol, turn):
                                if self.check_empty(subrow - 1, subcol - 1):
                                    possible_moves.add((subrow - 1, subcol - 1))
                                    break
                            else:
                                break
                        
        return possible_moves

    def check_possible_moves(self) -> None:
        """ This function checks to see if the current player has run out of moves. If so, change the current
            turn to the opponent.
        """
        if len(self.possible_moves(self._turn)) == 0:
               self._turn = _opposite_turn(self._turn)
    
    def determine_score(self) -> dict:
        """ This function determines the current score of the game and updates it.
        """
        black_count = 0
        white_count = 0
        
        for row in range(self._rows):
            for col in range(self._columns):
                if self._game_board[row][col] == BLACK:
                    black_count += 1
                if self._game_board[row][col] == WHITE:
                    white_count += 1
                    
        self._score["black score"] = black_count
        self._score["white score"] = white_count
            
    def game_over(self) -> bool:
        """ This function checks to see whether or not the conditions of a completed game is met. If the conditions
            are met, the game is over. The conditions of a completed game are:
            1) Every space on the game board is occupied by a player.
                    OR
            2) Both players have run out of possible moves.
        """
        occupied_spaces = 0
        for row in range(self._rows):
            for col in range(self._columns):
                if self._game_board[row][col] != NONE:
                    occupied_spaces += 1

        if occupied_spaces == self._rows * self._columns or \
           (len(self.possible_moves(self._turn)) == 0 and len(self.possible_moves(_opposite_turn(self._turn))) == 0):
            return True
        else:
            return False

    def determine_winner(self) -> str:
        """ This function determines the winner of the Othello game based on the win style that was chosen by the
            players.
        """
        self.determine_score()
        
        if self._win_style == 1:
            if self._score["black score"] > self._score["white score"]:
                return BLACK
            elif self._score["white score"] > self._score["black score"]:
                return WHITE
            else:
                return NONE
        else:
            if self._score["black score"] < self._score["white score"]:
                return BLACK
            elif self._score["white score"] < self._score["black score"]:
                return WHITE
            else:
                return NONE            

    def check_ally(self, row: int, col: int, turn: str) -> bool:
        """ This function check to see if the given piece on the game board is an allied piece of the given
            player.
        """
        return self.move_on_board((row, col)) and self._game_board[row][col] == turn

    def check_empty(self, row: int, col: int) -> bool:
        """ This function check to see if the given location on the game board is empty.
        """
        return self.move_on_board((row, col)) and self._game_board[row][col] == NONE
    
    def check_opponent(self, row: int, col: int, turn: str) -> bool:
        """ This function check to see if the given location on the game board is an opponent of the given
            player.
        """
        return self.move_on_board((row, col)) and self._game_board[row][col] == _opposite_turn(turn)
        
    def move_on_board(self, move: tuple) -> bool:
        """ Given a pair of game board coordinates, check to see if the location is valid within the game
            board's rows and columns.
        """
        return move[0] >= 0 and move[0] <= self._rows - 1 and \
               move[1] >= 0 and move[1] <= self._columns - 1

        
def _new_game_board(rows: int, columns: int, first_player: str) -> [[str]]:
    """ Given an amount of rows, columns, and the first player, this function constructs the initial Othello
        game board.
    """
    game_board = [ ]

    for row in range(rows):
        game_board.append([ ])
        for col in range(columns):
            game_board[-1].append(NONE)
    
    game_board[int(rows/2 - 1)][int(columns/2 - 1)] = first_player
    game_board[int(rows/2 - 1)][int(columns/2)]     = _opposite_turn(first_player)
    game_board[int(rows/2)][int(columns/2 - 1)]     = _opposite_turn(first_player)
    game_board[int(rows/2)][int(columns/2)]         = first_player

    return game_board


def _copy_game_state(game_state: GameState) -> GameState:
    """ This function provides a copy of the current game state so that changes can be made before applying it
        to the official game state.
    """
    return copy.deepcopy(game_state)


def _opposite_turn(turn: str) -> str:
    """ This function switches the current turn to the opponent.
    """
    if turn == WHITE:
        return BLACK
    else:
        return WHITE            
