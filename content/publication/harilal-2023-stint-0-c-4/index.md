---
title: 'STint: Self-supervised Temporal Interpolation for Geospatial Data'

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Nidhin Harilal
- Bri-Mathias Hodge
- Aneesh Subramanian
- Claire Monteleoni

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2023-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-06T05:57:01.461724Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*arXiv*'
publication_short: ''

doi: 10.48550/arxiv.2309.00059

abstract: Supervised and unsupervised techniques have demonstrated the potential for
  temporal interpolation of video data. Nevertheless, most prevailing temporal interpolation
  techniques hinge on optical flow, which encodes the motion of pixels between video
  frames. On the other hand, geospatial data exhibits lower temporal resolution while
  encompassing a spectrum of movements and deformations that challenge several assumptions
  inherent to optical flow. In this work, we propose an unsupervised temporal interpolation
  technique, which does not rely on ground truth data or require any motion information
  like optical flow, thus offering a promising alternative for better generalization
  across geospatial domains. Specifically, we introduce a self-supervised technique
  of dual cycle consistency. Our proposed technique incorporates multiple cycle consistency
  losses, which result from interpolating two frames between consecutive input frames
  through a series of stages. This dual cycle consistent constraint causes the model
  to produce intermediate frames in a self-supervised manner. To the best of our knowledge,
  this is the first attempt at unsupervised temporal interpolation without the explicit
  use of optical flow. Our experimental evaluations across diverse geospatial datasets
  show that STint significantly outperforms existing state-of-the-art methods for
  unsupervised temporal interpolation.

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
