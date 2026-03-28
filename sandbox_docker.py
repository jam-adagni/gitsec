import os
import subprocess
import shutil
import stat

TEMP_DIR = "sandbox_temp"


# ----------------------------
# FORCE DELETE (Windows fix)
# ----------------------------
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


# ----------------------------
# CLONE REPO
# ----------------------------
def clone_repo(url):
    if os.path.exists(TEMP_DIR):
        print("🧹 Cleaning old sandbox...")
        shutil.rmtree(TEMP_DIR, onerror=remove_readonly)

    print("⬇️ Cloning repo...")
    subprocess.run(["git", "clone", "--depth=1", url, TEMP_DIR])


# ----------------------------
# FIND PY FILES
# ----------------------------
def find_python_files():
    py_files = []

    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))

    return py_files


# ----------------------------
# RUN IN DOCKER
# ----------------------------
def run_in_docker(py_files):
    print("\n🐳 Running inside Docker sandbox...")

    if not py_files:
        print("❌ No Python files found")
        return

    host_path = os.path.abspath(TEMP_DIR).replace("\\", "/")

    for file in py_files[:2]:
        rel_path = os.path.relpath(file, TEMP_DIR).replace("\\", "/")

        print(f"\n▶ Running: {rel_path}")

        cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "-v", f"{host_path}:/app",
            "python:3.11-slim",
            "python", f"/app/{rel_path}"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout + result.stderr
            print("📤 Output:\n", output)

            # ----------------------------
            # BEHAVIOR DETECTION
            # ----------------------------
            if any(word in output.lower() for word in ["key", "log", "password"]):
                print("🚨 Possible keylogging behavior")

            if "socket" in output.lower() or "connect" in output.lower():
                print("🚨 Network behavior detected")

            if "error" in output.lower():
                print("⚠️ Suspicious execution")

        except subprocess.TimeoutExpired:
            print("⏱ Timeout → suspicious")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    url = input("Enter GitHub repo URL: ").strip()

    if not url:
        print("❌ No URL provided")
    else:
        clone_repo(url)
        py_files = find_python_files()
        print(f"\n🔍 Found {len(py_files)} Python files")
        run_in_docker(py_files)