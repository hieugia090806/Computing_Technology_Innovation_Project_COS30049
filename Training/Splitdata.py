import pandas as pd
#-- Read big file --#
chunksize = 10000  # số dòng mỗi file nhỏ
for i, chunk in enumerate(pd.read_csv("../Data/Dataset15.csv", chunksize=chunksize)):
    chunk.to_csv(f"Dataset15_part{i}.csv", index=False)
