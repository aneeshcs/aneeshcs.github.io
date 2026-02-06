---
title: A variational Bayesian approach for ensemble filtering of stochastically    parametrized
  systems

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Boujemaa Ait-El-Fquih
- Aneesh C. Subramanian
- Ibrahim Hoteit

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2023-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-06T05:57:01.068178Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*QUARTERLY JOURNAL OF THE ROYAL METEOROLOGICAL SOCIETY*'
publication_short: ''

doi: 10.1002/qj.4481

abstract: Modern climate models use both deterministic and stochastic    parametrization
  schemes to represent uncertainties in their physics and inputs. This work considers
  the problem of estimating the involved parameters of such systems simultaneously
  with their state through data assimilation. Standard state-parameter filtering schemes
  cannot be applied to such systems, owing to the posterior dependence between the
  stochastic parameters and the ``dynamical'' augmented state, defined as the state
  augmented by the deterministic parameters. We resort to the variational Bayesian
  (VB) approach to break this dependence, by approximating the joint posterior probability
  density function (pdf) of the augmented state and the stochastic parameters with
  a separable product of two marginal pdfs that minimizes the Kullback-Leibler divergence.
  The resulting marginal pdf of the augmented state is then sampled using a one-step-ahead
  smoothing-based ensemble Kalman filter (EnKF-OSAS), whereas a closed form is derived
  for the marginal pdf of the stochastic parameters. The proposed approach combines
  the effectiveness of the OSAS filtering approach to mitigate inconsistency issues
  that often arise with the joint ensemble Kalman filter (EnKF), with the advantage
  of obtaining a full posterior pdf for the stochastic parameters, which is not possible
  with the traditional maximum-likelihood method. We demonstrate the relevance of
  the proposed approach through extensive numerical experiments with a one-scale Lorenz-96
  model, which includes a stochastic parametrization representing subgrid-scale effects.

# Summary. An optional shortened abstract.
summary: ''

tags:
- data assimilation; ensemble Kalman filter; one-step-ahead smoothing;    stochastic
  parametrization; variational Bayes

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
