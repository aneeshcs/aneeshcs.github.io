---
title: 'SKRIPS v1.0: a regional coupled ocean-atmosphere modeling framework    (MITgcm-WRF)
  using ESMF/NUOPC, description and preliminary results for the Red Sea'

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Rui Sun
- Aneesh C. Subramanian
- Arthur J. Miller
- Matthew R. Mazloff
- Ibrahim Hoteit
- Bruce D. Cornuelle

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2019-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T15:46:10.836771Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*GEOSCIENTIFIC MODEL DEVELOPMENT*'
publication_short: ''

doi: 10.5194/gmd-12-4221-2019

abstract: 'A new regional coupled ocean-atmosphere model is developed and its    implementation
  is presented in this paper. The coupled model is based on two open-source community
  model components: the MITgcm ocean model and the Weather Research and Forecasting
  (WRF) atmosphere model. The coupling between these components is performed using
  ESMF (Earth System Modeling Framework) and implemented according to National United
  Operational Prediction Capability (NUOPC) protocols. The coupled model is named
  the Scripps-KAUST Regional Integrated Prediction System (SKRIPS). SKRIPS is demonstrated
  with a real-world example by simulating a 30 d period including a series of extreme
  heat events occurring on the eastern shore of the Red Sea region in June 2012. The
  results obtained by using the coupled model, along with those in forced stand-alone
  oceanic or atmospheric simulations, are compared with observational data and reanalysis
  products. We show that the coupled model is capable of performing coupled ocean-atmosphere
  simulations, although all configurations of coupled and uncoupled models have good
  skill in modeling the heat events. In addition, a scalability test is performed
  to investigate the parallelization of the coupled model. The results indicate that
  the coupled model code scales well and the ESMF/NUOPC coupler accounts for less
  than 5% of the total computational resources in the Red Sea test case. The coupled
  model and documentation are available at https://library.ucsd.edu/dc/collection/bb1847661c
  (last access: 26 September 2019), and the source code is maintained at https://github.com/iurnus/scripps_kaust
  _model (last access: 26 September 2019).'

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
