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
    # Rayleigh–Bénard Convection & the Lorenz 1963 Model
    ## An Interactive GFD Tutorial

    This notebook explores **Rayleigh–Bénard convection** — a fluid heated from below
    and cooled from above — and shows how Edward Lorenz derived his famous three-variable
    chaotic system directly from the Navier–Stokes equations applied to this problem.

    > **How to use:** Read through the theory, then press **▶ Run** in each section
    > to explore the interactive simulations.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 1 · Physical Setup

    A layer of fluid of depth $H$ sits between two horizontal plates:
    - **Bottom plate:** temperature $T_0 + \Delta T$ (hot)
    - **Top plate:** temperature $T_0$ (cold)

    Gravity $g$ acts downward. When the temperature difference $\Delta T$ is small,
    heat is carried by **conduction** alone and the fluid stays at rest. Above a
    critical threshold, the fluid spontaneously **overturns** — warm light fluid rises,
    cool dense fluid sinks — forming organised convection rolls.

    The competition between destabilising buoyancy and stabilising diffusion
    is captured by a single dimensionless number:

    $$Ra = \frac{g \alpha \Delta T H^3}{\nu \kappa}$$

    | Symbol | Meaning |
    |--------|---------|
    | $\alpha$ | Thermal expansion coefficient |
    | $\nu$ | Kinematic viscosity |
    | $\kappa$ | Thermal diffusivity |
    | $Pr = \nu/\kappa$ | Prandtl number |

    The **Prandtl number** $Pr$ sets the ratio of momentum to heat diffusion.
    For air $Pr \approx 0.7$; for water $Pr \approx 7$; for the Earth's mantle $Pr \sim 10^{23}$.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Governing Equations

    Non-dimensionalising with $H$, $H^2/\kappa$, and $\Delta T$, the
    Boussinesq equations in **vorticity–streamfunction** form are:

    $$\frac{\partial \zeta}{\partial t} + J(\psi, \zeta) = Pr\,\nabla^2\zeta + Pr\cdot Ra\,\frac{\partial \theta}{\partial x}$$

    $$\frac{\partial \theta}{\partial t} + J(\psi, \theta) = \nabla^2\theta + \frac{\partial \psi}{\partial x}$$

    $$\nabla^2 \psi = -\zeta$$

    where $\theta$ is the **temperature deviation** from the linear conduction profile,
    $\zeta = \partial_x v - \partial_z u$ is vorticity, and $\psi$ is the streamfunction
    with $(u,w) = (-\partial_z\psi,\, \partial_x\psi)$.

    The Jacobian $J(\psi,\theta) = \partial_x\psi\,\partial_z\theta - \partial_z\psi\,\partial_x\theta$
    represents advection of temperature by the flow.

    **Boundary conditions (free-slip, fixed temperature):**
    $$z=0,1: \quad \theta = 0,\quad \psi = 0,\quad \zeta = 0$$
    $$x: \quad \text{periodic with period } L = 2\pi / k_c$$
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Linear Stability & Critical Rayleigh Number

    Linearising around the conduction state $(\psi, \theta, \zeta) = 0$
    and seeking normal-mode solutions $\sim e^{\sigma t} \sin(kx)\sin(\pi z)$,
    the growth rate is:

    $$\sigma = \frac{Pr}{k^2 + \pi^2}\left[\frac{Ra\, k^2}{k^2 + \pi^2} - (k^2 + \pi^2)\right]$$

    Convection onset ($\sigma = 0$) requires:

    $$Ra_c(k) = \frac{(k^2 + \pi^2)^3}{k^2}$$

    Minimising over horizontal wavenumber $k$ gives the **critical Rayleigh number**:

    $$Ra_c = \frac{27\pi^4}{4} \approx 657.5 \qquad \text{at} \qquad k_c = \frac{\pi}{\sqrt{2}}$$

    The aspect ratio of the first unstable roll is $L/H = 2\pi/k_c = 2\sqrt{2} \approx 2.83$.
    """)
    return


@app.cell
def _(mo):
    import numpy as np
    import matplotlib.pyplot as plt

    _k = np.linspace(0.3, 5, 400)
    _Ra_c_k = ((_k**2 + np.pi**2)**3) / _k**2
    _k_crit = np.pi / np.sqrt(2)
    _Ra_crit = 27 * np.pi**4 / 4

    _fig, _ax = plt.subplots(figsize=(7, 4))
    _ax.plot(_k, _Ra_c_k, lw=2, color="#2563eb")
    _ax.axhline(_Ra_crit, color="crimson", lw=1.5, ls="--",
                label=f"$Ra_c = 27\\pi^4/4 \\approx {_Ra_crit:.0f}$")
    _ax.axvline(_k_crit, color="gray", lw=1.2, ls=":")
    _ax.set_xlabel("Horizontal wavenumber $k$", fontsize=12)
    _ax.set_ylabel("$Ra_c(k)$", fontsize=12)
    _ax.set_title("Neutral stability curve", fontsize=12)
    _ax.set_ylim(0, 3000)
    _ax.legend(fontsize=11)
    _ax.grid(True, alpha=0.3)
    _ax.annotate(f"$k_c = \\pi/\\sqrt{{2}} \\approx {_k_crit:.2f}$",
                 xy=(_k_crit, _Ra_crit), xytext=(_k_crit + 0.5, _Ra_crit + 300),
                 arrowprops=dict(arrowstyle="->", color="gray"),
                 fontsize=10)
    plt.tight_layout()
    _fig
    return np, plt


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 4 · The Lorenz 1963 Truncation

    Following Saltzman (1962) and Lorenz (1963), we keep only the **three most
    energetic Fourier modes** consistent with the boundary conditions.
    Writing:

    $$\psi = \sqrt{2}\,\frac{(1+a^2)}{a} X(t)\, \sin\!\left(\frac{\pi a x}{H}\right)\sin\!\left(\frac{\pi z}{H}\right)$$

    $$\theta = \sqrt{2}\,\frac{Ra_c}{Ra}\,\frac{\pi}{\sigma} Y(t)\cos\!\left(\frac{\pi a x}{H}\right)\sin\!\left(\frac{\pi z}{H}\right) - \frac{Ra_c}{Ra}\frac{\pi}{\sigma} Z(t)\sin\!\left(\frac{2\pi z}{H}\right)$$

    and substituting into the governing equations, all other modes are discarded.
    The three amplitudes $(X, Y, Z)$ satisfy:

    $$\dot{X} = \sigma(Y - X)$$
    $$\dot{Y} = rX - Y - XZ$$
    $$\dot{Z} = XY - b Z$$

    with $\sigma = Pr$, $r = Ra/Ra_c$, and $b = 8/3$ (from geometry).

    | Variable | Physical meaning |
    |----------|-----------------|
    | $X$ | Intensity of convective circulation |
    | $Y$ | Temperature difference between ascending and descending fluid |
    | $Z$ | Distortion of the vertical temperature profile from linearity |
    | $r = Ra/Ra_c$ | Reduced Rayleigh number |

    **Fixed points:**
    - $(0,0,0)$: conduction state — stable for $r < 1$
    - $(\pm\sqrt{b(r-1)},\, \pm\sqrt{b(r-1)},\, r-1)$: convection rolls — exist for $r > 1$

    For $r > r_H \approx 24.74$ (with $\sigma=10$, $b=8/3$), the convective fixed points
    also become unstable and the system enters **chaos**.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Interactive Lorenz Model

    Adjust the parameters and press **▶ Run Lorenz** to integrate the system.
    Try $r = 28$, $\sigma = 10$, $b = 8/3$ for the classic butterfly attractor.
    """)
    return


