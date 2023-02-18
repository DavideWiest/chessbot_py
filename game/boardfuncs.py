from .relations import *

def updateBoardInfo(board, boardInfo, piecesPos, side, pieceId, pieceIndex, previousPosition):
    boardInfo["lastMovePos"] = piecesPos[side][pieceId][pieceIndex]

    rookStartPosY = 0 if side==0 else 7

    if pieceId == ROOK:
        if previousPosition == (rookStartPosY, 0) and board[rookStartPosY, 0, side] == ROOK:
            boardInfo["firstRookMoved"] = True
        elif previousPosition == (rookStartPosY, 7) and board[rookStartPosY, 7, side] == ROOK:
            boardInfo["secondRookMoved"] = True

    elif pieceId == KING:
        boardInfo["kingMoved"] = True

    return boardInfo


