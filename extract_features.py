import os
from dotenv import load_dotenv
from github import Github, Auth
import pandas as pd
from datetime import datetime, timezone
import time

load_dotenv()



# 🔑 Put your GitHub token here
TOKEN = os.getenv("GITHUB_TOKEN")

# Auth setup
auth = Auth.Token(TOKEN)
g = Github(auth=auth)

# Current time (timezone-aware)
now = datetime.now(timezone.utc)

# Load repo list
df = pd.read_csv("repos.csv")

data = []

# ----------------------------
# MAIN LOOP
# ----------------------------
for index, row in df.iterrows():
    url = row["url"]
    label = row["label"]

    try:
        print(f"\nProcessing: {url}")

        # Extract repo name
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
        # LIGHT CLEANING (SAFE)
        # ----------------------------
        if stars == 0 and forks == 0:
            print("❌ Skipped (very low quality)")
            continue

        if repo.archived:
            print("❌ Skipped (archived repo)")
            continue

        # ----------------------------
        # DERIVED FEATURES
        # ----------------------------
        issue_ratio = issues / (stars + 1)
        fork_ratio = forks / (stars + 1)
        activity = 1 / (commit_gap + 1)

        # ----------------------------
        # STORE DATA
        # ----------------------------
        data.append([
            stars, forks, issues, watchers,
            age_days, commit_gap,
            issue_ratio, fork_ratio, activity,
            label
        ])

        print("✅ Kept")

        # Avoid API rate limit
        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Error: {url} → {e}")

# ----------------------------
# CREATE DATASET
# ----------------------------
columns = [
    "stars", "forks", "issues", "watchers",
    "age_days", "commit_gap",
    "issue_ratio", "fork_ratio", "activity",
    "label"
]

dataset = pd.DataFrame(data, columns=columns)

# Save dataset
dataset.to_csv("dataset.csv", index=False)

print("\n✅ Dataset saved as dataset.csv")
print("Total rows:", len(dataset))






# from github import Github
# import pandas as pd
# from datetime import datetime
# import time
# from datetime import datetime, timezone
# now = datetime.now(timezone.utc)

# # 🔑 Put your GitHub token here (important to avoid rate limit)
# GITHUB_TOKEN = ""

# from github import Auth
# auth = Auth.Token(GITHUB_TOKEN)
# g = Github(auth=auth)

# # Load your repo list
# df = pd.read_csv("repos.csv")

# data = []

# for index, row in df.iterrows():
#     url = row["url"]
#     label = row["label"]

#     try:
#         print(f"Processing: {url}")

#         # Extract owner/repo name
#         repo_name = "/".join(url.replace(".git", "").split("/")[-2:])
#         repo = g.get_repo(repo_name)

#         # Basic features
#         stars = repo.stargazers_count
#         forks = repo.forks_count
#         issues = repo.open_issues_count
#         watchers = repo.subscribers_count

#         # Dates
#         created_at = repo.created_at
#         pushed_at = repo.pushed_at

        

#         age_days = (now - created_at).days
#         commit_gap = (now - pushed_at).days

#         # Derived features
#         issue_ratio = issues / (stars + 1)
#         fork_ratio = forks / (stars + 1)
#         activity = 1 / (commit_gap + 1)

#         # Append data
#         data.append([
#             stars, forks, issues, watchers,
#             age_days, commit_gap,
#             issue_ratio, fork_ratio, activity,
#             label
#         ])

#         # Avoid rate limits
#         time.sleep(1)

#     except Exception as e:
#         print(f"Error processing {url}: {e}")

# # Create dataset
# columns = [
#     "stars", "forks", "issues", "watchers",
#     "age_days", "commit_gap",
#     "issue_ratio", "fork_ratio", "activity",
#     "label"
# ]

# # ----------------------------
# # LIGHT CLEANING + EXTRACTION
# # ----------------------------

# # Skip extremely low-quality repos only
# if stars == 0 and forks == 0:
#     continue

# # Skip archived repos (dead)
#     if repo.archived:
#      continue

# # Derived features
# issue_ratio = issues / (stars + 1)
# fork_ratio = forks / (stars + 1)
# activity = 1 / (commit_gap + 1)

# data.append([
#     stars, forks, issues, watchers,
#     age_days, commit_gap,
#     issue_ratio, fork_ratio, activity,
#     label
# ])

# print(f"Kept: {url}")
# dataset = pd.DataFrame(data, columns=columns)

# # Save dataset
# dataset.to_csv("dataset.csv", index=False)

# print("\n✅ Dataset saved as dataset.csv")