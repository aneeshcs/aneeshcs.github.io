---
title: A Stochastic Representation of Subgrid Uncertainty for Dynamical Core    Development

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Aneesh Subramanian
- Stephan Juricke
- Peter Dueben
- Tim Palmer

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2019-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T16:26:33.512063Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*BULLETIN OF THE AMERICAN METEOROLOGICAL SOCIETY*'
publication_short: ''

doi: 10.1175/bams-d-17-0040.1

abstract: Numerical weather prediction and climate models comprise a) a dynamical    core
  describing resolved parts of the climate system and b) parameterizations describing
  unresolved components. Development of new subgrid-scale parameterizations is particularly
  uncertain compared to representing resolved scales in the dynamical core. This uncertainty
  is currently represented by stochastic approaches in several operational weather
  models, which will inevitably percolate into the dynamical core. Hence, implementing
  dynamical cores with excessive numerical accuracy will not bring forecast gains,
  may even hinder them since valuable computer resources will be tied up doing insignificant
  computation, and therefore cannot be deployed for more useful gains, such as increasing
  model resolution or ensemble sizes. Here we describe a low-cost stochastic scheme
  that can be implemented in any existing deterministic dynamical core as an additive
  noise term. This scheme could be used to adjust accuracy in future dynamical core
  development work. We propose that such an additive stochastic noise test case should
  become a part of the routine testing and development of dynamical cores in a stochastic
  framework. The overall key point of the study is that we should not develop dynamical
  cores that are more precise than the level of uncertainty provided by our stochastic
  scheme. In this way, we present a new paradigm for dynamical core development work,
  ensuring that weather and climate models become more computationally efficient.
  We show some results based on tests done with the European Centre for Medium-Range
  Weather Forecasts (ECMWF) Integrated Forecasting System (IFS) dynamical core.

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
