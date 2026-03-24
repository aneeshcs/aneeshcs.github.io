# aneeshcs.github.io — Claude Code Instructions

## Site overview

Hugo Blox academic site deployed to GitHub Pages via GitHub Actions (`master` branch → deploy).

- Source: `content/` (Hugo markdown), `static/` (copied as-is), `notebooks/` (marimo `.py` files)
- Build: Hugo + marimo WASM export runs in CI (`.github/workflows/deploy.yml`)
- Live: https://aneeshcs.github.io

## Marimo notebooks

Notebook sources live in `notebooks/`. The deploy workflow exports them to `static/gfd/` using:

```bash
uvx marimo export html-wasm --sandbox --mode edit notebooks/<name>.py -o static/gfd/<name>.html
```

To preview a notebook locally:

```bash
cd /Users/ansu6268/github/GeophysicalFluidDynamics
marimo edit twodnavierstokes.py
```

## Monthly: check for broken references

Run a broken-link check against the live site on the first of each month.

**Command:**

```bash
uvx linkchecker https://aneeshcs.github.io --check-extern \
  --ignore-url "linkedin\." \
  --ignore-url "twitter\." \
  --ignore-url "x\.com" \
  --output failures
```

**What to look for:**

- Internal 404s (missing pages, moved content, renamed files)
- Broken `href` or `src` attributes in Hugo shortcodes or raw HTML blocks
- Dead DOI or publication links in `content/publication/`
- Iframe `src` paths to marimo notebooks that no longer exist

**If broken links are found:**

1. Fix the source in `content/` or `static/`
2. For moved Hugo pages, add an `aliases:` entry in the front matter
3. Commit and push — the deploy workflow handles the rest