@app.cell
def _(mo):
    get_lorenz, set_lorenz = mo.state(None)
    return get_lorenz, set_lorenz


@app.cell
def _(mo):
    lorenz_sigma = mo.ui.slider(1.0, 20.0, step=0.5, value=10.0,
                                label="$\\sigma$ (Prandtl)", show_value=True)
    lorenz_r     = mo.ui.slider(0.5, 60.0, step=0.5, value=28.0,
                                label="$r = Ra/Ra_c$", show_value=True)
    lorenz_b     = mo.ui.slider(0.5, 4.0, step=1/6, value=8/3,
                                label="$b$", show_value=True)
    lorenz_T     = mo.ui.slider(10, 100, step=5, value=50,
                                label="Integration time", show_value=True)
    lorenz_ntrj  = mo.ui.slider(1, 5, step=1, value=3,
                                label="Trajectories", show_value=True)

    mo.vstack([
        mo.hstack([lorenz_sigma, lorenz_r, lorenz_b], justify="start"),
        mo.hstack([lorenz_T, lorenz_ntrj], justify="start"),
    ])
    return lorenz_T, lorenz_b, lorenz_ntrj, lorenz_r, lorenz_sigma


@app.cell
def _(mo):
    lorenz_btn = mo.ui.run_button(label="▶  Run Lorenz")
    lorenz_btn
    return (lorenz_btn,)


