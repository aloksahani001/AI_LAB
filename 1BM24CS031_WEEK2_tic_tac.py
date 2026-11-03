import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]

        while True:
            choice = input("Choose X or O: ").upper()

            if choice == 'X' or choice == 'O':
                self.player = choice
                self.computer = 'O' if choice == 'X' else 'X'
                break
            else:
                print("Invalid choice. Please choose X or O.")

    def displayBoard(self):
        print()
        print(self.board[0], '|', self.board[1], '|', self.board[2])
        print("---------")
        print(self.board[3], '|', self.board[4], '|', self.board[5])
        print("---------")
        print(self.board[6], '|', self.board[7], '|', self.board[8])
        print()

    def checkWinner(self, symbol):
        if self.board[0] == self.board[1] == self.board[2] == symbol:
            return True
        if self.board[3] == self.board[4] == self.board[5] == symbol:
            return True
        if self.board[6] == self.board[7] == self.board[8] == symbol:
            return True
        if self.board[0] == self.board[3] == self.board[6] == symbol:
            return True
        if self.board[1] == self.board[4] == self.board[7] == symbol:
            return True
        if self.board[2] == self.board[5] == self.board[8] == symbol:
            return True
        if self.board[0] == self.board[4] == self.board[8] == symbol:
            return True
        if self.board[2] == self.board[4] == self.board[6] == symbol:
            return True

        return False

    def playerMove(self):
        while True:
            try:
                position = int(input("Enter position (1-9): "))

                if position < 1 or position > 9:
                    print("Invalid position. Enter a number between 1 and 9.")
                elif self.board[position - 1] != ' ':
                    print("Position already occupied.")
                else:
                    self.board[position - 1] = self.player
                    break

            except ValueError:
                print("Invalid input. Enter a number between 1 and 9.")

    def computerMove(self):
        emptyPositions = []

        for i in range(9):
            if self.board[i] == ' ':
                emptyPositions.append(i)

        position = random.choice(emptyPositions)
        self.board[position] = self.computer

        print("Computer chose position", position + 1)

    def play(self):
        currentPlayer = 'X'

        for turn in range(9):
            self.displayBoard()

            if currentPlayer == self.player:
                print("Your turn")
                self.playerMove()

                if self.checkWinner(self.player):
                    self.displayBoard()
                    print("You win!")
                    return

                currentPlayer = self.computer

            else:
                print("Computer's turn")
                self.computerMove()

                if self.checkWinner(self.computer):
                    self.displayBoard()
                    print("Computer wins!")
                    return

                currentPlayer = self.player

        self.displayBoard()
        print("It's a Draw!")


game = TicTacToe()
game.play()