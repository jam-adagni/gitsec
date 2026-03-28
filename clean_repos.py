from dotenv import load_dotenv
import pandas as pd
from dotenv import load_dotenv
import time
import os
# 🔑 Token
TOKEN = os.getenv("GITHUB_TOKEN")
load_dotenv()

auth = Auth.Token(TOKEN)
g = Github(auth=auth)

# Load dataset
df = pd.read_csv("repos.csv")

cleaned_data = []

for index, row in df.iterrows():
    url = row["url"]
    label = row["label"]

    try:
        repo_name = "/".join(url.replace(".git", "").split("/")[-2:])
        repo = g.get_repo(repo_name)

        stars = repo.stargazers_count
        forks = repo.forks_count
        description = (repo.description or "").lower()

        # ----------------------------
        # ❌ FILTER RULES
        # ----------------------------

      
        # Remove defensive/security tools (for malicious class)
        if label == 1:
            if any(word in description for word in ["detect", "defense", "protection"]):
                continue

        # ----------------------------
        # ✅ KEEP VALID REPOS
        # ----------------------------
        cleaned_data.append([url, label])
        print(f"Kept: {url}")

        time.sleep(0.5)

    except Exception as e:
        print(f"Skipped: {url} → {e}")

# Save cleaned dataset
cleaned_df = pd.DataFrame(cleaned_data, columns=["url", "label"])
cleaned_df.drop_duplicates(inplace=True)

cleaned_df.to_csv("repos_cleaned.csv", index=False)

print("\n✅ Cleaned dataset saved as repos_cleaned.csv")
print("Total valid repos:", len(cleaned_df))