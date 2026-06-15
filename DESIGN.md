# DESIGN.md — Climate Processes & Predictability Website

Design reference for **https://aneeshcs.com**. Audience: site owner returning after a long break, or a student/RA making updates. Covers layout boundaries, component rules, academic tone, and maintenance conventions.

---

## 1. Site Identity

| Property | Value |
|---|---|
| Full name | Climate Processes & Predictability @ CUB |
| Tagline | Climate Processes and Predictability @ CU Boulder |
| Description | Our group aims to advance the fundamental understanding of climate processes in the earth system in order to improve weather and climate predictions. |
| Canonical URL | `https://aneeshcs.com` |
| Redirect | `www.aneeshcs.com` and `aneeshcs.github.io` → `aneeshcs.com` |
| Build stack | Hugo + Hugo Blox Kit, deployed via GitHub Actions on push to `master` |

---

## 2. Color & Typography

### Theme
- **Mode**: `system` — respects the visitor's OS light/dark preference; manual toggle available in the header.
- **Font**: Inter (sans-serif), loaded by Hugo Blox. Body weight 400, bold 500, heading weight 600.
- **Border radius**: `md` (0.5rem). **Spacing**: `comfortable`.
- **Primary color**: unset in `params.yaml` (uses Hugo Blox default blue). To change, set `hugoblox.theme.colors.primary` in `config/_default/params.yaml`.

### Key colors (people page & custom components)
| Role | Light mode | Dark mode |
|---|---|---|
| Avatar border | `#63b3ed` | `#63b3ed` |
| Name link | `#2b6cb0` | `#63b3ed` |
| Role / muted text | `#4a5568` | `#9ca3af` |
| Bio text | `#718096` | `#9ca3af` |
| Group headers | `#2d3748` | `#e2e8f0` |
| People section bg | `#ffffff` | `#111827` |
| Hero overlay | `rgba(0,0,0,0.6)` with `backdrop-filter: blur(8px)` | — |

All custom CSS lives in `layouts/_partials/hooks/head-end/custom-css.html`. Do not duplicate rules in `assets/scss/custom.scss` (hero-only styles live there).

---

## 3. Layout Boundaries

### Page width
- **Content max-width**: `max-w-7xl` = 1280px, horizontally centered with `mx-auto`.
- **Horizontal padding**: `px-4` (mobile) → `sm:px-6` → `lg:px-8`.
- **Section vertical padding**: 6rem top/bottom (set by Hugo Blox `.hbb-section`).
- **Hero exception**: full viewport (`100vw × 100vh`), zero padding.

### Breakpoints (Tailwind defaults)
| Name | Min-width | Typical use |
|---|---|---|
| sm | 640px | 2-col grids start |
| md | 768px | tablet |
| lg | 1024px | desktop nav, wider padding |
| xl | 1280px | max content width |

---

## 4. Page Inventory

| URL | Type | Notes |
|---|---|---|
| `/` | Landing | Full-viewport looping video hero with text overlay |
| `/tour` | Markdown | Lab overview / introduction to the group |
| `/people` | Landing (team-showcase block) | See §5 |
| `/post` | List | News and updates |
| `/projects` | List | Research projects |
| `/gfd` | Custom list | Marimo WASM notebook viewer |
| `/da_tutorial` | Custom list | Data assimilation tutorial notebooks |
| `/publication` | List | Filterable publications |
| `/contact` | Contact block | |
| `/authors/{slug}/` | Author profile | Auto-generated from `data/authors/` + `content/authors/` |

---

## 5. People Page Component

