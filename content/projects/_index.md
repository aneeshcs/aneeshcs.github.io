---
title: Projects
type: landing

sections:
  - block: markdown
    id: projects
    content:
      title: ""
      text: |
        <style>
        .projects-container {
          width: 100vw;
          position: relative;
          left: 50%;
          right: 50%;
          margin-left: -50vw;
          margin-right: -50vw;
          background: linear-gradient(135deg, #0f2744 0%, #1a3a5c 50%, #0d3348 100%);
          color: white;
          padding: 3rem 2rem;
          box-sizing: border-box;
          min-height: 100vh;
        }
        .projects-inner { max-width: 1200px; margin: 0 auto; }
        .projects-section-title { font-size: 2rem; font-weight: 700; color: white; margin: 0 0 0.5rem 0; border-left: 4px solid #60a5fa; padding-left: 1rem; }
        .projects-section-subtitle { color: #93c5fd; font-size: 0.95rem; margin: 0 0 2rem 1.25rem; }
        .projects-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 3rem; }
        .project-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; overflow: hidden; transition: transform 0.2s ease, box-shadow 0.2s ease; display: flex; flex-direction: column; }
        .project-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.4); }
        .project-card-image { width: 100%; height: 160px; object-fit: cover; display: block; }
        .project-card-placeholder { width: 100%; height: 160px; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 600; text-align: center; padding: 1rem; box-sizing: border-box; color: white; letter-spacing: 0.04em; }
        .project-card-logo-bg { width: 100%; height: 160px; display: flex; align-items: center; justify-content: center; padding: 1.5rem; box-sizing: border-box; }
        .project-card-logo { max-width: 100%; max-height: 120px; object-fit: contain; }
        .project-card-body { padding: 1.25rem; flex: 1; display: flex; flex-direction: column; }
        .project-card-title { font-size: 1.05rem; font-weight: 700; color: white; margin: 0 0 0.5rem 0; line-height: 1.3; }
        .project-card-funder { font-size: 0.75rem; font-weight: 600; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem; }
        .project-card-desc { font-size: 0.88rem; color: #cbd5e1; line-height: 1.6; flex: 1; margin: 0 0 1rem 0; }
        .project-card-link { display: inline-block; font-size: 0.82rem; font-weight: 600; color: #93c5fd; text-decoration: none; border: 1px solid rgba(147,197,253,0.4); border-radius: 6px; padding: 0.3rem 0.75rem; transition: background 0.2s; align-self: flex-start; }
        .project-card-link:hover { background: rgba(147,197,253,0.15); color: white; }
        .past-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .past-item { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1rem 1.25rem; }
        .past-item-title { font-size: 0.95rem; font-weight: 600; color: #e2e8f0; margin: 0 0 0.25rem 0; }
        .past-item-meta { font-size: 0.78rem; color: #94a3b8; margin: 0; }
        .section-divider { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 2.5rem 0; }
        </style>
        <div class="projects-container">
        <div class="projects-inner">
        <h1 class="projects-section-title">Current Projects</h1>
        <p class="projects-section-subtitle">Active research funded by federal agencies and collaborative partnerships</p>
        <div class="projects-grid">
        <div class="project-card">
        <img class="project-card-image" src="https://iharp.umbc.edu/wp-content/uploads/sites/686/2022/01/iharp-logo.jpg" alt="iHARP" onerror="this.style.display='none'">
        <div class="project-card-body">
        <div class="project-card-funder">NSF</div>
        <h2 class="project-card-title">iHARP: Institute for Harnessing Data and Model Revolution in the Polar Regions</h2>
        <p class="project-card-desc">An NSF-funded institute combining data science and polar science to improve understanding of ice sheet dynamics and their contribution to sea-level rise through physics-informed, data-driven discoveries.</p>
        <a class="project-card-link" href="https://iharp.umbc.edu/" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        <div class="project-card">
        <div class="project-card-logo-bg" style="background:#0d1f3c;"><img class="project-card-logo" src="/media/logos/onr.png" alt="ONR"></div>
        <div class="project-card-body">
        <div class="project-card-funder">ONR</div>
        <h2 class="project-card-title">ASTraL: Arabian Sea Transition Layer</h2>
        <p class="project-card-desc">Understanding the dynamical mechanisms controlling the structure and coupling across the ocean and atmospheric boundary layer in the Arabian Sea, targeting climate model biases in ocean heat, atmospheric moisture, and precipitation.</p>
        <a class="project-card-link" href="https://www.onr.navy.mil/organization/departments/code-32/division-322/physical-oceanography/astral" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        <div class="project-card">
        <div class="project-card-logo-bg" style="background:#0b1d3a;"><img class="project-card-logo" src="/media/logos/nasa.png" alt="NASA"></div>
        <div class="project-card-body">
        <div class="project-card-funder">NASA</div>
        <h2 class="project-card-title">NASA Salinity Mission</h2>
        <p class="project-card-desc">Studying ocean salt content and its connections to climate, ocean circulation, and the global water cycle using satellite measurements and coordinated field research campaigns.</p>
        <a class="project-card-link" href="https://salinity.oceansciences.org/highlights.htm" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        <div class="project-card">
        <div class="project-card-logo-bg" style="background:#0d1f3c;"><img class="project-card-logo" src="/media/logos/onr.png" alt="ONR"></div>
        <div class="project-card-body">
        <div class="project-card-funder">ONR</div>
        <h2 class="project-card-title">SAFARI: Sea Air Flux and Atmospheric River Initiative</h2>
        <p class="project-card-desc">A distributed research initiative advancing understanding of physical processes associated with air-sea interaction and diabatic amplification that affect weather prediction accuracy and maritime storm development.</p>
        <a class="project-card-link" href="https://www.onr.navy.mil/organization/departments/code-32/division-322/marine-meteorology-space/sea-air-flux" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        <div class="project-card">
        <div class="project-card-logo-bg" style="background:#fff;"><img class="project-card-logo" src="/media/logos/doe.png" alt="DOE Office of Science"></div>
        <div class="project-card-body">
        <div class="project-card-funder">DOE</div>
        <h2 class="project-card-title">Earth and Environmental Systems Modeling: Sea Level Extremes</h2>
        <p class="project-card-desc">Investigating how climate patterns drive extreme sea level events along the U.S. East Coast using high-resolution Earth System Models to simulate past conditions and project future coastal flooding risks.</p>
        <a class="project-card-link" href="https://eesm.science.energy.gov/projects/sea-level-extremes-along-us-east-coast-e3sm-simulation-recent-past-and-projection-near" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        <div class="project-card">
        <div class="project-card-logo-bg" style="background:#003366;"><img class="project-card-logo" src="/media/logos/dwr.svg" alt="California DWR"></div>
        <div class="project-card-body">
        <div class="project-card-funder">California DWR</div>
        <h2 class="project-card-title">Atmospheric River Program</h2>
        <p class="project-card-desc">Combining statistical and dynamical forecasting to improve predictions of atmospheric rivers and integrated vapor transport targeting the U.S. West Coast for heavy precipitation monitoring.</p>
        <a class="project-card-link" href="https://cw3e.ucsd.edu/california-ar-program-theme/" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        <div class="project-card">
        <div class="project-card-logo-bg" style="background:#4a3728;"><img class="project-card-logo" src="/media/logos/usace.svg" alt="US Army Corps of Engineers"></div>
        <div class="project-card-body">
        <div class="project-card-funder">USACE</div>
        <h2 class="project-card-title">FIRO: Forecast Informed Reservoir Operations</h2>
        <p class="project-card-desc">Analyzing global model forecasts to evaluate the impact of atmospheric river reconnaissance observations on landfall predictions, supporting water management decisions in western U.S. watersheds.</p>
        <a class="project-card-link" href="https://cw3e.ucsd.edu/wp-content/uploads/Two_Pagers/C3WE_FIRO.pdf" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        <div class="project-card">
        <div class="project-card-logo-bg" style="background:#fff;"><img class="project-card-logo" src="/media/logos/noaa_cvp.png" alt="NOAA CVP"></div>
        <div class="project-card-body">
        <div class="project-card-funder">NOAA CVP</div>
        <h2 class="project-card-title">Tropical Pacific Process Studies (TEPEX)</h2>
        <p class="project-card-desc">Studying the dynamics of the tropical Pacific through coordinated observational and modeling efforts to advance understanding of ENSO and related climate variability.</p>
        <a class="project-card-link" href="https://cpo.noaa.gov/tropical-pacific-observing-system-tpos-equatorial-pacific-experiment-tepex/" target="_blank" rel="noopener">Learn more →</a>
        </div>
        </div>
        </div>
        <hr class="section-divider">
        <h1 class="projects-section-title">Past Projects</h1>
        <p class="projects-section-subtitle">Completed research</p>
        <div class="past-grid">
        <div class="past-item"><p class="past-item-title">Mesoscale Drivers of Oxygen in the Tropical Pacific</p><p class="past-item-meta">2020–2023 · NSF</p></div>
        <div class="past-item"><p class="past-item-title">MISO-BOB: Prediction of Monsoon Intra-Seasonal Oscillations</p><p class="past-item-meta">2018–2022 · ONR</p></div>
        <div class="past-item"><p class="past-item-title">Atmospheric River Program Phase II</p><p class="past-item-meta">2020–2022 · California DWR</p></div>
        <div class="past-item"><p class="past-item-title">Air-Sea Interaction in Tropical Western Pacific</p><p class="past-item-meta">2019–2021 · NOAA CVP</p></div>
        <div class="past-item"><p class="past-item-title">Marine Ecosystem Driver Predictability in California Current</p><p class="past-item-meta">2018–2021 · NOAA MAPP</p></div>
        <div class="past-item"><p class="past-item-title">Spring Heat Wave Predictability</p><p class="past-item-meta">2019–2021 · USBR</p></div>
        <div class="past-item"><p class="past-item-title">Pacific Decadal Climate Variability (EASM-3)</p><p class="past-item-meta">2014–2018 · NSF</p></div>
        <div class="past-item"><p class="past-item-title">CESM Tropical Pacific Bias Reduction</p><p class="past-item-meta">2014–2018 · NOAA</p></div>
        <div class="past-item"><p class="past-item-title">Diurnal Wind Variability Assessment</p><p class="past-item-meta">2014–2018 · NASA</p></div>
        <div class="past-item"><p class="past-item-title">Probabilistic Earth-System Model Development</p><p class="past-item-meta">2014–2017 · ERC</p></div>
        </div>
        </div>
        </div>
    design:
      css_class: dark
      spacing:
        padding: ["0", "0", "0", "0"]
---
