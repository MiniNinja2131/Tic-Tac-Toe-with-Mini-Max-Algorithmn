from player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer
import time

class TicTacToe:
    def __init__(self):
        # Representing a 3x3 board where index 0 = top left and 9 = bottom right
        self.board = [' ' for _ in range(9)]
        # Keep track of winner
        self.currentWinner = None

    def printBoard(self):
        # Getting the rows of the board
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    @staticmethod
    def printBoardNums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        numberBoard = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in numberBoard:
            print('| ' + ' | '.join(row) + ' |')
    
    def availableMove(self):
    # To comment out multiple lines you can use either Alt + Shift + A or Ctrl + /
    #  Essentially does the same thing as the for loop below  
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    #    moves = []
    #    for (i, spot) in enumerate(self.board):
    #        # For example ['x', 'x', 'o'] --> [(0, 'x'), (1, 'x'), (2, 'x')]
    #        if spot == ' ':
    #            moves.append(i)
    #        return moves

    # Return true or false to see if theres any more empty spaces on the board
    def emptySquare(self):
        return ' ' in self.board

    # Return how many more empty spaces are on the board
    def numEmptySquare(self):
        return self.board.count(' ')
        # return len(self.availableMove())

    def makeMove(self, square, letter):
        # If valid move, then make the move (assign the letter to the square)
        # Then return true. If invalid then return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.currentWinner = letter
            return True
        else:
            return False
    
    # Winner if 3 in a row anywhere, must check all possibility 
    def winner(self, square, letter):
        # Checking row first
        rowIndex = square // 3
        row = self.board[rowIndex*3 : (rowIndex+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Check column
        colIndex = square % 3
        column = [self.board[colIndex+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals
        # But only if the square is an even number (0, 2 , 4, 6, 8)
        # Since these are the only possible move to win as an diagonal
        if square % 2 == 0:
            # Top left to bottom right diagonal line
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            # Top right to bottom left diagonal line
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        # If failed then false no winner yet
        return False

def play(game, xPlayer, oPlayer, printGame=True):
    # Return the winner of the game (the letter either X or O) if None then it means that the game was an tie
    if printGame:
        game.printBoardNums()
    
    # Where X starts first in this game
    letter = 'X'
    # Iterate while the game still has empty spaces left
    # (we don't need to have to worry about winner because we'll just return that which breaks the loop)

    while game.emptySquare():
        # Get the move from the appropriate player
        if letter == 'O':
            square = oPlayer.getMove(game)
        else:
            square = xPlayer.getMove(game)

        # Function which allow the user to make their move
        if game.makeMove(square, letter):
            if printGame:
                print(letter + f' makes a move to square {square}')
                game.printBoard()
                # Just creating an empty line
                print('')
            
            if game.currentWinner:
                if printGame:
                    print(letter + ' has won!')
                return letter
            
            # Allow the game to alternate between both players so between X and O
            letter = 'O' if letter == 'X' else 'X'

            # Pause before the next player move (ie computer)
            time.sleep(0.8)

    if printGame:
        print('It\'s an draw!')

# __name__ allow you to check when the file is directly or imported as a module ~ kind of running a script essentially 
if __name__ == '__main__':
    # Data sanitization (Limit user inputting numbers only)
    while True:
        try:
            # Listing out the options that the user can choose from
            print("Here are the option: \nOption 1) Player v Player \nOption 2) Player vs AI(Random) \nOption 3) Player vs AI(Min-Max)")
            gameSetting = int(input("Choose a game setting: "))
            if(gameSetting < 1  or gameSetting > 3):
                raise ValueError

            # Player vs Player option
            if(gameSetting == 1):
                # Player 1
                xplayer = HumanPlayer('X')
                # Player 2
                oPlayer = HumanPlayer('O')
            # Player vs AI (Choose a random square) option
            elif(gameSetting == 2):
                xplayer = HumanPlayer('X')
                oPlayer = RandomComputerPlayer('O')
            # Player vs AI (Min-Max Algorithm) option
            else:
                xplayer = HumanPlayer('X')
                oPlayer = GeniusComputerPlayer('O')
            game = TicTacToe()
            play(game, xplayer, oPlayer, printGame=True)
            break
        except ValueError:
            print("Please enter a valid integer in the range of 1-3 \n")