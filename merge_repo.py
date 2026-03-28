import pandas as pd

df1 = pd.read_csv("repos_large.csv")
df2 = pd.read_csv("repos_batch2.csv")

combined = pd.concat([df1, df2]).drop_duplicates()

combined.to_csv("repos_final.csv", index=False)

print("✅ Combined dataset saved as repos_final.csv")
print("Total repos:", len(combined))



# import pandas as pd

# df1 = pd.read_csv("repos_large.csv")
# df2 = pd.read_csv("dataset.csv")

# df = pd.concat([df1, df2]).drop_duplicates()

# df.to_csv("repos_final1.csv", index=False)