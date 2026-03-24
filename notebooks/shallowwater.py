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
    # Geostrophic Adjustment & the Shallow Water Model
    ## An Interactive GFD Tutorial

    This notebook solves the **linearised shallow water equations on a rotating
    beta-plane** and uses them to illustrate **geostrophic adjustment** — the
    fundamental process by which the atmosphere and ocean reach a state of
    balance between pressure gradients and the Coriolis force.

    A Gaussian height perturbation is released from rest. Two things happen
    simultaneously:
    - **Fast inertia-gravity waves** radiate outward at speed $c = \sqrt{gH}$
    - **Slower Rossby waves** drift westward, driven by the $\beta$-effect

    > **How to use:** Read the theory, adjust the sliders, then press
    > **▶ Run Simulation** to integrate the equations and generate the animation.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 1 · Physical Setup

    Consider a thin layer of fluid of mean depth $H$ on a rotating sphere.
    We work on a **beta-plane** centred at latitude $\phi_0$:

    $$f(y) = f_0 + \beta y, \qquad
      f_0 = 2\Omega\sin\phi_0, \qquad
      \beta = \frac{2\Omega\cos\phi_0}{a}$$

    where $\Omega$ is Earth's rotation rate and $a$ its radius.

    | Symbol | Typical value | Role |
    |--------|--------------|------|
    | $f_0$ | $10^{-4}$ s$^{-1}$ (45°N) | Background rotation |
    | $\beta$ | $1.6\times10^{-11}$ m$^{-1}$s$^{-1}$ | Planetary vorticity gradient |
    | $H$ | 500–5000 m | Mean layer depth |
    | $c = \sqrt{gH}$ | 70–200 m s$^{-1}$ | Gravity wave speed |
    | $L_R = c/f_0$ | 700–2000 km | **Rossby deformation radius** |

    $L_R$ is the most important scale in geophysical fluid dynamics:
    it separates the regime where **rotation dominates** (scales $\gg L_R$)
    from where **gravity dominates** (scales $\ll L_R$).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Linearised Shallow Water Equations

    Linearising about a state of rest $(\mathbf{u}=0,\, h=H)$:

    $$\frac{\partial u}{\partial t} - f v = -g\frac{\partial \eta}{\partial x}$$

    $$\frac{\partial v}{\partial t} + f u = -g\frac{\partial \eta}{\partial y}$$

    $$\frac{\partial \eta}{\partial t} + H\!\left(\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y}\right) = 0$$

    where $\eta$ is the free-surface height anomaly (positive = raised surface).

    **Non-dimensionalisation** with $L_R$, $f_0^{-1}$, $c = \sqrt{gH}$, and $H$:

    $$u_t - \hat f\, v = -\eta_x$$
    $$v_t + \hat f\, u = -\eta_y$$
    $$\eta_t + u_x + v_y = 0$$

    where $\hat f = 1 + \hat\beta\, y$ and $\hat\beta = \beta L_R / f_0$.
    For Earth at 45°N, $\hat\beta \approx 0.16$.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Wave Dispersion Relations

    Seeking plane-wave solutions $\sim e^{i(kx+ly-\omega t)}$ in the
    **f-plane** ($\beta=0$) gives three wave modes for each wavenumber $(k,l)$:

    **Geostrophic mode** ($\omega = 0$):
    $$u = -\frac{g}{f}\frac{\partial\eta}{\partial y}, \qquad v = \frac{g}{f}\frac{\partial\eta}{\partial x}$$
    This is the *steady balanced state* — the end-point of geostrophic adjustment.

    **Inertia-gravity modes** ($\omega = \pm\,\omega_{IG}$):
    $$\omega_{IG}^2 = f^2 + c^2(k^2 + l^2)$$
    Fast oscillations that carry energy outward from the perturbation.

    When $\beta \neq 0$, the geostrophic mode acquires a slow westward phase speed — **Rossby waves**:
    $$\omega_R = \frac{-\beta k}{k^2 + l^2 + L_R^{-2}}$$

    The negative sign means Rossby waves always propagate **westward**.
    """)
    return


@app.cell
def _(mo):
    import numpy as np
    import matplotlib.pyplot as plt

    _beta_hat = 0.16
    _k = np.linspace(0.05, 4, 300)
    _l = 0.0

    _omega_ig = np.sqrt(1.0 + _k**2 + _l**2)
    _omega_r  = -_beta_hat * _k / (_k**2 + _l**2 + 1.0)

    _fig, _axes = plt.subplots(1, 2, figsize=(11, 4))

    _axes[0].plot(_k, _omega_ig, lw=2, color="#2563eb", label="$\\omega_{IG}$ (inertia-gravity)")
    _axes[0].plot(_k, -_omega_ig, lw=2, color="#2563eb", ls="--", alpha=0.5)
    _axes[0].axhline(1, color="gray", lw=1, ls=":", label="$\\omega = f_0$ (inertial)")
    _axes[0].set_xlabel("Wavenumber $k$ ($L_R^{-1}$)")
    _axes[0].set_ylabel("Frequency $\\omega$ ($f_0$)")
    _axes[0].set_title("Inertia-gravity wave dispersion")
    _axes[0].legend(fontsize=9); _axes[0].grid(True, alpha=0.3)

    _axes[1].plot(_k, _omega_r, lw=2, color="crimson", label="$\\omega_R$ (Rossby, $l=0$)")
    _axes[1].fill_between(_k, _omega_r, 0, alpha=0.12, color="crimson")
    _axes[1].axhline(0, color="black", lw=0.8)
    _axes[1].set_xlabel("Wavenumber $k$ ($L_R^{-1}$)")
    _axes[1].set_ylabel("Frequency $\\omega$ ($f_0$)")
    _axes[1].set_title("Rossby wave dispersion ($\\hat\\beta=0.16$)")
    _axes[1].legend(fontsize=9); _axes[1].grid(True, alpha=0.3)
    _axes[1].annotate("Westward\npropagation", xy=(1.5, -0.025), fontsize=9,
                      color="crimson", ha="center")

    plt.tight_layout()
    _fig
    return np, plt


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 4 · Geostrophic Adjustment

    When an unbalanced perturbation is released, the system evolves toward a
    **geostrophically balanced state** in which Coriolis force and pressure
    gradient are in balance:

    $$f\,\mathbf{k}\times\mathbf{u}_g = -g\nabla\eta_g$$

    The **adjustment radius** determines how the final state is partitioned
    between velocity and height anomaly:

    - At scales $\ll L_R$: the height field adjusts toward the velocity field
    - At scales $\gg L_R$: the velocity field adjusts toward the height field

    Starting from $\eta = \eta_0 e^{-(r/\sigma)^2/2}$, $\mathbf{u}=0$, the
    geostrophically balanced final state is:

    $$\eta_\infty = \eta_0\left(1 - \frac{K_0(r/L_R)}{K_0(0)}\right) \times e^{-(r/\sigma)^2/2} \quad (\sigma \gg L_R)$$

    The gravity waves carry away the *imbalance*; what remains is balanced.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Interactive Simulation

    The solver uses a **pseudo-spectral method**:
    - Spatial derivatives via 2D FFT (exact for periodic domains)
    - Variable Coriolis $f(y) = f_0 + \beta y$ computed in physical space
    - **RK4** time integration

    Adjust the parameters below and press **▶ Run Simulation**.

    > **Browser tip:** use $n \leq 64$ for fast runs. $n = 128$ takes ~20 s locally.
    """)
    return


