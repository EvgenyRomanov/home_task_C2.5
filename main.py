from external_logic import *


board_ai = Game.random_board()
board_user = Game.random_board(hid=False)

user = User(board_user, board_ai)
ai = AI(board_ai, board_user)

game = Game(user, ai)
game.start()













