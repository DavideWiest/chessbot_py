from .relations import *

def updateBoardInfo(board, boardInfoOfSide, piecesPos, side, pieceId, pieceIndex, previousPosition):
    boardInfoOfSide["lastMovePos"] = piecesPos[side][pieceId][pieceIndex]

    rookStartPosY = 0 if side==0 else 7

    if pieceId == ROOK:
        if previousPosition == (rookStartPosY, 0) and board[rookStartPosY, 0, side] == ROOK:
            boardInfoOfSide["firstRookMoved"] = True
        elif previousPosition == (rookStartPosY, 7) and board[rookStartPosY, 7, side] == ROOK:
            boardInfoOfSide["secondRookMoved"] = True

    elif pieceId == KING:
        boardInfoOfSide["kingMoved"] = True

    return boardInfoOfSide


