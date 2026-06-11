import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Data Assimilation: From Chaos to Analysis
        ## 3DVAR · 4DVAR · Ensemble Kalman Filter on the Lorenz 63 System

        **FERS Summer School — AI and Machine Learning for Earth System Modeling and Prediction**

        ---

        > *"All models are wrong, but some are useful — and with data assimilation, we can make them more useful."*

        Data assimilation (DA) is the discipline of **combining a dynamical model with noisy observations**
        to obtain the best possible estimate of the true state of a system.
        It sits at the heart of numerical weather prediction (NWP), ocean reanalysis, and increasingly,
        hybrid AI/physics forecasting systems.

        In this tutorial we explore three foundational DA algorithms using the **Lorenz 63 system** as
        a low-dimensional but chaotic testbed:

        | Algorithm | Temporal scope | Background covariance |
        |-----------|---------------|----------------------|
        | **3DVAR** | Single analysis time | Static $\mathbf{B}$ |
        | **4DVAR** | Time window $[t_0, t_N]$ | Static $\mathbf{B}$, implicit flow-dependence |
        | **EnKF**  | Sequential / cycling | Flow-dependent from ensemble |

        ### Prerequisites assumed
        - Familiarity with ODEs and chaos (you know what a strange attractor is)
        - Basic linear algebra (matrix inversion, eigenvalues)
        - Some exposure to Bayesian reasoning or least-squares estimation
        - Python / NumPy comfort
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 1  The Lorenz 63 System

        Edward Lorenz (1963) derived a minimal 3-variable ODE system from the Navier–Stokes
        equations for Rayleigh–Bénard convection:

        $$
        \frac{dx}{dt} = \sigma(y - x)
        \qquad
        \frac{dy}{dt} = x(\rho - z) - y
        \qquad
        \frac{dz}{dt} = xy - \beta z
        $$

        With the classic parameters $\sigma=10,\; \rho=28,\; \beta=8/3$ the system is **chaotic**:
        trajectories starting from nearly identical initial conditions diverge exponentially,
        with a Lyapunov time $\tau_\Lambda \approx 1.1$ time units.

        This makes L63 an ideal DA testbed — the chaotic divergence *is* the problem DA is trying to solve.
        """
    )
    return


@app.cell
def _():
    import numpy as np
    from scipy.integrate import solve_ivp
    from scipy.optimize import minimize
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.colors import Normalize
    import warnings
    warnings.filterwarnings("ignore")

    # reproducibility
    rng = np.random.default_rng(42)
    return (
        Normalize,
        gridspec,
        minimize,
        np,
        plt,
        rng,
        solve_ivp,
        warnings,
    )


@app.cell
def _(np, solve_ivp):
    def lorenz63(t, state, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
        x, y, z = state
        return [
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z,
        ]

    def integrate_l63(
        x0, t_span, t_eval=None, sigma=10.0, rho=28.0, beta=8.0 / 3.0
    ):
        # Clip t_eval to t_span to guard against floating-point overshoot
        if t_eval is not None:
            mask   = (t_eval >= t_span[0] - 1e-10) & (t_eval <= t_span[1] + 1e-10)
            t_eval = np.clip(t_eval[mask], t_span[0], t_span[1])
        sol = solve_ivp(
            lorenz63,
            t_span,
            x0,
            t_eval=t_eval,
            args=(sigma, rho, beta),
            method="RK45",
            rtol=1e-9,
            atol=1e-12,
        )
        return sol.y.T  # shape (n_steps, 3)

    return integrate_l63, lorenz63


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 1.1  Visualising the attractor""")
    return