@app.cell
def _(mo):
    get_sw, set_sw = mo.state(None)
    return get_sw, set_sw


@app.cell
def _(mo):
    sw_n      = mo.ui.slider(32, 128, step=32, value=64,
                              label="Grid $n$", show_value=True)
    sw_beta   = mo.ui.slider(0.0, 0.5, step=0.02, value=0.16,
                              label="$\\hat\\beta$ (planetary vorticity gradient)",
                              show_value=True)
    sw_f0     = mo.ui.slider(0.5, 2.0, step=0.1, value=1.0,
                              label="$f_0$ (background rotation)", show_value=True)
    sw_sigma  = mo.ui.slider(0.5, 4.0, step=0.25, value=2.0,
                              label="Perturbation width $\\sigma/L_R$", show_value=True)
    sw_amp    = mo.ui.slider(0.1, 1.0, step=0.05, value=0.5,
                              label="Perturbation amplitude", show_value=True)
    sw_T      = mo.ui.slider(5, 50, step=5, value=30,
                              label="Run time ($f_0^{-1}$)", show_value=True)

    mo.vstack([
        mo.hstack([sw_n, sw_f0, sw_beta], justify="start"),
        mo.hstack([sw_sigma, sw_amp, sw_T], justify="start"),
    ])
    return sw_T, sw_amp, sw_beta, sw_f0, sw_n, sw_sigma


