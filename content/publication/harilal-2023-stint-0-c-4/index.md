---
title: 'STint: Self-supervised Temporal Interpolation for Geospatial Data'
date: '2023-01-01'
draft: false
publishDate: '2026-02-01T16:51:38.143442Z'
authors:
- Nidhin Harilal
- Bri-Mathias Hodge
- Aneesh Subramanian
- Claire Monteleoni
publication_types:
- '2'
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
featured: false
publication: '*arXiv*'
doi: 10.48550/arxiv.2309.00059
---

