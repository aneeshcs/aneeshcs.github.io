---
title: GFD Portal
type: landing

sections:
  - block: markdown
    id: gfd-portal
    content:
      title: ""
      text: |
        <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        .gfd-wrap {
          width: 100vw;
          position: relative;
          left: 50%;
          right: 50%;
          margin-left: -50vw;
          margin-right: -50vw;
          background: linear-gradient(160deg, #0f2744 0%, #0e3d5c 50%, #082f45 100%);
          color: #e2e8f0;
          padding: 3rem 1.5rem 4rem;
          font-family: "Inter var", "Inter", system-ui, sans-serif;
        }

        .gfd-inner {
          max-width: 900px;
          margin: 0 auto;
        }

        /* ── Header ── */
        .gfd-hero {
          text-align: center;
          margin-bottom: 3rem;
        }
        .gfd-hero h1 {
          font-size: 2.2rem;
          font-weight: 600;
          letter-spacing: -0.01em;
          color: #7dd3fc;
          margin-bottom: 0.75rem;
        }
        .gfd-hero p {
          font-size: 1rem;
          color: #94a3b8;
          line-height: 1.7;
          max-width: 620px;
          margin: 0 auto;
        }

        /* ── Card grid ── */
        .gfd-cards {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
          gap: 1.5rem;
        }

        .gfd-card {
          background: rgba(10, 25, 47, 0.7);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          padding: 1.75rem;
          display: flex;
          flex-direction: column;
          gap: 1rem;
          transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
          backdrop-filter: blur(6px);
        }
        .gfd-card:hover {
          border-color: #06b6d4;
          transform: translateY(-3px);
          box-shadow: 0 8px 30px rgba(6, 182, 212, 0.15);
        }

        /* ── Card tag ── */
        .gfd-tag {
          font-family: monospace;
          font-size: 0.7rem;
          text-transform: uppercase;
          letter-spacing: 0.12em;
          color: #06b6d4;
          background: rgba(6, 182, 212, 0.1);
          border: 1px solid rgba(6, 182, 212, 0.35);
          border-radius: 4px;
          padding: 2px 9px;
          display: inline-block;
          width: fit-content;
        }

        /* ── Card title ── */
        .gfd-card h2 {
          font-size: 1.15rem;
          font-weight: 600;
          color: #e2e8f0;
          line-height: 1.3;
        }

        /* ── Description ── */
        .gfd-card p.gfd-desc {
          font-size: 0.9rem;
          color: #94a3b8;
          line-height: 1.65;
          flex-grow: 1;
        }

        /* ── Equation box ── */
        .gfd-eq {
          font-family: "Courier New", Courier, monospace;
          font-size: 0.85rem;
          color: #67e8f9;
          background: rgba(6, 182, 212, 0.06);
          border: 1px solid rgba(6, 182, 212, 0.2);
          border-radius: 6px;
          padding: 0.6rem 0.9rem;
          line-height: 1.5;
          letter-spacing: 0.01em;
        }

        /* ── Highlights list ── */
        .gfd-card ul {
          list-style: none;
          padding: 0;
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
        }
        .gfd-card ul li {
          font-size: 0.875rem;
          color: #94a3b8;
          padding-left: 1.1rem;
          position: relative;
          line-height: 1.5;
        }
        .gfd-card ul li::before {
          content: "✦";
          position: absolute;
          left: 0;
          color: #06b6d4;
          font-size: 0.6rem;
          top: 0.25rem;
        }

        /* ── Button ── */
        .gfd-card .gfd-btn-link {
          display: inline-block;
          text-align: center;
          padding: 0.6rem 1.3rem;
          background: #0369a1;
          color: #e0f2fe;
          border-radius: 7px;
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 500;
          transition: background 0.2s ease;
          align-self: flex-start;
          margin-top: auto;
        }
        .gfd-btn-link:hover {
          background: #0284c7;
          color: #fff;
          text-decoration: none;
        }

        /* ── Footer ── */
        .gfd-footer {
          margin-top: 3.5rem;
          text-align: center;
          font-size: 0.8rem;
          color: #475569;
          line-height: 1.8;
        }
        .gfd-footer a {
          color: #475569;
          text-decoration: underline;
          text-underline-offset: 2px;
        }
        .gfd-footer a:hover { color: #7dd3fc; }

        @media (max-width: 600px) {
          .gfd-cards { grid-template-columns: 1fr; }
          .gfd-hero h1 { font-size: 1.6rem; }
        }
        </style>

        <div class="gfd-wrap">
          <div class="gfd-inner">

            <header class="gfd-hero">
              <h1>Geophysical Fluid Dynamics</h1>
              <p>Interactive pedagogical notebooks exploring the mathematics and physics
              of rotating, stratified geophysical flows. Each notebook runs entirely in
              your browser via WebAssembly — no installation required.</p>
            </header>

            <div class="gfd-cards">

              <!-- Card 1: Rayleigh-Bénard -->
              <div class="gfd-card">
                <span class="gfd-tag">Convection</span>
                <h2>Rayleigh-Bénard Convection &amp; Lorenz Chaos</h2>
                <p class="gfd-desc">
                  2D thermal convection in a Boussinesq fluid heated from below.
                  Truncating the governing equations to three Fourier amplitudes
                  yields the Lorenz (1963) system — the canonical model of
                  deterministic chaos and the original "butterfly effect."
                </p>
                <div class="gfd-eq">Ra = g α ΔT H³ / (ν κ)</div>
                <ul>
                  <li>Lattice-Boltzmann D2Q9 solver with real-time rendering</li>
                  <li>Lorenz attractor: sensitive dependence on initial conditions</li>
                  <li>Bifurcation from conduction → steady rolls → chaos</li>
                  <li>Nusselt number as a function of Rayleigh number</li>
                </ul>
                <a href="/gfd/rayleighbenard.html" class="gfd-btn-link" target="_blank">▶ Open Notebook</a>
              </div>

              <!-- Card 2: Geostrophic Adjustment -->
              <div class="gfd-card">
                <span class="gfd-tag">Rotating Fluids</span>
                <h2>Geostrophic Adjustment &amp; Shallow Water Waves</h2>
                <p class="gfd-desc">
                  Linearised shallow water equations on a rotating beta-plane.
                  A Gaussian height perturbation simultaneously radiates fast
                  inertia-gravity waves and slowly adjusts toward geostrophic
                  balance, with Rossby waves drifting westward via the β-effect.
                </p>
                <div class="gfd-eq">ω² = f² + c²(k² + l²) &nbsp;·&nbsp; L_R = c / f₀</div>
                <ul>
                  <li>Pseudo-spectral RK4 solver on a doubly-periodic domain</li>
                  <li>Inertia-gravity vs. Rossby wave dispersion relations</li>
                  <li>Rossby deformation radius controls adjustment scale</li>
                  <li>KE / PE energy partition during geostrophic adjustment</li>
                </ul>
                <a href="/gfd/shallowwater.html" class="gfd-btn-link" target="_blank">▶ Open Notebook</a>
              </div>

              <!-- Card 3: 2D Navier-Stokes -->
              <div class="gfd-card">
                <span class="gfd-tag">Turbulence</span>
                <h2>2D Navier-Stokes Turbulence</h2>
                <p class="gfd-desc">
                  Decaying turbulence governed by the 2D incompressible
                  Navier-Stokes equations in vorticity-streamfunction form.
                  Unlike 3D turbulence, energy cascades <em>upscale</em> while
                  enstrophy cascades to small scales — a consequence of the
                  additional conservation law in two dimensions.
                </p>
                <div class="gfd-eq">∂ω/∂t + J(ψ, ω) = ν ∇²ω</div>
                <ul>
                  <li>Pseudo-spectral solver with 2/3-rule dealiasing</li>
                  <li>Inverse energy cascade: k⁻⁵/³ power-law spectrum</li>
                  <li>Forward enstrophy cascade: k⁻³ spectrum</li>
                  <li>Vortex merging and coherent structure formation</li>
                </ul>
                <a href="/gfd/twodnavierstokes.html" class="gfd-btn-link" target="_blank">▶ Open Notebook</a>
              </div>

              <!-- Card 4: Internal Waves -->
              <div class="gfd-card">
                <span class="gfd-tag">Stratification</span>
                <h2>Internal Gravity Waves</h2>
                <p class="gfd-desc">
                  Internal waves propagate through a stably stratified fluid,
                  carrying energy at angles set by the ratio of wave frequency
                  to the Brunt-Väisälä frequency. Their peculiar dispersion
                  relation — energy and phase propagate perpendicular to each
                  other — makes them unlike any surface wave.
                </p>
                <div class="gfd-eq">N² = -(g/ρ₀)(∂ρ/∂z) &nbsp;·&nbsp; ω = N cos θ</div>
                <ul>
                  <li>Brunt-Väisälä (buoyancy) frequency and stable stratification</li>
                  <li>Angle-dependent dispersion: group velocity ⊥ phase velocity</li>
                  <li>Saint Andrews Cross wave-beam pattern</li>
                  <li>Wave reflection, focusing, and critical layers</li>
                </ul>
                <a href="/gfd/internalwaves.html" class="gfd-btn-link" target="_blank">▶ Open Notebook</a>
              </div>

            </div><!-- /.gfd-cards -->

            <footer class="gfd-footer">
              Built with <a href="https://marimo.io" target="_blank">marimo</a> &amp;
              <a href="https://numpy.org" target="_blank">NumPy</a> ·
              Runs in-browser via <a href="https://pyodide.org" target="_blank">Pyodide</a> WebAssembly ·
              <a href="https://github.com/aneeshcs/aneeshcs.github.io" target="_blank">Source on GitHub</a>
            </footer>

          </div>
        </div>