@app.cell
def _(mo):
    sw_btn = mo.ui.run_button(label="▶  Run Simulation")
    sw_btn
    return (sw_btn,)


@app.cell
def _(mo, np, set_sw, sw_T, sw_amp, sw_beta, sw_btn, sw_f0, sw_n, sw_sigma):
    mo.stop(not sw_btn.value, mo.callout(
        mo.md("Press **▶ Run Simulation** to integrate the equations."), kind="info"
    ))

    _n     = sw_n.value
    _beta  = sw_beta.value
    _f0    = sw_f0.value
    _sigma = sw_sigma.value
    _amp   = sw_amp.value
    _T     = sw_T.value

    # ── Non-dimensional domain: ±10 L_R in each direction ──────────────────
    _L  = 20.0      # domain size in L_R units
    _nx = _n
    _ny = _n
    _dx = _L / _nx
    _dy = _L / _ny

    _x = np.linspace(-_L/2, _L/2, _nx, endpoint=False)
    _y = np.linspace(-_L/2, _L/2, _ny, endpoint=False)
    _XX, _YY = np.meshgrid(_x, _y)    # shape (ny, nx)

    # ── Coriolis field f(y) ─────────────────────────────────────────────────
    _f = _f0 + _beta * _YY             # shape (ny, nx)

    # ── Wavenumbers for pseudo-spectral derivatives ─────────────────────────
    _kx = np.fft.rfftfreq(_nx, d=_dx / (2 * np.pi * _dx))   # = rfftfreq*2π/dx
    _ky = np.fft.fftfreq(_ny,  d=_dy / (2 * np.pi * _dy))
    # Simpler:
    _kx = np.fft.rfftfreq(_nx) * _nx * (2 * np.pi / _L)
    _ky = np.fft.fftfreq(_ny)  * _ny * (2 * np.pi / _L)
    _KX, _KY = np.meshgrid(_kx, _ky)   # shape (ny, nx//2+1)

    def _ddx(f2d):
        return np.fft.irfft2(1j * _KX * np.fft.rfft2(f2d), s=(_ny, _nx))

    def _ddy(f2d):
        return np.fft.irfft2(1j * _KY * np.fft.rfft2(f2d), s=(_ny, _nx))

    def _div(u2d, v2d):
        return _ddx(u2d) + _ddy(v2d)

    # ── RHS of linearised SWE ───────────────────────────────────────────────
    def _rhs(eta, u, v):
        deta_dt = -_div(u, v)
        du_dt   =  _f * v - _ddx(eta)
        dv_dt   = -_f * u - _ddy(eta)
        return deta_dt, du_dt, dv_dt

    # ── RK4 step ────────────────────────────────────────────────────────────
    def _rk4(eta, u, v, dt):
        k1e, k1u, k1v = _rhs(eta, u, v)
        k2e, k2u, k2v = _rhs(eta+0.5*dt*k1e, u+0.5*dt*k1u, v+0.5*dt*k1v)
        k3e, k3u, k3v = _rhs(eta+0.5*dt*k2e, u+0.5*dt*k2u, v+0.5*dt*k2v)
        k4e, k4u, k4v = _rhs(eta+dt*k3e,     u+dt*k3u,     v+dt*k3v)
        return (
            eta + (dt/6)*(k1e+2*k2e+2*k3e+k4e),
            u   + (dt/6)*(k1u+2*k2u+2*k3u+k4u),
            v   + (dt/6)*(k1v+2*k2v+2*k3v+k4v),
        )

    # ── Initial condition: Gaussian height perturbation ─────────────────────
    _eta = _amp * np.exp(-(_XX**2 + _YY**2) / (2 * _sigma**2))
    _u   = np.zeros((_ny, _nx))
    _v   = np.zeros((_ny, _nx))

    # ── CFL: gravity wave c=1, dt < dx ─────────────────────────────────────
    _dt     = 0.4 * _dx
    _nsteps = int(_T / _dt)
    _nsubs  = max(1, _nsteps // 80)     # ~80 frames

    _snaps_eta, _snaps_u, _snaps_v, _t_hist = [], [], [], []
    _t = 0.0
    for _s in range(_nsteps + 1):
        if _s % _nsubs == 0:
            _snaps_eta.append(_eta.copy())
            _snaps_u.append(_u.copy())
            _snaps_v.append(_v.copy())
            _t_hist.append(_t)
        if _s < _nsteps:
            _eta, _u, _v = _rk4(_eta, _u, _v, _dt)
            _t += _dt

    set_sw({
        "eta": _snaps_eta, "u": _snaps_u, "v": _snaps_v,
        "t": np.array(_t_hist),
        "x": _x, "y": _y, "XX": _XX, "YY": _YY,
        "f0": _f0, "beta": _beta, "sigma": _sigma, "amp": _amp,
    })

    mo.callout(mo.md(
        f"**Done.** Grid {_n}×{_n}, {_nsteps} steps → {len(_snaps_eta)} snapshots saved."
    ), kind="success")
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 6 · Overview: Initial, Mid-point & Final State
    """)
    return


@app.cell
def _(get_sw, mo, np, plt):
    _sim = get_sw()
    mo.stop(_sim is None, mo.callout(
        mo.md("Results appear here after running."), kind="warn"
    ))

    _eta = _sim["eta"]; _u = _sim["u"]; _v = _sim["v"]
    _t   = _sim["t"];   _x = _sim["x"]; _y = _sim["y"]
    _XX  = _sim["XX"];  _YY = _sim["YY"]
    _amp = _sim["amp"]

    _fig, _axes = plt.subplots(1, 3, figsize=(13, 4.5))
    _idxs = [0, len(_t)//2, -1]

    for _col, _idx in enumerate(_idxs):
        _vm = _amp * 0.6
        _im = _axes[_col].pcolormesh(
            _x, _y, _eta[_idx], cmap="RdBu_r",
            vmin=-_vm, vmax=_vm, shading="auto"
        )
        # Velocity vectors (subsampled)
        _skip = max(1, len(_x) // 16)
        _axes[_col].quiver(
            _x[::_skip], _y[::_skip],
            _u[_idx][::_skip, ::_skip], _v[_idx][::_skip, ::_skip],
            scale=4, width=0.004, alpha=0.6, color="k"
        )
        plt.colorbar(_im, ax=_axes[_col], fraction=0.046, label="$\\eta/H$")
        _axes[_col].set_title(f"$t = {_t[_idx]:.1f}\\,f_0^{{-1}}$", fontsize=11)
        _axes[_col].set_xlabel("$x / L_R$"); _axes[_col].set_ylabel("$y / L_R$")
        _axes[_col].set_aspect("equal")

    _fig.suptitle("Height anomaly $\\eta$ and velocity field (arrows) during geostrophic adjustment",
                  fontsize=11)
    plt.tight_layout()
    _fig
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 7 · Animation
    """)
    return


