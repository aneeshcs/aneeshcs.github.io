---
title: Uncertainty Quantification and Bayesian Inference of Cloud    Parameterization
  in the NCAR Single Column Community Atmosphere Model (SCAM6)

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Raju Pathak
- Hari Prasad Dasari
- Samah El Mohtar
- Aneesh C. Subramanian
- Sandeep Sahany
- Saroj Kanta Mishra
- Omar Knio
- Ibrahim Hoteit

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2021-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-06T05:57:01.208945Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*FRONTIERS IN CLIMATE*'
publication_short: ''

doi: 10.3389/fclim.2021.670740

abstract: 'Uncertainty quantification (UQ) in weather and climate models is    required
  to assess the sensitivity of their outputs to various parameterization schemes and
  thereby improve their consistency with observations. Herein, we present an efficient
  UQ and Bayesian inference for the cloud parameters of the NCAR Single Column Atmosphere
  Model (SCAM6) using surrogate models based on a polynomial chaos expansion. The
  use of a surrogate model enables to efficiently propagate uncertainties in parameters
  into uncertainties in model outputs. We investigated eight uncertain parameters:
  the auto-conversion size threshold for ice to snow (dcs), the fall speed parameter
  for stratiform cloud ice (ai), the fall speed parameter for stratiform snow (as),
  the fall speed parameter for cloud water (ac), the collection efficiency of aggregation
  ice (eii), the efficiency factor of the Bergeron effect (berg_eff), the threshold
  maximum relative humidity for ice clouds (rhmaxi), and the threshold minimum relative
  humidity for ice clouds (rhmini). We built two surrogate models using two non-intrusive
  methods: spectral projection (SP) and basis pursuit denoising (BPDN). Our results
  suggest that BPDN performs better than SP as it enables to filter out internal noise
  during the process of fitting the surrogate model. Five out of the eight parameters
  (namely dcs, ai, rhmaxi, rhmini, and eii) account for most of the variance in predicted
  climate variables (e.g., total precipitation, cloud distribution, shortwave and
  longwave cloud radiative effect, ice, and liquid water path). A first-order sensitivity
  analysis reveals that dcs contributes similar to 40-80% of the total variance of
  the climate variables, ai around 15-30 %, and rhmaxi, rhmini, and eii around 5-15
  %. The second- and higher-order effects contribute similar to 7 and 20 %, respectively.
  The sensitivity of the model to these parameters was further explored using response
  curves. A Markov chain Monte Carlo (MCMC) sampling algorithm was also implemented
  for the Bayesian inference of dcs, ai, as, rhmini, and berg _eff using cloud distribution
  data collected at the Southern Great Plains (USA). The inferred parameters suggest
  improvements in the global Climate Earth System Model (CESM2) simulations of the
  tropics and sub-tropics.'

# Summary. An optional shortened abstract.
summary: ''

tags:
- climate modeling; uncertainty quantification; Bayesian inference; cloud    parameters;
  parameterization schemes

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
