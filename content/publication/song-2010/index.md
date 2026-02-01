---
title: An Adaptive Approach to Mitigate Background Covariance Limitations in the Ensemble
  Kalman Filter
date: '2010-01-01'
draft: true
publishDate: '2026-02-01T16:50:37.771509Z'
authors:
- Hajoon Song
- Ibrahim Hoteit
- Bruce D. Cornuelle
- Aneesh C. Subramanian
publication_types:
- '2'
abstract: A new approach is proposed to address the background covariance limitations
  arising from undersampled ensembles and unaccounted model errors in the ensemble
  Kalman filter (EnKF). The method enhances the representativeness of the EnKF ensemble
  by augmenting it with new members chosen adaptively to add missing information that
  prevents the EnKF from fully fitting the data to the ensemble. The vectors to be
  added are obtained by back projecting the residuals of the observation misfits from
  the EnKF analysis step onto the state space. The back projection is done using an
  optimal interpolation (OI) scheme based on an estimated covariance of the subspace
  missing from the ensemble. In the experiments reported here, the OI uses a preselected
  stationary background covariance matrix, as in the hybrid EnKF–three-dimensional
  variational data assimilation (3DVAR) approach, but the resulting correction is
  included as a new ensemble member instead of being added to all existing ensemble
  members. The adaptive approach is tested with the Lorenz-96 model. The hybrid EnKF–3DVAR
  is used as a benchmark to evaluate the performance of the adaptive approach. Assimilation
  experiments suggest that the new adaptive scheme significantly improves the EnKF
  behavior when it suffers from small size ensembles and neglected model errors. It
  was further found to be competitive with the hybrid EnKF–3DVAR approach, depending
  on ensemble size and data coverage.
featured: false
publication: '*Monthly Weather Review*'
doi: 10.1175/2010mwr2871.1
---

