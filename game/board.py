from .pieces import *
from .move import *
import numpy



class ChessBoard():
    """"
    Chess board where all positions are stored
    side is the respective player side (white = 1, black = 0)
    """

    def __init__(self):
        "initialize board"

        self.board = numpy.zeros((8,8,2), dtype=numpy.byte)

        # 0 = white = on the top half
        # 1 = black = on the bottom half
        # will be switched upside down when viewing because x=0 is at the bottom in chess

        # pawn row
        self.board[1, :, 0] = PAWN

        # rooks
        self.board[0, 7, 0] = ROOK
        self.board[0, 0, 0] = ROOK

        # knights
        self.board[0, 6, 0] = KNIGHT
        self.board[0, 1, 0] = KNIGHT

        # bishops
        self.board[0, 5, 0] = BISHOP
        self.board[0, 2, 0] = BISHOP

        # queens
        self.board[0, 4, 0] = QUEEN

        # kings
        self.board[0, 3, 0] = KING


        # pawn row
        self.board[6, :, 1] = PAWN

        # rooks
        self.board[7, 7, 0] = ROOK
        self.board[7, 0, 0] = ROOK

        # knights
        self.board[7, 6, 0] = KNIGHT
        self.board[7, 1, 0] = KNIGHT

        # bishops
        self.board[7, 5, 0] = BISHOP
        self.board[7, 2, 0] = BISHOP

        # queens
        self.board[7, 4, 0] = QUEEN

        # kings
        self.board[7, 3, 0] = KING

        self.piecesPos = {
            0: {
                KING: [[0,0]]
            },
            1: {
                KING: [[0,0]]
            }
            impement
        }


    def getBoard(self, dim: int = 1):
        "get the board either 1 or 2 dimensional"

        assert dim in (1,2)

        # to implement

    
    def makeMove(self, piecePos: tuple, move: Move):
        "move piece"

        currentPiecePos = self.piecesPos[move.side][move.p]
        piecePosIndex = currentPiecePos.index(list(piecePos))

        self.board[
            currentPiecePos[piecePosIndex][0], currentPiecePos[piecePosIndex][1], move.side
        ] = 0

        currentPiecePos[piecePosIndex][0] += move.x
        currentPiecePos[piecePosIndex][1] += move.y

        toRemove = None
        for enemyPId, enemyPiecesPos in self.piecesPos[0 if move.side==1 else 1].items():
            for enemyPiecePos in enemyPiecesPos:
                if enemyPiecePos == currentPiecePos[piecePosIndex]:
                    toRemove = (enemyPId, enemyPiecesPos.index(enemyPiecePos))
                    break

        if toRemove != None:
            self.piecesPos[0 if move.side==1 else 1][toRemove[0]].pop(toRemove[1])
            self.board[
                currentPiecePos[piecePosIndex][0],
                currentPiecePos[piecePosIndex][1],
                0 if move.side==1 else 1
            ] = 0

        # castling

        if move.original.lower() == "o-o":
            self.handleCastling(move, 0, 2)
            
        elif move.original.lower() == "o-o-o":
            self.handleCastling(move, 7, 5)

        # promoting
        elif "=" in move.original:
            self.handlePromotion(move, piecePosIndex)

        return True

    def handleCastling(self, move: Move, rookPosBefore: int, rookPosAfter: int):
        primaryPieceRow = 0 if move.side == 0 else 7
        rookIndex = self.piecesPos[move.side][ROOK].index([
            rookPosBefore, primaryPieceRow
        ])

        rookPos = self.piecesPos[move.side][ROOK][rookIndex]
        self.piecesPos[move.side][ROOK][rookIndex] = [rookPosAfter, primaryPieceRow]
        self.board[rookPos[0], rookPos[1], move.side] = 0
        self.board[rookPosAfter, primaryPieceRow, move.side] = ROOK

    def handlePromotion(self, move: Move, piecePosIndex):
        pieceId = PIECES_STR_TO_ID[move.original.split("=")[1]]
        piecePos = self.piecesPos[move.side][PAWN][piecePosIndex]
        self.piecesPos[move.side][PAWN].pop(piecePosIndex)
        self.piecesPos[move.side][pieceId].append(piecePos)
        self.board[piecePos[0], piecePos[1], move.side] = pieceId

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # to implement

        return str(self.board)
