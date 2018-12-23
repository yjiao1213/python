# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 17:14:03 2018

@author: fzhan
"""
from MCTS import MCTS
import random
from board import Board

class Human(object):
    """
    human player
    """

    def __init__(self, board, player):
        self.board = board
        self.player = player

    def get_action(self):
        try:
            location = [int(n, 10) for n in input("Your move: format #,#        ").split(",")]
            move = self.board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in self.board.availables:
            print("invalid move")
            move = self.get_action()
        return move

    def __str__(self):
        return "Human"
    
    
class Game(object):
    """
    game server
    """

    def __init__(self, board, **kwargs):
        self.board = board
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.time = float(kwargs.get('time', 5))
        self.player = [1, 2] # player1 and player2

                
    def start(self):   
        #[p1,p2]=random.sample([1,2],2)
        [p1,p2] = [1,2]
        self.board.init_board()            
        ai1 = MCTS(self.board, [p1,p2], self.n_in_row, self.time)
        ai2 = MCTS(self.board, [p1,p2], self.n_in_row, self.time)
        #human = Human(self.board, p2)

        turn=[p1,p2]
        #players={p1:ai1,p2:human}
        players = {p1:ai1,p2:ai2}
        #random.shuffle(turn) #randomly choose human or computer move firstly
        while True:
            p = turn.pop(0)
            turn.append(p)
            player_in_turn = players[p]
            print(players[p])
            move = player_in_turn.get_action()
            
            location = self.board.move_to_location(move)

            print("%s move: %d,%d\n" % (player_in_turn,location[0], location[1]))
            self.board.update(p, move)

            #self.graphic(self.board, human, ai1)
            #self.graphic(self.board,ai2,ai1)
            end, winner = self.game_end(ai1)
            if end:
                if winner != -1:
                    
                    print("Game end. Winner is", players[winner])
                break

    def start_2(self):
        # [p1,p2]=random.sample([1,2],2)
        [p1, p2] = [1, 2]
        self.board.init_board()
        ai1 = MCTS(self.board, [p1, p2], self.n_in_row, self.time)
        ai2 = MCTS(self.board, [p1, p2], self.n_in_row, self.time)
        # human = Human(self.board, p2)

        turn = [p1, p2]
        # players={p1:ai1,p2:human}
        players = {p1: ai1, p2: ai2}
        # random.shuffle(turn) #randomly choose human or computer move firstly
        while True:
            p = turn.pop(0)
            turn.append(p)
            player_in_turn = players[p]
            print(players[p])
            move = player_in_turn.get_action()

            location = self.board.move_to_location(move)


            print("%s move: %d,%d\n" % (player_in_turn, location[0], location[1]))
            self.board.update(p, move)


            # self.graphic(self.board, human, ai1)
            # self.graphic(self.board,ai2,ai1)
            end, winner = self.game_end(ai1)
            if end:
                if winner != -1:
                    print("Game end. Winner is", players[winner])
                break


    def game_end(self, ai):
        """
        check if game is over
        """
        win, winner = ai.has_a_winner(self.board)
        if win:
            return True, winner
        elif not len(self.board.availables):
            print("Game end. Tie")
            return True, -1
        return False, -1
    

    def graphic(self, board, human, ai):
        """
        visilize the board
        """
        width = board.width
        height = board.height

        print("Human Player", human.player, "with X".rjust(3))
        print("AI    Player", ai.player, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                if board.states[loc] == human.player:
                    print('X'.center(8), end='')
                elif board.states[loc] == ai.player:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')
            
if __name__ == "__main__":
    board=Board()
    g=Game(board)
    g.start_2()
    # turn = [1,2]
    # t = turn.pop(0)
    # print(turn,t)