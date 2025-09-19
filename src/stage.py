import os
import shutil
import subprocess
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # /website
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # repo root
BUILD_DIR = os.path.join(SCRIPT_DIR, "site_build")  # temp build output


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
    cwd=SCRIPT_DIR,
)

# 2. Prepare temp folder for gh-pages
tmp_dir = tempfile.mkdtemp(prefix="ghpages_")

# Get repo URL
repo_url = subprocess.check_output(
    ["git", "config", "--get", "remote.origin.url"], cwd=REPO_ROOT
).decode().strip()

# Clone gh-pages branch
run(["git", "clone", "--branch", "gh-pages", "--single-branch", repo_url, tmp_dir])

STAGED_DIR = os.path.join(tmp_dir, "staged")

# 3. Replace staged
if os.path.exists(STAGED_DIR):
    shutil.rmtree(STAGED_DIR)
shutil.copytree(BUILD_DIR, STAGED_DIR)

# 4. Commit & push
run(["git", "add", "staged"], cwd=tmp_dir)
try:
    run(["git", "commit", "-m", "Stage build"], cwd=tmp_dir)
except subprocess.CalledProcessError:
    print("No changes to commit.")
run(["git", "push", "origin", "gh-pages"], cwd=tmp_dir)

# 5. Cleanup
shutil.rmtree(tmp_dir)

print("✅ Staged build deployed to /staged")
