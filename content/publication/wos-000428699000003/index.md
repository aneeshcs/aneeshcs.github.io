---
title: Improving Weather Forecast Skill through Reduced-Precision Data    Assimilation

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Sam Hatfield
- Aneesh Subramanian
- Tim Palmer
- Peter Duben

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2018-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-06T05:57:01.382333Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*MONTHLY WEATHER REVIEW*'
publication_short: ''

doi: 10.1175/mwr-d-17-0132.1

abstract: A new approach for improving the accuracy of data assimilation, by    trading
  numerical precision for ensemble size, is introduced. Data assimilation is inherently
  uncertain because of the use of noisy observations and imperfect models. Thus, the
  larger rounding errors incurred from reducing precision may be within the tolerance
  of the system. Lower-precision arithmetic is cheaper, and so by reducing precision
  in ensemble data assimilation, computational resources can be redistributed toward,
  for example, a larger ensemble size. Because larger ensembles provide a better estimate
  of the underlying distribution and are less reliant on covariance inflation and
  localization, lowering precision could actually permit an improvement in the accuracy
  ofweather forecasts. Here, this idea is tested on an ensemble data assimilation
  systemcomprising the Lorenz ` 96 toy atmospheric model and the ensemble square root
  filter. The system is run at double-, single-, and halfprecision (the latter using
  an emulation tool), and the performance of each precision ismeasured throughmean
  error statistics and rank histograms. The sensitivity of these results to the observation
  error and the length of the observation window are addressed. Then, by reinvesting
  the saved computational resources from reducing precision into the ensemble size,
  assimilation error can be reduced for (hypothetically) no extra cost. This results
  in increased forecasting skill, with respect to double-precision assimilation.

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
