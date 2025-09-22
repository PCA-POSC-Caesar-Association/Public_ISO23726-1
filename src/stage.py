import os
import shutil
import subprocess
import tempfile
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # /website
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # repo root
BUILD_DIR = os.path.join(SCRIPT_DIR, "site_build")        # MkDocs build output
DEPLOY_SUBDIR = "staged"                                  # where site goes in gh-pages


def run(cmd, cwd=None, check=True):
    """Run a command cross-platform with logging."""
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


def main():
    # 1. Build MkDocs site
    safe_rmtree(BUILD_DIR)
    run([
        "mkdocs", "build",
        "-f", os.path.join(SCRIPT_DIR, "mkdocs.yml"),
        "-d", BUILD_DIR
    ], cwd=SCRIPT_DIR)

    # 2. Clone gh-pages branch into temp dir
    tmp_dir = tempfile.mkdtemp(prefix="ghpages_")
    # clone from remote instead of local
    remote_url = subprocess.check_output(
        ["git", "config", "--get", "remote.origin.url"], cwd=REPO_ROOT
    ).decode().strip()
    run(["git", "clone", "--branch", "gh-pages", "--depth", "1", remote_url, tmp_dir])


    staged_dir = os.path.join(tmp_dir, DEPLOY_SUBDIR)

    # 3. Replace staged build
    safe_rmtree(staged_dir)
    shutil.copytree(BUILD_DIR, staged_dir)

    # 4. Commit & push
    run(["git", "add", "."], cwd=tmp_dir)
    try:
        run(["git", "commit", "-m", "Deploy staged build"], cwd=tmp_dir)
    except subprocess.CalledProcessError:
        print("ℹ️ No changes to commit.")
    else:
        run(["git", "push", "origin", "gh-pages"], cwd=tmp_dir)

    # 5. Cleanup
    safe_rmtree(tmp_dir)
    print(f"✅ Site deployed to /{DEPLOY_SUBDIR}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        sys.exit(1)
