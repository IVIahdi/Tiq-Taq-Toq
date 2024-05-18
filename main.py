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
black = '#000000'
###########################
class StartupScreen:
    def __init__(self):
        self.root = Tk()
        self.root.title('Tiq-Taq-Toq Mode Selection')

        self.canvas = Canvas(self.root, width=400, height=300)
        self.canvas.pack()

        entangle_btn = Button(self.root, text='Entanglement Mode (Fair)', command=lambda: self.start_game(0), width=25, height=4, bg='lightgreen', fg='black')
        entangle_btn_canvas = self.canvas.create_window(200, 100, window=entangle_btn)

        superpos_btn = Button(self.root, text='Superposition Mode (Unfair)', command=lambda: self.start_game(1), width=25, height=4, bg='#FFCCCC', fg='black')
        superpos_btn_canvas = self.canvas.create_window(200, 200, window=superpos_btn)

    def start_game(self, mode):
        self.root.destroy()
        game_instance = Tiq_Taq_Toq(mode)
        game_instance.mainloop()

    def run(self):
        self.root.mainloop()
###########################################
class Tiq_Taq_Toq():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self, mode):
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
        self.gamemode = mode
        self.update_status_text()
        ########

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0


    ###########################################
    def myQuatum(self):
        qc = QuantumCircuit(2, 2)
        qc.h(0)

        if self.gamemode:
            qc.h(1)
        else:
            qc.cx(0, 1)
            qc.x(0)
        
        qc.measure([0, 1], [0, 1])

        # E 0 S 1

        Aer = AerSimulator()
        result = Aer.run(qc, shots=1).result().get_counts()
        mBits = list(result.keys())[0][::-1]
        print(mBits)
        #1 X 0 O

        board_positions = np.argwhere(self.board_status == 5)

        for i, pos in enumerate(board_positions):
            if i < len(mBits):
                if mBits[i] == '1':
                    self.board_status[pos[0], pos[1]] = -1
                else:
                    self.board_status[pos[0], pos[1]] = 1
        
        self.redraw_board()
        
    def update_status_text(self):
        status = f'Quantum Move {"O" if self.turn  % 2 == 1 else "X"}' if self.turn in [2,3,6,7] else f'Classical Move {"O" if self.turn  % 2 == 1 else "X"}'
        self.canvas.delete("status_text")
        self.canvas.create_text(size_of_board / 2, size_of_board / 2, text=status, font="cmr 20 bold", fill="purple", tags="status_text")

    ######################################

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
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
        self.update_status_text()
        ########


    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def redraw_board(self):
        self.canvas.delete("all")
        self.initialize_board()

        for i in range(3):
            for j in range(3):
                pos = [i, j]
                if self.board_status[i][j] == 1:  # 1 is O
                    self.draw_O(pos)
                elif self.board_status[i][j] == -1:  # -1 is X
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

        offset = radius * 0.707

        self.canvas.create_line(grid_position[0] - offset, grid_position[1] - offset,
                                grid_position[0] + offset, grid_position[1] + offset,
                                width=symbol_thickness, fill=symbol_X_color)

        self.canvas.create_line(grid_position[0] - offset, grid_position[1] + offset,
                                grid_position[0] + offset, grid_position[1] - offset,
                            width=symbol_thickness, fill=symbol_X_color)

    ###############
    def display_gameover(self):

        if self.X_wins and not self.O_wins:
            self.X_score += 1
            text = 'Winner: (X)'
            color = symbol_X_color
        elif self.O_wins and not self.X_wins:
            self.O_score += 1
            text = 'Winner: (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        
        # self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=black,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie               : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=black,
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
    # Check winners
        self.X_wins = self.is_winner('X')
        self.O_wins = self.is_winner('O')

        if self.X_wins and self.O_wins:
            print("Anomaly detected: both players marked as winners.")
            print("Game is declared a tie.")
            self.tie = True 
        elif self.X_wins:
            print('X wins')
            return True 
        elif self.O_wins:
            print('O wins')
            return True 

        if not self.X_wins and not self.O_wins:
            self.tie = self.is_tie()
            if self.tie:
                print('Its a tie')

        return self.X_wins or self.O_wins or self.tie

    
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
                        if self.turn != 0:
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


            self.update_status_text()  ####################

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


# game_instance = Tiq_Taq_Toq()
# game_instance.mainloop()

startup_screen = StartupScreen()
startup_screen.run()