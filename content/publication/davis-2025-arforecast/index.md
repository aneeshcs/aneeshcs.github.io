---
title: 'Physics-Based Versus AI Weather Prediction Models: A Comparative Performance
  Assessment of Atmospheric River Prediction'

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Isaac W. Davis
- Aneesh C. Subramanian
- Timothy B. Higgins
- Agniv Sengupta
- Luca Delle Monache

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2026-02-14'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T16:26:32.951235Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*Geophysical Research Letters*'
publication_short: '*GRL*'

hugoblox:
  ids:
    doi: 10.1029/2025GL117609

abstract: 'Machine learning (ML) poses a potential paradigm shift in weather forecasting,
  but critical questions arise regarding its ability to predict high-impact weather
  events. This study evaluates five state-of-the-art ML models—Aurora, GraphCast,
  PanguWeather, FourCastNetV2, FourCastNet—in forecasting U.S. West Coast atmospheric
  rivers (ARs), compared to the high-performing physics-based European Center for
  Medium-Range Weather Forecasts'' high-resolution system (HRES) model. Analysis of
  152 daily forecast cycles (November 2023–March 2024) reveals significant performance
  differences between the systems. While ML models often show better variable-specific
  root mean square error (RMSE), HRES has superior AR detection skill for the first
  four forecast days. PanguWeather matches HRES skill beyond day four; other ML models
  lag slightly. Aurora consistently exhibits the lowest AR detection performance,
  despite strong variable-specific RMSE metrics, highlighting a disconnect between
  RMSE performance and its ability to predict AR events. These findings underscore
  the need for phenomenon-specific metrics for ML-based numerical weather prediction
  model assessment and operational implementation.'

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

aliases:
  - /publication/davis-2025-arforecast-inreview/
---

Add the **full text** or **supplementary notes** for the publication here using Markdown formatting.
