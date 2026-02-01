---
title: Improving Weather Forecast Skill through Reduced-Precision Data    Assimilation
date: '2018-01-01'
draft: false
publishDate: '2026-02-01T16:51:22.099720Z'
authors:
- Sam Hatfield
- Aneesh Subramanian
- Tim Palmer
- Peter Duben
publication_types:
- '2'
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
featured: false
publication: '*MONTHLY WEATHER REVIEW*'
doi: 10.1175/mwr-d-17-0132.1
---

