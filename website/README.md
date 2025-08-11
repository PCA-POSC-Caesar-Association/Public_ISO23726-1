## 🚀 Releasing the MkDocs Site

This project publishes its documentation to **GitHub Pages** using a versioned layout:

### **One-time setup (per developer)**

1. **Clone the repo**:

   ```bash
   git clone https://github.com/PCA-POSC-Caesar-Association/Public_ISO23726-1
   cd Public_ISO23726-1
   ```

2. **Add `gh-pages` as a local worktree**:
   This checks out the `gh-pages` branch into the `site/` folder at the repo root.

   ```bash
   git fetch origin
   git worktree add -B gh-pages site origin/gh-pages
   ```

---

### **Releasing a new version**

Place new version of `index.md` into `website/docs/` folder. Place additional files, e.g. figures, into `website/docs/p1_files/`.

From the repo root:

```bash
python3 website/release.py
```

---

### **Viewing versions**

* Latest: `https://pca-posc-caesar-association.github.io/Public_ISO23726-1/`
* Specific version: `https://pca-posc-caesar-association.github.io/Public_ISO23726-1/?version=YYYY-MM-DD_N`

---

### **Tips**

* You only need to set up the `gh-pages` worktree once.
* If `release.py` fails with “no such file or directory: site”, re-run:

  ```bash
  git worktree add -B gh-pages site origin/gh-pages
  ```