import marimo

__generated_with = "0.19.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Two-Dimensional Navier–Stokes
    ## An Interactive GFD Tutorial

    This notebook introduces **2D turbulence**. The solver is implemented here in NumPy so it runs in your browser.

    > **How to use:** Read the theory below, choose a scenario, press **▶ Run Simulation**,
    > then explore the results interactively.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 1 · Governing Equations

    We track the **vorticity** $\zeta = \partial_x v - \partial_y u$
    (the curl of the 2D velocity field). Its evolution is:

    $$\partial_t \zeta + J(\psi,\zeta)
    = -\nu(-\nabla^2)^{n_{\nu}}\zeta + F$$

    where $J(\psi,\zeta)$ is the advection term (Jacobian),
    $\nu$ is viscosity, $n_{\nu}$ its order, and $F$ is external forcing.

    **Streamfunction** $\psi$ relates to vorticity via the Poisson equation:

    $$\nabla^2\psi = -\zeta \qquad\Longrightarrow\qquad
    \hat{\psi}_{\mathbf{k}} = \frac{\hat{\zeta}_{\mathbf{k}}}{|\mathbf{k}|^2}$$

    **Velocity** is recovered from $\psi$:

    $$(u,v) = \left(-\partial_y\psi,\;\partial_x\psi\right)$$

    **Jacobian** (advection) in physical space:

    $$J(\psi,\zeta) = \frac{\partial\psi}{\partial x}\frac{\partial\zeta}{\partial y} - \frac{\partial\psi}{\partial y}\frac{\partial\zeta}{\partial x} = u\,\partial_x\zeta + v\,\partial_y\zeta$$

    | Parameter | Symbol | Role |
    |-----------|--------|------|
    | Kinematic viscosity | $\nu$ | Damps small-scale motion |
    | Viscosity order | $n_\nu \geq 1$ | $n_\nu=1$ is regular viscosity; $n_\nu>1$ is *hyperviscosity* |
    | Forcing | $F(x,y,t)$ | Energy injection (zero in decaying runs) |
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Pseudo-Spectral Method

    All spatial derivatives are computed **exactly in Fourier space**:

    $$\partial_x \;\longleftrightarrow\; i k_x, \qquad
      \partial_y \;\longleftrightarrow\; i k_y$$

    The full equation in spectral space:

    $$\partial_t \hat{\zeta}_{\mathbf{k}} = -\widehat{J(\psi,\zeta)}_{\mathbf{k}} - \nu|\mathbf{k}|^{2n_{\nu}}\hat{\zeta}_{\mathbf{k}} + \hat{F}_{\mathbf{k}}$$

    The first term is computed in physical space (inverse FFT, multiply, forward FFT);
    the second is applied directly in spectral space.

    **Time integration:** 4th-order Runge–Kutta (RK4).

    **Dealiasing (Orszag 2/3 rule):** All modes with
    $|\mathbf{k}| > \frac{2}{3}k_{\max}$ are zeroed after every step.
    This prevents nonlinear aliasing and stabilises the simulation
    even with $\nu = 0$.

    **Diagnostics** (domain-averaged):

    $$E = \frac{1}{2}\langle|\nabla\psi|^2\rangle
        = \sum_{\mathbf{k}}\tfrac{1}{2}|\mathbf{k}|^2|\hat\psi_{\mathbf{k}}|^2,
    \qquad
    Z = \frac{1}{2}\langle\zeta^2\rangle
        = \sum_{\mathbf{k}}\tfrac{1}{2}|\hat\zeta_{\mathbf{k}}|^2$$

    In freely decaying flow (no forcing, no viscosity), both $E$ and $Z$
    are **conserved invariants**. Any decay you observe is solely from the
    dealiasing filter acting at the grid scale.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Choose a Scenario & Parameters

    Select a preset or customise the sliders below.
    The **decaying** case follows [McWilliams (1984)](https://doi.org/10.1017/S0022112084001750),
    the landmark paper that characterised 2D turbulence.
    """)
    return


@app.cell
def _(mo):
    scenario = mo.ui.dropdown(
        options={
            "Decaying turbulence (McWilliams 1984)": "decay",
            "Hyperviscosity (n=2) — sharper cascade": "hyper",
            "High-wavenumber initial energy": "highk",
        },
        value="Decaying turbulence (McWilliams 1984)",
        label="Preset scenario",
    )
    scenario
    return (scenario,)


@app.cell
def _(mo, scenario):
    _presets = {
        "decay": dict(n=128, dt=0.01, nsteps=2000, k0=6,  nu=0.0,   nnu=1),
        "hyper": dict(n=128, dt=0.01, nsteps=2000, k0=6,  nu=1e-8,  nnu=2),
        "highk": dict(n=128, dt=0.01, nsteps=2000, k0=14, nu=0.0,   nnu=1),
    }
    _p = _presets[scenario.value]

    n_slider = mo.ui.slider(32, 256, step=32, value=_p["n"],
                            label="Grid $n$", show_value=True)
    dt_slider = mo.ui.slider(0.002, 0.02, step=0.002, value=_p["dt"],
                             label="Time step $\\Delta t$", show_value=True)
    nsteps_slider = mo.ui.slider(500, 5000, step=500, value=_p["nsteps"],
                                 label="Steps", show_value=True)
    k0_slider = mo.ui.slider(2, 20, step=1, value=_p["k0"],
                             label="Peak wavenumber $k_0$", show_value=True)
    nu_slider = mo.ui.slider(0.0, 1e-6, step=1e-7, value=_p["nu"],
                             label="Viscosity $\\nu$", show_value=True)
    nnu_slider = mo.ui.slider(1, 4, step=1, value=_p["nnu"],
                              label="Viscosity order $n_\\nu$", show_value=True)

    mo.vstack([
        mo.hstack([n_slider, dt_slider, nsteps_slider], justify="start"),
        mo.hstack([k0_slider, nu_slider, nnu_slider], justify="start"),
        mo.md(r"""
        > **Tip for browser/WASM:** keep $n \leq 64$ and steps $\leq 1000$ for fast runs.
        > A $128\times128$ grid with 2000 steps takes ~15 s locally.
        """),
    ])
    return dt_slider, k0_slider, n_slider, nnu_slider, nsteps_slider, nu_slider


@app.cell
def _(mo):
    # Persistent state — survives run_btn resetting to False
    get_sim, set_sim = mo.state(None)
    return get_sim, set_sim


@app.cell
def _(mo):
    run_btn = mo.ui.run_button(label="▶  Run Simulation")
    run_btn
    return (run_btn,)


@app.cell
def _(
    dt_slider,
    k0_slider,
    mo,
    n_slider,
    nnu_slider,
    nsteps_slider,
    nu_slider,
    run_btn,
    set_sim,
):
    mo.stop(not run_btn.value, mo.callout(
        mo.md("Press **▶ Run Simulation** above to start."), kind="info"
    ))

    import numpy as _np

    _n      = n_slider.value
    _L      = 2 * _np.pi
    _dt     = dt_slider.value
    _nsteps = nsteps_slider.value
    _nsubs  = max(1, _nsteps // 120)   # ~120 saved frames
    _k0     = k0_slider.value
    _nu     = nu_slider.value
    _nnu    = nnu_slider.value
    _E0     = 0.5

    # ── Grid & wavenumbers ──────────────────────────────────────────────────
    _x  = _np.linspace(0, _L, _n, endpoint=False)
    _y  = _np.linspace(0, _L, _n, endpoint=False)
    _kx = _np.fft.rfftfreq(_n) * _n * (2 * _np.pi / _L)
    _ky = _np.fft.fftfreq(_n)  * _n * (2 * _np.pi / _L)
    _KX, _KY = _np.meshgrid(_kx, _ky)
    _Ksq   = _KX**2 + _KY**2
    _invKsq = _np.where(_Ksq == 0, 0.0, 1.0 / _np.where(_Ksq == 0, 1.0, _Ksq))

    # ── Orszag 2/3 dealiasing filter ────────────────────────────────────────
    _kmax = (_n // 2) * (2 * _np.pi / _L)
    _filt = (_np.sqrt(_Ksq) <= (2.0 / 3.0) * _kmax).astype(float)

    # ── Linear operator (viscosity) ─────────────────────────────────────────
    _L_op = -_nu * _Ksq**_nnu

    # ── Initial condition: peaked isotropic spectrum (McWilliams 1984) ──────
    _rng    = _np.random.default_rng(1234)
    _K      = _np.sqrt(_Ksq)
    _Ks     = _np.where(_K == 0, 1e-10, _K)
    _amp    = _Ks * _np.sqrt(1.0 / (1.0 + (_Ks / _k0)**4))
    _phase  = 2 * _np.pi * _rng.random((_n, _n // 2 + 1))
    _zeta_h = _filt * _amp * _np.exp(1j * _phase)
    _ph0    = -_invKsq * _zeta_h
    _u0     = _np.fft.irfft2(-1j * _KY * _ph0)
    _v0     = _np.fft.irfft2( 1j * _KX * _ph0)
    _Einit  = 0.5 * _np.mean(_u0**2 + _v0**2)
    if _Einit > 0:
        _zeta_h *= _np.sqrt(_E0 / _Einit)

    # ── Nonlinear term  N(ζ) = −J(ψ,ζ) ────────────────────────────────────
    def _N(zh):
        ph  = -_invKsq * zh
        u   = _np.fft.irfft2(-1j * _KY * ph)
        v   = _np.fft.irfft2( 1j * _KX * ph)
        dzx = _np.fft.irfft2(1j * _KX * zh)
        dzy = _np.fft.irfft2(1j * _KY * zh)
        return -_np.fft.rfft2(u * dzx + v * dzy)

    # ── Filtered RK4 step ───────────────────────────────────────────────────
    def _step(zh):
        def rhs(z): return _L_op * z + _N(z)
        k1 = rhs(zh)
        k2 = rhs(zh + 0.5 * _dt * k1)
        k3 = rhs(zh + 0.5 * _dt * k2)
        k4 = rhs(zh + _dt * k3)
        return _filt * (zh + (_dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4))

    # ── Diagnostics ─────────────────────────────────────────────────────────
    def _E(zh):
        ph = -_invKsq * zh
        u  = _np.fft.irfft2(-1j * _KY * ph)
        v  = _np.fft.irfft2( 1j * _KX * ph)
        return float(0.5 * _np.mean(u**2 + v**2))

    def _Z(zh):
        return float(0.5 * _np.mean(_np.fft.irfft2(zh)**2))

    # ── Time-stepping loop ──────────────────────────────────────────────────
    _t_hist, _E_hist, _Z_hist, _snaps = [], [], [], []
    _t = 0.0
    for _s in range(_nsteps + 1):
        if _s % _nsubs == 0:
            _t_hist.append(_t)
            _E_hist.append(_E(_zeta_h))
            _Z_hist.append(_Z(_zeta_h))
            _snaps.append(_np.fft.irfft2(_zeta_h).copy())
        if _s < _nsteps:
            _zeta_h = _step(_zeta_h)
            _t += _dt

    set_sim({
        "snaps":  _snaps,
        "t_hist": _np.array(_t_hist),
        "E_hist": _np.array(_E_hist),
        "Z_hist": _np.array(_Z_hist),
        "n": _n, "L": _L, "x": _x, "y": _y,
    })

    mo.callout(
        mo.md(f"**Done.** {_nsteps} steps on a {_n}×{_n} grid · {len(_snaps)} snapshots saved."),
        kind="success",
    )
    return


@app.cell
def _(get_sim, mo):
    import numpy as np

    _sim = get_sim()
    mo.stop(_sim is None, mo.callout(
        mo.md("Results will appear here once the simulation has run."), kind="warn"
    ))

    snaps  = _sim["snaps"]
    t_hist = _sim["t_hist"]
    E_hist = _sim["E_hist"]
    Z_hist = _sim["Z_hist"]
    sim_n  = _sim["n"]
    sim_L  = _sim["L"]
    return E_hist, Z_hist, np, sim_L, sim_n, snaps, t_hist


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 4 · Results

    ### Overview: Initial & Final Vorticity
    """)
    return


