import pandas as pd
import os

data_folder = "data"

files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

dfs = []

for file in files:
    path = os.path.join(data_folder, file)
    df = pd.read_csv(path)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

combined_df = combined_df[combined_df["product"] == "pink morsel"]

combined_df["price"] = combined_df["price"].replace("[$,]", "", regex=True).astype(float)
combined_df["sales"] = combined_df["quantity"] * combined_df["price"]

final_df = combined_df[["sales", "date", "region"]]

final_df.to_csv("formatted_output.csv", index=False)

print("Done! formatted_output.csv created.")