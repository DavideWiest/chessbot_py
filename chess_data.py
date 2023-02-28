import pandas as pd

PATH = "C:/Users/DavWi/OneDrive/Desktop/storage/datasets/club_games_data.csv"
SAVE_PATH = "data/meanTilesThreatening.json"
# read into pandas df

df = pd.read_csv(PATH)
print(df.head(1))

# get legal moves of each piece of each side

# find out mean meanTilesThreatening of piece

# possibly make convertion of pId to realValue