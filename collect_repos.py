import os
from dotenv import load_dotenv
import pandas as pd
from github import Github, Auth
import pandas as pd
import time

# 🔑 Add your GitHub token
TOKEN = os.getenv("GITHUB_TOKEN")
load_dotenv()

auth = Auth.Token(TOKEN)
g = Github(auth=auth)

repos_data = []

# ----------------------------
# ✅ CLEAN REPOS (SAFE)
# ----------------------------
clean_query = "stars:>1000 language:python"
clean_repos = g.search_repositories(query=clean_query)

print("Collecting CLEAN repos...")

count = 0
for repo in clean_repos:
    if count >= 20:
        break

    url = repo.html_url
    repos_data.append([url, 0])
    print("Clean:", url)

    count += 1
    time.sleep(0.5)

# ----------------------------
# 🚨 MALICIOUS REPOS
# ----------------------------
malicious_queries = [
    "keylogger python",
    "reverse shell python",
    "malware python",
    "crypto miner python"
]

print("\nCollecting MALICIOUS repos...")

count = 0
for query in malicious_queries:
    results = g.search_repositories(query=query)

    for repo in results:
        if count >= 20:
            break

        url = repo.html_url
        repos_data.append([url, 1])
        print("Malicious:", url)

        count += 1
        time.sleep(0.5)

    if count >= 20:
        break

# ----------------------------
# SAVE DATA
# ----------------------------
df = pd.DataFrame(repos_data, columns=["url", "label"])
df.drop_duplicates(inplace=True)

df.to_csv("repos.csv", index=False)

print("\n✅ repos.csv created successfully!")
print("Total repos:", len(df))