@app.cell(hide_code=True)
def _(integrate_l63, np, plt):
    # Spin-up trajectory to land on the attractor, then visualise
    _t_spinup = np.linspace(0, 10, 5000)
    _x0_spinup = np.array([1.0, 0.0, 0.0])
    _spinup = integrate_l63(_x0_spinup, (0, 10), _t_spinup)

    _t_attr = np.linspace(0, 30, 15000)
    _traj = integrate_l63(_spinup[-1], (0, 30), _t_attr)

    _fig = plt.figure(figsize=(13, 4))
    _ax1 = _fig.add_subplot(131, projection="3d")
    _ax1.plot(*_traj.T, lw=0.4, alpha=0.7, color="steelblue")
    _ax1.set_title("Lorenz Attractor (3D)")
    _ax1.set_xlabel("x"); _ax1.set_ylabel("y"); _ax1.set_zlabel("z")
    _ax1.tick_params(labelsize=7)

    _ax2 = _fig.add_subplot(132)
    for _i, (_lbl, _col) in enumerate(
        zip(["x", "y", "z"], ["tab:blue", "tab:orange", "tab:green"])
    ):
        _ax2.plot(_t_attr, _traj[:, _i], lw=0.6, label=_lbl, color=_col)
    _ax2.set_xlabel("time"); _ax2.set_title("Time series"); _ax2.legend(fontsize=9)

    _ax3 = _fig.add_subplot(133)
    _ax3.scatter(
        _traj[::10, 0], _traj[::10, 2],
        s=0.5, alpha=0.4, c=_t_attr[::10], cmap="viridis",
    )
    _ax3.set_xlabel("x"); _ax3.set_ylabel("z"); _ax3.set_title("x–z projection")

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 2  The Twin-Experiment Framework

        We work in a **perfect-model, twin-experiment** setup:

        1. **Nature run** (truth): integrate L63 from a known IC for time $T$.
        2. **Observations**: sample the truth at every $\Delta t_{\rm obs}$ and add Gaussian noise $\mathcal{N}(0, \mathbf{R})$.
        3. **Background** $\mathbf{x}^b$: a perturbed IC that represents our prior / first-guess.
        4. **Analysis** $\mathbf{x}^a$: the DA estimate we want to evaluate.

        **Error metric**: Root-Mean-Square Error (RMSE) between analysis/background and truth.
        """
    )
    return


@app.cell
def _(integrate_l63, np, rng):
    # ── Experiment parameters ──────────────────────────────────────────────
    DT_MODEL  = 0.01          # model time step (non-dimensional)
    T_SPINUP  = 5.0           # spin-up to attractor
    T_ASSIM   = 5.0           # assimilation window length
    DT_OBS    = 0.2           # observation interval
    OBS_SIGMA = 2.0           # observation error std (each component)
    BG_SIGMA  = 3.0           # background error std (each component)

    # ── Spin-up: land on the attractor ────────────────────────────────────
    t_spinup = np.linspace(0, T_SPINUP, int(round(T_SPINUP / DT_MODEL)) + 1)
    x0_truth = np.array([1.0, 1.0, 20.0])
    spinup   = integrate_l63(x0_truth, (0, T_SPINUP), t_spinup)
    x_start  = spinup[-1]  # point on attractor

    # ── Nature run (truth) ────────────────────────────────────────────────
    n_steps  = int(round(T_ASSIM / DT_MODEL)) + 1
    t_assim  = np.linspace(0, T_ASSIM, n_steps)
    truth    = integrate_l63(x_start, (0, T_ASSIM), t_assim)  # (n_steps, 3)

    # ── Synthetic observations ─────────────────────────────────────────────
    # Observe all 3 components (H = I_3).  Can be made partial easily.
    obs_times_idx = np.arange(0, n_steps, int(DT_OBS / DT_MODEL))
    obs_times     = t_assim[obs_times_idx]
    n_obs_times   = len(obs_times_idx)
    R_diag        = OBS_SIGMA**2 * np.ones(3)
    R             = np.diag(R_diag)
    R_inv         = np.diag(1.0 / R_diag)
    observations  = truth[obs_times_idx] + rng.normal(0, OBS_SIGMA, (n_obs_times, 3))

    # ── Background ────────────────────────────────────────────────────────
    # Perturb the true IC to create an "imperfect" background
    x_bg   = x_start + rng.normal(0, BG_SIGMA, 3)
    B_diag = BG_SIGMA**2 * np.ones(3)
    B      = np.diag(B_diag)
    B_inv  = np.diag(1.0 / B_diag)

    print(f"Truth start    : {x_start}")
    print(f"Background start: {x_bg}")
    print(f"Initial bg error: {np.linalg.norm(x_bg - x_start):.3f}")
    return (
        B,
        B_diag,
        B_inv,
        BG_SIGMA,
        DT_MODEL,
        DT_OBS,
        OBS_SIGMA,
        R,
        R_diag,
        R_inv,
        T_ASSIM,
        T_SPINUP,
        n_obs_times,
        n_steps,
        obs_times,
        obs_times_idx,
        observations,
        rng,
        t_assim,
        truth,
        x_bg,
        x_start,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 3  3DVAR — Three-Dimensional Variational Assimilation

        ### Theory

        3DVAR finds the analysis $\mathbf{x}^a$ by minimising the **cost function**

        $$
        \mathcal{J}(\mathbf{x}) =
        \underbrace{\frac{1}{2}(\mathbf{x} - \mathbf{x}^b)^T \mathbf{B}^{-1}(\mathbf{x} - \mathbf{x}^b)}_{\mathcal{J}_b \text{ — background term}}
        +
        \underbrace{\frac{1}{2}(\mathbf{y} - H\mathbf{x})^T \mathbf{R}^{-1}(\mathbf{y} - H\mathbf{x})}_{\mathcal{J}_o \text{ — observation term}}
        $$

        - $\mathbf{x}^b \in \mathbb{R}^n$ — background (prior) state
        - $\mathbf{B} \in \mathbb{R}^{n \times n}$ — background error covariance
        - $\mathbf{y} \in \mathbb{R}^m$ — observation vector
        - $H: \mathbb{R}^n \to \mathbb{R}^m$ — observation operator
        - $\mathbf{R} \in \mathbb{R}^{m \times m}$ — observation error covariance

        **Analytic solution** (linear $H$):
        $$
        \mathbf{x}^a = \mathbf{x}^b + \mathbf{K}(\mathbf{y} - H\mathbf{x}^b), \quad
        \mathbf{K} = \mathbf{B} H^T (H \mathbf{B} H^T + \mathbf{R})^{-1}
        $$

        The gradient needed by the minimiser is:
        $$
        \nabla_{\mathbf{x}} \mathcal{J} = \mathbf{B}^{-1}(\mathbf{x} - \mathbf{x}^b) - H^T \mathbf{R}^{-1}(\mathbf{y} - H\mathbf{x})
        $$

        ### Key limitations

        * **Atemporal**: uses observations at a single time — no memory of the trajectory.
        * **Static $\mathbf{B}$**: does not adapt to the flow of the day.
        * Simple to implement and fast — still used operationally in many regional NWP systems.
        """
    )
    return


