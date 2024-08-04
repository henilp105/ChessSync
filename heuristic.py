import chess
import chess.svg
import chess.polyglot
from evaluation import *
from app import get_board
from redis_auth import r

board = None

def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = (
        100 * (wp - bp)
        + 320 * (wn - bn)
        + 330 * (wb - bb)
        + 500 * (wr - br)
        + 900 * (wq - bq)
    )

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum(
        [
            -pawntable[chess.square_mirror(i)]
            for i in board.pieces(chess.PAWN, chess.BLACK)
        ]
    )
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum(
        [
            -knightstable[chess.square_mirror(i)]
            for i in board.pieces(chess.KNIGHT, chess.BLACK)
        ]
    )
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum(
        [
            -bishopstable[chess.square_mirror(i)]
            for i in board.pieces(chess.BISHOP, chess.BLACK)
        ]
    )
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum(
        [
            -rookstable[chess.square_mirror(i)]
            for i in board.pieces(chess.ROOK, chess.BLACK)
        ]
    )
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum(
        [
            -queenstable[chess.square_mirror(i)]
            for i in board.pieces(chess.QUEEN, chess.BLACK)
        ]
    )
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum(
        [
            -kingstable[chess.square_mirror(i)]
            for i in board.pieces(chess.KING, chess.BLACK)
        ]
    )

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval


# Searching the best move using minimax and alphabeta algorithm with negamax implementation
def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if depthleft == 0:
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
        if score > alpha:
            alpha = score
    return bestscore


def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def selectmove(depth):
    try:
        move = (
            chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(board).move
        )
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            board.pop()
        return bestMove


def algomove(game_id):
    global board
    board = get_board(game_id)
    move = selectmove(3)
    board.push(move)
    r.set(game_id, board.fen())
