
from gamehandler import GameHandler, GAMES_DIR
from autoplayer import AutoPlayer, DATA_PIECES_AT_INDEX
from datamanipulation import getAvgOf2Dicts
import pandas as pd
import json
from game.relations import PIECES_ID_TO_STR


PATH = "C:/Users/DavWi/OneDrive/Desktop/storage/datasets/chess_dataset_parsed.json"
SAVE_PATH = "data/chessdata.json"

# read into pandas df
df = pd.read_json(PATH)

with open(SAVE_PATH, "r") as f:
    chess_data = json.load(f)


START_INDEX = min(divsByDataPoints["matchIndex"] for divsByDataPoints in chess_data["divisors"].values())

if __name__ == '__main__':
    for dp in DATA_PIECES_AT_INDEX:
        if dp not in chess_data["values"]:
            chess_data["values"][dp] = 0
        if dp not in chess_data["divisors"]:
            chess_data["divisors"][dp] = 1

    for index, game in df.iloc[START_INDEX:].iterrows():
        lenMoves = len(game["moves"])
        # moves as strings
        movesWhite = [game["moves"][i] for i in range(lenMoves) if i % 2 == 0]
        movesBlack = [game["moves"][i] for i in range(lenMoves) if i % 2 == 1]

        p0 = AutoPlayer(movesWhite, 0)
        p1 = AutoPlayer(movesBlack, 1)

        gh = GameHandler(p0, p1, GAMES_DIR, False, "analysisGame", 0)

        gh.run()
        
        for i, dp in enumerate(DATA_PIECES_AT_INDEX):
            if chess_data["divisors"][dp] < index:
                for pId in PIECES_ID_TO_STR.keys():
                    avgMoves = (p0.data[i][pId] + p1.data[i][pId]) / 2
                    chess_data["values"][dp][str(pId)] += (avgMoves - chess_data["values"][dp][str(pId)]) * avgMoves / chess_data["divisors"][dp][str(pId)]
                    chess_data["divisors"][dp][str(pId)] += 2

                chess_data["divisors"][dp]["matchIndex"] += 1

        if index % 10 == 0:
            print(f"SAVING MATCH at index={index}")
            with open(SAVE_PATH, "w") as f:
                json.dump(chess_data)
        
        print(f"Match ")

    with open(SAVE_PATH, "w") as f:
                json.dump(chess_data)


