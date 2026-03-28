import os
import sys
import subprocess
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def load_model():
    with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
        return pickle.load(f)


def ml_check():
    print("\n[🔍 Stage 1] ML Analysis...")

    sample = pd.DataFrame([[100, 50, 10, 5, 100, 10, 0.1, 0.2, 0.5]],
                          columns=[
                              "stars", "forks", "issues", "watchers",
                              "age_days", "commit_gap",
                              "issue_ratio", "fork_ratio", "activity"
                          ])

    model = load_model()
    pred = model.predict(sample)[0]

    if pred == 1:
        print("🚨 ML: Suspicious repo")
    else:
        print("✅ ML: Looks safe")


def yara_scan():
    print("\n[🔍 Stage 2] YARA Scan...")
    
    yara_path = os.path.join(BASE_DIR, "scan_yara.py")
    
    subprocess.run(["python", yara_path])


def sandbox(repo_url):
    print("\n[🔍 Stage 3] Sandbox...")

    sandbox_path = os.path.join(BASE_DIR, "sandbox_docker.py")

    subprocess.run(
        ["python", sandbox_path],
        input=repo_url,
        text=True
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python gitsec.py <repo_url>")
        return

    repo_url = sys.argv[1]

    print("\n🚀 GitSec Security Tool")

    ml_check()
    yara_scan()
    sandbox(repo_url)

    print("\n✅ Analysis Complete")


if __name__ == "__main__":
    main()