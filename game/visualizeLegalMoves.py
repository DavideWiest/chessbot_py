from .relations import *
from .pieces import *

def visualizeLegalMoves(self, pieceId: int, startPos: tuple=(4,4)):
    
    newBoard = numpy.zeros((8,8,2), dtype=numpy.byte)

    newBoard[startPos[0], startPos[1],0] = pieceId

    newPiecesPos = {
        0: {KING: [], PAWN: [], BISHOP: [], ROOK: [], QUEEN: [], KNIGHT: []},
        1: {KING: [], PAWN: [], BISHOP: [], ROOK: [], QUEEN: [], KNIGHT: []}
    }

    newPiecesPos[0][pieceId].append([4,4])

    #### edit board and piecePos
    newBoard[:, 3, 1] = 1


    ####

    legalMoves = PIECES_ID_TO_CLASS[pieceId].getLegalMoves(newBoard, startPos, 0, newPiecesPos, pieceId, 0, 2)

    for x, y in legalMoves:
        newBoard[x,y,1] = 12

    rows = []

    for rowindex in range(8):
        # rows.append(f"{8-rowindex}   " + "   ".join(
        rows.append(f"{rowindex}   " + "   ".join(
            str(
                self.preparePiece(newBoard[rowindex, colindex, 0], 0, 12)
                if newBoard[rowindex, colindex, 0] != 0 
                else self.preparePiece(newBoard[rowindex, colindex, 1], 1, 12)
            )
            for colindex in range(8)
            ))
    # rows.append(
    #     "    " + "   ".join([f"{ascii_uppercase[i]}" for i in range(8)])
    # )
    rows.append(
        "    " + "   ".join([f"{i}" for i in range(8)])
    )

    print("\n\n".join(rows))