@app.cell
def _(B, B_inv, DT_MODEL, R_inv, integrate_l63, np, obs_times_idx, observations, t_assim, truth, x_bg):
    def var3d_cost_and_grad(x, xb, B_inv, y_obs, H, R_inv):
        """3DVAR cost function J and its gradient ∇J."""
        innov = y_obs - H @ x
        bg_departure = x - xb
        J  = 0.5 * bg_departure @ B_inv @ bg_departure + 0.5 * innov @ R_inv @ innov
        dJ = B_inv @ bg_departure - H.T @ R_inv @ innov
        return J, dJ

    def run_3dvar(xb, B_inv, obs_seq, obs_idx, R_inv, t_grid, dt):
        """
        Cycling 3DVAR: at each observation time, assimilate the observation,
        then propagate the analysis forward to the next observation time.
        """
        H = np.eye(3)   # observe all components
        x_curr = xb.copy()
        analyses  = []
        fcst_traj = []

        for k, idx in enumerate(obs_idx):
            y_k = obs_seq[k]
            t_start = t_grid[idx] if k == 0 else t_grid[obs_idx[k - 1]]
            t_end   = t_grid[idx]

            # Forecast to obs time (except at k=0 we are already there)
            if k > 0:
                _dt_seg = t_end - t_start
                t_seg   = np.linspace(0, _dt_seg, max(2, int(round(_dt_seg / dt)) + 1))
                segment = integrate_l63(x_curr, (0, _dt_seg), t_seg)
                fcst_traj.append((t_start, t_end, t_seg, segment))
                x_curr  = segment[-1]

            # Minimise J
            res = minimize(
                var3d_cost_and_grad,
                x_curr,
                jac=True,
                args=(x_curr, B_inv, y_k, H, R_inv),
                method="L-BFGS-B",
                options={"maxiter": 200, "ftol": 1e-12, "gtol": 1e-8},
            )
            x_curr = res.x
            analyses.append((t_grid[idx], x_curr.copy()))

        return analyses, fcst_traj

    analyses_3dvar, _ = run_3dvar(
        x_bg, B_inv, observations, obs_times_idx, R_inv, t_assim, DT_MODEL
    )

    # Reconstruct full trajectory from analyses
    # Propagate each analysis to the next obs time
    traj_3dvar = np.full_like(truth, np.nan)
    traj_3dvar[0] = x_bg
    for _k in range(len(analyses_3dvar) - 1):
        _t0, _xa = analyses_3dvar[_k]
        _t1, _   = analyses_3dvar[_k + 1]
        _ddt     = _t1 - _t0
        _seg_t   = np.linspace(0, _ddt, max(2, int(round(_ddt / DT_MODEL)) + 1))
        _seg     = integrate_l63(_xa, (0, _ddt), _seg_t)
        _i0      = obs_times_idx[_k]
        _i1      = obs_times_idx[_k + 1]
        _n       = min(len(_seg), _i1 - _i0 + 1)
        traj_3dvar[_i0:_i0 + _n] = _seg[:_n]

    # RMSE at analysis times
    rmse_3dvar_bg = np.sqrt(np.mean(
        [(truth[obs_times_idx[k]] - x_bg if k == 0 else
          truth[obs_times_idx[k]] - analyses_3dvar[k - 1][1])**2
         for k in range(len(analyses_3dvar))]
    ))
    rmse_3dvar_an = np.sqrt(np.mean(
        [(truth[obs_times_idx[k]] - xa)**2
         for k, (_, xa) in enumerate(analyses_3dvar)]
    ))
    print(f"3DVAR | Background RMSE: {rmse_3dvar_bg:.3f}  Analysis RMSE: {rmse_3dvar_an:.3f}")
    return analyses_3dvar, rmse_3dvar_an, rmse_3dvar_bg, run_3dvar, traj_3dvar, var3d_cost_and_grad


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 3DVAR — Results""")
    return


@app.cell(hide_code=True)
def _(analyses_3dvar, np, obs_times, obs_times_idx, observations, plt, t_assim, truth, x_bg):
    _fig, _axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)
    _labels = ["x", "y", "z"]
    _colors = ["tab:blue", "tab:orange", "tab:green"]

    for _i in range(3):
        _ax = _axes[_i]
        _ax.plot(t_assim, truth[:, _i], "k-", lw=1.5, label="Truth")
        _ax.plot(
            obs_times, observations[:, _i],
            ".", color="gray", ms=4, alpha=0.6, label="Obs"
        )
        # background trajectory (free forecast from perturbed IC)
        _ax.axhline(x_bg[_i], ls="--", color="salmon", lw=1, label="Background IC")
        # analysis points
        _an_times = [t for t, _ in analyses_3dvar]
        _an_vals  = [xa[_i] for _, xa in analyses_3dvar]
        _ax.plot(_an_times, _an_vals, "o", color=_colors[_i],
                 ms=5, zorder=5, label="3DVAR analysis")
        _ax.set_ylabel(_labels[_i], fontsize=12)
        _ax.legend(loc="upper right", fontsize=7, ncol=4)
    _axes[-1].set_xlabel("time")
    _fig.suptitle("3DVAR: Cycling Analysis vs Truth", fontsize=13)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 4  4DVAR — Four-Dimensional Variational Assimilation

        ### Theory

        4DVAR extends 3DVAR to **a time window** $[t_0, t_N]$.
        We seek the initial condition $\mathbf{x}_0$ that, when propagated by the model
        $\mathcal{M}$, best fits *all* observations in the window:

        $$
        \mathcal{J}(\mathbf{x}_0) =
        \frac{1}{2}(\mathbf{x}_0 - \mathbf{x}_0^b)^T \mathbf{B}^{-1}(\mathbf{x}_0 - \mathbf{x}_0^b)
        +
        \sum_{k=0}^{N}
        \frac{1}{2}(\mathbf{y}_k - H\mathbf{x}_k)^T \mathbf{R}^{-1}(\mathbf{y}_k - H\mathbf{x}_k)
        $$

        where $\mathbf{x}_k = \mathcal{M}_{0 \to t_k}(\mathbf{x}_0)$.

        **Gradient** requires the **adjoint model** $\mathcal{M}^{\ast}$ (backward integration):

        $$
        \nabla_{\mathbf{x}_0}\mathcal{J} = \mathbf{B}^{-1}(\mathbf{x}_0 - \mathbf{x}_0^b) +
        \mathcal{M}^{\ast}_{t_N \to t_0}\left[
        \sum_k H^T \mathbf{R}^{-1}(\mathbf{y}_k - H\mathbf{x}_k)\delta(t - t_k)
        \right]
        $$

        Here we approximate the gradient via **finite differences** (also called
        implicit-differentiation / ensemble gradient in some contexts). For production
        systems, an actual adjoint code is used.

        ### Advantage over 3DVAR
        * Uses observations distributed over a **time window** → the model trajectory is
          simultaneously fit to multiple obs times.
        * Implicitly captures **flow-dependent** error growth during the window via the
          model's nonlinear dynamics.
        """
    )
    return


