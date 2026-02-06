---
title: 'Waves in SKRIPS: WAVEWATCH III coupling implementation and a case study    of
  Tropical Cyclone Mekunu'

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Rui Sun
- Alison Cobb
- Ana B. Villas Boas
- Sabique Langodan
- Aneesh C. Subramanian
- Matthew R. Mazloff
- Bruce D. Cornuelle
- Arthur J. Miller
- Raju Pathak
- Ibrahim Hoteit

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2023-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-06T05:57:01.048014Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*GEOSCIENTIFIC MODEL DEVELOPMENT*'
publication_short: ''

doi: 10.5194/gmd-16-3435-2023

abstract: In this work, we integrated the WAVEWATCH III model into the regional    coupled
  model SKRIPS (Scripps-KAUST Regional Integrated Prediction System). The WAVEWATCH
  III model is implemented with flexibility, meaning the coupled system can run with
  or without the wave component. In our implementations, we considered the effect
  of Stokes drift, Langmuir turbulence, sea surface roughness, and wave-induced momentum
  fluxes. To demonstrate the impact of coupling we performed a case study using a
  series of coupled and uncoupled simulations of Tropical Cyclone Mekunu, which occurred
  in the Arabian Sea in May 2018. We examined the model skill in these simulations
  and further investigated the impact of Langmuir turbulence in the coupled system.
  Because of the chaotic nature of the atmosphere, we ran an ensemble of 20 members
  for each coupled and uncoupled experiment. We found that the characteristics of
  the tropical cyclone are not significantly different due to the effect of surface
  waves when using different parameterizations, but the coupled models better capture
  the minimum pressure and maximum wind speed compared with the benchmark stand-alone
  Weather Research and Forecasting (WRF) model. Moreover, in the region of the cold
  wake, when Langmuir turbulence is considered in the coupled system, the sea surface
  temperature is about 0.5 & LCIRC;C colder, and the mixed layer is about 20 m deeper.
  This indicates the ocean model is sensitive to the parameterization of Langmuir
  turbulence in the coupled simulations.

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
