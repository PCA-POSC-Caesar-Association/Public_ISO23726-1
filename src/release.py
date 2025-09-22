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


def run(cmd, cwd=None, check=True):
    """Run a command cross-platform."""
    if isinstance(cmd, str):
        cmd = cmd.split()
    print(f"+ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check)


def safe_rmtree(path):
    """Robust folder delete: skip locked files on Windows."""
    def onerror(func, p, exc_info):
        err = exc_info[1]
        if isinstance(err, PermissionError):
            print(f"⚠️ Skipping locked file: {p}")
        else:
            raise err
    if os.path.exists(path):
        shutil.rmtree(path, onerror=onerror)


# 1. Build MkDocs
safe_rmtree(BUILD_DIR)
run(
    ["mkdocs", "build", "-f", os.path.join(SCRIPT_DIR, "mkdocs.yml"), "-d", BUILD_DIR],
    cwd=SCRIPT_DIR
)

# 2. Prepare worktree for gh-pages
tmp_dir = tempfile.mkdtemp(prefix="ghpages_")
# Ensure branch exists locally
run(["git", "fetch", "origin", "gh-pages"], cwd=REPO_ROOT)
# Add worktree (checkout gh-pages branch into tmp_dir)
run(["git", "worktree", "add", "--force", tmp_dir, "gh-pages"], cwd=REPO_ROOT)

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
safe_rmtree(LATEST_DIR)
shutil.copytree(BUILD_DIR, LATEST_DIR)

# 5. Add to archive
safe_rmtree(version_path)
shutil.copytree(BUILD_DIR, version_path)

# 6. Clean old root files except KEEP_AT_ROOT
for item in os.listdir(tmp_dir):
    if item not in KEEP_AT_ROOT and item not in {"latest", "archive", ".git"}:
        path = os.path.join(tmp_dir, item)
        safe_rmtree(path) if os.path.isdir(path) else os.remove(path)

# 7. Commit & push
run(["git", "add", "."], cwd=tmp_dir)
try:
    run(["git", "commit", "-m", f"Release {version_str}"], cwd=tmp_dir)
except subprocess.CalledProcessError:
    print("No changes to commit.")
run(["git", "push", "origin", "gh-pages"], cwd=tmp_dir)

# 8. Cleanup: remove worktree & temp dir
run(["git", "worktree", "remove", "--force", tmp_dir], cwd=REPO_ROOT)
safe_rmtree(tmp_dir)

print(f"✅ Released version {version_str}")