@app.cell
def _(B_inv, DT_MODEL, R_inv, integrate_l63, np, obs_times_idx, observations, t_assim, truth, x_bg):
    def _linspace_seg(t_end, dt):
        n = max(2, int(round(t_end / dt)) + 1)
        return np.linspace(0.0, t_end, n)

    def var4d_cost_and_grad(x0, xb, B_inv, obs_window, obs_idx_window, t_grid, dt, R_inv, eps=1e-5):
        """
        4DVAR cost J and gradient ∇J w.r.t. x0.
        Gradient computed via finite differences (approximates adjoint).
        """
        H = np.eye(3)
        n = len(x0)

        def _J(x0_):
            t_end = t_grid[obs_idx_window[-1]]
            Jb = 0.5 * (x0_ - xb) @ B_inv @ (x0_ - xb)
            Jo = 0.0
            if t_end < dt * 0.5:
                # Degenerate single-obs window at t=0: no model propagation needed
                for k, idx in enumerate(obs_idx_window):
                    innov = obs_window[k] - H @ x0_
                    Jo   += 0.5 * innov @ R_inv @ innov
            else:
                t_seg = _linspace_seg(t_end, dt)
                traj  = integrate_l63(x0_, (0.0, t_end), t_seg)
                for k, idx in enumerate(obs_idx_window):
                    # map obs time to nearest traj index
                    ti = t_grid[idx]
                    li = min(int(round(ti / dt)), len(traj) - 1)
                    innov = obs_window[k] - H @ traj[li]
                    Jo   += 0.5 * innov @ R_inv @ innov
            return Jb + Jo

        J0 = _J(x0)
        grad = np.zeros(n)
        for _j in range(n):
            x_p      = x0.copy(); x_p[_j] += eps
            grad[_j] = (_J(x_p) - J0) / eps
        return J0, grad

    def run_4dvar(xb, B_inv, obs_seq, obs_idx, R_inv, t_grid, dt, window_size=5):
        """
        Cycling 4DVAR: assimilate 'window_size' observations at a time,
        then advance the analysis to the start of the next window.
        """
        x_curr   = xb.copy()
        analyses = []
        n_obs    = len(obs_idx)

        for k in range(0, n_obs, window_size):
            win_end     = min(k + window_size, n_obs)
            win_obs_idx = obs_idx[k:win_end] - obs_idx[k]   # relative indices
            win_obs     = obs_seq[k:win_end]
            t_start     = t_grid[obs_idx[k]]
            t_win_end   = t_grid[obs_idx[win_end - 1]] - t_start
            t_win       = _linspace_seg(t_win_end, dt)

            res = minimize(
                var4d_cost_and_grad,
                x_curr,
                jac=True,
                args=(x_curr, B_inv, win_obs, win_obs_idx, t_win, dt, R_inv),
                method="L-BFGS-B",
                options={"maxiter": 100, "ftol": 1e-10, "gtol": 1e-6},
            )
            x0_opt = res.x
            analyses.append((t_start, x0_opt.copy()))

            # Propagate to end of window → becomes background for next
            if win_end < n_obs:
                t_advance = t_grid[obs_idx[win_end]] - t_start
                seg       = integrate_l63(x0_opt, (0.0, t_advance), _linspace_seg(t_advance, dt))
                x_curr    = seg[-1]

        return analyses

    analyses_4dvar = run_4dvar(
        x_bg, B_inv, observations, obs_times_idx, R_inv, t_assim, DT_MODEL, window_size=5
    )

    # Reconstruct trajectory from 4DVAR analyses
    traj_4dvar = np.full_like(truth, np.nan)
    traj_4dvar[0] = x_bg
    for _k in range(len(analyses_4dvar) - 1):
        _t0, _xa = analyses_4dvar[_k]
        _t1, _   = analyses_4dvar[_k + 1]
        _dt      = _t1 - _t0
        _seg     = integrate_l63(_xa, (0.0, _dt), _linspace_seg(_dt, DT_MODEL))
        _i0      = int(round(_t0 / DT_MODEL))
        _n       = min(len(_seg), int(round(_dt / DT_MODEL)) + 1)
        traj_4dvar[_i0:_i0 + _n] = _seg[:_n]

    rmse_4dvar = np.sqrt(np.mean(
        [(truth[obs_times_idx[k * 5]] - xa)**2
         for k, (_, xa) in enumerate(analyses_4dvar)
         if k * 5 < len(obs_times_idx)]
    ))
    print(f"4DVAR | Analysis RMSE at window starts: {rmse_4dvar:.3f}")
    return (
        analyses_4dvar,
        rmse_4dvar,
        run_4dvar,
        traj_4dvar,
        var4d_cost_and_grad,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 4DVAR — Results""")
    return


@app.cell(hide_code=True)
def _(analyses_4dvar, np, obs_times, obs_times_idx, observations, plt, t_assim, truth, x_bg):
    _fig, _axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)
    _labels = ["x", "y", "z"]
    _colors = ["tab:blue", "tab:orange", "tab:green"]
    _win = 5   # window_size used above

    for _i in range(3):
        _ax = _axes[_i]
        _ax.plot(t_assim, truth[:, _i], "k-", lw=1.5, label="Truth")
        _ax.plot(obs_times, observations[:, _i], ".", color="gray",
                 ms=4, alpha=0.5, label="Obs")
        _ax.axhline(x_bg[_i], ls="--", color="salmon", lw=1, label="Background IC")
        _an_times = [t for t, _ in analyses_4dvar]
        _an_vals  = [xa[_i] for _, xa in analyses_4dvar]
        _ax.plot(_an_times, _an_vals, "s", color=_colors[_i],
                 ms=6, zorder=5, label="4DVAR analysis (window start)")
        _ax.set_ylabel(_labels[_i], fontsize=12)
        _ax.legend(loc="upper right", fontsize=7, ncol=4)
    _axes[-1].set_xlabel("time")
    _fig.suptitle("4DVAR: Cycling Analysis vs Truth", fontsize=13)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 5  Ensemble Kalman Filter (EnKF)

        ### Theory

        The EnKF (Evensen 1994) replaces the static **B** with a **flow-dependent**
        background error covariance estimated from an ensemble of $N$ model trajectories:

        $$
        \mathbf{B}^f \approx \mathbf{P}^f = \frac{1}{N-1}\sum_{i=1}^{N}
        (\mathbf{x}^f_i - \bar{\mathbf{x}}^f)(\mathbf{x}^f_i - \bar{\mathbf{x}}^f)^T
        $$

        **Forecast step**: propagate each ensemble member through the model:
        $$
        \mathbf{x}^f_i(t+1) = \mathcal{M}(\mathbf{x}^a_i(t))
        $$

        **Analysis step** (perturbed-observation EnKF):
        $$
        \mathbf{x}^a_i = \mathbf{x}^f_i + \mathbf{K}(\mathbf{y}_i - H\mathbf{x}^f_i), \quad
        \mathbf{y}_i = \mathbf{y} + \boldsymbol{\epsilon}_i, \quad
        \boldsymbol{\epsilon}_i \sim \mathcal{N}(0, \mathbf{R})
        $$
        $$
        \mathbf{K} = \mathbf{P}^f H^T (H \mathbf{P}^f H^T + \mathbf{R})^{-1}
        $$

        ### Key strengths
        * Fully nonlinear forecast step — no adjoint needed.
        * $\mathbf{P}^f$ adapts to the local geometry of the attractor (e.g., collapses onto
          the unstable manifold).
        * Natural framework for ensemble forecasting.

        ### Practical notes
        * **Ensemble size** $N$ is critical: too small → **rank deficiency** and
          **spurious long-range correlations** → filter divergence.
        * Remedies: **inflation** (multiply $\mathbf{P}^f$ by $1 + \delta$) and
          **localisation** (Gaspari–Cohn taper).
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    N_ens = mo.ui.slider(start=10, stop=100, step=10, value=20, label="Ensemble size N")
    inflation = mo.ui.slider(start=1.0, stop=1.5, step=0.05, value=1.05,
                             label="Inflation factor α")
    mo.vstack([
        mo.md("**Interactive controls** — change these and the EnKF results below will update:"),
        mo.hstack([N_ens, inflation]),
    ])
    return N_ens, inflation


@app.cell
def _(
    B_diag,
    DT_MODEL,
    N_ens,
    R,
    inflation,
    integrate_l63,
    np,
    obs_times_idx,
    observations,
    rng,
    t_assim,
    truth,
    x_start,
):
    def run_enkf(x_start, N, B_diag, obs_seq, obs_idx, R, t_grid, dt, alpha=1.05):
        """
        Perturbed-observation EnKF with multiplicative inflation α.
        Returns ensemble mean trajectory and spread at each obs time.
        """
        n_state = 3
        H       = np.eye(n_state)

        # Initialise ensemble around true IC with background uncertainty
        ensemble = x_start + rng.normal(0, np.sqrt(B_diag), (N, n_state))
        means, spreads, analyses = [], [], []
        prev_idx = 0

        for k, idx in enumerate(obs_idx):
            # ── Forecast: advance each member from prev_idx to idx ────────
            dt_seg   = t_grid[idx] - t_grid[prev_idx]
            if dt_seg > 0:
                t_seg = np.linspace(0, dt_seg, max(2, int(round(dt_seg / dt)) + 1))
                new_ens = np.array([
                    integrate_l63(ensemble[i], (0, dt_seg), t_seg)[-1]
                    for i in range(N)
                ])
            else:
                new_ens = ensemble.copy()

            # ── Inflate ───────────────────────────────────────────────────
            xf_mean = new_ens.mean(axis=0)
            new_ens = xf_mean + alpha * (new_ens - xf_mean)

            # ── Compute Pf ────────────────────────────────────────────────
            Xf  = new_ens - xf_mean           # (N, 3) anomalies
            Pf  = (Xf.T @ Xf) / (N - 1)      # (3, 3) sample covariance

            # ── Kalman gain ───────────────────────────────────────────────
            S   = H @ Pf @ H.T + R            # (3, 3)
            K   = Pf @ H.T @ np.linalg.inv(S) # (3, 3)

            # ── Analysis ─────────────────────────────────────────────────
            y_pert   = obs_seq[k] + rng.multivariate_normal(np.zeros(3), R, N)
            ensemble = new_ens + (y_pert - (H @ new_ens.T).T) @ K.T

            xa_mean = ensemble.mean(axis=0)
            spread  = np.sqrt(np.mean(np.var(ensemble, axis=0)))
            means.append(xa_mean)
            spreads.append(spread)
            analyses.append((t_grid[idx], xa_mean.copy(), ensemble.copy()))
            prev_idx = idx

        return analyses, means, spreads

    enkf_results, enkf_means, enkf_spreads = run_enkf(
        x_start, N_ens.value, B_diag, observations, obs_times_idx,
        R, t_assim, DT_MODEL, alpha=inflation.value
    )

    # Evaluate RMSE
    rmse_enkf = np.sqrt(np.mean(
        [(truth[obs_times_idx[k]] - m)**2
         for k, m in enumerate(enkf_means)]
    ))
    print(f"EnKF (N={N_ens.value}, α={inflation.value}) | Analysis RMSE: {rmse_enkf:.3f}")
    return enkf_means, enkf_results, enkf_spreads, rmse_enkf, run_enkf


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### EnKF — Results""")
    return


