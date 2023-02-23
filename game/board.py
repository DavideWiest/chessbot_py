from .pieces import *
from .move import *
import numpy as np
from .boardfuncs import updateBoardInfo

from string import ascii_uppercase
from colorama import Fore, Back, Style
import json

class ChessBoard():
    """"
    Chess board where all positions are stored
    side is the respective player side (white = 1, black = 0)
    """

    def __init__(self, gamesDir):
        "initialize board"

        self.board = np.zeros((8,8,2), dtype=np.byte)
        self.boardInfo = [
            {
                "lastMovePos": (-1, -1),
                "kingMoved": False,
                "firstRookMoved": False,
                "secondRookMoved": False,
                "doPrintInfo": True
            }, {
                "lastMovePos": (-1, -1),
                "kingMoved": False,
                "firstRookMoved": False,
                "secondRookMoved": False,
                "doPrintInfo": True
            }
        ]

        self.gamesDir = gamesDir

        # 0 = black = on the bottom half
        # 1 = white = on the top half
        # will be switched upside down when viewing because x=0 is at the bottom in chess

        # pawn row
        self.board[1, :, BLACK] = PAWN

        # rooks
        self.board[0, 7, BLACK] = ROOK
        self.board[0, 0, BLACK] = ROOK

        # knights
        self.board[0, 6, BLACK] = KNIGHT
        self.board[0, 1, BLACK] = KNIGHT

        # bishops
        self.board[0, 5, BLACK] = BISHOP
        self.board[0, 2, BLACK] = BISHOP

        # queens
        self.board[0, 4, BLACK] = QUEEN

        # kings
        self.board[0, 3, BLACK] = KING


        # pawn row
        self.board[6, :, WHITE] = PAWN

        # rooks
        self.board[7, 7, WHITE] = ROOK
        self.board[7, 0, WHITE] = ROOK

        # knights
        self.board[7, 6, WHITE] = KNIGHT
        self.board[7, 1, WHITE] = KNIGHT

        # bishops
        self.board[7, 5, WHITE] = BISHOP
        self.board[7, 2, WHITE] = BISHOP

        # queens
        self.board[7, 4, WHITE] = QUEEN

        # kings
        self.board[7, 3, WHITE] = KING

        self.piecesPos = {
            0: {
                KING: [[0,3]],
                PAWN: [[1,x] for x in range(8)],
                BISHOP: [[0,2], [0,5]],
                ROOK: [[0,0], [0,7]],
                QUEEN: [[0,4]],
                KNIGHT: [[0,1], [0,6]]
            },
            1: {
                KING: [[7,3]],
                PAWN: [[6,x] for x in range(8)],
                BISHOP: [[7,2], [7,5]],
                ROOK: [[7,0], [7,7]],
                QUEEN: [[7,4]],
                KNIGHT: [[7,1], [7,6]]
            }
        }


    def getBoard(self, dim: int = 1):
        "get the board either 1 or 2 dimensional"

        assert dim in (1,2)

        # to implement

    
    def makeMove(self, piecePos: tuple, move: Move, absolute=False):
        "move piece"

        currentPiecePos = self.piecesPos[move.side][move.p]
        piecePosIndex = currentPiecePos.index(list(piecePos))
        previousPosition = currentPiecePos[piecePosIndex]

        self.board[
            currentPiecePos[piecePosIndex][0], currentPiecePos[piecePosIndex][1], move.side
        ] = 0

        if not absolute:
            currentPiecePos[piecePosIndex][0] += move.y
            currentPiecePos[piecePosIndex][1] += move.x

            self.piecesPos[move.side][move.p][piecePosIndex][0] += move.y
            self.piecesPos[move.side][move.p][piecePosIndex][1] += move.x
        else:
            currentPiecePos[piecePosIndex][0] = move.y
            currentPiecePos[piecePosIndex][1] = move.x

            self.piecesPos[move.side][move.p][piecePosIndex][0] = move.y
            self.piecesPos[move.side][move.p][piecePosIndex][1] = move.x

        toRemove = None
        for enemyPId, enemyPiecesPos in self.piecesPos[OTHERSIDE(move.side)].items():
            for enemyPiecePos in enemyPiecesPos:
                if enemyPiecePos == currentPiecePos[piecePosIndex]:
                    toRemove = (enemyPId, enemyPiecesPos.index(enemyPiecePos))
                    break

        if toRemove != None:
            del self.piecesPos[OTHERSIDE(move.side)][toRemove[0]][toRemove[1]]
            self.board[
                currentPiecePos[piecePosIndex][0],
                currentPiecePos[piecePosIndex][1],
                OTHERSIDE(move.side)
            ] = 0

        self.board[
                currentPiecePos[piecePosIndex][0],
                currentPiecePos[piecePosIndex][1],
                move.side
            ] = move.p

        # castling

        if move.original.lower() == "o-o":
            self.handleCastling(move, 0, 2)
            
        elif move.original.lower() == "o-o-o":
            self.handleCastling(move, 7, 5)

        # promoting
        elif "=" in move.original:
            self.handlePromotion(move, piecePosIndex)

        self.boardInfo[move.side] = updateBoardInfo(self.board, self.boardInfo[move.side], self.piecesPos, move.side, move.p, piecePosIndex, previousPosition)

        return True

    def handleCastling(self, move: Move, rookPosBefore: int, rookPosAfter: int):
        primaryPieceRow = 0 if move.side == 0 else 7
        rookIndex = self.piecesPos[move.side][ROOK].index([
            rookPosBefore, primaryPieceRow
        ])

        rookPos = self.piecesPos[move.side][ROOK][rookIndex]
        self.piecesPos[move.side][ROOK][rookIndex] = [primaryPieceRow, rookPosAfter]
        self.board[rookPos[0], rookPos[1], move.side] = 0
        self.board[primaryPieceRow, rookPosAfter, move.side] = ROOK

    def handlePromotion(self, move: Move, piecePosIndex):
        pieceId = PIECES_STR_TO_ID[move.original.split("=")[1].lower()]
        piecePos = self.piecesPos[move.side][PAWN][piecePosIndex]
        del self.piecesPos[move.side][PAWN][piecePosIndex]
        self.piecesPos[move.side][pieceId].append(piecePos)
        self.board[piecePos[0], piecePos[1], move.side] = pieceId

    def __repr__(self):
        return self.toString()

    def __str__(self):
        return self.toString()

    def toString(self, preferredSide=0):
        rows = []

        for rowindex in range(8):
            rows.append(f"{8-rowindex}   " + "   ".join(
            # rows.append(f"{rowindex}   " + "   ".join(
                str(
                    self.preparePiece(self.board[rowindex, colindex, 0], 0)
                    if self.board[rowindex, colindex, 0] != 0 
                    else self.preparePiece(self.board[rowindex, colindex, 1], 1)
                ) if preferredSide == 0 else str(
                    self.preparePiece(self.board[rowindex, colindex, 1], 1)
                    if self.board[rowindex, colindex, 1] != 0 
                    else self.preparePiece(self.board[rowindex, colindex, 0], 0)
                )
                for colindex in range(8)
                ))
        rows.append(
            "    " + "   ".join([f"{ascii_uppercase[i]}" for i in range(8)])
        )
        # rows.append(
        #     "    " + "   ".join([f"{i}" for i in range(8)])
        # )

        return "\n\n".join(rows)

    def preparePiece(self, pieceId: int, side: int, testPieceId=None):
        if pieceId == 0:
            return Style.DIM + Fore.LIGHTWHITE_EX +  "_"  + Fore.RESET + Style.RESET_ALL
        if pieceId == testPieceId:
            return TEST_COLOR + "T" + Fore.RESET
        return COLOR_SIDE(side) + PIECES_ID_TO_STR[pieceId].upper() + Fore.RESET

    def visualizeLegalMoves(self, pieceId: int, pieceIndex: int, side: int, level: int=2, legalMoves: list = None):
        
        newBoard = self.board.copy()

        pos = self.piecesPos[side][pieceId][pieceIndex]

        if legalMoves == None:
            legalMoves = PIECES_ID_TO_CLASS[pieceId].getLegalMoves(newBoard, pos, side, self.piecesPos, pieceId, pieceIndex, self.boardInfo, level)

        for y, x in legalMoves:
            newBoard[y,x,OTHERSIDE(side)] = 12
 
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

    def saveGame(self, filename, moveIndex: int):
        np.save(self.gamesDir + "/" + filename, self.board, allow_pickle=True)
        
        fileToSave = {"moveIndex": moveIndex, "pp": self.piecesPos, "bi": self.boardInfo}
        with open(self.gamesDir + "/" + filename + ".json", "w") as f:
            json.dump(fileToSave, f)

    def loadGame(self, filename):
        self.board = np.load(self.gamesDir + "/" + filename + ".npy", allow_pickle=True)
            
        with open(self.gamesDir + "/" + filename + ".json", "r") as f:
            fileToLoad = json.load(f)
            self.piecePos = fileToLoad["pp"]
            self.boardInfo = fileToLoad["bi"]
        
        return fileToLoad["moveIndex"]
