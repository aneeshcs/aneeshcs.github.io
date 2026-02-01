---
title: 'Machine Learning for Stochastic Parameterization: Generative Adversarial    Networks
  in the Lorenz `96 Model'
date: '2020-01-01'
draft: false
publishDate: '2026-02-01T16:51:05.222987Z'
authors:
- II Gagne
- Hannah M. Christensen
- Aneesh C. Subramanian
- Adam H. Monahan
publication_types:
- '2'
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
featured: false
publication: '*JOURNAL OF ADVANCES IN MODELING EARTH SYSTEMS*'
tags:
- machine learning; stochastic parameterization; generative adversarial    networks;
  lorenz; climate; weather
doi: 10.1029/2019ms001896
---

