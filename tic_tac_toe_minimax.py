import tkinter as tk
from tkinter import messagebox
import copy

PLAYER = 'X'
COMPUTER = 'O'

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with Minimax")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', font=('Arial', 32), width=5, height=2,
                                command=lambda row=i, col=j: self.player_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def player_move(self, row, col):
        if self.board[row][col] == '' and not self.check_winner(self.board):
            self.board[row][col] = PLAYER
            self.buttons[row][col].config(text=PLAYER, state='disabled')
            if self.check_winner(self.board):
                self.end_game("You win!")
            elif self.is_full(self.board):
                self.end_game("It's a draw!")
            else:
                self.root.after(300, self.computer_move)

    def computer_move(self):
        _, move = self.minimax(copy.deepcopy(self.board), True)
        if move:
            row, col = move
            self.board[row][col] = COMPUTER
            self.buttons[row][col].config(text=COMPUTER, state='disabled')
            if self.check_winner(self.board):
                self.end_game("Computer wins!")
            elif self.is_full(self.board):
                self.end_game("It's a draw!")

    def minimax(self, board, is_maximizing):
        winner = self.check_winner(board)
        if winner == PLAYER:
            return -1, None
        elif winner == COMPUTER:
            return 1, None
        elif self.is_full(board):
            return 0, None

        if is_maximizing:
            best_score = -float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = COMPUTER
                        score, _ = self.minimax(board, False)
                        board[i][j] = ''
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = PLAYER
                        score, _ = self.minimax(board, True)
                        board[i][j] = ''
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)
            return best_score, best_move

    def is_full(self, board):
        return all(cell != '' for row in board for cell in row)

    def check_winner(self, board):
        # Rows, columns and diagonals
        lines = board + list(zip(*board)) + [
            [board[i][i] for i in range(3)],
            [board[i][2 - i] for i in range(3)]
        ]
        for line in lines:
            if all(cell == PLAYER for cell in line):
                return PLAYER
            if all(cell == COMPUTER for cell in line):
                return COMPUTER
        return None

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')


# Run the game
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
