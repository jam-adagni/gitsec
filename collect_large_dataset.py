import os
from dotenv import load_dotenv
import pandas as pd
from github import Github, Auth
import pandas as pd
import time
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

auth = Auth.Token(TOKEN)
g = Github(auth=auth)

repos_data = set()

TARGET_CLEAN = 100
TARGET_MALICIOUS = 100

# ----------------------------
# CLEAN REPOS
# ----------------------------
clean_queries = [
    "stars:>10000 language:python",
    "stars:5000..10000 language:python",
    "stars:1000..5000 language:python",
    "stars:500..1000 language:python",
]

print("Collecting CLEAN repos...")

for query in clean_queries:
    results = g.search_repositories(query=query)

    for repo in results:
        clean_count = len([r for r in repos_data if r[1] == 0])
        if clean_count >= TARGET_CLEAN:
            break

        repos_data.add((repo.html_url, 0))
        print(f"[CLEAN {clean_count}] {repo.html_url}")

        time.sleep(1)

    if clean_count >= TARGET_CLEAN:
        break


# ----------------------------
# MALICIOUS REPOS
# ----------------------------
malicious_queries = [
    "keylogger python",
    "reverse shell python",
    "malware python",
    "crypto miner python",
    "botnet python",
    "ransomware python",
]

print("\nCollecting MALICIOUS repos...")

for query in malicious_queries:
    results = g.search_repositories(query=query)

    for repo in results:
        mal_count = len([r for r in repos_data if r[1] == 1])
        if mal_count >= TARGET_MALICIOUS:
            break

        repos_data.add((repo.html_url, 1))
        print(f"[MAL {mal_count}] {repo.html_url}")

        time.sleep(1)

    if mal_count >= TARGET_MALICIOUS:
        break


# ----------------------------
# SAVE
# ----------------------------
df = pd.DataFrame(list(repos_data), columns=["url", "label"])
df.to_csv("repos_large.csv", index=False)

print("\n✅ Dataset created!")
print("Total:", len(df))