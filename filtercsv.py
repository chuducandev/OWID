import pandas as pd

data = pd.read_csv("./co-emissions-per-capita.csv")

entity_list = ["Afghanistan", "Asia", "Azerbaijan"]

filtered_data = data[data["Entity"].isin(entity_list)]

filtered_data.to_csv("./new_co-emissions-per-capita.csv", index=False)