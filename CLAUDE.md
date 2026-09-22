# aneeshcs.github.io — Claude Code Instructions

## Site overview

Hugo Blox academic site deployed to GitHub Pages via GitHub Actions (`master` branch → deploy).

- Source: `content/` (Hugo markdown), `static/` (copied as-is), `notebooks/` (marimo `.py` files)
- Build: Hugo + marimo WASM export runs in CI (`.github/workflows/deploy.yml`)
- Live: https://aneeshcs.com (custom domain; `www.aneeshcs.com` and `aneeshcs.github.io` redirect here)

## Marimo notebooks

Notebook sources live in `notebooks/`. Three are live, feeding two sections:

| notebook | exported to | page |
|---|---|---|
| `lorenz63_ensemble_explorer.py` | `static/chaos/` | `/chaos/` |
| `pendulum_chaos_explorer.py` | `static/chaos/` | `/chaos/` |
| `da_l63_tutorial.py` | `static/da_tutorial/` | `/da_tutorial/` |

Each is exported twice, `--mode run --no-show-code` and `--mode edit`; the two chaos
notebooks also get a downloadable `.ipynb` via `scripts/export_ipynb.py`.

**`static/chaos/` and `static/da_tutorial/` are git-ignored.** The deploy workflow
regenerates them from `notebooks/` on every push, so committing them would store a second,
immediately-stale copy — and because marimo's JS chunk filenames are content hashes, every
re-export rewrites all ~1,400 files. The exact commands are the "Export marimo notebooks"
step in `.github/workflows/deploy.yml`; run them locally if a preview needs the exports:

```bash
uvx marimo export html-wasm --sandbox --mode run --no-show-code \
  notebooks/pendulum_chaos_explorer.py -o static/chaos/pendulum_chaos_explorer.html
```

To edit a notebook interactively:

```bash
marimo edit notebooks/pendulum_chaos_explorer.py
```

Two things the workflow does after exporting, both load-bearing:

- `rm -f static/*/CLAUDE.md` — `marimo export` drops a stray copy of this file into every
  output directory, which would otherwise be published.
- `scripts/patch_chunk_reload.py` — with fresh chunk hashes on every deploy, a reader
  holding a stale cache gets "Failed to fetch dynamically imported module". The script
  injects a reload-once handler.

The GFD notebooks that used to export to `static/gfd/` were the prototypes of the textbook
now at <https://anigfd.github.io/> (repo `anigfd/anigfd.github.io`); `/gfd/` is a landing
page pointing there.

## Monthly: new publication check

A GitHub Actions cron job runs on the 1st of each month (`.github/workflows/check-publications.yml`).
It queries **Semantic Scholar author ID `47680095`** (Aneesh C. Subramanian) for papers not yet
in `content/publication/` or `publications.bib`, fetches their bibtex from doi.org, and opens
a PR titled **"📚 N new publication(s) found — please review"** on the `publications/monthly-update` branch.

**To review the PR:**

1. Open the PR — the body lists every new paper with title, venue, year, and DOI
2. Edit `publications.bib` in the PR branch to correct or remove any entries
3. **Merge** to add the papers to the site (triggers Hugo page generation automatically)
4. **Close without merging** to skip all papers this month

**To manually trigger the check:**

Go to Actions → "Monthly publication check" → Run workflow.

**To add a paper immediately (outside the monthly cycle):**

```bash
# 1. Append its bibtex to publications.bib
# 2. Run the import locally to generate Hugo pages
pip install "academic>=0.10.0"
academic import publications.bib content/publication/ --compact
# 3. Commit and push
git add publications.bib content/publication/ && git commit -m "publications: add <slug>"
git push
```

**Notes:**
- Semantic Scholar may not index a paper for weeks after publication — check manually if needed
- Set up Google Scholar email alerts at https://scholar.google.com/scholar_alerts as a faster notification layer
- The script ignores papers with no DOI on Semantic Scholar; add those manually

## Monthly: check for broken references

Run a broken-link check against the live site on the first of each month.

**Command:**

```bash
uvx linkchecker https://aneeshcs.com --check-extern \
  --no-warnings \
  --ignore-url "linkedin\." \
  --ignore-url "twitter\." \
  --ignore-url "x\.com" \
  --ignore-url "doi\.org" \
  --ignore-url "onlinelibrary\.wiley\.com" \
  --ignore-url "journals\.ametsoc\.org" \
  --output text
```

DOI and publisher links (doi.org, AMS, AGU/Wiley) are excluded because those
hosts block automated crawlers and always fail from scripts even when the
links work in a browser; DOI validity is covered by the monthly publication
check instead.

**What to look for:**

- Internal 404s (missing pages, moved content, renamed files)
- Broken `href` or `src` attributes in Hugo shortcodes or raw HTML blocks
- Dead DOI or publication links in `content/publication/`
- Iframe `src` paths to marimo notebooks that no longer exist

**If broken links are found:**

1. Fix the source in `content/` or `static/`
2. For moved Hugo pages, add an `aliases:` entry in the front matter
3. Commit and push — the deploy workflow handles the rest
