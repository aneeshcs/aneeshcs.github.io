---
title: Enhanced Regional Ocean Ensemble Data Assimilation Through Atmospheric Coupling
  in the SKRIPS Model

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Rui Sun
- Aneesh Subramanian
- Matthew R Mazloff
- Bruce Cornuelle
- Ganesh Gopalakrishnan
- Arthur J Miller
- Ibrahim Hoteit

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2024-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T16:26:33.147529Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: ''
publication_short: ''

doi: 10.22541/essoar.170560036.67163458/v1

abstract: We investigate the impact of ocean data assimilation using the Ensemble
  Adjustment Kalman Filter (EAKF) from the Data Assimilation Research Testbed (DART)
  on the oceanic and atmospheric states of the Red Sea. Our study extends the ocean
  data assimilation experiment performed by Sanikommu et al. (2020) by utilizing the
  SKRIPS model coupling the MITgcm ocean model and the Weather Research and Forecasting
  (WRF) atmosphere model. Using a 50-member ensemble, we assimilate satellite-derived
  sea surface temperature and height and in-situ temperature and salinity profiles
  every three days for one year, starting January 01 2011. Atmospheric data are not
  assimilated in the experiments. To improve the ensemble realism, perturbations are
  added to the WRF model using several physics options and the stochastic kinetic
  energy backscatter (SKEB) scheme. Compared with the control experiments using uncoupled
  MITgcm with ECMWF ensemble forcing, the EAKF ensemble mean oceanic states from the
  coupled model are better or insignificantly worse (root-mean-square-errors are 30%
  to -2% smaller), especially when the atmospheric model uncertainties are accounted
  for with stochastic perturbations. We hypothesize that the ensemble spreads of the
  air–sea fluxes are better represented in the downscaled WRF ensembles when uncertainties
  are well accounted for, leading to improved representation of the ensemble oceanic
  states in EAKF. Although the feedback from ocean to atmosphere is included in this
  two-way regional coupled configuration, we find no significant effect of ocean data
  assimilation on the latent heat flux and 10-m wind speed, suggesting the improved
  skill is from downscaling the ensemble atmospheric forcings.

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
