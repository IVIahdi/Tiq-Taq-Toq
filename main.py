# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'

symbol_XO_color = '#800080'
Green_color = '#7BC043'


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tiq-Taq-Toq')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        ##########
        self.turn = 0
        self.Ent = False
        self.gamemode = 0
        ########

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0


    ###########################################
    def myQuatum(self):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.x(0)
        qc.measure([0, 1], [0, 1])

        Aer = AerSimulator()
        result = Aer.run(qc, shots=1).result().get_counts()
        mBits = list(result.keys())[0]  # Get measurement bits as a string e.g., '01'
        print(mBits)

        board_positions = np.argwhere(self.board_status == 5)

        for i, pos in enumerate(board_positions):
            if i < len(mBits):
                if mBits[i] == '1':
                    self.board_status[pos[0], pos[1]] = -1
                else:
                    self.board_status[pos[0], pos[1]] = 1
        
        self.redraw_board()


    def show_start_screen(self):
        # Clear the current canvas
        self.canvas.delete("all")

        # Add title or instructions
        self.canvas.create_text(size_of_board / 2, size_of_board / 4, 
                                text='Select Game Mode', font='cmr 20 bold', fill='black')

        # Button for Easy Mode
        easy_btn = Button(self.window, text='Easy Mode', command=lambda: self.set_game_mode('easy'))
        easy_btn_canvas = self.canvas.create_window(size_of_board / 2, size_of_board / 2 - 30,
                                                    window=easy_btn)

        # Button for Hard Mode
        hard_btn = Button(self.window, text='Hard Mode', command=lambda: self.set_game_mode('hard'))
        hard_btn_canvas = self.canvas.create_window(size_of_board / 2, size_of_board / 2 + 30,
                                                window=hard_btn)



    ######################################

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        # Reset the game variables
        self.player_X_turns = not self.player_X_starts
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        self.turn = 0
        self.Ent = False
        self.board_status = np.zeros(shape=(3, 3))
        self.redraw_board()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def redraw_board(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Redraw the grid lines
        self.initialize_board()

        # Redraw all the symbols based on board_status
        for i in range(3):  # Assume 3x3 board
            for j in range(3):
                pos = [i, j]
                if self.board_status[i][j] == 1:  # Assuming 1 is O
                    self.draw_O(pos)
                elif self.board_status[i][j] == -1:  # Assuming -1 is X
                    self.draw_X(pos)

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    ###################
    def draw_X_in_circle(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(np.array(logical_position))

        radius = symbol_size

        self.canvas.create_oval(grid_position[0] - radius, grid_position[1] - radius,
                                grid_position[0] + radius, grid_position[1] + radius,
                                width=symbol_thickness, outline=symbol_O_color)

        offset = radius * 0.707  # This adjusts the X to fit inside the circle (radius / sqrt(2))

        self.canvas.create_line(grid_position[0] - offset, grid_position[1] - offset,
                                grid_position[0] + offset, grid_position[1] + offset,
                                width=symbol_thickness, fill=symbol_X_color)

        self.canvas.create_line(grid_position[0] - offset, grid_position[1] + offset,
                                grid_position[0] + offset, grid_position[1] - offset,
                            width=symbol_thickness, fill=symbol_X_color)

    ###############
    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')

        print(self.board_status)


        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        
        return gameover

    
    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        
        #################
        if self.turn in [2,6]:
            self.Ent = True
        ########################

        
        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    if self.Ent: ###########3
                        self.draw_X_in_circle(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = 5
                        self.player_X_turns = not self.player_X_turns
                    else:
                        self.draw_X(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = -1
                        self.player_X_turns = not self.player_X_turns
                        ###################
                        self.myQuatum()
                        ###############
                    self.turn +=1 ###############33
            else:
                if not self.is_grid_occupied(logical_position):
                    if self.Ent: ####################3
                        self.draw_X_in_circle(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = 5
                        self.player_X_turns = not self.player_X_turns

                        
                        self.Ent = False
                    else:
                        self.draw_O(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = 1
                        self.player_X_turns = not self.player_X_turns
                    self.turn += 1 ###########3



            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = Tic_Tac_Toe()
game_instance.mainloop()

