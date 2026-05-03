---
title: A study of reduced numerical precision to make superparameterization    more
  competitive using a hardware emulator in the OpenIFS model

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Peter D. Duben
- Aneesh Subramanian
- Andrew Dawson
- T. N. Palmer

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2017-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T16:26:33.735910Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*JOURNAL OF ADVANCES IN MODELING EARTH SYSTEMS*'
publication_short: ''

hugoblox:
  ids:
    doi: 10.1002/2016ms000862

abstract: The use of reduced numerical precision to reduce computing costs for the    cloud
  resolving model of superparameterized simulations of the atmosphere is investigated.
  An approach to identify the optimal level of precision for many different model
  components is presented, and a detailed analysis of precision is performed. This
  is nontrivial for a complex model that shows chaotic behavior such as the cloud
  resolving model in this paper. It is shown not only that numerical precision can
  be reduced significantly but also that the results of the reduced precision analysis
  provide valuable information for the quantification of model uncertainty for individual
  model components. The precision analysis is also used to identify model parts that
  are of less importance thus enabling a reduction of model complexity. It is shown
  that the precision analysis can be used to improve model efficiency for both simulations
  in double precision and in reduced precision. Model simulations are performed with
  a superparameterized single-column model version of the OpenIFS model that is forced
  by observational data sets. A software emulator was used to mimic the use of reduced
  precision floating point arithmetic in simulations. Plain Language Summary Weather
  and climate models cannot represent physical processes of the Earth System explicitly
  that are smaller than the distance between model grid points. Due to limitations
  in computing power, this distance is typically larger than 10 km in simulations
  of the global atmosphere. However, the spatial scale for many important physical
  processes, such as clouds, is much smaller than this and large errors are generated
  for predictions of both weather and climate due to limited resolution. To approximate
  the behavior of subgrid-scale processes within atmosphere models, superparameterization
  was developed that is running a two-dimensional small-scale model within each grid
  column of the global model. Superparameterization can improve model simulations
  but it causes a very large increase in computational cost in comparison to standard
  simulations. To reduce computational cost, this paper investigates whether it is
  possible to reduce numerical precision when running the small-scale model. It is
  shown that precision can indeed be reduced such that computing costs can potentially
  be reduced significantly. It is also shown that results of an investigation of reduced
  numerical precision provide valuable information for the quantification of model
  uncertainty and model development.

# Summary. An optional shortened abstract.
summary: ''

tags:
- superparameterization; reduced precision; inexact hardware; cloud    resolving model;
  high-performance computing; model uncertainty

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
