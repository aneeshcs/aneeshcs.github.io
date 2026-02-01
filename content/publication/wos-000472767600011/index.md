---
title: A Stochastic Representation of Subgrid Uncertainty for Dynamical Core    Development
date: '2019-01-01'
draft: false
publishDate: '2026-02-01T16:51:12.913793Z'
authors:
- Aneesh Subramanian
- Stephan Juricke
- Peter Dueben
- Tim Palmer
publication_types:
- '2'
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
featured: false
publication: '*BULLETIN OF THE AMERICAN METEOROLOGICAL SOCIETY*'
doi: 10.1175/bams-d-17-0040.1
---

