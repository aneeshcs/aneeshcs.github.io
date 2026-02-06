---
title: Time Series Classification of Supraglacial Lakes Evolution over Greenland Ice
  Sheet

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Emam Hossain
- Md Osman Gani
- Devon Dunmire
- Aneesh Subramanian
- Hammad Younas

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2024-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-06T05:57:01.471370Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*arXiv*'
publication_short: ''

doi: 10.48550/arxiv.2410.05638

abstract: "The Greenland Ice Sheet (GrIS) has emerged as a significant contributor
  to global sea level rise, primarily due to increased meltwater runoff. Supraglacial
  lakes, which form on the ice sheet surface during the summer months, can impact
  ice sheet dynamics and mass loss; thus, better understanding these lakes' seasonal
  evolution and dynamics is an important task. This study presents a computationally
  efficient time series classification approach that uses Gaussian Mixture Models
  (GMMs) of the Reconstructed Phase Spaces (RPSs) to identify supraglacial lakes based
  on their seasonal evolution: 1) those that refreeze at the end of the melt season,
  2) those that drain during the melt season, and 3) those that become buried, remaining
  liquid insulated a few meters beneath the surface. Our approach uses time series
  data from the Sentinel-1 and Sentinel-2 satellites, which utilize microwave and
  visible radiation, respectively. Evaluated on a GrIS-wide dataset, the RPS-GMM model,
  trained on a single representative sample per class, achieves 85.46% accuracy with
  Sentinel-1 data alone and 89.70% with combined Sentinel-1 and Sentinel-2 data. This
  performance significantly surpasses existing machine learning and deep learning
  models which require a large training data. The results demonstrate the robustness
  of the RPS-GMM model in capturing the complex temporal dynamics of supraglacial
  lakes with minimal training data."

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
