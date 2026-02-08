---
title: 'Machine Learning for Stochastic Parameterization: Generative Adversarial    Networks
  in the Lorenz `96 Model'

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- II Gagne
- Hannah M. Christensen
- Aneesh C. Subramanian
- Adam H. Monahan

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '2020-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2026-02-08T15:46:10.807481Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: '*JOURNAL OF ADVANCES IN MODELING EARTH SYSTEMS*'
publication_short: ''

doi: 10.1029/2019ms001896

abstract: Stochastic parameterizations account for uncertainty in the    representation
  of unresolved subgrid processes by sampling from the distribution of possible subgrid
  forcings. Some existing stochastic parameterizations utilize data-driven approaches
  to characterize uncertainty, but these approaches require significant structural
  assumptions that can limit their scalability. Machine learning models, including
  neural networks, are able to represent a wide range of distributions and build optimized
  mappings between a large number of inputs and subgrid forcings. Recent research
  on machine learning parameterizations has focused only on deterministic parameterizations.
  In this study, we develop a stochastic parameterization using the generative adversarial
  network (GAN) machine learning framework. The GAN stochastic parameterization is
  trained and evaluated on output from the Lorenz `96 model, which is a common baseline
  model for evaluating both parameterization and data assimilation techniques. We
  evaluate different ways of characterizing the input noise for the model and perform
  model runs with the GAN parameterization at weather and climate time scales. Some
  of the GAN configurations perform better than a baseline bespoke parameterization
  at both time scales, and the networks closely reproduce the spatiotemporal correlations
  and regimes of the Lorenz `96 system. We also find that, in general, those models
  which produce skillful forecasts are also associated with the best climate simulations.
  Plain Language Summary Simulations of the atmosphere must approximate the effects
  of small-scale processes with simplified functions called parameterizations. Standard
  parameterizations only predict one output for a given input, but stochastic parameterizations
  can sample from all the possible outcomes that can occur under certain conditions.
  We have developed and evaluated a machine learning stochastic parameterization,
  which builds a mapping between large-scale current conditions and the range of small-scale
  outcomes from data about both. We test the machine learning stochastic parameterization
  in a simplified mathematical simulation that produces multiscale chaotic waves like
  the atmosphere. We find that some configurations of the machine learning stochastic
  parameterization perform slightly better than a simpler baseline stochastic parameterization
  over both weather- and climate-like time spans.

# Summary. An optional shortened abstract.
summary: ''

tags:
- machine learning; stochastic parameterization; generative adversarial    networks;
  lorenz; climate; weather

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
