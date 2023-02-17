from .relations import *

def updateBoardInfo(board, boardInfo, side, piecePos, pieceId, pieceIndex, previousPosition):
    boardInfo["lastMovePos"] = piecePos[side][pieceId][pieceIndex]

    rookStartPosY = 0 if side==0 else 7

    if pieceId == ROOK:
        if previousPosition == board[rookStartPosY, 0, side] == ROOK:
            boardInfo["firstRookMoved"] = True
        elif previousPosition == board[rookStartPosY, 7, side] == ROOK:
            boardInfo["secondRookMoved"] = True

    elif pieceId == KING:
        boardInfo["kingMoved"] = True

    return boardInfo