@app.cell
def _(E_hist, Z_hist, np, snaps, t_hist):
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as _gs
    from matplotlib.colors import TwoSlopeNorm as _TSN

    _vmax = float(np.percentile(np.abs(snaps[0]), 99.5)) or 1.0
    _norm = _TSN(vmin=-_vmax, vcenter=0, vmax=_vmax)

    _fig = plt.figure(figsize=(13, 4.5))
    _gs0 = _gs.GridSpec(1, 3, figure=_fig, wspace=0.35)

    # Initial vorticity
    _ax0 = _fig.add_subplot(_gs0[0])
    _ax0.imshow(snaps[0], origin="lower", cmap="RdBu_r", norm=_norm,
                extent=[0, 2*np.pi, 0, 2*np.pi])
    _ax0.set_title(f"Initial  ($t={t_hist[0]:.1f}$)", fontsize=11)
    _ax0.set_xlabel("$x$"); _ax0.set_ylabel("$y$")

    # Final vorticity
    _ax1 = _fig.add_subplot(_gs0[1])
    _im1 = _ax1.imshow(snaps[-1], origin="lower", cmap="RdBu_r", norm=_norm,
                       extent=[0, 2*np.pi, 0, 2*np.pi])
    _ax1.set_title(f"Final  ($t={t_hist[-1]:.1f}$)", fontsize=11)
    _ax1.set_xlabel("$x$")
    plt.colorbar(_im1, ax=_ax1, label="$\\zeta$", fraction=0.046)

    # Energy & Enstrophy
    _ax2 = _fig.add_subplot(_gs0[2])
    _ax2.plot(t_hist, E_hist / E_hist[0], lw=2, label="$E/E_0$")
    _ax2.plot(t_hist, Z_hist / Z_hist[0], lw=2, color="crimson", label="$Z/Z_0$")
    _ax2.set_xlabel("$t$"); _ax2.set_ylabel("Normalized")
    _ax2.set_title("Energy & Enstrophy", fontsize=11)
    _ax2.legend(fontsize=10); _ax2.set_ylim(0, 1.15)
    _ax2.grid(True, alpha=0.3)

    plt.suptitle("2D Decaying Turbulence — Vorticity Field", fontsize=13, y=1.01)
    plt.tight_layout()
    _fig
    return (plt,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Animation of Vorticity Evolution

    The GIF below shows how vorticity evolves over time.
    Notice how small vortices **merge** into larger structures — this is the
    **inverse energy cascade**, a hallmark of 2D turbulence absent in 3D flows.
    """)
    return


@app.cell
def _(mo, np, plt, snaps, t_hist):
    import io as _io
    from PIL import Image as _Image

    _vmax_a = float(np.percentile(np.abs(snaps[0]), 99.5)) or 1.0

    # Subsample frames for a manageable GIF (max 40 frames)
    _step_gif = max(1, len(snaps) // 40)
    _frames_idx = list(range(0, len(snaps), _step_gif))

    _pil_frames = []
    for _fi in _frames_idx:
        _fig_g, _ax_g = plt.subplots(figsize=(4, 3.5), dpi=80)
        _im_g = _ax_g.imshow(
            snaps[_fi], origin="lower", cmap="RdBu_r",
            vmin=-_vmax_a, vmax=_vmax_a,
            extent=[0, 2*np.pi, 0, 2*np.pi],
        )
        _ax_g.set_title(f"$t = {t_hist[_fi]:.1f}$", fontsize=10)
        _ax_g.set_xlabel("$x$"); _ax_g.set_ylabel("$y$")
        plt.colorbar(_im_g, ax=_ax_g, label="$\\zeta$", fraction=0.046)
        plt.tight_layout()
        _buf = _io.BytesIO()
        _fig_g.savefig(_buf, format="png", dpi=80)
        plt.close(_fig_g)
        _buf.seek(0)
        _pil_frames.append(_Image.open(_buf).convert("RGB"))

    _gif_buf = _io.BytesIO()
    _pil_frames[0].save(
        _gif_buf, format="GIF",
        append_images=_pil_frames[1:],
        save_all=True, duration=120, loop=0,
    )
    _gif_buf.seek(0)

    mo.image(_gif_buf.read(), alt="Vorticity animation", width=420)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Interactive Snapshot Browser
    """)
    return