@app.cell(hide_code=True)
def _(enkf_results, enkf_spreads, np, obs_times, observations, plt, t_assim, truth):
    _fig, _axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)
    _labels = ["x", "y", "z"]
    _colors = ["tab:blue", "tab:orange", "tab:green"]

    for _i in range(3):
        _ax = _axes[_i]
        _ax.plot(t_assim, truth[:, _i], "k-", lw=1.5, label="Truth")
        _ax.plot(obs_times, observations[:, _i], ".", color="gray",
                 ms=4, alpha=0.5, label="Obs")

        _an_times = [t for t, _, _ in enkf_results]
        _an_means = [xa[_i] for _, xa, _ in enkf_results]
        _an_spreads = [
            np.std([ens[j, _i] for j in range(ens.shape[0])])
            for _, _, ens in enkf_results
        ]
        _ax.plot(_an_times, _an_means, "^", color=_colors[_i],
                 ms=5, zorder=5, label="EnKF mean")
        _ax.fill_between(
            _an_times,
            np.array(_an_means) - np.array(_an_spreads),
            np.array(_an_means) + np.array(_an_spreads),
            alpha=0.2, color=_colors[_i], label="±1 std"
        )
        _ax.set_ylabel(_labels[_i], fontsize=12)
        _ax.legend(loc="upper right", fontsize=7, ncol=5)
    _axes[-1].set_xlabel("time")
    _fig.suptitle("EnKF: Ensemble Mean ± Spread vs Truth", fontsize=13)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 6  Side-by-Side Comparison

        Let's put all three methods on the same plot and compare their RMSE.
        """
    )
    return


@app.cell(hide_code=True)
def _(
    analyses_3dvar,
    analyses_4dvar,
    enkf_means,
    enkf_results,
    np,
    obs_times,
    obs_times_idx,
    observations,
    plt,
    rmse_3dvar_an,
    rmse_4dvar,
    rmse_enkf,
    t_assim,
    truth,
):
    _fig = plt.figure(figsize=(14, 10))
    _gs  = _fig.add_gridspec(4, 3, hspace=0.45, wspace=0.35)

    _labels = ["x", "y", "z"]
    _methods = ["3DVAR", "4DVAR", "EnKF"]
    _rmses   = [rmse_3dvar_an, rmse_4dvar, rmse_enkf]
    _colors  = ["tab:red", "tab:purple", "tab:cyan"]

    def _get_vals(method, comp):
        if method == "3DVAR":
            return (
                [t for t, _ in analyses_3dvar],
                [xa[comp] for _, xa in analyses_3dvar],
            )
        elif method == "4DVAR":
            return (
                [t for t, _ in analyses_4dvar],
                [xa[comp] for _, xa in analyses_4dvar],
            )
        else:
            return (
                [t for t, _, _ in enkf_results],
                [xa[comp] for _, xa, _ in enkf_results],
            )

    for _col, (_method, _col_color, _rmse) in enumerate(zip(_methods, _colors, _rmses)):
        for _row, _lbl in enumerate(_labels):
            _ax = _fig.add_subplot(_gs[_row, _col])
            _ax.plot(t_assim, truth[:, _row], "k-", lw=1.2, alpha=0.7)
            _ax.plot(obs_times, observations[:, _row], ".", color="lightgray",
                     ms=3, alpha=0.5)
            _t, _v = _get_vals(_method, _row)
            _ax.plot(_t, _v, "o", color=_col_color, ms=4, label=_method)
            _ax.set_ylabel(_lbl, fontsize=10)
            if _row == 0:
                _ax.set_title(f"{_method}\nRMSE={_rmse:.3f}", fontsize=10,
                              color=_col_color, fontweight="bold")
            if _row == 2:
                _ax.set_xlabel("time", fontsize=9)

    # RMSE bar chart
    _ax_bar = _fig.add_subplot(_gs[3, :])
    _bars   = _ax_bar.bar(_methods, _rmses, color=_colors, edgecolor="k", width=0.4)
    for _bar, _r in zip(_bars, _rmses):
        _ax_bar.text(_bar.get_x() + _bar.get_width() / 2,
                     _bar.get_height() + 0.005,
                     f"{_r:.3f}", ha="center", va="bottom", fontsize=11)
    _ax_bar.set_ylabel("Analysis RMSE", fontsize=11)
    _ax_bar.set_title("RMSE Comparison", fontsize=11)
    _ax_bar.set_ylim(0, max(_rmses) * 1.3)

    _fig.suptitle("Data Assimilation Methods — Lorenz 63 Testbed", fontsize=14, y=1.01)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 7  Ensemble Spread vs Error — Reliability Diagram

        A well-calibrated ensemble should have **spread ≈ RMSE** at each analysis time.
        This is the cornerstone of probabilistic DA and ensemble NWP.
        """
    )
    return