@app.cell
def _(lorenz_T, lorenz_b, lorenz_btn, lorenz_ntrj, lorenz_r, lorenz_sigma, mo, np, set_lorenz):
    mo.stop(not lorenz_btn.value, mo.callout(
        mo.md("Press **▶ Run Lorenz** above to integrate."), kind="info"
    ))

    _sigma = lorenz_sigma.value
    _r     = lorenz_r.value
    _b     = lorenz_b.value
    _T     = lorenz_T.value
    _n     = lorenz_ntrj.value

    def _lorenz_rhs(state, s, r, b):
        x, y, z = state
        return np.array([s*(y - x), r*x - y - x*z, x*y - b*z])

    def _rk4(state, dt, s, r, b):
        k1 = _lorenz_rhs(state,            s, r, b)
        k2 = _lorenz_rhs(state + 0.5*dt*k1, s, r, b)
        k3 = _lorenz_rhs(state + 0.5*dt*k2, s, r, b)
        k4 = _lorenz_rhs(state + dt*k3,      s, r, b)
        return state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

    _dt  = 0.01
    _nt  = int(_T / _dt)
    _rng = np.random.default_rng(42)

    _trajectories = []
    for _i in range(_n):
        # Slightly perturbed initial conditions around the attractor
        _ic = np.array([1.0, 1.0, 1.0]) + _rng.normal(0, 0.5, 3)
        _traj = np.zeros((_nt + 1, 3))
        _traj[0] = _ic
        for _s in range(_nt):
            _traj[_s+1] = _rk4(_traj[_s], _dt, _sigma, _r, _b)
        _trajectories.append(_traj)

    _t_arr = np.linspace(0, _T, _nt + 1)
    set_lorenz({"trajectories": _trajectories, "t": _t_arr,
                "sigma": _sigma, "r": _r, "b": _b})

    mo.callout(mo.md(
        f"**Done.** Integrated {_n} trajectory/ies for $t \\in [0, {_T}]$ "
        f"with $\\sigma={_sigma}$, $r={_r}$, $b={_b:.2f}$."
    ), kind="success")
    return


