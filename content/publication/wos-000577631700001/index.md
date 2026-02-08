---
title: Enhancing ensemble data assimilation into one-way-coupled models with    one-step-ahead
  smoothing

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Naila F. Raboudi
- Boujemaa Ait-El-Fquih
- Aneesh C. Subramanian
- Ibrahim Hoteit

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2021-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T15:46:10.715676Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*QUARTERLY JOURNAL OF THE ROYAL METEOROLOGICAL SOCIETY*'
publication_short: ''

doi: 10.1002/qj.3916

abstract: This study investigates the filtering problem with one-way coupled (OWC)    state-space
  systems, for which the joint ensemble Kalman filter (EnKF) is the standard solution.
  In this approach, the states of the two coupled sub-systems are jointly updated
  with all incoming observations. This enables transfer of the information across
  the sub-systems, which should provide coupled-state estimates in better agreement
  with the observations. The state estimates of the joint EnKF highly depend on the
  relevance of the joint ensembles' cross-covariances between the sub-systems' variables.
  In this work, we propose a new joint EnKF scheme based on the One-Step-Ahead (OSA)
  smoothing formulation of the filtering problem for efficient assimilation into OWC
  systems. The scheme introduces an extra smoothing step for both states' sub-systems
  with the future observations, followed by an analysis step for each sub-system state
  using only its own observation, all within a Bayesian-consistent framework. The
  extra OSA smoothing step enables us to more efficiently exploit the observations,
  to enhance the representativeness of the EnKF covariances, and to mitigate for reported
  inconsistencies in the joint EnKF analysis step. We demonstrate the relevance of
  the proposed approach by presenting and analyzing results of various numerical experiments
  conducted with a OWC Lorenz-96 model.

# Summary. An optional shortened abstract.
summary: ''

tags:
- ensemble Kalman filter; one-step-ahead smoothing; one-way coupling

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