@app.cell
def _(mo, np, snaps):
    # Fixed colorscale across all snapshots
    _vmax_global = max(float(np.percentile(np.abs(snaps[0]), 99.5)), 1e-6)

    snap_slider = mo.ui.slider(
        start=0, stop=len(snaps) - 1, step=1, value=0,
        label="Time step", show_value=True,
    )
    return (snap_slider,)


@app.cell
def _(mo, np, snap_slider, snaps, t_hist):
    import matplotlib.pyplot as _plt2
    from matplotlib.colors import TwoSlopeNorm as _TSN2

    _idx  = snap_slider.value
    _snap = snaps[_idx]
    _vmax_global = max(float(np.percentile(np.abs(snaps[0]), 99.5)), 1e-6)

    _plt2.close("all")
    _fig3, _ax3 = _plt2.subplots(figsize=(5.5, 4.8))
    _im3 = _ax3.imshow(
        _snap, origin="lower", cmap="RdBu_r",
        norm=_TSN2(vmin=-_vmax_global, vcenter=0, vmax=_vmax_global),
        extent=[0, 2*np.pi, 0, 2*np.pi],
    )
    _ax3.set_title(f"Vorticity $\\zeta$ at $t = {t_hist[_idx]:.2f}$", fontsize=12)
    _ax3.set_xlabel("$x$"); _ax3.set_ylabel("$y$")
    _plt2.colorbar(_im3, ax=_ax3, label="$\\zeta$", fraction=0.046)
    _plt2.tight_layout()
    mo.vstack([snap_slider, _fig3])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ### Radial Energy Spectrum

    In the **enstrophy inertial range** of 2D turbulence, theory predicts a
    $k^{-3}$ energy spectrum (Kraichnan 1967). The **energy inertial range**
    (scales larger than the forcing scale) follows $k^{-5/3}$, but requires
    a forced run to observe clearly.
    """)
    return


@app.cell
def _(E_hist, Z_hist, sim_L, sim_n, snaps, t_hist):
    import numpy as _np3
    import matplotlib.pyplot as _plt3

    # Radial spectrum at initial and final times
    def _radial_spectrum(zeta, n, L):
        kx = _np3.fft.rfftfreq(n) * n * (2*_np3.pi/L)
        ky = _np3.fft.fftfreq(n)  * n * (2*_np3.pi/L)
        KX, KY = _np3.meshgrid(kx, ky)
        Ksq = KX**2 + KY**2
        invKsq = _np3.where(Ksq==0, 0.0, 1.0/_np3.where(Ksq==0,1.0,Ksq))
        zh  = _np3.fft.rfft2(zeta)
        ph  = -invKsq * zh
        E   = 0.5 * Ksq * _np3.abs(ph)**2 / n**2
        K   = _np3.sqrt(Ksq)
        k_bins = _np3.arange(1, n//2)
        Ek = _np3.array([E[(K>=k-0.5)&(K<k+0.5)].sum() for k in k_bins])
        return k_bins, Ek
    _k0_sp, _Ek0 = _radial_spectrum(snaps[0],  sim_n, sim_L)
    _kf_sp, _Ekf = _radial_spectrum(snaps[-1], sim_n, sim_L)

    _fig4, _axes4 = _plt3.subplots(1, 2, figsize=(13, 4.5))

    # Spectrum
    _axes4[0].loglog(_k0_sp, _Ek0, lw=2, alpha=0.6, label=f"$t={t_hist[0]:.1f}$ (initial)")
    _axes4[0].loglog(_kf_sp, _Ekf, lw=2, color="crimson", label=f"$t={t_hist[-1]:.1f}$ (final)")
    _kref = _np3.array([3, sim_n//4])
    _axes4[0].loglog(_kref, _Ekf[2]*(_kref/_kref[0])**(-3), "k--", lw=1.2, label="$k^{-3}$")
    _axes4[0].set_xlabel(r"$k_r$"); _axes4[0].set_ylabel(r"$E(k_r)$")
    _axes4[0].set_title("Radial Energy Spectrum", fontsize=12)
    _axes4[0].legend(fontsize=9); _axes4[0].grid(True, which="both", alpha=0.2)

    # E & Z log-scale time series
    _axes4[1].semilogy(t_hist, E_hist, lw=2, label="$E(t)$")
    _axes4[1].semilogy(t_hist, Z_hist, lw=2, color="crimson", label="$Z(t)$")
    _axes4[1].set_xlabel("$t$")
    _axes4[1].set_title("Energy & Enstrophy (log scale)", fontsize=12)
    _axes4[1].legend(fontsize=10); _axes4[1].grid(True, alpha=0.3)

    _plt3.tight_layout()
    _fig4
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Physical Interpretation

    ### Inverse Energy Cascade
    In **3D turbulence**, energy flows from large to small scales (Richardson cascade).
    In **2D turbulence**, the opposite happens: energy flows **upscale** (inverse cascade)
    while enstrophy cascades to small scales. This is why the vorticity animation shows
    small patches merging into large coherent vortices.

    ### Why does 2D turbulence behave differently?
    In 2D, vortex stretching — the mechanism that drives the 3D energy cascade — is absent.
    Two conservation laws operate simultaneously:

    | Conserved quantity | Consequence |
    |--------------------|-------------|
    | Energy $E$ | Cannot be destroyed, so it accumulates at large scales |
    | Enstrophy $Z$ | Acts as an additional constraint, forcing the upscale energy transfer |

    ### The $k^{-3}$ spectrum
    In the **enstrophy inertial range** ($k > k_0$), Kraichnan (1967) predicted:
    $$E(k) \propto k^{-3}$$
    The radial spectrum plot above should approach this slope at late times.

    ### Geophysical relevance
    Large-scale atmospheric and oceanic flows are approximately 2D
    (stratification + rotation suppress vertical motions).
    The inverse cascade explains why weather systems grow and why
    ocean eddies tend to aggregate into large gyres.
    """)
    return


if __name__ == "__main__":
    app.run()