@app.cell
def _(get_lorenz, mo, np, plt):
    _data = get_lorenz()
    mo.stop(_data is None, mo.callout(
        mo.md("Lorenz results will appear here after running."), kind="warn"
    ))

    _trajs = _data["trajectories"]
    _t     = _data["t"]
    _r     = _data["r"]
    _sigma = _data["sigma"]
    _b     = _data["b"]
    _colors = ["#2563eb", "crimson", "#16a34a", "#d97706", "#7c3aed"]

    _fig, _axes = plt.subplots(2, 3, figsize=(13, 8))

    # Phase portraits
    for _idx, _traj in enumerate(_trajs):
        _c = _colors[_idx % len(_colors)]
        _skip = max(1, len(_t)//2000)   # downsample for speed
        _x, _y, _z = _traj[::_skip, 0], _traj[::_skip, 1], _traj[::_skip, 2]
        _axes[0,0].plot(_x, _y, lw=0.4, alpha=0.7, color=_c)
        _axes[0,1].plot(_x, _z, lw=0.4, alpha=0.7, color=_c)
        _axes[0,2].plot(_y, _z, lw=0.4, alpha=0.7, color=_c)
        # Time series (full resolution, first trajectory only)
        if _idx == 0:
            _axes[1,0].plot(_t, _traj[:,0], lw=0.7, color=_c)
            _axes[1,1].plot(_t, _traj[:,1], lw=0.7, color=_c)
            _axes[1,2].plot(_t, _traj[:,2], lw=0.7, color=_c)

    _axes[0,0].set_xlabel("$X$"); _axes[0,0].set_ylabel("$Y$")
    _axes[0,1].set_xlabel("$X$"); _axes[0,1].set_ylabel("$Z$")
    _axes[0,2].set_xlabel("$Y$"); _axes[0,2].set_ylabel("$Z$")
    _axes[1,0].set_xlabel("$t$"); _axes[1,0].set_ylabel("$X$ (flow intensity)")
    _axes[1,1].set_xlabel("$t$"); _axes[1,1].set_ylabel("$Y$ (temp. contrast)")
    _axes[1,2].set_xlabel("$t$"); _axes[1,2].set_ylabel("$Z$ (profile distortion)")

    for _ax in _axes[0]:
        _ax.grid(True, alpha=0.2)
    for _ax in _axes[1]:
        _ax.grid(True, alpha=0.2)

    _title = f"Lorenz system  ($\\sigma={_sigma}$,  $r={_r}$,  $b={_b:.2f}$)"
    _fig.suptitle(_title, fontsize=13)
    plt.tight_layout()
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 6 · Sensitivity to Initial Conditions

    The butterfly attractor owes its fame to **chaos**: exponential divergence of
    nearby trajectories. Below we integrate two trajectories that start $\epsilon$
    apart and track their separation $\|\delta\mathbf{u}(t)\|$.

    The average rate of separation is characterised by the **largest Lyapunov exponent**
    $\lambda_1$. For the classic Lorenz parameters $\lambda_1 \approx 0.906$, meaning
    errors double roughly every $\ln 2/\lambda_1 \approx 0.77$ time units.
    """)
    return


@app.cell
def _(get_lorenz, mo, np, plt):
    _data = get_lorenz()
    mo.stop(_data is None, mo.callout(
        mo.md("Run the Lorenz model above first."), kind="warn"
    ))

    _sigma = _data["sigma"]; _r = _data["r"]; _b = _data["b"]

    def _rhs(s, si, ri, bi): return np.array([si*(s[1]-s[0]), ri*s[0]-s[1]-s[0]*s[2], s[0]*s[1]-bi*s[2]])
    def _rk4s(s, dt, si, ri, bi):
        k1=_rhs(s,si,ri,bi); k2=_rhs(s+0.5*dt*k1,si,ri,bi)
        k3=_rhs(s+0.5*dt*k2,si,ri,bi); k4=_rhs(s+dt*k3,si,ri,bi)
        return s+(dt/6)*(k1+2*k2+2*k3+k4)

    _dt = 0.01; _T = 20; _nt = int(_T/_dt)
    _eps = 1e-8
    _ic1 = np.array([1.0, 1.0, 1.0])
    _ic2 = _ic1 + np.array([_eps, 0, 0])

    _s1 = np.zeros((_nt+1, 3)); _s2 = np.zeros((_nt+1, 3))
    _s1[0] = _ic1; _s2[0] = _ic2
    for _i in range(_nt):
        _s1[_i+1] = _rk4s(_s1[_i], _dt, _sigma, _r, _b)
        _s2[_i+1] = _rk4s(_s2[_i], _dt, _sigma, _r, _b)

    _t = np.linspace(0, _T, _nt+1)
    _sep = np.linalg.norm(_s1 - _s2, axis=1)

    _fig2, _axes2 = plt.subplots(1, 2, figsize=(12, 4))

    _axes2[0].plot(_t, _s1[:,0], lw=1, label="trajectory 1")
    _axes2[0].plot(_t, _s2[:,0], lw=1, ls="--", label=f"trajectory 1 + $10^{{-8}}$", alpha=0.8)
    _axes2[0].set_xlabel("$t$"); _axes2[0].set_ylabel("$X$")
    _axes2[0].set_title("Two initially close trajectories", fontsize=11)
    _axes2[0].legend(fontsize=9); _axes2[0].grid(True, alpha=0.3)

    _valid = _sep > 1e-15
    _axes2[1].semilogy(_t[_valid], _sep[_valid], lw=1.5, color="crimson", label="$\\|\\delta u(t)\\|$")
    # Fit slope in the linear-growth region (roughly t=2..10)
    _mask = (_t > 2) & (_t < 10) & _valid
    if _mask.sum() > 5:
        _lam = np.polyfit(_t[_mask], np.log(_sep[_mask]), 1)[0]
        _axes2[1].semilogy(_t[_mask], np.exp(np.log(_sep[_mask][0]) + _lam*(_t[_mask]-_t[_mask][0])),
                          "k--", lw=1.2, label=f"slope $\\lambda_1 \\approx {_lam:.2f}$")
    _axes2[1].set_xlabel("$t$"); _axes2[1].set_ylabel("Separation $\\|\\delta u\\|$")
    _axes2[1].set_title("Exponential error growth (Lyapunov)", fontsize=11)
    _axes2[1].legend(fontsize=9); _axes2[1].grid(True, alpha=0.2)

    plt.tight_layout()
    _fig2
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 7 · Full 2D Rayleigh–Bénard Simulation

    We now solve the full 2D Boussinesq equations numerically using a
    **pseudo-spectral method**: FFT in the (periodic) horizontal direction $x$,
    finite-differences in the vertical direction $z$, and RK4 time-stepping.

    The domain is $[0, L] \times [0, 1]$ with $L = 2\sqrt{2}$ (two critical-wavelength rolls).
    """)
    return


@app.cell
def _(mo):
    get_rb2d, set_rb2d = mo.state(None)
    return get_rb2d, set_rb2d