**Reference design**: [zanna-researchteam.github.io/people](https://zanna-researchteam.github.io/people/)  
**Template override**: `layouts/_partials/hbx/blocks/team-showcase/block.html`

### Layout
- **Container**: `flexbox`, `flex-wrap: wrap`, `justify-content: center`, `gap: 2rem`.
- **Card width**: fixed `190px` — required for flex centering to work on partial rows.
- **Do not switch to CSS grid with `auto-fill`** — empty phantom columns prevent centering.

### Per-person card (top to bottom)
1. Circular avatar, `160×160px`, `3px solid #63b3ed` border, links to `/authors/{slug}/`
2. Name (`h3`), linked to profile, bold, `#2b6cb0`
3. Pronouns (optional `span`, muted, appended to name line)
4. Role (`h4`), muted gray, weight 400
5. Social icon row (`ul`, centered flex)
6. Bio (`p`, 3-line clamp via `-webkit-line-clamp`)

### Group ordering
Defined in `content/people/index.md`. Current order:
1. Principal Investigator
2. PhD Students
3. Postdoctoral Researchers
4. Research Scientists
5. Undergraduate Researchers
6. Visitors
7. PhD Alumni
8. Postdoctoral Alumni
9. Research Scientists Alumni
10. Masters Alumni
11. Undergraduate Alumni

To add or reorder groups, edit the `user_groups` list in that file and update `user_groups` in the relevant author YAML files.

---

## 6. Author Profiles

### Files
- **Data**: `data/authors/{slug}.yaml` — all structured metadata.
- **Content**: `content/authors/{slug}/_index.md` — extended bio in Markdown (shown on the individual author page, not the people page).

### Required YAML fields
```yaml
schema: "hugoblox/author/v1"
slug: "firstname-lastname"          # must match the directory name
name:
  display: "Full Name"
  given: "First"
  family: "Last"
role: "PhD Student"                 # see role naming below
user_groups:
  - "PhD Students"                  # must match a group in content/people/index.md
```

### Optional YAML fields
```yaml
name:
  pronouns: "she/her"
bio: "Two to four sentences. Third person. Lead with research focus."
affiliations:
  - name: "Department of Atmospheric and Oceanic Sciences, CU Boulder"
    url: "https://www.colorado.edu/atoc/"
links:                              # ordered as below
  - icon: "at-symbol"
    url: "mailto:email@colorado.edu"
    label: "E-mail"
  - icon: "brands/x"
    url: "https://twitter.com/handle"
  - icon: "brands/github"
    url: "https://github.com/handle"
  - icon: "brands/linkedin"
    url: "https://linkedin.com/in/handle"
  - icon: "hero/document-text"
    url: "https://link-to-cv.pdf"
    label: "Curriculum Vitae"
  - icon: "hero/globe-alt"
    url: "https://personalwebsite.com"
    label: "Website"
```

### Social link ordering convention
Email → Twitter/X → GitHub → LinkedIn → CV → Personal website. Keep it consistent across all profiles.

### Role naming (capitalize exactly as shown)
| Group | Role string |
|---|---|
| Principal Investigator | `Associate Professor` / `Assistant Professor` |
| PhD Students | `PhD Student` |
| Postdoctoral Researchers | `Postdoctoral Researcher` |
| Research Scientists | `Research Scientist` |
| Undergraduate Researchers | `Undergraduate Researcher` |
| Visitors | `Visiting Researcher` or `Visiting Scholar` |
| Alumni | original role + current position in bio |

### Author photos
- **Size**: minimum 400×400px source; square crop with face centered.
- **Format**: WebP preferred (Hugo auto-converts JPEG/PNG → WebP at build time).
- **Storage**: `assets/media/authors/` — do NOT put photos in `static/`.
- **File size**: keep source under 500KB; Hugo resizes and optimizes at build.
- **Style**: consistent headshots — plain or natural background, not logos or group shots.

---

## 7. Academic Tone & Voice

- **Register**: formal but accessible. Avoid unexplained jargon; spell out acronyms on first use.
- **Bios**: third person, 2–4 sentences. Lead with the research focus, not credentials. End with current position or advisor if student.
  - ✓ *"Investigates subseasonal predictability of atmospheric rivers using coupled ocean-atmosphere models."*
  - ✗ *"I am a PhD student working on climate stuff."*
- **Page text**: active voice where possible. "The group develops…" not "Methods are developed by…"
- **Capitalization**: capitalize official titles (Associate Professor), department names, and funding agency names. Do not capitalize "postdoctoral researcher" mid-sentence.
- **Numbers**: spell out one through nine; use numerals for 10+.

---

## 8. Publications

### Source of truth
`publications.bib` in the repository root. Hugo pages in `content/publication/` are generated from it and should not be edited by hand.

### Required BibTeX fields
```
author, title, year, journal or booktitle
```
**Strongly preferred**: `doi`. Papers with no DOI will not be picked up by the monthly auto-check and must be added manually.

### Adding a paper manually
```bash
# 1. Append the BibTeX entry to publications.bib
# 2. Generate Hugo pages
pip install "academic>=0.10.0"
academic import publications.bib content/publication/ --compact
# 3. Commit
git add publications.bib content/publication/
git commit -m "publications: add <slug>"
git push
```

### Monthly auto-check
A GitHub Actions cron runs on the 1st of each month, queries **Semantic Scholar author ID `47680095`**, and opens a PR titled *"📚 N new publication(s) found — please review"* on the `publications/monthly-update` branch. Merge to add; close without merging to skip.

### Slug naming
Auto-generated by `academic import` as `{firstauthor}-{year}-{firstword}`. Do not rename slugs after the page is live (breaks inbound links).

### Publication types
Use the standard type codes from Hugo Blox: `article-journal`, `paper-conference`, `preprint`, `book`, `chapter`, `thesis`. Set via the `ENTRYTYPE` field in BibTeX.

---

## 9. Marimo Notebooks (GFD & DA Tutorial)

- **Sources**: `notebooks/*.py` (marimo format).
- **Export**: CI runs `uvx marimo export html-wasm --sandbox --mode edit notebooks/<name>.py -o static/gfd/<name>.html` at deploy time.
- **To preview locally**: `marimo edit notebooks/<name>.py` from the GeophysicalFluidDynamics repo.
- **Do not commit** the exported `.html` files — CI regenerates them.
- **Notebook tone**: instructional, self-contained. Include markdown cells explaining the physics before the code.

---

## 10. Accessibility Baseline (target: WCAG 2.1 AA)

- All `<img>` must have descriptive `alt` text (not just the filename).
- Minimum contrast: **4.5:1** for body text, **3:1** for large text (18px+ or 14px bold+).
- Interactive elements that are not `<a>` or `<button>` must have `tabindex="0"`, `role="button"`, and respond to Enter/Space keydown.
- The people page person cards already implement this pattern — follow it for any new interactive components.
- Dark mode is supported via the system preference toggle; test new custom CSS in both modes.

---

## 11. SEO & Metadata

- Canonical domain is `https://aneeshcs.com`. The `baseURL` in `hugo.yaml` is set to `aneeshcs.github.io` — the CNAME file and GitHub Pages settings handle the redirect.
- Each non-auto-generated page should have a `description:` in its front matter.
- Publication pages automatically get `schema.org` structured data via Hugo Blox.
- Sitemap is auto-generated at `/sitemap.xml`. Robots.txt is auto-generated.
- DOI links in publications should always point to `https://doi.org/{doi}`, not journal-specific URLs (journals change; DOIs are permanent).

---

## 12. Performance Rules

- **Images**: always served via Hugo's image processing pipeline from `assets/media/` — never from `static/` unless they are already optimized (e.g., the pre-exported notebook HTML assets).
- **Lazy loading**: all images below the fold must use `loading="lazy"`. Hugo Blox sets this by default; maintain it in custom templates.
- **Homepage video**: must use `muted`, `autoplay`, `loop`, `playsinline`. Playback is slowed to `0.1×` via JavaScript to reduce visual motion. Keep the WebM file under 5MB.
- **No unoptimized images** larger than 500KB should be committed. Use `cwebp` or Squoosh to compress before committing.

---

## 13. What NOT to Customize

| Location | Status | Why |
|---|---|---|
| `~/.cache/hugo_cache/` | ❌ Never edit | Module cache; overwritten on `hugo mod get` |
| `node_modules/` | ❌ Never edit | Managed by npm/pnpm |
| `go.sum` | ❌ Never edit by hand | Managed by `hugo mod` |
| `content/publication/*/index.md` | ⚠️ Avoid editing | Regenerated by `academic import`; edits will be overwritten |
| `public/` | ❌ Never commit | Build output; generated by CI |

### Safe override pattern
To customize a Hugo Blox template without touching the module cache, place an override file at the equivalent path under `layouts/_partials/hbx/blocks/`. The project's `layouts/` directory takes precedence over module files.

**Example**: the team-showcase block is overridden at  
`layouts/_partials/hbx/blocks/team-showcase/block.html`.

---

## 14. File Structure Reference

```
config/_default/       Hugo & Hugo Blox config (params, menus, modules)
content/               Hugo Markdown source pages (edit freely)
  _index.md            Homepage (video hero block)
  people/index.md      People page (group ordering here)
  authors/{slug}/      Per-author Markdown bio
  publication/{slug}/  Publication pages (auto-generated — see §8)
data/authors/          Author YAML profiles (edit freely — see §6)
assets/
  media/authors/       Author headshots (source files)
  scss/custom.scss     Hero section overrides only
static/                Copied as-is; use sparingly
notebooks/             Marimo source files
layouts/               Local template overrides (safe to edit)
  _partials/hbx/blocks/team-showcase/block.html
  _partials/hooks/head-end/custom-css.html   ← main custom CSS
  _partials/hooks/head-end/github-button.html
.github/workflows/
  deploy.yml           Main deploy (Hugo build + marimo export)
  check-publications.yml  Monthly Semantic Scholar check
```
