---
title: Home
type: landing

sections:
  - block: markdown
    id: hero
    content:
      title: ""
      text: |
        <div style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; min-height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden;">
          <video autoplay loop muted playsinline id="bg-video" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;">
            <source src="/media/earth-loop.webm" type="video/webm">
          </video>
          <script>
            // Slow down the video playback
            var vid = document.getElementById('bg-video');
            vid.playbackRate = 0.1;
          </script>
          <div style="position: relative; z-index: 1; max-width: 650px; padding: 3rem; background: rgba(0,0,0,0.6); border-radius: 16px; text-align: center; backdrop-filter: blur(8px);">
            <h1 style="font-size: 2.8rem; font-weight: 400; margin-bottom: 12px; line-height: 1.2; color: white;">CHAOS &amp; Predictability Research Group</h1>
            <p style="font-size: 0.95rem; color: #bbb; letter-spacing: 0.04em; margin-bottom: 24px;">Computing Hydroclimate, Atmosphere and Ocean Systems</p>
            <p style="font-size: 1.15rem; color: #ddd; line-height: 1.7;">Our group aims to advance the fundamental understanding of climate processes in the earth system in order to improve weather and climate predictions.</p>
          </div>
        </div>
    design:
      css_class: dark
      spacing:
        padding: ["0", "0", "0", "0"]
---






