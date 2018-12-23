# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 17:12:17 2018

@author: fzhan
"""

class Board(object):
    """
    board for game
    """
    def __init__(self, width=19, height=19, n_in_row=5):
        self.width = width
        self.height = height 
        self.states = {} # {location:player} record the current states of board
        self.n_in_row = n_in_row # A number of identical pieces are counted as a victory.

    def init_board(self):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not less than %d' % self.n_in_row) 
        self.availables = list(range(self.width * self.height)) 
        for m in self.availables:
            self.states[m] = -1 # -1 means the position is empty

    def move_to_location(self, move):
        h = move  // self.width
        w = move  %  self.width
        return [h, w]

    def location_to_move(self, location):
        if(len(location) != 2):
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if(move not in range(self.width * self.height)):
            return -1
        return move

    def update(self, player, move): # once a player move, update the board
        self.states[move] = player
        self.availables.remove(move)