@app.cell
def _(mo):
    rb_Ra  = mo.ui.slider(500, 5000, step=100, value=1000,
                          label="Rayleigh number $Ra$", show_value=True)
    rb_Pr  = mo.ui.slider(0.1, 10.0, step=0.1, value=1.0,
                          label="Prandtl $Pr$", show_value=True)
    rb_nx  = mo.ui.slider(32, 128, step=32, value=64,
                          label="Grid $n_x$", show_value=True)
    rb_nz  = mo.ui.slider(16, 64, step=16, value=32,
                          label="Grid $n_z$", show_value=True)
    rb_T   = mo.ui.slider(0.05, 1.0, step=0.05, value=0.3,
                          label="Run time", show_value=True)

    mo.vstack([
        mo.hstack([rb_Ra, rb_Pr], justify="start"),
        mo.hstack([rb_nx, rb_nz, rb_T], justify="start"),
        mo.md(r"""
        > **Tip:** For browser/WASM, use $n_x \leq 64$, $n_z \leq 32$.
        > $Ra < Ra_c \approx 658$ → no convection; $Ra \gg Ra_c$ → vigorous turbulence.
        """),
    ])
    return rb_Pr, rb_Ra, rb_T, rb_nx, rb_nz


@app.cell
def _(mo):
    rb_btn = mo.ui.run_button(label="▶  Run 2D Simulation")
    rb_btn
    return (rb_btn,)


