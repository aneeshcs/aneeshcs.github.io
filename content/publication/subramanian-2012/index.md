---
title: Linear versus Nonlinear Filtering with Scale-Selective Corrections for Balanced
  Dynamics in a Simple Atmospheric Model

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Aneesh C. Subramanian
- Ibrahim Hoteit
- Bruce Cornuelle
- Arthur J. Miller
- Hajoon Song

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2012-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T16:26:34.313588Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*Journal of the Atmospheric Sciences*'
publication_short: ''

doi: 10.1175/jas-d-11-0332.1

abstract: This paper investigates the role of the linear analysis step of the ensemble
  Kalman filters (EnKF) in disrupting the balanced dynamics in a simple atmospheric
  model and compares it to a fully nonlinear particle-based filter (PF). The filters
  have a very similar forecast step but the analysis step of the PF solves the full
  Bayesian filtering problem while the EnKF analysis only applies to Gaussian distributions.
  The EnKF is compared to two flavors of the particle filter with different sampling
  strategies, the sequential importance resampling filter (SIRF) and the sequential
  kernel resampling filter (SKRF). The model admits a chaotic vortical mode coupled
  to a comparatively fast gravity wave mode. It can also be configured either to evolve
  on a so-called slow manifold, where the fast motion is suppressed, or such that
  the fast-varying variables are diagnosed from the slow-varying variables as slaved
  modes. Identical twin experiments show that EnKF and PF capture the variables on
  the slow manifold well as the dynamics is very stable. PFs, especially the SKRF,
  capture slaved modes better than the EnKF, implying that a full Bayesian analysis
  estimates the nonlinear model variables better. The PFs perform significantly better
  in the fully coupled nonlinear model where fast and slow variables modulate each
  other. This suggests that the analysis step in the PFs maintains the balance in
  both variables much better than the EnKF. It is also shown that increasing the ensemble
  size generally improves the performance of the PFs but has less impact on the EnKF
  after a sufficient number of members have been used.

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
