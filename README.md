# Arslan Majal — Academic Website

A lightweight, responsive academic portfolio built with plain HTML, CSS, and JavaScript for free hosting on GitHub Pages.

## Pages

- Home
- Research
- Publications
- Projects
- Teaching
- Public academic CV

## Preview locally

From this folder, run:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Publish with GitHub Pages

1. Create a public repository named `majal-1036.github.io` under the GitHub account `Majal-1036`.
2. Upload all files from this folder to the repository root.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Select the `main` branch and `/(root)`, then save.

The site will be available at `https://majal-1036.github.io/` after deployment completes.

## Updating content

Each research and project illustration is stored as an individual SVG in `assets/images/`. Replace a file while keeping its filename to update the visual without changing the page markup.