@app.cell
def _(get_sw, mo, np, plt):
    import io as _io
    from PIL import Image as _Image

    _sim2 = get_sw()
    mo.stop(_sim2 is None, mo.callout(
        mo.md("Run the simulation above to generate the animation."), kind="warn"
    ))

    _eta2 = _sim2["eta"]; _u2 = _sim2["u"]; _v2 = _sim2["v"]
    _t2   = _sim2["t"];   _x2 = _sim2["x"]; _y2 = _sim2["y"]
    _amp2 = _sim2["amp"]

    _step_gif = max(1, len(_t2) // 50)
    _frames_idx = list(range(0, len(_t2), _step_gif))

    _vm2   = _amp2 * 0.65
    _skip2 = max(1, len(_x2) // 12)

    _pil_frames = []
    for _fi in _frames_idx:
        _fig_g, _ax_g = plt.subplots(figsize=(5, 4.5), dpi=80)
        _im_g = _ax_g.pcolormesh(
            _x2, _y2, _eta2[_fi], cmap="RdBu_r",
            vmin=-_vm2, vmax=_vm2, shading="auto"
        )
        _ax_g.quiver(
            _x2[::_skip2], _y2[::_skip2],
            _u2[_fi][::_skip2, ::_skip2], _v2[_fi][::_skip2, ::_skip2],
            scale=3.5, width=0.005, alpha=0.65, color="k"
        )
        plt.colorbar(_im_g, ax=_ax_g, label="$\\eta/H$", fraction=0.046)
        _ax_g.set_title(f"$t = {_t2[_fi]:.1f}\\,f_0^{{-1}}$", fontsize=10)
        _ax_g.set_xlabel("$x/L_R$"); _ax_g.set_ylabel("$y/L_R$")
        _ax_g.set_aspect("equal")
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
        save_all=True, duration=100, loop=0
    )
    _gif_buf.seek(0)
    mo.image(_gif_buf.read(), alt="Geostrophic adjustment animation", width=460)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 8 · Interactive Snapshot Browser
    """)
    return


@app.cell
def _(get_sw, mo):
    _sim3 = get_sw()
    mo.stop(_sim3 is None)
    sw_slider = mo.ui.slider(0, len(_sim3["t"]) - 1, step=1, value=0,
                             label="Snapshot", show_value=True)
    return (sw_slider,)


@app.cell
def _(get_sw, mo, np, plt, sw_slider):
    import matplotlib.pyplot as _plt5

    _sim4 = get_sw()
    mo.stop(_sim4 is None)

    _idx = sw_slider.value
    _eta4 = _sim4["eta"][_idx]
    _u4   = _sim4["u"][_idx]
    _v4   = _sim4["v"][_idx]
    _t4   = _sim4["t"][_idx]
    _x4   = _sim4["x"]; _y4 = _sim4["y"]
    _amp4 = _sim4["amp"]

    # Vorticity and divergence
    _kx4 = np.fft.rfftfreq(len(_x4)) * len(_x4) * (2*np.pi/20.0)
    _ky4 = np.fft.fftfreq(len(_y4))  * len(_y4) * (2*np.pi/20.0)
    _KX4, _KY4 = np.meshgrid(_kx4, _ky4)
    _ny4, _nx4 = _eta4.shape

    def _d_dx4(f): return np.fft.irfft2(1j*_KX4*np.fft.rfft2(f), s=(_ny4, _nx4))
    def _d_dy4(f): return np.fft.irfft2(1j*_KY4*np.fft.rfft2(f), s=(_ny4, _nx4))

    _vort4 = _d_dx4(_v4) - _d_dy4(_u4)    # relative vorticity ζ = ∂v/∂x − ∂u/∂y
    _div4  = _d_dx4(_u4) + _d_dy4(_v4)    # divergence ∇·u

    _vm4  = _amp4 * 0.65
    _vvm4 = float(np.percentile(np.abs(_vort4), 99)) or 1e-6
    _dvm4 = float(np.percentile(np.abs(_div4),  99)) or 1e-6

    _fig5, _ax5 = _plt5.subplots(1, 3, figsize=(13, 4))

    _im5a = _ax5[0].pcolormesh(_x4, _y4, _eta4, cmap="RdBu_r",
                                vmin=-_vm4, vmax=_vm4, shading="auto")
    _skip4 = max(1, len(_x4)//12)
    _ax5[0].quiver(_x4[::_skip4], _y4[::_skip4],
                   _u4[::_skip4, ::_skip4], _v4[::_skip4, ::_skip4],
                   scale=3.5, width=0.005, alpha=0.6, color="k")
    _plt5.colorbar(_im5a, ax=_ax5[0], fraction=0.046, label="$\\eta$")
    _ax5[0].set_title(f"Height $\\eta$ + velocity   $t={_t4:.1f}$")
    _ax5[0].set_xlabel("$x/L_R$"); _ax5[0].set_ylabel("$y/L_R$")
    _ax5[0].set_aspect("equal")

    _im5b = _ax5[1].pcolormesh(_x4, _y4, _vort4, cmap="PuOr",
                                vmin=-_vvm4, vmax=_vvm4, shading="auto")
    _plt5.colorbar(_im5b, ax=_ax5[1], fraction=0.046, label="$\\zeta$")
    _ax5[1].set_title("Relative vorticity $\\zeta = v_x - u_y$")
    _ax5[1].set_xlabel("$x/L_R$"); _ax5[1].set_aspect("equal")

    _im5c = _ax5[2].pcolormesh(_x4, _y4, _div4, cmap="PRGn",
                                vmin=-_dvm4, vmax=_dvm4, shading="auto")
    _plt5.colorbar(_im5c, ax=_ax5[2], fraction=0.046, label="$\\nabla\\cdot u$")
    _ax5[2].set_title("Divergence $\\nabla\\cdot\\mathbf{u}$ (gravity waves)")
    _ax5[2].set_xlabel("$x/L_R$"); _ax5[2].set_aspect("equal")

    _plt5.tight_layout()
    mo.vstack([sw_slider, _fig5])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 9 · Energy Partition

    A key diagnostic for geostrophic adjustment is how energy is partitioned
    between the **kinetic** (KE) and **potential** (PE) components.

    In non-dimensional units:

    $$KE = \tfrac{1}{2}\langle u^2 + v^2\rangle, \qquad PE = \tfrac{1}{2}\langle\eta^2\rangle$$

    Initially $KE = 0$, $PE = PE_0$ (all energy in the height field).
    Gravity waves carry away kinetic energy; the balanced state satisfies
    $KE/PE = O(1)$ (energy equipartition for inertia-gravity waves).
    """)
    return


