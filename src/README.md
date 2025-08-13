## Updating the ISO Markdown Document

```bash
git clone https://github.com/PCA-POSC-Caesar-Association/Public_ISO23726-1
cd Public_ISO23726-1
````

If already cloned:

```bash
git pull
```

1. Save the HTML version from the ISO website as `p1.html` in `src/docs/`.
2. If figures have changed, download the Word version from the ISO website, extract each figure, and save as `Fig1.png`, `Fig2.png`, etc. in `src/docs/figs/`.
3. Run the notebook to generate the sanitized Markdown file `index.md`.

---

## Releasing the New Version to the MkDocs Site

### Setup Environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install mkdocs mkdocs-material
```

### Release

```bash
python3 src/release.py
```

---

## Viewing Versions

* **Latest:** [https://pca-posc-caesar-association.github.io/Public\_ISO23726-1/](https://pca-posc-caesar-association.github.io/Public_ISO23726-1/)
* **Specific version:** `https://pca-posc-caesar-association.github.io/Public_ISO23726-1/?version=YYYY-MM-DD_N`