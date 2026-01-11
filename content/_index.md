---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: '6rem'

sections:
  - block: markdown
    content:
      title: 'Climate Processes and Predictability Research Group'
      subtitle: ''
      text: |-
        Our group aims to advance the fundamental understanding of climate processes in the earth system in order to improve weather and climate predictions.
    design:
      columns: '1'
  - block: collection
    id: news
    content:
      title: Latest News
      subtitle: ''
      text: ''
      # Page type to display. E.g. post, talk, publication...
      page_type: post
      # Choose how many pages you would like to display (0 = all pages)
      count: 5
      # Filter on criteria
      filters:
        author: ''
        category: ''
        tag: ''
        exclude_featured: false
        exclude_future: false
        exclude_past: false
        publication_type: ''
      # Choose how many pages you would like to offset by
      offset: 0
      # Page order: descending (desc) or ascending (asc) date.
      order: desc
    design:
      # Choose a layout view
      view: card
      columns: 2
  - block: collection
    id: projects
    content:
      title: Recent Projects
      subtitle: ''
      text: ''
      # Page type to display. E.g. post, talk, publication...
      page_type: project
      # Choose how many pages you would like to display (0 = all pages)
      count: 3
      # Filter on criteria
      filters:
        author: ''
        category: ''
        tag: ''
        exclude_featured: false
        exclude_future: false
        exclude_past: false
        publication_type: ''
      # Choose how many pages you would like to offset by
      offset: 0
      # Page order: descending (desc) or ascending (asc) date.
      order: desc
    design:
      # Choose a layout view
      view: card
      columns: 2
  - block: markdown
    content:
      title: ''
      subtitle: ''
      text: |-
        [Meet the team →](/people/)
    design:
      columns: '1'
---
