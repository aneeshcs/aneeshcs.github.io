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
        .gfd-container {
          width: 100vw;
          position: relative;
          left: 50%;
          right: 50%;
          margin-left: -50vw;
          margin-right: -50vw;
          min-height: calc(100vh - 70px);
          background: linear-gradient(135deg, #1e3a5f 0%, #1e4d6f 50%, #0d4f5f 100%);
          color: white;
          padding: 2rem;
          box-sizing: border-box;
        }
        .gfd-header {
          max-width: 1400px;
          margin: 0 auto 1.5rem auto;
          padding: 1rem 1.5rem;
          background: rgba(0,0,0,0.3);
          backdrop-filter: blur(8px);
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.2);
        }
        .gfd-header h1 {
          font-size: 2rem;
          font-weight: bold;
          margin: 0;
          color: white;
        }
        .gfd-header p {
          color: #93c5fd;
          font-size: 0.9rem;
          margin: 0.25rem 0 0 0;
        }
        .gfd-nav {
          max-width: 1400px;
          margin: 0 auto 1.5rem auto;
          padding: 1rem;
          background: rgba(0,0,0,0.3);
          backdrop-filter: blur(8px);
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.2);
        }
        .gfd-nav h2 {
          font-size: 0.875rem;
          font-weight: 600;
          color: #93c5fd;
          margin: 0 0 0.75rem 0;
        }
        .gfd-nav-buttons {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 0.75rem;
        }
        .gfd-nav-btn {
          padding: 0.75rem 1rem;
          border-radius: 8px;
          font-weight: 500;
          font-size: 0.9rem;
          cursor: pointer;
          transition: all 0.3s;
          border: none;
          background: rgba(255,255,255,0.1);
          color: #dbeafe;
        }
        .gfd-nav-btn:hover {
          background: rgba(255,255,255,0.2);
        }
        .gfd-nav-btn.active {
          background: #06b6d4;
          color: white;
          box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
        }
        .gfd-info {
          max-width: 1400px;
          margin: 0 auto 1.5rem auto;
          padding: 1rem;
          background: rgba(6, 182, 212, 0.2);
          backdrop-filter: blur(8px);
          border-radius: 12px;
          border: 1px solid rgba(6, 182, 212, 0.3);
        }
        .gfd-info h3 {
          font-weight: bold;
          color: #a5f3fc;
          margin: 0 0 0.5rem 0;
          font-size: 1.1rem;
        }
        .gfd-info p {
          color: #ecfeff;
          font-size: 0.9rem;
          margin: 0;
          line-height: 1.5;
        }
        .gfd-main {
          max-width: 1400px;
          margin: 0 auto;
          padding: 1.5rem;
          background: rgba(0,0,0,0.3);
          backdrop-filter: blur(8px);
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.2);
        }
        .gfd-layout {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        @media (min-width: 1024px) {
          .gfd-layout {
            flex-direction: row;
          }
        }
        .gfd-canvas-container {
          flex: 1;
        }
        .gfd-canvas {
          width: 100%;
          border-radius: 12px;
          box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
          border: 1px solid rgba(255,255,255,0.2);
          background: black;
        }
        .gfd-sidebar {
          width: 100%;
        }
        @media (min-width: 1024px) {
          .gfd-sidebar {
            width: 320px;
            flex-shrink: 0;
          }
        }
        .gfd-panel {
          background: rgba(255,255,255,0.1);
          border-radius: 12px;
          padding: 1rem;
          margin-bottom: 1rem;
        }
        .gfd-panel h3 {
          font-weight: bold;
          color: #a5f3fc;
          margin: 0 0 0.75rem 0;
          font-size: 1rem;
        }
        .gfd-controls {
          display: flex;
          gap: 0.75rem;
        }
        .gfd-btn {
          flex: 1;
          padding: 0.625rem 1rem;
          border-radius: 8px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          border: none;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          font-size: 0.9rem;
        }
        .gfd-btn-primary {
          background: #06b6d4;
          color: white;
        }
        .gfd-btn-primary:hover {
          background: #0891b2;
        }
        .gfd-btn-secondary {
          background: rgba(255,255,255,0.2);
          color: white;
        }
        .gfd-btn-secondary:hover {
          background: rgba(255,255,255,0.3);
        }
        .gfd-slider-group {
          margin-bottom: 1rem;
        }
        .gfd-slider-label {
          font-size: 0.875rem;
          color: #bfdbfe;
          display: block;
          margin-bottom: 0.5rem;
        }
        .gfd-slider {
          width: 100%;
          height: 6px;
          border-radius: 3px;
          background: rgba(255,255,255,0.2);
          outline: none;
          -webkit-appearance: none;
        }
        .gfd-slider::-webkit-slider-thumb {
          -webkit-appearance: none;
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: #06b6d4;
          cursor: pointer;
        }
        .gfd-legend-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 0.5rem;
        }
        .gfd-legend-color {
          width: 16px;
          height: 16px;
          border-radius: 4px;
        }
        .gfd-legend-text {
          font-size: 0.875rem;
          color: #dbeafe;
        }
        .gfd-concept p {
          font-size: 0.875rem;
          color: #dbeafe;
          line-height: 1.5;
          margin: 0;
        }
        </style>
        <div class="gfd-container">
        <div class="gfd-header">
        <h1>Geophysical Fluid Dynamics Portal</h1>
        <p>Interactive Educational Simulations</p>
        </div>
        <div class="gfd-nav">
        <h2>SELECT MODEL</h2>
        <div class="gfd-nav-buttons">
        <button class="gfd-nav-btn active" onclick="selectModel('rayleigh-benard')">Rayleigh-Bénard</button>
        <button class="gfd-nav-btn" onclick="selectModel('coriolis')">Coriolis Effect</button>
        <button class="gfd-nav-btn" onclick="selectModel('geostrophic')">Geostrophic Balance</button>
        <button class="gfd-nav-btn" onclick="selectModel('stratified')">Stratified Flow</button>
        <button class="gfd-nav-btn" onclick="selectModel('rossby')">Rossby Waves</button>
        </div>
        </div>
        <div class="gfd-info" id="gfd-info">
        <h3 id="model-title">Rayleigh-Bénard Convection</h3>
        <p id="model-description">Demonstrates thermal convection when fluid is heated from below. Hot fluid rises, cools at the top, and sinks, forming convection cells.</p>
        </div>
        <div class="gfd-main">
        <div class="gfd-layout">
        <div class="gfd-canvas-container">
        <canvas id="gfd-canvas" class="gfd-canvas" width="800" height="450"></canvas>
        </div>
        <div class="gfd-sidebar">
        <div class="gfd-panel">
        <h3>Controls</h3>
        <div class="gfd-controls">
        <button class="gfd-btn gfd-btn-primary" id="play-btn" onclick="togglePlay()">
        <span id="play-icon">⏸</span>
        <span id="play-text">Pause</span>
        </button>
        <button class="gfd-btn gfd-btn-secondary" onclick="resetSimulation()">↺ Reset</button>
        </div>
        </div>
        <div class="gfd-panel" id="params-panel">
        <h3>Parameters</h3>
        <div id="params-container"></div>
        </div>
        <div class="gfd-panel" id="legend-panel">
        <h3>Legend</h3>
        <div id="legend-container"></div>
        </div>
        <div class="gfd-panel gfd-concept" id="concept-panel">
        <h3>Key Concept</h3>
        <p id="concept-text"></p>
        </div>
        </div>
        </div>
        </div>
        </div>
        <script>
        let currentModel = 'rayleigh-benard';
        let isPlaying = true;
        let animationId = null;
        let params = {};
        const models = {
          'rayleigh-benard': {
            name: 'Rayleigh-Bénard Convection',
            description: 'Lattice Boltzmann simulation of thermal convection. Fluid heated from below becomes buoyant and rises, forming convection cells — the same physics that drives plate tectonics and atmospheric circulation.',
            concept: 'This uses the Lattice Boltzmann Method (D2Q9) with a double distribution function for thermal coupling. The Rayleigh number controls buoyancy strength; the Prandtl number sets the ratio of momentum to thermal diffusivity. Convection cells emerge spontaneously from tiny perturbations.',
            params: [
              { id: 'rayleighExp', label: 'Rayleigh Number (10^x)', min: 10, max: 20, step: 0.5, default: 13, format: 'rayleigh' },
              { id: 'prandtlNumber', label: 'Prandtl Number', min: 0.5, max: 7.0, step: 0.5, default: 1.0 },
              { id: 'stepsPerFrame', label: 'Simulation Speed', min: 1, max: 20, step: 1, default: 5 }
            ],
            legend: [
              { color: 'rgb(255, 60, 30)', label: 'Hot fluid (T=1)' },
              { color: 'rgb(30, 60, 255)', label: 'Cool fluid (T=0)' },
              { color: 'rgba(255, 255, 255, 0.5)', label: 'Velocity vectors' }
            ]
          },
          'coriolis': {
            name: 'Coriolis Effect',
            description: 'Shows how rotation deflects moving fluid. Critical for understanding atmospheric and oceanic circulation patterns.',
            concept: 'Particles deflect to the right in the Northern Hemisphere and to the left in the Southern Hemisphere. This is why hurricanes rotate counterclockwise in the north!',
            params: [
              { id: 'rotationRate', label: 'Rotation Rate', min: 0, max: 1, step: 0.1, default: 0.5 },
              { id: 'initialSpeed', label: 'Initial Speed', min: 0, max: 1, step: 0.1, default: 0.5 }
            ],
            legend: [
              { color: 'rgb(0, 255, 255)', label: 'Particle trails' },
              { color: 'rgba(100, 100, 100, 0.5)', label: 'Rotating reference frame' }
            ]
          },
          'geostrophic': {
            name: 'Geostrophic Balance',
            description: 'Balance between pressure gradient and Coriolis force. Fundamental to large-scale ocean and atmospheric currents.',
            concept: 'Wind flows parallel to pressure contours (isobars), not from high to low pressure, due to the balance between pressure gradient force and Coriolis force.',
            params: [
              { id: 'pressureGradient', label: 'Pressure Gradient', min: 0, max: 1, step: 0.1, default: 0.5 },
              { id: 'coriolisParameter', label: 'Coriolis Parameter', min: 0, max: 1, step: 0.1, default: 0.5 }
            ],
            legend: [
              { color: 'rgb(200, 100, 0)', label: 'High pressure' },
              { color: 'rgb(0, 100, 200)', label: 'Low pressure' },
              { color: 'white', label: 'Geostrophic wind' }
            ]
          },
          'stratified': {
            name: 'Stratified Flow',
            description: 'Layers of fluid with different densities. Shows internal waves and mixing behavior.',
            concept: 'Different density layers resist mixing. Internal waves form at layer boundaries. Common in oceans (thermocline) and atmosphere (temperature inversions).',
            params: [
              { id: 'densityDifference', label: 'Density Stratification', min: 0, max: 1, step: 0.1, default: 0.5 },
              { id: 'flowSpeed', label: 'Flow Speed', min: 0, max: 1, step: 0.1, default: 0.5 }
            ],
            legend: [
              { color: 'rgb(50, 75, 200)', label: 'Dense (heavy) fluid' },
              { color: 'rgb(150, 175, 255)', label: 'Light fluid' },
              { color: 'rgba(255, 255, 255, 0.5)', label: 'Layer interfaces' }
            ]
          },
          'rossby': {
            name: 'Rossby Waves',
            description: 'Large-scale meandering patterns in atmosphere and ocean caused by rotation and latitude variations.',
            concept: 'Large-scale meanders in the jet stream caused by planetary rotation and latitude variations. These waves influence weather patterns and transport heat poleward.',
            params: [
              { id: 'wavelength', label: 'Wavelength', min: 0, max: 1, step: 0.1, default: 0.5 },
              { id: 'amplitude', label: 'Amplitude', min: 0, max: 1, step: 0.1, default: 0.5 }
            ],
            legend: [
              { color: 'rgb(0, 255, 255)', label: 'Jet stream path' },
              { color: 'rgb(255, 200, 0)', label: 'Air parcels' },
              { color: 'rgb(255, 100, 100)', label: 'High pressure (H)' },
              { color: 'rgb(100, 100, 255)', label: 'Low pressure (L)' }
            ]
          }
        };
        let simState = {};
        function init() {
          selectModel('rayleigh-benard');
        }
        function selectModel(modelId) {
          currentModel = modelId;
          const model = models[modelId];
          document.querySelectorAll('.gfd-nav-btn').forEach(btn => btn.classList.remove('active'));
          const buttons = document.querySelectorAll('.gfd-nav-btn');
          const modelKeys = Object.keys(models);
          buttons[modelKeys.indexOf(modelId)].classList.add('active');
          document.getElementById('model-title').textContent = model.name;
          document.getElementById('model-description').textContent = model.description;
          document.getElementById('concept-text').textContent = model.concept;
          params = {};
          const paramsHtml = model.params.map(p => {
            params[p.id] = p.default;
            const displayVal = p.format === 'rayleigh' ? formatRayleigh(p.default) : (Number.isInteger(p.default) ? p.default : p.default.toFixed(2));
            return '<div class="gfd-slider-group"><label class="gfd-slider-label">' + p.label + ': <span id="val-' + p.id + '">' + displayVal + '</span></label><input type="range" class="gfd-slider" id="param-' + p.id + '" min="' + p.min + '" max="' + p.max + '" step="' + p.step + '" value="' + p.default + '" oninput="updateParam(\'' + p.id + '\', this.value, \'' + (p.format || '') + '\')"></div>';
          }).join('');
          document.getElementById('params-container').innerHTML = paramsHtml;
          const legendHtml = model.legend.map(item => '<div class="gfd-legend-item"><div class="gfd-legend-color" style="background: ' + item.color + '"></div><span class="gfd-legend-text">' + item.label + '</span></div>').join('');
          document.getElementById('legend-container').innerHTML = legendHtml;
          resetSimulation();
        }
        function formatRayleigh(exp) {
          if (Number.isInteger(exp)) return '10' + String(exp).split('').map(d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]).join('');
          return '10' + String(Math.floor(exp)).split('').map(d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]).join('') + '·⁵';
        }
        function updateParam(id, value, format) {
          params[id] = parseFloat(value);
          if (format === 'rayleigh') {
            document.getElementById('val-' + id).textContent = formatRayleigh(params[id]);
          } else {
            document.getElementById('val-' + id).textContent = Number.isInteger(params[id]) ? params[id] : params[id].toFixed(2);
          }
        }
        function togglePlay() {
          isPlaying = !isPlaying;
          document.getElementById('play-icon').textContent = isPlaying ? '⏸' : '▶';
          document.getElementById('play-text').textContent = isPlaying ? 'Pause' : 'Play';
        }
        function resetSimulation() {
          if (animationId) cancelAnimationFrame(animationId);
          initSimState();
          animate();
        }
        // ── LBM D2Q9 infrastructure ──
        const LBM_NX = 256, LBM_NY = 144, LBM_SIZE = LBM_NX * LBM_NY;
        const Q = 9;
        const ex = [0, 1, 0, -1, 0, 1, -1, -1, 1];
        const ey = [0, 0, 1, 0, -1, 1, 1, -1, -1];
        const w  = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36];
        const opp = [0, 3, 4, 1, 2, 7, 8, 5, 6];
        let lbm_f = new Float64Array(LBM_SIZE * Q);
        let lbm_fTemp = new Float64Array(LBM_SIZE * Q);
        let lbm_g = new Float64Array(LBM_SIZE * Q);
        let lbm_gTemp = new Float64Array(LBM_SIZE * Q);
        let lbm_rho = new Float64Array(LBM_SIZE);
        let lbm_ux = new Float64Array(LBM_SIZE);
        let lbm_uy = new Float64Array(LBM_SIZE);
        let lbm_T = new Float64Array(LBM_SIZE);
        let lbm_offCanvas = null;
        let lbm_imageData = null;
        function idx(x, y) { return y * LBM_NX + x; }
        function cidx(x, y, i) { return (y * LBM_NX + x) * Q + i; }
        function feq(i, rho, ux, uy) {
          const eu = ex[i] * ux + ey[i] * uy;
          const usq = ux * ux + uy * uy;
          return w[i] * rho * (1 + 3 * eu + 4.5 * eu * eu - 1.5 * usq);
        }
        function geq(i, T, ux, uy) {
          const eu = ex[i] * ux + ey[i] * uy;
          const usq = ux * ux + uy * uy;
          return w[i] * T * (1 + 3 * eu + 4.5 * eu * eu - 1.5 * usq);
        }
        function initLBM() {
          if (!lbm_offCanvas) {
            lbm_offCanvas = document.createElement('canvas');
            lbm_offCanvas.width = LBM_NX;
            lbm_offCanvas.height = LBM_NY;
            lbm_imageData = lbm_offCanvas.getContext('2d').createImageData(LBM_NX, LBM_NY);
          }
          for (let y = 0; y < LBM_NY; y++) {
            for (let x = 0; x < LBM_NX; x++) {
              const n = idx(x, y);
              const T0 = 1.0 - y / (LBM_NY - 1) + (Math.random() - 0.5) * 0.01;
              lbm_T[n] = T0;
              lbm_rho[n] = 1.0;
              lbm_ux[n] = 0;
              lbm_uy[n] = 0;
              for (let i = 0; i < Q; i++) {
                lbm_f[cidx(x, y, i)] = feq(i, 1.0, 0, 0);
                lbm_g[cidx(x, y, i)] = geq(i, T0, 0, 0);
              }
            }
          }
        }
        function lbmStep(tau_f, tau_g, g_beta) {
          // Macroscopic quantities
          for (let y = 0; y < LBM_NY; y++) {
            for (let x = 0; x < LBM_NX; x++) {
              const n = idx(x, y);
              let r = 0, vx = 0, vy = 0, t = 0;
              for (let i = 0; i < Q; i++) {
                const fi = lbm_f[cidx(x, y, i)];
                const gi = lbm_g[cidx(x, y, i)];
                r += fi;
                vx += fi * ex[i];
                vy += fi * ey[i];
                t += gi;
              }
              // Guo force correction: add half-force to velocity
              const Fy = g_beta * (t - 0.5);
              vx /= r;
              vy = vy / r + Fy * 0.5 / r;
              lbm_rho[n] = r;
              lbm_ux[n] = vx;
              lbm_uy[n] = vy;
              lbm_T[n] = t;
            }
          }
          // Collision
          for (let y = 0; y < LBM_NY; y++) {
            for (let x = 0; x < LBM_NX; x++) {
              const n = idx(x, y);
              const r = lbm_rho[n], vx = lbm_ux[n], vy = lbm_uy[n], t = lbm_T[n];
              const Fy = g_beta * (t - 0.5);
              for (let i = 0; i < Q; i++) {
                const c = cidx(x, y, i);
                // Guo forcing term
                const eu = ex[i] * vx + ey[i] * vy;
                const Si = (1 - 0.5 / tau_f) * w[i] * (3 * (ey[i] - vy) + 9 * eu * ey[i]) * Fy;
                lbm_fTemp[c] = lbm_f[c] - (lbm_f[c] - feq(i, r, vx, vy)) / tau_f + Si;
                lbm_gTemp[c] = lbm_g[c] - (lbm_g[c] - geq(i, t, vx, vy)) / tau_g;
              }
            }
          }
          // Streaming with boundary conditions
          for (let y = 0; y < LBM_NY; y++) {
            for (let x = 0; x < LBM_NX; x++) {
              for (let i = 0; i < Q; i++) {
                // periodic in x
                let xn = (x + ex[i] + LBM_NX) % LBM_NX;
                let yn = y + ey[i];
                const cDst = cidx(x, y, i);
                if (yn < 0 || yn >= LBM_NY) {
                  // Bounce-back for flow
                  lbm_f[cidx(x, y, opp[i])] = lbm_fTemp[cDst];
                  // Anti-bounce-back for temperature (Dirichlet)
                  const Twall = (yn < 0) ? 1.0 : 0.0; // bottom hot, top cold
                  lbm_g[cidx(x, y, opp[i])] = -lbm_gTemp[cDst] + 2 * w[opp[i]] * Twall;
                } else {
                  lbm_f[cidx(xn, yn, i)] = lbm_fTemp[cDst];
                  lbm_g[cidx(xn, yn, i)] = lbm_gTemp[cDst];
                }
              }
            }
          }
        }
        function tempToColor(t) {
          // blue -> white -> red
          t = t < 0 ? 0 : (t > 1 ? 1 : t);
          let r, g, b;
          if (t < 0.5) {
            const s = t * 2;
            r = Math.floor(s * 255);
            g = Math.floor(s * 255);
            b = 255;
          } else {
            const s = (t - 0.5) * 2;
            r = 255;
            g = Math.floor((1 - s) * 255);
            b = Math.floor((1 - s) * 255);
          }
          return [r, g, b];
        }
        function initSimState() {
          const canvas = document.getElementById('gfd-canvas');
          const width = canvas.width;
          const height = canvas.height;
          if (currentModel === 'rayleigh-benard') {
            initLBM();
            simState = { frameCount: 0 };
          } else if (currentModel === 'coriolis') {
            const particles = [];
            for (let i = 0; i < 8; i++) particles.push(createCoriolisParticle(width, height));
            simState = { particles, angle: 0 };
          } else if (currentModel === 'geostrophic') {
            simState = { time: 0 };
          } else if (currentModel === 'stratified') {
            const layers = 5, layerHeight = height / layers, particles = [];
            for (let layer = 0; layer < layers; layer++) {
              const density = 1 - (layer / layers) * 0.5;
              const speed = 0.5 * (1 + layer * 0.2);
              for (let i = 0; i < 30; i++) {
                particles.push({ x: Math.random() * width, y: layer * layerHeight + Math.random() * layerHeight, layer, density, speed, baseY: layer * layerHeight + layerHeight / 2 });
              }
            }
            simState = { particles, layers, time: 0 };
          } else if (currentModel === 'rossby') {
            const particles = [];
            for (let i = 0; i < 100; i++) particles.push({ x: Math.random() * width, phase: Math.random() * Math.PI * 2 });
            simState = { particles, time: 0, jetStreamY: height / 2 };
          }
        }
        function createCoriolisParticle(width, height) {
          const centerX = width / 2, centerY = height / 2;
          const angleOffset = Math.random() * Math.PI * 2;
          return { x: centerX, y: centerY, vx: Math.cos(angleOffset) * params.initialSpeed * 3, vy: Math.sin(angleOffset) * params.initialSpeed * 3, trail: [] };
        }
        function animate() {
          if (isPlaying) update();
          draw();
          animationId = requestAnimationFrame(animate);
        }
        function update() {
          const canvas = document.getElementById('gfd-canvas');
          const width = canvas.width, height = canvas.height;
          if (currentModel === 'rayleigh-benard') {
            const logRa = params.rayleighExp;  // 3 to 13
            const Pr = params.prandtlNumber;
            // Map log Ra [3,13] to effective g_beta [1e-5, 1e-3] for stable simulation
            const nu = 0.1;
            const kappa = nu / Pr;
            const tau_f = 3 * nu + 0.5;
            const tau_g = 3 * kappa + 0.5;
            const g_beta = 1e-5 * Math.pow(10, (logRa - 10) * 0.2);
            const steps = Math.round(params.stepsPerFrame);
            for (let s = 0; s < steps; s++) {
              lbmStep(tau_f, tau_g, g_beta);
            }
            simState.frameCount++;
          } else if (currentModel === 'coriolis') {
            const centerX = width / 2, centerY = height / 2;
            simState.angle += params.rotationRate * 0.02;
            simState.particles.forEach(p => {
              const coriolisX = -p.vy * params.rotationRate * 0.1;
              const coriolisY = p.vx * params.rotationRate * 0.1;
              p.vx += coriolisX; p.vy += coriolisY;
              p.x += p.vx; p.y += p.vy;
              p.trail.push({ x: p.x, y: p.y });
              if (p.trail.length > 100) p.trail.shift();
              const dist = Math.sqrt((p.x - centerX) ** 2 + (p.y - centerY) ** 2);
              if (dist > Math.min(width, height) / 2 || p.trail.length > 95) Object.assign(p, createCoriolisParticle(width, height));
            });
          } else if (currentModel === 'geostrophic') {
            simState.time += 0.02;
          } else if (currentModel === 'stratified') {
            simState.time += 0.02;
            simState.particles.forEach(p => {
              p.x += p.speed * params.flowSpeed;
              if (p.x > width) p.x = 0;
              const waveAmp = 10 * (1 - params.densityDifference);
              p.y = p.baseY + Math.sin(p.x * 0.02 + simState.time + p.layer) * waveAmp;
            });
          } else if (currentModel === 'rossby') {
            simState.time += 0.02;
            simState.particles.forEach(p => { p.x += 2; if (p.x > width) p.x = 0; });
          }
        }
        function draw() {
          const canvas = document.getElementById('gfd-canvas');
          const ctx = canvas.getContext('2d');
          const width = canvas.width, height = canvas.height;
          ctx.fillStyle = '#000';
          ctx.fillRect(0, 0, width, height);
          if (currentModel === 'rayleigh-benard') {
            const data = lbm_imageData.data;
            for (let y = 0; y < LBM_NY; y++) {
              for (let x = 0; x < LBM_NX; x++) {
                const n = idx(x, y);
                const [r, g, b] = tempToColor(lbm_T[n]);
                const p = (y * LBM_NX + x) * 4;
                data[p] = r; data[p + 1] = g; data[p + 2] = b; data[p + 3] = 255;
              }
            }
            const offCtx = lbm_offCanvas.getContext('2d');
            offCtx.putImageData(lbm_imageData, 0, 0);
            ctx.imageSmoothingEnabled = true;
            ctx.drawImage(lbm_offCanvas, 0, 0, width, height);
            // Velocity vectors every 3rd frame
            if (simState.frameCount % 3 === 0) {
              ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
              ctx.lineWidth = 1;
              const sx = width / LBM_NX, sy = height / LBM_NY;
              for (let y = 5; y < LBM_NY; y += 10) {
                for (let x = 5; x < LBM_NX; x += 10) {
                  const n = idx(x, y);
                  const vx = lbm_ux[n], vy = lbm_uy[n];
                  const mag = Math.sqrt(vx * vx + vy * vy);
                  if (mag < 1e-6) continue;
                  const scale = 800;
                  const px = (x + 0.5) * sx, py = (y + 0.5) * sy;
                  ctx.beginPath();
                  ctx.moveTo(px, py);
                  ctx.lineTo(px + vx * scale, py + vy * scale);
                  ctx.stroke();
                }
              }
            }
          } else if (currentModel === 'coriolis') {
            const centerX = width / 2, centerY = height / 2;
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, width, height);
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(simState.angle);
            ctx.strokeStyle = 'rgba(100, 100, 100, 0.3)';
            ctx.lineWidth = 1;
            for (let i = -400; i <= 400; i += 50) {
              ctx.beginPath(); ctx.moveTo(i, -400); ctx.lineTo(i, 400); ctx.stroke();
              ctx.beginPath(); ctx.moveTo(-400, i); ctx.lineTo(400, i); ctx.stroke();
            }
            ctx.restore();
            simState.particles.forEach(p => {
              ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)'; ctx.lineWidth = 2;
              ctx.beginPath();
              p.trail.forEach((pt, i) => { if (i === 0) ctx.moveTo(pt.x, pt.y); else ctx.lineTo(pt.x, pt.y); });
              ctx.stroke();
              ctx.fillStyle = 'rgb(0, 255, 255)';
              ctx.beginPath(); ctx.arc(p.x, p.y, 4, 0, Math.PI * 2); ctx.fill();
            });
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.beginPath(); ctx.arc(centerX, centerY, 8, 0, Math.PI * 2); ctx.fill();
          } else if (currentModel === 'geostrophic') {
            const gridSize = 40, cellWidth = width / gridSize, cellHeight = height / gridSize, time = simState.time;
            for (let y = 0; y < gridSize; y++) {
              for (let x = 0; x < gridSize; x++) {
                const pressure = Math.sin(x * 0.3 * params.pressureGradient + time) * Math.cos(y * 0.3 * params.pressureGradient);
                const intensity = (pressure + 1) / 2;
                const r = Math.floor(intensity * 200), g = Math.floor(intensity * 100), b = Math.floor((1 - intensity) * 200);
                ctx.fillStyle = 'rgb(' + r + ', ' + g + ', ' + b + ')';
                ctx.fillRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
              }
            }
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)'; ctx.fillStyle = 'white'; ctx.lineWidth = 2;
            for (let y = 2; y < gridSize - 2; y += 2) {
              for (let x = 2; x < gridSize - 2; x += 2) {
                const px = (x + 0.5) * cellWidth, py = (y + 0.5) * cellHeight;
                const gradX = Math.cos(x * 0.3 * params.pressureGradient + time) * 0.3 * params.pressureGradient;
                const gradY = -Math.sin(y * 0.3 * params.pressureGradient) * 0.3 * params.pressureGradient;
                const windX = -gradY * params.coriolisParameter * 20, windY = gradX * params.coriolisParameter * 20;
                ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + windX, py + windY); ctx.stroke();
                const angle = Math.atan2(windY, windX);
                ctx.beginPath();
                ctx.moveTo(px + windX, py + windY);
                ctx.lineTo(px + windX - 8 * Math.cos(angle - 0.5), py + windY - 8 * Math.sin(angle - 0.5));
                ctx.lineTo(px + windX - 8 * Math.cos(angle + 0.5), py + windY - 8 * Math.sin(angle + 0.5));
                ctx.closePath(); ctx.fill();
              }
            }
          } else if (currentModel === 'stratified') {
            const { particles, layers, time } = simState, layerHeight = height / layers;
            for (let layer = 0; layer < layers; layer++) {
              const density = 1 - (layer / layers) * params.densityDifference;
              const brightness = Math.floor(density * 150 + 50);
              ctx.fillStyle = 'rgb(' + (brightness * 0.3) + ', ' + (brightness * 0.5) + ', ' + brightness + ')';
              ctx.fillRect(0, layer * layerHeight, width, layerHeight);
            }
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)'; ctx.lineWidth = 2;
            for (let layer = 1; layer < layers; layer++) {
              ctx.beginPath();
              for (let x = 0; x < width; x += 5) {
                const wave = Math.sin(x * 0.02 + time + layer) * 10 * (1 - params.densityDifference);
                const y = layer * layerHeight + wave;
                if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
              }
              ctx.stroke();
            }
            particles.forEach(p => {
              const brightness = Math.floor(p.density * 200 + 55);
              ctx.fillStyle = 'rgba(' + brightness + ', ' + (brightness + 50) + ', 255, 0.8)';
              ctx.beginPath(); ctx.arc(p.x, p.y, 3, 0, Math.PI * 2); ctx.fill();
            });
            ctx.fillStyle = 'white'; ctx.font = '14px sans-serif';
            ctx.fillText('Less Dense (lighter)', 10, 25);
            ctx.fillText('More Dense (heavier)', 10, height - 10);
          } else if (currentModel === 'rossby') {
            const { particles, time, jetStreamY } = simState;
            ctx.strokeStyle = 'rgba(100, 100, 100, 0.3)'; ctx.lineWidth = 1;
            for (let y = 0; y < height; y += height / 8) {
              ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
            }
            const getWaveY = (x) => { const k = (1 - params.wavelength) * 0.05 + 0.01; return jetStreamY + Math.sin(k * x - time) * params.amplitude * 150; };
            ctx.strokeStyle = 'rgba(0, 255, 255, 0.8)'; ctx.lineWidth = 4;
            ctx.beginPath();
            for (let x = 0; x <= width; x += 5) { const y = getWaveY(x); if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }
            ctx.stroke();
            ctx.fillStyle = 'rgba(0, 255, 255, 0.1)';
            ctx.beginPath(); ctx.moveTo(0, jetStreamY);
            for (let x = 0; x <= width; x += 5) ctx.lineTo(x, getWaveY(x));
            ctx.lineTo(width, jetStreamY); ctx.closePath(); ctx.fill();
            particles.forEach(p => {
              ctx.fillStyle = 'rgba(255, 200, 0, 0.8)';
              ctx.beginPath(); ctx.arc(p.x, getWaveY(p.x), 3, 0, Math.PI * 2); ctx.fill();
            });
            ctx.fillStyle = 'white'; ctx.font = '14px sans-serif';
            ctx.fillText('North', 10, 25); ctx.fillText('South', 10, height - 10);
            ctx.fillText('Jet Stream Meanders →', width - 200, 25);
            const waveLength = Math.PI * 2 / ((1 - params.wavelength) * 0.05 + 0.01);
            for (let i = 0; i < 3; i++) {
              const x = (i * waveLength + time * 40) % width;
              ctx.fillStyle = 'rgba(255, 100, 100, 0.3)';
              ctx.beginPath(); ctx.arc(x, getWaveY(x), 40, 0, Math.PI * 2); ctx.fill();
              ctx.fillStyle = 'white'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
              ctx.fillText('H', x, getWaveY(x) + 5);
              const x2 = (x + waveLength / 2) % width;
              ctx.fillStyle = 'rgba(100, 100, 255, 0.3)';
              ctx.beginPath(); ctx.arc(x2, getWaveY(x2), 40, 0, Math.PI * 2); ctx.fill();
              ctx.fillStyle = 'white'; ctx.fillText('L', x2, getWaveY(x2) + 5);
            }
            ctx.textAlign = 'left';
          }
        }
        document.addEventListener('DOMContentLoaded', init);
        if (document.readyState !== 'loading') init();
        </script>
    design:
      spacing:
        padding: ["0", "0", "0", "0"]
---
