import os
from ABpruning.GoAI import searcher
from ABpruning.chess_board import ChessBoard
from MCTS.MCTS import MCTS
from MCTS.board import Board

EMPTY = 0
BLACK = 1
WHITE = 2

# ai_1 = searcher()
# print(ai_1)

class Game(object):

### alpha-beta vs alpha-beta

    def ab_vs_ab(self):
        step = 0
        board = ChessBoard()
        ab_ab_end = False
        ## BLACK goes first
        ini_x = 9
        ini_y = 9
        board.draw_xy(ini_x,ini_y,BLACK)
        print("BLACK Places at position :",ini_x,ini_y)
        step = step + 1
        ai_1 = searcher()
        ai_2 = searcher()

        while ab_ab_end == False:

            # ai 2 place chess
            ai_2.board = board.board()
            score_2,x_2,y_2 = ai_2.search(WHITE,2)
            print("WHITE Places at position :", x_2, y_2,"Score:",score_2)
            board.draw_xy(x_2,y_2,WHITE)
            step = step + 1
            winner = board.anyone_win(x_2,y_2)
            if winner != EMPTY:
                if winner == BLACK:
                    print("Winner is Black")
                else:
                    print("Winner is WHITE")
                ab_ab_end = True
                break

            # ai 1 place chess
            ai_1.board = board.board()
            score_1,x_1,y_1 = ai_1.search(BLACK,2)
            print("BLACK Places at position :", x_1, y_1, "Score:", score_1)
            board.draw_xy(x_1,y_1,BLACK)
            step = step + 1
            winner = board.anyone_win(x_1, y_1)
            if winner != EMPTY:
                if winner == BLACK:
                    print("Winner is Black")
                else:
                    print("Winner is WHITE")
                ab_ab_end = True
                break

    def mc_vs_mc(self):
        print("Monte Carlo AI vs. Monte Carlo AI")
        # [p1,p2]=random.sample([1,2],2)
        [p1, p2] = [1, 2]
        board = Board()
        board.init_board()

        ai1 = MCTS(board, [p1, p2], 5,5)
        ai2 = MCTS(board, [p1, p2], 5,5)
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
            print("Move, ",move)

            location = board.move_to_location(move)#self.board.move_to_location(move)
            #print("%s move: %d,%d\n" % (player_in_turn, location[0], location[1]))
            #self.board.update(p, move)
            board.update(p,move)

            # self.graphic(self.board, human, ai1)
            # self.graphic(self.board,ai2,ai1)
            #end, winner = self.game_end(ai1)
            end,winner = self.mc_vs_mc_game_end(ai1,board)
            if end:
                if winner != -1:
                    print("Game end. Winner is", players[winner])
                break

    def ab_vs_mc(self):
        print("Alpha-Beta Pruning vs. Monte Carlo Search")
        print("Alpha-Beta Pruning is BLACK, Monte Carlo Search is WHITE")
        ab_mc_board_1 = ChessBoard()
        ab_mc_board_2 = Board()
        ab_mc_board_2.init_board()

        ini_x = 9
        ini_y = 9
        ab_mc_board_1.draw_xy(ini_x, ini_y, BLACK)

        # Define The AIs
        ai_1 = searcher()
        ai_2 = MCTS(ab_mc_board_2,[1,2],5,5)

        players = {1: "Alpha-Beta Pruning: White", 2: "Monte Carlo Search: Black"}

        turn = [2,1]
        while True:
            p = turn.pop(0)
            turn.append(p)

            if p == 1: #ai_2's turn,WHITE
                move = ai_2.get_action()
                location = ab_mc_board_2.move_to_location(move)
                ab_mc_board_2.update(p,move)

                end, winner = self.mc_vs_mc_game_end(ai_2, ab_mc_board_2)
                if end:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                    break


                ab_mc_board_1.draw_xy(location[0],location[1],WHITE)



            else:  #ai_1's turn, BLACK

                ai_1.board = ab_mc_board_1.board()
                score_2, x_2, y_2 = ai_1.search(BLACK, 2)
                ab_mc_board_1.draw_xy(x_2,y_2,BLACK)
                print("ai 1 move",x_2, y_2)
                winner = ab_mc_board_1.anyone_win(x_2,y_2)

                if winner != EMPTY:
                    if winner == BLACK:
                        print("Winner is Black")
                    else:
                        print("Winner is WHITE")
                    break

                ab_mc_board_1.draw_xy(x_2,y_2,BLACK)
                location = [x_2,y_2]
                move = ab_mc_board_2.location_to_move(location)
                ab_mc_board_2.update(p,move)

    def mc_vs_mc_game_end(self,ai,board):

        """
        check if game is over
        """
        win, winner = ai.has_a_winner(board)
        if win:
            return True, winner
        elif not len(board.availables):
            print("Game end. Tie")
            return True, -1
        return False, -1




# Black vs White


### MCTS vs MCTS


### Competition

if __name__ == "__main__":

    Game = Game()
    var = input("Please enter 1: Alpha-Beta Pruning Search; 2: Monte Carlo Search; 3: Alpha-Beta Pruning vs. Monte Carlo: ")
    print("Var, ",var)

    if int(var) == 1:
        Game.ab_vs_ab()
    elif int(var) == 2:
        Game.mc_vs_mc()
    elif int(var) == 3:
        Game.ab_vs_mc()
    else:
        print("Plesae Input again.")
    #Game.ab_vs_ab()
    #Game.mc_vs_mc()
    #Game.ab_vs_mc()