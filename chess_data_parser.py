
import json
import pandas as pd

PATH = "C:/Users/DavWi/OneDrive/Desktop/storage/datasets/club_games_data.csv"
SAVE_PATH = "C:/Users/DavWi/OneDrive/Desktop/storage/datasets/chess_dataset_parsed.json"

SAVE_PATH2 = "data/meanTilesThreatening.json"

# read into pandas df
df = pd.read_csv(PATH)

file = df.to_dict("records")

# parse the other data points in pgn
for i in range(len(file)):
    file[i]["moves"] = [
        m for m in file[i]["pgn"].split("\n\n")[1].split(" ") if not (m.endswith(".") and m[:-1].isnumeric())
    ][:-1]
    file[i]["data"] = {
        line.split(" \"")[0][1:]: line.split(" \"")[1][:-2]
        for line in file[i]["pgn"].split("\n\n")[0].split("\n")
    }
    del file[i]["pgn"]

with open(SAVE_PATH, "w") as f:
    json.dump(file, f, indent=4)