@app.cell
def _(get_sw, mo, np, plt):
    _sim5 = get_sw()
    mo.stop(_sim5 is None, mo.callout(
        mo.md("Run the simulation above to see the energy time series."), kind="warn"
    ))

    _eta5 = _sim5["eta"]; _u5 = _sim5["u"]; _v5 = _sim5["v"]
    _t5   = _sim5["t"]

    _KE = np.array([0.5 * np.mean(u**2 + v**2) for u, v in zip(_u5, _v5)])
    _PE = np.array([0.5 * np.mean(e**2) for e in _eta5])
    _TE = _KE + _PE

    _fig6, _axes6 = plt.subplots(1, 2, figsize=(11, 4))

    _axes6[0].plot(_t5, _KE/_TE[0], lw=2, color="#2563eb", label="$KE / E_0$")
    _axes6[0].plot(_t5, _PE/_TE[0], lw=2, color="crimson",  label="$PE / E_0$")
    _axes6[0].plot(_t5, _TE/_TE[0], lw=1.5, color="gray", ls="--", label="$TE / E_0$")
    _axes6[0].set_xlabel("$t\\, (f_0^{-1})$"); _axes6[0].set_ylabel("Normalised energy")
    _axes6[0].set_title("Energy partition during adjustment")
    _axes6[0].legend(fontsize=10); _axes6[0].grid(True, alpha=0.3)

    _axes6[1].plot(_t5, _KE/_PE.clip(1e-12), lw=2, color="#7c3aed")
    _axes6[1].axhline(1, color="gray", ls="--", lw=1, label="$KE = PE$ (equipartition)")
    _axes6[1].set_xlabel("$t\\, (f_0^{-1})$"); _axes6[1].set_ylabel("$KE / PE$")
    _axes6[1].set_title("KE/PE ratio")
    _axes6[1].legend(fontsize=10); _axes6[1].grid(True, alpha=0.3)

    plt.tight_layout()
    _fig6
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 10 · Physical Interpretation

    ### What you should observe

    | Timescale | Phenomenon | Signature in the fields |
    |-----------|------------|------------------------|
    | $t \sim 1\text{–}5\,f_0^{-1}$ | Gravity wave radiation | Circular rings in $\eta$; high divergence $\nabla\cdot\mathbf{u}$ |
    | $t \sim 5\text{–}20\,f_0^{-1}$ | Geostrophic adjustment | $KE$ rises; circular vortex forms |
    | $t \gg 20\,f_0^{-1}$ | Rossby wave propagation | Asymmetric westward drift of $\eta$ anomalies |

    ### The role of the Rossby deformation radius

    $L_R$ controls everything:
    - **$\sigma \ll L_R$**: small initial perturbation — height field adjusts to match
      pre-existing zero velocity, leaving a weak height anomaly
    - **$\sigma \gg L_R$**: large initial perturbation — velocity field adjusts to match
      the height field; a strong geostrophic jet forms

    Try $\hat\beta = 0$ to isolate pure inertia-gravity waves (no Rossby drift).
    Try $\hat\beta = 0.4$–$0.5$ to see pronounced westward propagation.

    ### Geophysical relevance

    - **Atmosphere:** Geostrophic adjustment occurs after convective storms,
      jet-stream meanders, and orographic forcing
    - **Ocean:** Mesoscale eddies form by geostrophic adjustment after wind-driven
      upwelling or baroclinic instability
    - **Climate:** Rossby wave trains link tropical forcing to extratropical weather
      (teleconnections, e.g. El Niño → Pacific–North America pattern)

    ### Key references

    - Rossby, C.-G. (1938). *On the mutual adjustment of pressure and velocity distributions in certain simple current systems.* J. Mar. Res. **1**, 239–263.
    - Gill, A. E. (1982). *Atmosphere-Ocean Dynamics.* Academic Press. (Ch. 7)
    - Vallis, G. K. (2017). *Atmospheric and Oceanic Fluid Dynamics.* Cambridge. (Ch. 3)
    """)
    return


if __name__ == "__main__":
    app.run()
