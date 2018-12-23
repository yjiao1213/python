# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 17:13:28 2018

@author: fzhan
"""

 
#alpha-beta pruning
#record self.board,self.play_times,self.win_times for each action
#adjent expand to 2 or 3

import time
from copy import deepcopy
import math
import random
from itertools import product

class MCTS(object):
    """
    AI player, use Monte Carlo Tree Search with UCB
    """

    def __init__(self, board, play_turn, n_in_row=5, time=5):

        self.board = board
        self.play_turn = play_turn 
        self.time_limit = float(time) # time limit of each step
        self.n_in_row = n_in_row #if 5 positions in one line, win
        self.player = play_turn[0] 
        self.confident = 1.96 # the constant in UCB
        self.play_times = {} # {(player,move):times} record (player,move) simulating times
        self.win_times = {} # record win times of (player,mover)


    def get_action(self): # return move
        # if there is just one available position, return this one
        if len(self.board.availables) == 1:
            return self.board.availables[0] 

        self.play_times = {} 
        self.win_times = {}
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.time_limit:
            #simulation will change board, so separate the new board with old one
            board_copy = deepcopy(self.board)  
            play_turn_copy = deepcopy(self.play_turn) 
            self.run_simulation(board_copy, play_turn_copy) # run MCTS
            simulations += 1
            
        move = self.select_one_move() # choose the best move
        #print(self.play_times)
        return move


    def run_simulation(self, board, play_turn):
        """
        MCTS main process
        """
        visited_states = set() # records all moves before expand
        expand = True
        
        while True:
            # Selection
            player = self.get_player(play_turn) # get the current player
            availables = board.availables
            # if there is statistical information for each move, get move with maximum UCB
            if all(self.play_times.get((player, move)) for move in availables):
                log_total = math.log(
                    sum(self.play_times[(player, move)] for move in availables))
                value, move = max(
                    ((self.win_times[(player, move)] / self.play_times[(player, move)]) +
                     math.sqrt(self.confident * log_total / self.play_times[(player, move)]), move)
                    for move in availables) 
            else:
            #if there are the adjacent positions without statistical information
            #randomly choose position from them
                adjacents = []
                if len(availables) > self.n_in_row:                    
                    adjacents = self.adjacent_moves(board, player)     
                if len(adjacents):
                    move = random.choice(adjacents)
                else:
                    # else randomly choose a move from peripheral positions without statistical information
                    peripherals = []
                    for move in availables:
                        if not self.play_times.get((player, move)):
                            peripherals.append(move) 
                    move = random.choice(peripherals) 

            board.update(player, move)
            if expand:
                visited_states.add((player, move))

            # Expand
            # for each simulation, just expand once and add one move
            if expand and (player, move) not in self.play_times:
                expand = False
                self.play_times[(player, move)] = 0
                self.win_times[(player, move)] = 0
                
            #End simulation
            #if there is a winner or not postion left on board, the simulation is over
            is_full = not len(availables)
            win, winner = self.has_a_winner(board)
            if is_full or win: 
                break           

        # Back-propagation
        for player, move in visited_states:
            self.play_times[(player, move)] += 1 
            if player == winner:
                self.win_times[(player, move)] += 1 


    def get_player(self, players):
        p = players.pop(0)
        players.append(p)
        return p
  
    
    def isLegalMove(self,board,x,y):
        if 0<=x<board.width and 0<=y<board.height: return True
        else: return False

    
    def adjacent_moves(self, board, player):
        """
        get all adjacent positions in current board without statistical information
        """
        width = board.width
        height = board.height
        moved = list(set(range(width * height)) - set(board.availables))
        adjacents = set()           
        for m in moved:
            h = m // width
            w = m % width
            # within 2 steps
            digi=[-2,-1,0,1,2]
            for i,j in product(digi,repeat=2):
                if self.isLegalMove(board,w+i,h+j):
                    adjacents.add((w+i)*width+(h+j))
    
        adjacents = list(set(adjacents) - set(moved))
        for move in adjacents:
            if self.play_times.get((player, move)):
                adjacents.remove(move)
        return adjacents
    

    def select_one_move(self):
        percent_wins={}
        for move in self.board.availables:
            percent_wins[move]=self.win_times.get((self.player, move), 0) / self.play_times.get((self.player, move), 1)
        # select the move with most win percentage
        return max(percent_wins,key=percent_wins.get)

    def has_a_winner(self, board):
        """
        check if there is a winner
        """
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if(len(moved) < self.n_in_row + 2):
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = self.n_in_row
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]
            # Horizontal alignment.
            if (w in range(width - n + 1) and
                len(set(states[i] for i in range(m, m + n))) == 1): 
                return True, player
            # Vertical alignment.
            if (h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * width, width))) == 1): 
                return True, player
            # the right angle 
            if (w in range(width - n + 1) and h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1): 
                return True, player
            # the left angle
            if (w in range(n - 1, width) and h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1): 
                return True, player

        return False, -1
    
    def __str__(self):
        return "AI "

