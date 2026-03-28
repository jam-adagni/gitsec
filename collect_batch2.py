import os
from dotenv import load_dotenv
import pandas as pd
from github import Github, Auth
import pandas as pd
import time

# 🔑 Token
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

auth = Auth.Token(TOKEN)
g = Github(auth=auth)

# Load existing dataset (to avoid duplicates)
existing_df = pd.read_csv("repos_large.csv")
existing_urls = set(existing_df["url"].tolist())

repos_data = []

TARGET_CLEAN = 100
TARGET_MALICIOUS = 100

# ----------------------------
# CLEAN REPOS (NEW)
# ----------------------------
clean_queries = [
    "stars:300..1000 language:python",
    "stars:100..300 language:python",
]

print("Collecting NEW CLEAN repos...")

clean_count = 0
for query in clean_queries:
    results = g.search_repositories(query=query)

    for repo in results:
        if clean_count >= TARGET_CLEAN:
            break

        url = repo.html_url

        if url in existing_urls:
            continue

        repos_data.append([url, 0])
        existing_urls.add(url)

        clean_count += 1
        print(f"[CLEAN {clean_count}] {url}")

        time.sleep(0.5)

    if clean_count >= TARGET_CLEAN:
        break


# ----------------------------
# MALICIOUS REPOS (NEW)
# ----------------------------
malicious_queries = [
    "keylogger python pushed:>2023-01-01",
    "reverse shell python pushed:>2023-01-01",
    "malware python pushed:>2023-01-01",
    "crypto miner python pushed:>2023-01-01",
    "botnet python pushed:>2023-01-01",
]

print("\nCollecting NEW MALICIOUS repos...")

mal_count = 0
for query in malicious_queries:
    results = g.search_repositories(query=query)

    for repo in results:
        if mal_count >= TARGET_MALICIOUS:
            break

        url = repo.html_url

        if url in existing_urls:
            continue

        repos_data.append([url, 1])
        existing_urls.add(url)

        mal_count += 1
        print(f"[MAL {mal_count}] {url}")

        time.sleep(0.5)

    if mal_count >= TARGET_MALICIOUS:
        break


# ----------------------------
# SAVE
# ----------------------------
df = pd.DataFrame(repos_data, columns=["url", "label"])

df.to_csv("repos_batch2.csv", index=False)

print("\n✅ repos_batch2.csv created!")
print("Total new repos:", len(df))