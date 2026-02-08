---
title: Quantifying Causes of Arctic Amplification via Deep Learning Based Time-Series
  Causal Inference

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- Sahara Ali
- Omar Faruque
- Yiyi Huang
- Md. Osman Gani
- Aneesh Subramanian
- Nicole-Jeanne Schlegel
- Jianwu Wang

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2023-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T15:46:10.475459Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*2023 International Conference on Machine Learning and Applications
  (ICMLA)*'
publication_short: ''

doi: 10.1109/icmla58977.2023.00101

abstract: The warming of the Arctic, also known as Arctic amplification, is led by
  several atmospheric and oceanic drivers. However, the details of its underlying
  thermodynamic causes are still unknown. Inferring the causal effects of atmospheric
  processes on sea ice melt using fixed treatment effect strategies leads to unrealistic
  counterfactual estimations. Such methods are also prone to bias due to time-varying
  confoundedness. Further, the complex non-linearity in Earth science data makes it
  infeasible to perform causal inference using existing marginal structural techniques.
  In order to tackle these challenges, we propose TCINet - Time-series Causal Inference
  Network to infer causation under continuous treatment using recurrent neural networks
  and a novel probabilistic balancing technique. More specifically, we propose a neural
  network based potential outcome model using the long-short-term-memory (LSTM) layers
  for time-delayed factual and counterfactual predictions with a custom weighted loss.
  To tackle the confounding bias, we experiment with multiple balancing strategies,
  namely TCINet with the inverse probability weighting (IPTW), TCINet with stabilized
  weights using Gaussian Mixture Model (GMMs) and TCINet without any balancing technique.
  Through experiments on synthetic and observational data, we show how our research
  can substantially improve the ability to quantify leading causes of Arctic sea ice
  melt, further paving paths for causal inference in observational Earth science.

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
