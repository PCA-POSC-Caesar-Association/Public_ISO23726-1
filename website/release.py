import os
import shutil
import subprocess
import datetime
import glob

# --- Paths ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # /website
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # repo root
GH_PAGES_WORKTREE = os.path.join(REPO_ROOT, "site")  # gh-pages worktree
BUILD_DIR = os.path.join(SCRIPT_DIR, "site_build")   # temp build output
LATEST_DIR = os.path.join(GH_PAGES_WORKTREE, "latest")
ARCHIVE_DIR = os.path.join(GH_PAGES_WORKTREE, "archive")
KEEP_AT_ROOT = {".nojekyll", "index.html", "CNAME"}  # Files to keep at root

def run(cmd):
    print(f"+ {cmd}")
    subprocess.check_call(cmd, shell=True)

# 1. Build MkDocs into temp folder
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

mkdocs_yml = os.path.join(SCRIPT_DIR, "mkdocs.yml")
run(f"mkdocs build -f {mkdocs_yml} -d {BUILD_DIR}")

# 2. Ensure archive dir exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 3. Create version string
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

# 4. Clean /latest/ and copy build
if os.path.exists(LATEST_DIR):
    shutil.rmtree(LATEST_DIR)
shutil.copytree(BUILD_DIR, LATEST_DIR)

# 5. Copy build to archive
if os.path.exists(version_path):
    shutil.rmtree(version_path)
shutil.copytree(BUILD_DIR, version_path)

# 6. Remove old root files except KEEP_AT_ROOT
for item in os.listdir(GH_PAGES_WORKTREE):
    if item not in KEEP_AT_ROOT and item not in {"latest", "archive"}:
        path = os.path.join(GH_PAGES_WORKTREE, item)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

# 7. Commit and push
run(f'cd "{GH_PAGES_WORKTREE}" && git add .')
run(f'cd "{GH_PAGES_WORKTREE}" && git commit -m "Release {version_str}" || echo "No changes to commit"')
run(f'cd "{GH_PAGES_WORKTREE}" && git push origin gh-pages')

print(f"✅ Released version {version_str}")
