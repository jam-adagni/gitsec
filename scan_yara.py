import os
import yara
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_FILE = os.path.join(BASE_DIR, "rules.yar")
# ----------------------------
# LOAD RULES
# ----------------------------
RULES_FILE = "rules.yar"

def load_rules():
    try:
        return yara.compile(filepath=RULES_FILE)
    except Exception as e:
        print("❌ Error loading YARA rules:", e)
        return None


# ----------------------------
# SCAN FILES
# ----------------------------
def scan_folder(folder_path):
    rules = load_rules()
    if not rules:
        return

    print(f"\n🔍 Scanning: {folder_path}")

    suspicious_found = False

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)

            try:
                matches = rules.match(filepath)

                if matches:
                    suspicious_found = True
                    print(f"\n🚨 Suspicious file: {filepath}")

                    for match in matches:
                        print(f"   → Rule matched: {match}")

            except Exception:
                continue

    if not suspicious_found:
        print("✅ CLEAN (no YARA matches found)")
    else:
        print("\n🚨 MALICIOUS PATTERNS DETECTED")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ No folder path provided")
        sys.exit(1)

    folder = sys.argv[1]

    if not os.path.exists(folder):
        print("❌ Invalid path")
    else:
        scan_folder(folder)