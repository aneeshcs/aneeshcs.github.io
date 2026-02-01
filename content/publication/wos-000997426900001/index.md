---
title: A variational Bayesian approach for ensemble filtering of stochastically    parametrized
  systems
date: '2023-01-01'
draft: true
publishDate: '2026-02-01T16:50:43.507889Z'
authors:
- Boujemaa Ait-El-Fquih
- Aneesh C. Subramanian
- Ibrahim Hoteit
publication_types:
- '2'
abstract: Modern climate models use both deterministic and stochastic    parametrization
  schemes to represent uncertainties in their physics and inputs. This work considers
  the problem of estimating the involved parameters of such systems simultaneously
  with their state through data assimilation. Standard state-parameter filtering schemes
  cannot be applied to such systems, owing to the posterior dependence between the
  stochastic parameters and the ``dynamical'' augmented state, defined as the state
  augmented by the deterministic parameters. We resort to the variational Bayesian
  (VB) approach to break this dependence, by approximating the joint posterior probability
  density function (pdf) of the augmented state and the stochastic parameters with
  a separable product of two marginal pdfs that minimizes the Kullback-Leibler divergence.
  The resulting marginal pdf of the augmented state is then sampled using a one-step-ahead
  smoothing-based ensemble Kalman filter (EnKF-OSAS), whereas a closed form is derived
  for the marginal pdf of the stochastic parameters. The proposed approach combines
  the effectiveness of the OSAS filtering approach to mitigate inconsistency issues
  that often arise with the joint ensemble Kalman filter (EnKF), with the advantage
  of obtaining a full posterior pdf for the stochastic parameters, which is not possible
  with the traditional maximum-likelihood method. We demonstrate the relevance of
  the proposed approach through extensive numerical experiments with a one-scale Lorenz-96
  model, which includes a stochastic parametrization representing subgrid-scale effects.
featured: false
publication: '*QUARTERLY JOURNAL OF THE ROYAL METEOROLOGICAL SOCIETY*'
tags:
- data assimilation; ensemble Kalman filter; one-step-ahead smoothing;    stochastic
  parametrization; variational Bayes
doi: 10.1002/qj.4481
---

