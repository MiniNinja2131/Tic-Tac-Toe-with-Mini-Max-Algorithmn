import random
import math

class Player:
    def __init__(self, letter):
        # Either letter x or o
        self.letter = letter

    # Allow all players to get their next move given the current state of the game
    def getMove(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def getMove(self, game):
        # Computer will randomly choose an valid spot for their next move
        square = random.choice(game.availableMove())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def getMove(self, game):
        validSquare = False
        # User has not inputted an value ie 0 for the top left square
        val = None

        while not validSquare:
            square = input(self.letter + '\'s turn. Input (0-8):')
            # Validation checks
            # 1) Casting input to integer, if it fails then we can say its invalid
            # 2) if that spot is not available on the board, we can also say its invalid
            try:
                val = int(square)
                if val not in game.availableMove():#
                    raise ValueError
                # If both validation check passes then its an valid move
                validSquare = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def getMove(self, game):
        if len(game.availableMove()) == 9:
            # Randomly choose an move at the start
            square = random.choice(game.availableMove())
        else:
            # MinMax algorithm for AI
            square = self.miniMax(game, self.letter)['position']
        return square

    def miniMax(self, state, player):
        # This is myself ~ trying to maximise my chance to win
        maxPlayer = self.letter
        # Assigning computer with the right letter
        miniPlayer = 'O' if player == 'X' else 'X'

        # First, we check if the previous move is a winner
        # This would be our base case for this scenario
        if state.currentWinner == miniPlayer:
            # We should return position AND score because we need to keep track of the score for the minimax
            return {
                # Essentially look at the board and lets say there are 3 empty squares the calculation would be (3+1) mutiply by either 1 or -1 depending if you are the minimising or maximising player
                'position': None, 'score': 1 * (state.numEmptySquare() + 1) if miniPlayer == maxPlayer else -1 * (state.numEmptySquare() + 1)
            }
        # No empty squares left
        elif not state.emptySquare():
            return {'position': None, 'score': 0}

        if player == maxPlayer:
            # best variable will save the position of the move and the score that the maximising player could make (trying to get the highest score)
            # Initialise the score as negative infinity meaning any score would be better than current 
            best = {'position': None, 'score': -math.inf}
        else:
            # Initialise the score as positive infinity meaning any score would be better than current for the minimising player (trying to get the lowest score)
            best = {'position': None, 'score': math.inf}

        for possibleMove in state.availableMove():
            # Step 1: Make a move, try that space
            state.makeMove(possibleMove, player)

            # Step 2: Simulate game from that point using minimax recursively
            # Alternate between players
            simScore = self.miniMax(state, miniPlayer)

            # Step 3: Undo the move to try out the different possibilities
            state.board[possibleMove] = ' '
            state.currentWinner = None
            simScore['position'] = possibleMove

            # Step 4: Update the dictionaries if necessary (best)
            if player == maxPlayer:
                # Trying to maximise the max player
                if simScore['score'] > best['score']:
                    # Replace current best move with the new best move
                    best = simScore
            else:
                # Trying to minimise the other player (aka computer)
                if simScore['score'] < best['score']:
                    # Replace current best move with the new best move
                    best = simScore                 
        return best