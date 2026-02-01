---
title: Tour
type: landing

sections:
  - block: markdown
    id: tour-slider
    content:
      title: ""
      text: |
        <style>
          .tour-slideshow {
            width: 100vw;
            position: relative;
            left: 50%;
            right: 50%;
            margin-left: -50vw;
            margin-right: -50vw;
            height: calc(100vh - 70px);
            overflow: hidden;
          }
          .tour-slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            opacity: 0;
            transition: opacity 0.6s ease-in-out;
            pointer-events: none;
            background-repeat: no-repeat;
            background-size: cover;
          }
          .tour-slide.active {
            opacity: 1;
            pointer-events: auto;
          }
          .slide-1 { 
            background-image: url('/media/crepuscular_rays_ocean.jpg');
            background-position: right;
            justify-content: center; 
          }
          .slide-2 { 
            background-image: url('/media/clouds_over_ocean.jpg');
            background-position: center;
            justify-content: flex-start; 
          }
          .slide-3 { 
            background-image: url('/media/clouds_over_ocean_2.jpg');
            background-position: center;
            justify-content: flex-end; 
          }
          .slide-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.35);
          }
          .slide-content {
            max-width: 700px;
            padding: 3rem;
            position: relative;
            z-index: 2;
          }
          .slide-content h2 {
            font-size: 3rem;
            font-weight: 400;
            margin-bottom: 24px;
            line-height: 1.2;
            color: white;
          }
          .slide-content p {
            font-size: 1.2rem;
            color: rgba(255,255,255,0.9);
            line-height: 1.7;
            margin-bottom: 2rem;
          }
          .slide-content .btn {
            display: inline-block;
            padding: 14px 28px;
            background: white;
            color: #1e3a5f;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            font-size: 1.1rem;
          }
          .slide-content .btn:hover {
            background: #f0f0f0;
          }
          .tour-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            font-size: 2rem;
            padding: 1rem 1.2rem;
            cursor: pointer;
            border-radius: 50%;
            transition: background 0.3s;
            z-index: 10;
          }
          .tour-nav:hover {
            background: rgba(255,255,255,0.4);
          }
          .tour-nav.prev { left: 2rem; }
          .tour-nav.next { right: 2rem; }
          .tour-dots {
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            z-index: 10;
          }
          .tour-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(255,255,255,0.4);
            border: none;
            cursor: pointer;
            transition: background 0.3s;
          }
          .tour-dot.active, .tour-dot:hover {
            background: white;
          }
        </style>

        <div class="tour-slideshow">
          <div class="tour-slide slide-1 active">
            <div class="slide-overlay"></div>
            <div class="slide-content" style="text-align: center; margin: 0 auto;">
              <h2>👋 Welcome to the group</h2>
              <p>Take a look at what we're working on…</p>
            </div>
          </div>
          
          <div class="tour-slide slide-2">
            <div class="slide-overlay"></div>
            <div class="slide-content" style="margin-left: 4rem; text-align: left;">
              <h2>our group</h2>
              <p>Based in Boulder, CO, our group collaborates globally and works on problems from pole to pole!</p>
              <a href="/contact" class="btn">🎓 Join Us</a>
            </div>
          </div>
          
          <div class="tour-slide slide-3">
            <div class="slide-overlay"></div>
            <div class="slide-content" style="margin-right: 4rem; margin-left: auto; text-align: right;">
              <h2>Climate Processes and Predictability Lab</h2>
              <a href="/projects" class="btn">Discover our projects</a>
            </div>
          </div>
          
          <button class="tour-nav prev" onclick="changeSlide(-1)">❮</button>
          <button class="tour-nav next" onclick="changeSlide(1)">❯</button>
          
          <div class="tour-dots">
            <button class="tour-dot active" onclick="goToSlide(0)"></button>
            <button class="tour-dot" onclick="goToSlide(1)"></button>
            <button class="tour-dot" onclick="goToSlide(2)"></button>
          </div>
        </div>

        <script>
          let currentSlide = 0;
          const slides = document.querySelectorAll('.tour-slide');
          const dots = document.querySelectorAll('.tour-dot');
          
          function showSlide(n) {
            slides.forEach(s => s.classList.remove('active'));
            dots.forEach(d => d.classList.remove('active'));
            currentSlide = (n + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
          }
          
          function changeSlide(direction) {
            showSlide(currentSlide + direction);
          }
          
          function goToSlide(n) {
            showSlide(n);
          }
          
          // Keyboard navigation
          document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') changeSlide(-1);
            if (e.key === 'ArrowRight') changeSlide(1);
          });
        </script>
    design:
      spacing:
        padding: ["0", "0", "0", "0"]
---
