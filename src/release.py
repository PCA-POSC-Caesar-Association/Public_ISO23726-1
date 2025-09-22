import os
import shutil
import subprocess
import tempfile
import datetime
import glob
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # /website
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # repo root
BUILD_DIR = os.path.join(SCRIPT_DIR, "site_build")        # MkDocs build output
KEEP_AT_ROOT = {".nojekyll", "index.html", "CNAME"}       # Files to keep at repo root


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
    remote_url = subprocess.check_output(
        ["git", "config", "--get", "remote.origin.url"], cwd=REPO_ROOT
    ).decode().strip()
    run(["git", "clone", "--branch", "gh-pages", "--depth", "1", remote_url, tmp_dir])

    latest_dir = os.path.join(tmp_dir, "latest")
    archive_dir = os.path.join(tmp_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    # 3. Create version string (YYYY-MM-DD_buildNum)
    today = datetime.date.today().strftime("%Y-%m-%d")
    existing_versions = [
        os.path.basename(p)
        for p in glob.glob(os.path.join(archive_dir, f"{today}_*"))
    ]
    build_num = 1
    if existing_versions:
        try:
            build_num = max(int(v.split("_", 1)[1]) for v in existing_versions) + 1
        except Exception:
            pass
    version_str = f"{today}_{build_num}"
    version_path = os.path.join(archive_dir, version_str)

    # 4. Replace latest
    safe_rmtree(latest_dir)
    shutil.copytree(BUILD_DIR, latest_dir)

    # 5. Check if latest has changes
    has_changes = subprocess.run(
        ["git", "diff", "--quiet", "--", "latest"],
        cwd=tmp_dir
    ).returncode != 0

    if not has_changes:
        print("ℹ️ No changes in latest/, skipping archive and commit.")
        safe_rmtree(tmp_dir)
        print("✅ No release created (site unchanged).")
        return

    # 6. Add to archive (only if changes detected)
    safe_rmtree(version_path)
    shutil.copytree(BUILD_DIR, version_path)

    # 7. Clean root (except KEEP_AT_ROOT, .git, latest, archive)
    for item in os.listdir(tmp_dir):
        if item in {".git", "latest", "archive"} or item in KEEP_AT_ROOT:
            continue
        path = os.path.join(tmp_dir, item)
        safe_rmtree(path) if os.path.isdir(path) else os.remove(path)

    # 7b. Extra safety: clean junk, but spare latest/archive
    run(["git", "clean", "-fdx", "-e", "latest", "-e", "archive"], cwd=tmp_dir)

    # 8. Commit & push
    run(["git", "add", "."], cwd=tmp_dir)
    run(["git", "commit", "-m", f"Release {version_str}"], cwd=tmp_dir)
    run(["git", "push", "origin", "gh-pages"], cwd=tmp_dir)

    # 8. Cleanup
    safe_rmtree(tmp_dir)
    print(f"✅ Released version {version_str}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        sys.exit(1)
