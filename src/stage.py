import os
import shutil
import subprocess
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # /website
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # repo root
BUILD_DIR = os.path.join(SCRIPT_DIR, "site_build")  # temp build output


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
    cwd=SCRIPT_DIR,
)

# 2. Prepare worktree for gh-pages
tmp_dir = tempfile.mkdtemp(prefix="ghpages_")
run(["git", "fetch", "origin", "gh-pages"], cwd=REPO_ROOT)
run(["git", "worktree", "add", "--force", tmp_dir, "gh-pages"], cwd=REPO_ROOT)

STAGED_DIR = os.path.join(tmp_dir, "staged")

# 3. Replace staged
safe_rmtree(STAGED_DIR)
shutil.copytree(BUILD_DIR, STAGED_DIR)

# 4. Commit & push
run(["git", "add", "staged"], cwd=tmp_dir)
try:
    run(["git", "commit", "-m", "Stage build"], cwd=tmp_dir)
except subprocess.CalledProcessError:
    print("No changes to commit.")
run(["git", "push", "origin", "gh-pages"], cwd=tmp_dir)

# 5. Cleanup: remove worktree and delete temp dir
run(["git", "worktree", "remove", "--force", tmp_dir], cwd=REPO_ROOT)
safe_rmtree(tmp_dir)

print("✅ Staged build deployed to /staged")
