from flask import Flask
from redis_auth import r
import chess

app = Flask(__name__)

def get_board(game_id):
    board = chess.Board()    
    board.set_fen(r.get(game_id).decode('utf-8'))
    return board