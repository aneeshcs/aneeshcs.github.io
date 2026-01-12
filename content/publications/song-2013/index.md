---
title: An Adjoint-Based Adaptive Ensemble Kalman Filter

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Hajoon Song
- Ibrahim Hoteit
- Bruce D. Cornuelle
- Xiaodong Luo
- Aneesh C. Subramanian

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2013-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-01-12T05:46:53.704952Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*Monthly Weather Review*'
publication_short: ''

doi: 10.1175/mwr-d-12-00244.1

abstract: A new hybrid ensemble Kalman filter/four-dimensional variational data assimilation
  (EnKF/4D-VAR) approach is introduced to mitigate background covariance limitations
  in the EnKF. The work is based on the adaptive EnKF (AEnKF) method, which bears
  a strong resemblance to the hybrid EnKF/three-dimensional variational data assimilation
  (3D-VAR) method. In the AEnKF, the representativeness of the EnKF ensemble is regularly
  enhanced with new members generated after back projection of the EnKF analysis residuals
  to state space using a 3D-VAR [or optimal interpolation (OI)] scheme with a preselected
  background covariance matrix. The idea here is to reformulate the transformation
  of the residuals as a 4D-VAR problem, constraining the new member with model dynamics
  and the previous observations. This should provide more information for the estimation
  of the new member and reduce dependence of the AEnKF on the assumed stationary background
  covariance matrix. This is done by integrating the analysis residuals backward in
  time with the adjoint model. Numerical experiments are performed with the Lorenz-96
  model under different scenarios to test the new approach and to evaluate its performance
  with respect to the EnKF and the hybrid EnKF/3D-VAR. The new method leads to the
  least root-mean-square estimation errors as long as the linear assumption guaranteeing
  the stability of the adjoint model holds. It is also found to be less sensitive
  to choices of the assimilation system inputs and parameters.

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
