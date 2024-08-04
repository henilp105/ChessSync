import chess
import chess.svg
import chess.polyglot
import time
import chess.pgn
import chess.engine
from flask import Response, request, render_template, jsonify,abort
from evaluation import *
from app import app
from heuristic import algomove
import uuid
from redis_auth import r
from app import get_board

board = None
game_id = None

@app.route('/favicon.ico')
def favicon():
    abort(404)

@app.route("/")
def index():
    return main(None)

@app.route("/<gameid>")
def main(gameid=None,error=None):

    global board, game_id
    if gameid is None: 
        gameid = generate_local()

    game_id = gameid
    board = get_board(game_id)
    
    if board.is_stalemate():
        error = "draw by stalemate"
    elif board.is_checkmate():
        error = "Checkmate"
    elif board.is_insufficient_material():
        error = "draw by insufficient material"
    elif board.is_check():
        error = "Check"
    error = error if error else ""
    turn = str(board.turn) if not board.is_game_over() else ""
    return render_template("index.html", time=time.time(), error=error,turn=turn)


# Display Board
@app.route("/board.svg/")
def board_state():
    return Response(chess.svg.board(board=board, size=700), mimetype="image/svg+xml")


# Make player Move
@app.route("/move/")
def move():
    error = None
    global game_id
    try:
        move = request.args.get("move", default="")
        board.push_san(move)
        r.set(game_id, board.fen())
    except Exception as e:
        error = str(e)
    return main(game_id,error)


# Refresh to Recieve Player 2 Move
@app.route("/recieve/", methods=["POST"])
def recieve():
    global game_id
    return main(game_id)


# Algorithm Move
@app.route("/algo/",methods=["POST"])
def algo():
    error = None
    global game_id
    try:
        algomove(game_id)
    except Exception as e:
        error = "illegal move, try again: " + str(e)
    return main(game_id,error)


@app.route("/reset/", methods=["POST"])
def reset_game():
    board.reset()
    return main(None)

@app.route("/generate")
def generate():
    game_id = str(uuid.uuid4())
    board = chess.Board()
    r.set(game_id, board.fen())
    return jsonify({"data": game_id }), 200

def generate_local():
    game_id = str(uuid.uuid4())
    board = chess.Board()
    r.set(game_id, board.fen())
    return game_id


if __name__ == "__main__":
    app.run()
