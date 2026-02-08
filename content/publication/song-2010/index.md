---
title: An Adaptive Approach to Mitigate Background Covariance Limitations in the Ensemble
  Kalman Filter

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Hajoon Song
- Ibrahim Hoteit
- Bruce D. Cornuelle
- Aneesh C. Subramanian

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2010-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T16:26:34.332877Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*Monthly Weather Review*'
publication_short: ''

doi: 10.1175/2010mwr2871.1

abstract: A new approach is proposed to address the background covariance limitations
  arising from undersampled ensembles and unaccounted model errors in the ensemble
  Kalman filter (EnKF). The method enhances the representativeness of the EnKF ensemble
  by augmenting it with new members chosen adaptively to add missing information that
  prevents the EnKF from fully fitting the data to the ensemble. The vectors to be
  added are obtained by back projecting the residuals of the observation misfits from
  the EnKF analysis step onto the state space. The back projection is done using an
  optimal interpolation (OI) scheme based on an estimated covariance of the subspace
  missing from the ensemble. In the experiments reported here, the OI uses a preselected
  stationary background covariance matrix, as in the hybrid EnKF–three-dimensional
  variational data assimilation (3DVAR) approach, but the resulting correction is
  included as a new ensemble member instead of being added to all existing ensemble
  members. The adaptive approach is tested with the Lorenz-96 model. The hybrid EnKF–3DVAR
  is used as a benchmark to evaluate the performance of the adaptive approach. Assimilation
  experiments suggest that the new adaptive scheme significantly improves the EnKF
  behavior when it suffers from small size ensembles and neglected model errors. It
  was further found to be competitive with the hybrid EnKF–3DVAR approach, depending
  on ensemble size and data coverage.

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
