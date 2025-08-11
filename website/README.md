## 🚀 Releasing the MkDocs Site

This project publishes its documentation to **GitHub Pages** using a versioned layout. To release new version:

1. **Clone the repo**:

   ```bash
   git clone https://github.com/PCA-POSC-Caesar-Association/Public_ISO23726-1
   cd Public_ISO23726-1
   ```

2. Place new version of `index.md` into `website/docs/` folder. Place additional files, e.g. figures, into `website/docs/p1_files/`.

3. **Release**:

```bash
python3 website/release.py
```

---

### **Viewing versions**

* Latest: `https://pca-posc-caesar-association.github.io/Public_ISO23726-1/`
* Specific version: `https://pca-posc-caesar-association.github.io/Public_ISO23726-1/?version=YYYY-MM-DD_N`