@app.cell
def _(mo, np, rb_Pr, rb_Ra, rb_T, rb_btn, rb_nx, rb_nz, set_rb2d):
    mo.stop(not rb_btn.value, mo.callout(
        mo.md("Press **▶ Run 2D Simulation** to start."), kind="info"
    ))

    import numpy as _np2

    _Ra = rb_Ra.value
    _Pr = rb_Pr.value
    _nx = rb_nx.value
    _nz = rb_nz.value
    _Lx = 2 * _np2.sqrt(2)   # two critical rolls
    _run_T = rb_T.value

    # ── Grid ────────────────────────────────────────────────────────────────
    _dx = _Lx / _nx
    _dz = 1.0 / (_nz + 1)    # interior z points only (Dirichlet at 0 and 1)
    _x  = _np2.linspace(0, _Lx, _nx, endpoint=False)
    _z  = _np2.linspace(_dz, 1 - _dz, _nz)   # interior z

    # ── Wavenumbers (x is periodic) ─────────────────────────────────────────
    _kx  = _np2.fft.rfftfreq(_nx, d=_Lx / (2 * _np2.pi * _nx))   # physical kx
    _nkx = len(_kx)

    # ── Vertical second-derivative matrix (Dirichlet BCs) ───────────────────
    # d²/dz² with zero BCs: tridiagonal 1/dz² * (-2 on diag, 1 off-diag)
    _D2z = (_np2.diag(-2 * _np2.ones(_nz)) +
             _np2.diag(_np2.ones(_nz - 1), 1) +
             _np2.diag(_np2.ones(_nz - 1), -1)) / _dz**2

    # ── Poisson solver: (∂²/∂x² + ∂²/∂z²)ψ̂_k = -ζ̂_k ────────────────────
    # For each kx mode, invert (−kx²I + D2z) by LU
    from scipy.linalg import lu_factor, lu_solve as _lu_solve

    _poisson_lu = []
    for _ik in range(_nkx):
        _A = _D2z - _kx[_ik]**2 * _np2.eye(_nz)
        if _ik == 0:  # zero mode: fix gauge (mean ψ=0), replace first row
            _A[0, :] = 0; _A[0, 0] = 1
        _poisson_lu.append(lu_factor(_A))

    def _solve_poisson(rhs_hat):
        """Solve for ψ̂_k given RHS in spectral-z space (shape nkx×nz)."""
        _out = _np2.zeros_like(rhs_hat)
        for _ik in range(_nkx):
            _b = rhs_hat[_ik].copy()
            if _ik == 0:
                _b[0] = 0   # fix gauge
            _out[_ik] = _lu_solve(_poisson_lu[_ik], _b)
        return _out

    # ── Derivatives in x via FFT ─────────────────────────────────────────────
    def _dx_fft(f):
        """d/dx via FFT (f shape: nx×nz)."""
        fh = _np2.fft.rfft(f, axis=0)
        return _np2.fft.irfft(1j * _kx[:, None] * fh, n=_nx, axis=0)

    def _lap_fft(f):
        """∇² f via FFT in x, FD in z."""
        fh = _np2.fft.rfft(f, axis=0)
        # d²f/dx² + d²f/dz²
        d2x = _np2.fft.irfft(-_kx[:, None]**2 * fh, n=_nx, axis=0)
        d2z = _np2.zeros_like(f)
        d2z[:, 1:-1] = (f[:, :-2] - 2*f[:, 1:-1] + f[:, 2:]) / _dz**2
        d2z[:, 0]    = (-2*f[:, 0]  + f[:, 1])    / _dz**2   # ghost = 0 at z=0
        d2z[:, -1]   = (f[:, -2] - 2*f[:, -1])    / _dz**2   # ghost = 0 at z=1
        return d2x + d2z

    def _vort_from_psi(psi):
        """ζ = −∇²ψ."""
        return -_lap_fft(psi)

    def _psi_from_vort(zeta):
        """Solve ∇²ψ = −ζ spectrally."""
        rhs = _np2.fft.rfft(-zeta, axis=0)   # shape nkx×nz
        psi_hat = _solve_poisson(rhs)
        return _np2.fft.irfft(psi_hat, n=_nx, axis=0)

    def _jacobian(psi, f):
        """J(ψ,f) = ∂ψ/∂x ∂f/∂z − ∂ψ/∂z ∂f/∂x  (FD in z, FFT in x)."""
        dpsi_dx = _dx_fft(psi)
        dpsi_dz = _np2.zeros_like(psi)
        dpsi_dz[:, 1:-1] = (psi[:, 2:] - psi[:, :-2]) / (2*_dz)
        dpsi_dz[:, 0]    = psi[:, 1] / (2*_dz)
        dpsi_dz[:, -1]   = -psi[:, -2] / (2*_dz)

        df_dx = _dx_fft(f)
        df_dz = _np2.zeros_like(f)
        df_dz[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2*_dz)
        df_dz[:, 0]    = f[:, 1] / (2*_dz)
        df_dz[:, -1]   = -f[:, -2] / (2*_dz)

        return dpsi_dx * df_dz - dpsi_dz * df_dx

    def _rhs_rb(zeta, theta, psi):
        """RHS of the vorticity and temperature equations."""
        d_zeta  = -_jacobian(psi, zeta) + _Pr * _lap_fft(zeta) + _Pr * _Ra * _dx_fft(theta)
        d_theta = -_jacobian(psi, theta) + _lap_fft(theta) + _dx_fft(psi)
        return d_zeta, d_theta

    def _step_rb(zeta, theta, dt):
        psi1 = _psi_from_vort(zeta)
        dz1, dt1 = _rhs_rb(zeta, theta, psi1)

        zeta2 = zeta + 0.5*dt*dz1; theta2 = theta + 0.5*dt*dt1
        psi2  = _psi_from_vort(zeta2)
        dz2, dt2 = _rhs_rb(zeta2, theta2, psi2)

        zeta3 = zeta + 0.5*dt*dz2; theta3 = theta + 0.5*dt*dt2
        psi3  = _psi_from_vort(zeta3)
        dz3, dt3 = _rhs_rb(zeta3, theta3, psi3)

        zeta4 = zeta + dt*dz3; theta4 = theta + dt*dt3
        psi4  = _psi_from_vort(zeta4)
        dz4, dt4 = _rhs_rb(zeta4, theta4, psi4)

        new_z = zeta  + (dt/6)*(dz1 + 2*dz2 + 2*dz3 + dz4)
        new_t = theta + (dt/6)*(dt1 + 2*dt2 + 2*dt3 + dt4)
        return new_z, new_t

    # ── Initial condition: small random perturbation ─────────────────────────
    _rng2 = _np2.random.default_rng(7)
    _theta = 1e-3 * _rng2.standard_normal((_nx, _nz))
    _zeta  = _np2.zeros((_nx, _nz))

    # ── CFL-based dt ─────────────────────────────────────────────────────────
    _dt = 0.2 * min(_dx, _dz)**2   # diffusive CFL
    _nsteps = int(_run_T / _dt)
    _nsubs  = max(1, _nsteps // 80)   # ~80 saved frames

    _snaps_th = []; _snaps_psi = []; _t_hist2 = []
    _t2 = 0.0
    for _s in range(_nsteps + 1):
        if _s % _nsubs == 0:
            _t_hist2.append(_t2)
            _snaps_th.append(_theta.copy())
            _snaps_psi.append(_psi_from_vort(_zeta).copy())
        if _s < _nsteps:
            _zeta, _theta = _step_rb(_zeta, _theta, _dt)
            _t2 += _dt

    set_rb2d({
        "snaps_th":  _snaps_th,
        "snaps_psi": _snaps_psi,
        "t_hist":    _np2.array(_t_hist2),
        "x": _x, "z": _z,
        "Ra": _Ra, "Pr": _Pr,
    })

    mo.callout(mo.md(
        f"**Done.** $Ra={_Ra}$, $Pr={_Pr}$, grid {_nx}×{_nz}, "
        f"{_nsteps} steps → {len(_snaps_th)} snapshots."
    ), kind="success")
    return np


@app.cell
def _(get_rb2d, mo, np, plt):
    _sim = get_rb2d()
    mo.stop(_sim is None, mo.callout(
        mo.md("2D results appear here after running."), kind="warn"
    ))

    _th  = _sim["snaps_th"]
    _psi = _sim["snaps_psi"]
    _t   = _sim["t_hist"]
    _x   = _sim["x"];  _z = _sim["z"]
    _Ra  = _sim["Ra"]; _Pr = _sim["Pr"]
    _Ra_c = 27 * np.pi**4 / 4

    _fig3, _axes3 = plt.subplots(2, 3, figsize=(13, 7))

    _XX, _ZZ = np.meshgrid(_x, _z, indexing="ij")

    for _col, _idx in enumerate([0, len(_t)//2, -1]):
        _vm = max(float(np.abs(_th[_idx]).max()), 1e-10)
        _im = _axes3[0, _col].pcolormesh(
            _XX, _ZZ, _th[_idx], cmap="RdBu_r",
            vmin=-_vm, vmax=_vm, shading="auto"
        )
        plt.colorbar(_im, ax=_axes3[0, _col], fraction=0.046, label="$\\theta$")
        _axes3[0, _col].set_title(f"Temperature  $t={_t[_idx]:.3f}$", fontsize=10)
        _axes3[0, _col].set_xlabel("$x$"); _axes3[0, _col].set_ylabel("$z$")

        _vm2 = max(float(np.abs(_psi[_idx]).max()), 1e-10)
        _im2 = _axes3[1, _col].pcolormesh(
            _XX, _ZZ, _psi[_idx], cmap="PuOr",
            vmin=-_vm2, vmax=_vm2, shading="auto"
        )
        plt.colorbar(_im2, ax=_axes3[1, _col], fraction=0.046, label="$\\psi$")
        _axes3[1, _col].set_title(f"Streamfunction  $t={_t[_idx]:.3f}$", fontsize=10)
        _axes3[1, _col].set_xlabel("$x$"); _axes3[1, _col].set_ylabel("$z$")

    _fig3.suptitle(
        f"2D Rayleigh–Bénard  ($Ra={_Ra}$,  $Ra/Ra_c={_Ra/_Ra_c:.1f}$,  $Pr={_Pr}$)",
        fontsize=12
    )
    plt.tight_layout()
    _fig3
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Interactive snapshot browser
    """)
    return


@app.cell
def _(get_rb2d, mo):
    _sim2 = get_rb2d()
    mo.stop(_sim2 is None)
    _nsnaps = len(_sim2["snaps_th"])
    rb_snap_slider = mo.ui.slider(0, _nsnaps - 1, step=1, value=0,
                                  label="Snapshot", show_value=True)
    return (rb_snap_slider,)


@app.cell
def _(get_rb2d, mo, np, plt, rb_snap_slider):
    import matplotlib.pyplot as _plt4
    _sim3 = get_rb2d()
    mo.stop(_sim3 is None)

    _idx2  = rb_snap_slider.value
    _th2   = _sim3["snaps_th"][_idx2]
    _psi2  = _sim3["snaps_psi"][_idx2]
    _t2v   = _sim3["t_hist"][_idx2]
    _x2    = _sim3["x"]; _z2 = _sim3["z"]
    _XX2, _ZZ2 = np.meshgrid(_x2, _z2, indexing="ij")

    _fig4, _ax4 = _plt4.subplots(1, 2, figsize=(11, 4))
    _vm3 = max(float(np.abs(_th2).max()), 1e-10)
    _im3 = _ax4[0].pcolormesh(_XX2, _ZZ2, _th2, cmap="RdBu_r",
                               vmin=-_vm3, vmax=_vm3, shading="auto")
    _plt4.colorbar(_im3, ax=_ax4[0], label="$\\theta$", fraction=0.046)
    _ax4[0].set_title(f"Temperature deviation  $t={_t2v:.4f}$")
    _ax4[0].set_xlabel("$x$"); _ax4[0].set_ylabel("$z$")

    _vm4 = max(float(np.abs(_psi2).max()), 1e-10)
    _im4 = _ax4[1].pcolormesh(_XX2, _ZZ2, _psi2, cmap="PuOr",
                               vmin=-_vm4, vmax=_vm4, shading="auto")
    _plt4.colorbar(_im4, ax=_ax4[1], label="$\\psi$", fraction=0.046)
    _ax4[1].set_title(f"Streamfunction  $t={_t2v:.4f}$")
    _ax4[1].set_xlabel("$x$"); _ax4[1].set_ylabel("$z$")

    _plt4.tight_layout()
    mo.vstack([rb_snap_slider, _fig4])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 8 · Connecting the Full 2D Simulation to the Lorenz Model

    The three Lorenz variables $(X, Y, Z)$ can be extracted from the 2D simulation
    by projecting the fields onto the first Fourier–sine modes:

    $$X(t) \propto \hat\psi_{k_c,1}(t), \qquad Y(t) \propto \hat\theta_{k_c,1}(t), \qquad Z(t) \propto \hat\theta_{0,2}(t)$$

    where subscripts denote the $(k_x, n_z)$ mode.
    """)
    return


@app.cell
def _(get_rb2d, mo, np, plt):
    _sim4 = get_rb2d()
    mo.stop(_sim4 is None, mo.callout(
        mo.md("Run the 2D simulation above to see the Lorenz projection."), kind="warn"
    ))

    _th_snaps  = _sim4["snaps_th"]
    _psi_snaps = _sim4["snaps_psi"]
    _t_hist3   = _sim4["t_hist"]
    _x3        = _sim4["x"]; _z3 = _sim4["z"]
    _nz3       = len(_z3)
    _nx3       = len(_x3)

    # Lorenz-mode projections
    _X_proj, _Y_proj, _Z_proj = [], [], []
    for _th3, _psi3 in zip(_th_snaps, _psi_snaps):
        # X ~ k_c Fourier mode of ψ, first sine mode in z
        _psi_fft = np.fft.rfft(_psi3, axis=0)   # shape (nkx, nz)
        _ik1 = 1  # first non-zero x mode
        _X_proj.append(float(np.abs(_psi_fft[_ik1, _nz3//2])))

        # Y ~ k_c Fourier mode of θ, first sine mode in z
        _th_fft = np.fft.rfft(_th3, axis=0)
        _Y_proj.append(float(np.real(_th_fft[_ik1, _nz3//2])))

        # Z ~ zero x-mode of θ, second sine mode in z (mean profile distortion)
        _Z_proj.append(float(np.real(_th_fft[0, min(1, _nz3-1)])))

    _X_proj = np.array(_X_proj)
    _Y_proj = np.array(_Y_proj)
    _Z_proj = np.array(_Z_proj)

    _fig5, _axes5 = plt.subplots(1, 3, figsize=(13, 4))
    _axes5[0].plot(_t_hist3, _X_proj, lw=1.5, color="#2563eb")
    _axes5[0].set_xlabel("$t$"); _axes5[0].set_ylabel("$X \\propto \\hat{\\psi}_{k_c,1}$")
    _axes5[0].set_title("Flow intensity", fontsize=11); _axes5[0].grid(True, alpha=0.3)

    _axes5[1].plot(_t_hist3, _Y_proj, lw=1.5, color="crimson")
    _axes5[1].set_xlabel("$t$"); _axes5[1].set_ylabel("$Y \\propto \\hat{\\theta}_{k_c,1}$")
    _axes5[1].set_title("Temperature contrast", fontsize=11); _axes5[1].grid(True, alpha=0.3)

    _axes5[2].plot(_X_proj, _Z_proj, lw=0.8, alpha=0.8, color="#7c3aed")
    _axes5[2].set_xlabel("$X$"); _axes5[2].set_ylabel("$Z \\propto \\hat{\\theta}_{0,2}$")
    _axes5[2].set_title("Phase portrait ($X$–$Z$ plane)", fontsize=11); _axes5[2].grid(True, alpha=0.3)

    plt.suptitle("Lorenz-mode projections from full 2D simulation", fontsize=12)
    plt.tight_layout()
    _fig5
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 9 · Physical Interpretation & Further Reading

    ### Why does Lorenz matter?

    Lorenz's 1963 paper — derived entirely from the RB problem — was the founding
    document of **chaos theory**. Its key messages:

    1. **Deterministic chaos is possible** even in simple, low-dimensional systems
       derived from the laws of physics.
    2. **Predictability has a finite horizon**: errors grow exponentially with
       Lyapunov exponent $\lambda_1 \approx 0.9$, so a 10× better initial condition
       buys only $\ln(10)/\lambda_1 \approx 2.5$ extra time units.
    3. **Strange attractors** are fractal objects with non-integer dimension
       ($d_L \approx 2.06$ for the Lorenz attractor).

    ### Summary of parameter regimes

    | $r = Ra/Ra_c$ | Lorenz behaviour | RB physics |
    |---------------|-----------------|------------|
    | $r < 1$ | Origin is stable | Conduction — no flow |
    | $1 < r < r_H$ | Stable fixed points | Steady convection rolls |
    | $r > r_H \approx 24.74$ | Chaotic attractor | Unsteady/chaotic convection |

    ### Key references

    - Lorenz, E. N. (1963). *Deterministic Nonperiodic Flow.* J. Atmos. Sci. **20**, 130–141.
    - Saltzman, B. (1962). *Finite amplitude free convection as an initial value problem.* J. Atmos. Sci. **19**, 329–341.
    - Chandrasekhar, S. (1961). *Hydrodynamic and Hydromagnetic Stability.* Oxford.
    - Strogatz, S. H. (1994). *Nonlinear Dynamics and Chaos.* Addison-Wesley.
    """)
    return


if __name__ == "__main__":
    app.run()
