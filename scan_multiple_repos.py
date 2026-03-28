import os
import subprocess
import shutil
import yara

# Load YARA rules
rules = yara.compile(filepath="rules.yar")

# ----------------------------
# URL LIST (ADD YOUR REPOS)
# ----------------------------
repo_urls = [
    "https://github.com/aydinnyunus/Keylogger.git",
    "https://github.com/6ix7ine/Keylogger.git",
    "https://github.com/donnemartin/system-design-primer.git"
]

CLONE_DIR = "temp_repos"


# ----------------------------
# CLONE FUNCTION
# ----------------------------
def clone_repo(url):
    repo_name = url.split("/")[-1].replace(".git", "")
    path = os.path.join(CLONE_DIR, repo_name)

    try:
        subprocess.run(
            ["git", "clone", "--depth=1", url, path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return path
    except:
        return None


# ----------------------------
# YARA SCAN FUNCTION
# ----------------------------
def scan_repo(repo_path):
    suspicious = False

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                matches = rules.match(file_path)
                if matches:
                    print(f"🚨 {repo_path} → {file}")
                    for m in matches:
                        print(f"   Rule: {m.rule}")
                    suspicious = True
            except:
                continue

    return suspicious


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    for url in repo_urls:
        print(f"\n🔍 Processing: {url}")

        repo_path = clone_repo(url)

        if not repo_path:
            print("❌ Clone failed")
            continue

        result = scan_repo(repo_path)

        if result:
            print("⚠️ MALICIOUS")
        else:
            print("✅ CLEAN")

        # Cleanup (delete repo after scan)
        shutil.rmtree(repo_path, ignore_errors=True)


if __name__ == "__main__":
    main()