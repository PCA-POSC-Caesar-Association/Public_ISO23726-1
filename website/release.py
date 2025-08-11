import os
import shutil
import subprocess
import datetime
import glob
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # /website
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # repo root
BUILD_DIR = os.path.join(SCRIPT_DIR, "site_build")   # temp build output
KEEP_AT_ROOT = {".nojekyll", "index.html", "CNAME"}  # Files to keep at root


def run(cmd, cwd=None):
    """Run a command cross-platform."""
    if isinstance(cmd, str):
        cmd = cmd.split()  # basic split for safety
    print(f"+ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)


# 1. Build MkDocs
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
run(
    ["mkdocs", "build", "-f", os.path.join(SCRIPT_DIR, "mkdocs.yml"), "-d", BUILD_DIR],
    cwd=SCRIPT_DIR
)

# 2. Prepare temp folder for gh-pages
tmp_dir = tempfile.mkdtemp(prefix="ghpages_")

# Get repo URL
repo_url = subprocess.check_output(
    ["git", "config", "--get", "remote.origin.url"], cwd=REPO_ROOT
).decode().strip()

# Clone gh-pages branch
run(["git", "clone", "--branch", "gh-pages", "--single-branch", repo_url, tmp_dir])

LATEST_DIR = os.path.join(tmp_dir, "latest")
ARCHIVE_DIR = os.path.join(tmp_dir, "archive")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 3. Version string
today = datetime.date.today().strftime("%Y-%m-%d")
existing_versions = [
    os.path.basename(p) for p in glob.glob(os.path.join(ARCHIVE_DIR, f"{today}_*"))
]
build_num = 1
if existing_versions:
    try:
        build_num = max(int(v.split("_", 1)[1]) for v in existing_versions) + 1
    except Exception:
        pass
version_str = f"{today}_{build_num}"
version_path = os.path.join(ARCHIVE_DIR, version_str)

# 4. Replace latest
if os.path.exists(LATEST_DIR):
    shutil.rmtree(LATEST_DIR)
shutil.copytree(BUILD_DIR, LATEST_DIR)

# 5. Add to archive
if os.path.exists(version_path):
    shutil.rmtree(version_path)
shutil.copytree(BUILD_DIR, version_path)

# 6. Clean old root files except KEEP_AT_ROOT
for item in os.listdir(tmp_dir):
    if item not in KEEP_AT_ROOT and item not in {"latest", "archive", ".git"}:
        path = os.path.join(tmp_dir, item)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

# 7. Commit & push
run(["git", "add", "."], cwd=tmp_dir)
try:
    run(["git", "commit", "-m", f"Release {version_str}"], cwd=tmp_dir)
except subprocess.CalledProcessError:
    print("No changes to commit.")
run(["git", "push", "origin", "gh-pages"], cwd=tmp_dir)

# 8. Cleanup
shutil.rmtree(tmp_dir)

print(f"✅ Released version {version_str}")
