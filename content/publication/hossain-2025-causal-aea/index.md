---
title: Causal Time Series Modeling of Supraglacial Lake Evolution in Greenland under
  Distribution Shift

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Emam Hossain
- Muhammad Hasan Ferdous
- Devon Dunmire
- Aneesh Subramanian
- Md Osman Gani

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2025-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T16:26:33.099240Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*arXiv*'
publication_short: ''

doi: 10.48550/arxiv.2510.15265

abstract: Causal modeling offers a principled foundation for uncovering stable, invariant
  relationships in time-series data, thereby improving robustness and generalization
  under distribution shifts. Yet its potential is underutilized in spatiotemporal
  Earth observation, where models often depend on purely correlational features that
  fail to transfer across heterogeneous domains. We propose RIC-TSC, a regionally-informed
  causal time-series classification framework that embeds lag-aware causal discovery
  directly into sequence modeling, enabling both predictive accuracy and scientific
  interpretability. Using multi-modal satellite and reanalysis data-including Sentinel-1
  microwave backscatter, Sentinel-2 and Landsat-8 optical reflectance, and CARRA meteorological
  variables-we leverage Joint PCMCI+ (J-PCMCI+) to identify region-specific and invariant
  predictors of supraglacial lake evolution in Greenland. Causal graphs are estimated
  globally and per basin, with validated predictors and their time lags supplied to
  lightweight classifiers. On a balanced benchmark of 1000 manually labeled lakes
  from two contrasting melt seasons (2018-2019), causal models achieve up to 12.59%
  higher accuracy than correlation-based baselines under out-of-distribution evaluation.
  These results show that causal discovery is not only a means of feature selection
  but also a pathway to generalizable and mechanistically grounded models of dynamic
  Earth surface processes.

# Summary. An optional shortened abstract.
summary: ''

tags: []

# Display this page in a list of Featured pages?
featured: false

# Links
url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

# Publication image
# Add an image named `featured.jpg/png` to your page's folder then add a caption below.
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects: ['internal-project']` links to `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []
---

Add the **full text** or **supplementary notes** for the publication here using Markdown formatting.
