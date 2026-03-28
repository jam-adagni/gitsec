import os
from dotenv import load_dotenv
import pandas as pd
from github import Github, Auth
import pandas as pd
from datetime import datetime, timezone
import time

# 🔑 GitHub Token
TOKEN = os.getenv("GITHUB_TOKEN")
load_dotenv()

auth = Auth.Token(TOKEN)
g = Github(auth=auth)

now = datetime.now(timezone.utc)

# Load large repo list
df = pd.read_csv("repos_final.csv")

data = []

print("Starting feature extraction...\n")

for i, row in df.iterrows():
    url = row["url"]
    label = row["label"]

    try:
        print(f"[{i+1}/{len(df)}] Processing: {url}")

        repo_name = "/".join(url.replace(".git", "").split("/")[-2:])
        repo = g.get_repo(repo_name)

        # ----------------------------
        # BASIC FEATURES
        # ----------------------------
        stars = repo.stargazers_count
        forks = repo.forks_count
        issues = repo.open_issues_count
        watchers = repo.subscribers_count

        created_at = repo.created_at
        pushed_at = repo.pushed_at

        age_days = (now - created_at).days
        commit_gap = (now - pushed_at).days

        # ----------------------------
        # LIGHT CLEANING
        # ----------------------------
        if stars == 0 and forks == 0:
            print("❌ Skipped (low quality)")
            continue

        if repo.archived:
            print("❌ Skipped (archived)")
            continue

        # ----------------------------
        # DERIVED FEATURES
        # ----------------------------
        issue_ratio = issues / (stars + 1)
        fork_ratio = forks / (stars + 1)
        activity = 1 / (commit_gap + 1)

        # ----------------------------
        # STORE
        # ----------------------------
        data.append([
            stars, forks, issues, watchers,
            age_days, commit_gap,
            issue_ratio, fork_ratio, activity,
            label
        ])

        print("✅ Kept")

        # Rate limit control
        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Error: {url} → {e}")
        continue


# ----------------------------
# SAVE DATASET
# ----------------------------
columns = [
    "stars", "forks", "issues", "watchers",
    "age_days", "commit_gap",
    "issue_ratio", "fork_ratio", "activity",
    "label"
]

dataset = pd.DataFrame(data, columns=columns)

dataset.to_csv("dataset_large.csv", index=False)

print("\n✅ dataset_large.csv created!")
print("Total rows:", len(dataset))