@app.cell(hide_code=True)
def _(enkf_results, enkf_spreads, np, obs_times, obs_times_idx, plt, truth):
    _errors = [np.linalg.norm(truth[obs_times_idx[k]] - xa)
               for k, (_, xa, _) in enumerate(enkf_results)]

    _fig, _axes = plt.subplots(1, 2, figsize=(11, 4))

    _axes[0].plot(obs_times, _errors, "k-o", ms=4, label="Analysis error ‖eₐ‖")
    _axes[0].plot(obs_times, enkf_spreads, "b--s", ms=4, label="Ensemble spread σ")
    _axes[0].set_xlabel("time"); _axes[0].set_ylabel("magnitude")
    _axes[0].set_title("Spread vs Error over time")
    _axes[0].legend()

    _axes[1].scatter(_errors, enkf_spreads, c=obs_times, cmap="viridis", s=30, alpha=0.8)
    _lim = max(max(_errors), max(enkf_spreads)) * 1.05
    _axes[1].plot([0, _lim], [0, _lim], "r--", lw=1.5, label="Perfect calibration")
    _axes[1].set_xlabel("Analysis error"); _axes[1].set_ylabel("Ensemble spread")
    _axes[1].set_title("Reliability: spread vs error")
    _axes[1].legend()

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 8  Observation Impact — Sensitivity to Observation Frequency

        How does the analysis quality degrade as we observe less frequently?
        """
    )
    return


@app.cell
def _(
    B_diag,
    B_inv,
    DT_MODEL,
    R,
    R_inv,
    integrate_l63,
    np,
    observations,
    obs_times_idx,
    plt,
    rng,
    run_3dvar,
    run_enkf,
    t_assim,
    truth,
    x_bg,
    x_start,
):
    _dt_obs_list  = [0.1, 0.2, 0.3, 0.5, 0.8]
    _rmse_3dvar_v = []
    _rmse_enkf_v  = []

    for _dt_obs in _dt_obs_list:
        _step   = max(1, int(_dt_obs / DT_MODEL))
        _oi     = np.arange(0, len(t_assim), _step)
        _ot     = t_assim[_oi]
        _obs    = truth[_oi] + rng.normal(0, 2.0, (len(_oi), 3))

        _an3  = run_3dvar(x_bg, B_inv, _obs, _oi, R_inv, t_assim, DT_MODEL)
        _r3   = np.sqrt(np.mean([(truth[_oi[k]] - xa)**2
                                  for k, (_, xa) in enumerate(_an3[0])]))
        _rmse_3dvar_v.append(_r3)

        _ank, _, _ = run_enkf(x_start, 20, B_diag, _obs, _oi, R, t_assim, DT_MODEL)
        _re  = np.sqrt(np.mean([(truth[_oi[k]] - xa)**2
                                 for k, (_, xa, _) in enumerate(_ank)]))
        _rmse_enkf_v.append(_re)

    _fig, _ax = plt.subplots(figsize=(7, 4))
    _ax.plot(_dt_obs_list, _rmse_3dvar_v, "o-", color="tab:red",  label="3DVAR")
    _ax.plot(_dt_obs_list, _rmse_enkf_v,  "^-", color="tab:cyan", label="EnKF (N=20)")
    _ax.set_xlabel("Observation interval Δt_obs")
    _ax.set_ylabel("Analysis RMSE")
    _ax.set_title("RMSE vs Observation Frequency")
    _ax.legend()
    _ax.grid(alpha=0.3)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 9  Key Takeaways

        | Feature | 3DVAR | 4DVAR | EnKF |
        |---------|-------|-------|------|
        | **Background covariance** | Static $\mathbf{B}$ | Static $\mathbf{B}$ | Flow-dependent $\mathbf{P}^f$ |
        | **Temporal scope** | Single time | Time window | Sequential |
        | **Model adjoint** | Not required | Required (or FD) | Not required |
        | **Ensemble** | No | No | Yes |
        | **Parallelism** | Low | Low | High (member level) |
        | **Typical use** | Regional NWP, fast cycling | Global NWP (ECMWF) | Ensemble NWP, ocean, land |

        ### Connections to ML you already know

        * **3DVAR** is Tikhonov-regularised least squares — the same as Ridge Regression
          with $\mathbf{B}^{-1}$ as the regularisation matrix.
        * **4DVAR** is **backpropagation through time** (BPTT) for a physics model —
          the adjoint is exactly the reverse-mode AD graph.
        * **EnKF** is a **Monte-Carlo Kalman Filter** — analogous to particle methods
          in Bayesian deep learning.
        * Modern hybrid systems (e.g. ECMWF's IFS-AIFS) combine 4DVAR with neural
          emulators for the forecast model, making the adjoint tractable via AD frameworks.

        ### Further reading

        * Kalnay, E. (2003). *Atmospheric Modeling, Data Assimilation and Predictability*. Cambridge.
        * Evensen, G. (2009). *Data Assimilation: The Ensemble Kalman Filter*. Springer.
        * Bocquet, M. et al. (2023). *A guide to ensemble Kalman methods with implementation
          in Python*. arXiv:2305.00087.
        * Bauer, P. et al. (2015). The quiet revolution of NWP. *Nature*, 525, 47–55.
        """
    )
    return


if __name__ == "__main__":
    app.run()
