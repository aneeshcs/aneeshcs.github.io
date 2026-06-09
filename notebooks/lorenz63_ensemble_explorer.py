# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.19.10",
#   "numpy",
#   "scipy",
#   "plotly",
# ]
# ///
"""
Lorenz 63: Chaos, Predictability, and Ensemble Forecasting
FERS Summer School 2026 — Weather & Climate Predictability

Interactive tutorial notebook.

To run:
    uvx marimo run lorenz63_ensemble_explorer.py

To edit interactively:
    uvx marimo edit lorenz63_ensemble_explorer.py
"""

import marimo

__generated_with = "0.19.10"
app = marimo.App(width="full", app_title="Lorenz 63: Chaos & Predictability")


# ---------------------------------------------------------------------------
# Imports — define the Lorenz function once, share it across all cells
# ---------------------------------------------------------------------------
@app.cell
def imports():
    import marimo as mo
    import numpy as np
    from scipy.integrate import solve_ivp
    import plotly.graph_objects as go

    _sigma, _rho, _beta = 10.0, 28.0, 8.0 / 3.0

    def lorenz(t, s):
        x, y, z = s
        return [_sigma * (y - x), x * (_rho - z) - y, x * y - _beta * z]

    return go, lorenz, mo, np, solve_ivp


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
@app.cell
def title(mo):
    return mo.md(r"""
    # 🦋 Chaos, Predictability, and Ensemble Forecasting

    **FERS Summer School 2026 — Weather & Climate Predictability**

    This tutorial follows the lecture on predictability and chaos.
    Work through each section in order — each interactive panel lets you
    manipulate the physics in real time and build intuition before reading
    the explanation beneath it.

    > **One model time unit (MTU) ≈ 5 days in the real atmosphere.**
    """)


# ===========================================================================
# SECTION 1 — The Lorenz (1963) System
# ===========================================================================
@app.cell
def section1(mo):
    return mo.md(r"""
    ---
    ## 1 · The Lorenz (1963) System

    In 1963, Edward Lorenz showed that a drastically simplified model of
    Rayleigh–Bénard thermal convection is *chaotic*. The system has three
    variables — $X$ (convective overturning intensity), $Y$ (temperature
    contrast between ascending and descending air), and $Z$ (distortion of
    the vertical temperature profile):

    $$\frac{dX}{dt} = \sigma\,(Y - X)$$

    $$\frac{dY}{dt} = X\,(\rho - Z) - Y$$

    $$\frac{dZ}{dt} = X\,Y - \beta\,Z$$

    We use the classic parameters $\sigma = 10$, $\rho = 28$, $\beta = 8/3$.
    For these values the system is chaotic: solutions are bounded but never
    periodic.  The long-run trajectory traces out the **Lorenz strange attractor**
    shown below.

    **Rotate the plot** by clicking and dragging.  Notice the two "butterfly
    wings" — trajectories wind around one lobe, then the other, in an
    apparently random order.
    """)


@app.cell
def compute_attractor(lorenz, np, solve_ivp):
    _sol = solve_ivp(
        lorenz, (0, 80), [1.0, 1.0, 1.0],
        t_eval=np.linspace(10, 80, 8000),
        method="RK45", rtol=1e-9, atol=1e-12,
    )
    attractor_ref = _sol.y
    attractor_size = float(np.mean(np.std(attractor_ref, axis=1)))
    return attractor_ref, attractor_size


@app.cell
def fig_attractor(attractor_ref, go):
    _fig = go.Figure(go.Scatter3d(
        x=attractor_ref[0], y=attractor_ref[1], z=attractor_ref[2],
        mode="lines",
        line=dict(
            color=attractor_ref[2],
            colorscale="Viridis",
            width=1.5,
            cmin=float(attractor_ref[2].min()),
            cmax=float(attractor_ref[2].max()),
        ),
        hoverinfo="skip",
    ))
    _fig.update_layout(
        height=500,
        title=dict(
            text="The Lorenz Strange Attractor  (σ = 10, ρ = 28, β = 8/3)",
            x=0.5, font_size=14,
        ),
        scene=dict(
            xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
            bgcolor="rgba(245,248,255,0.8)",
            camera=dict(eye=dict(x=1.6, y=1.0, z=0.8)),
        ),
        margin=dict(l=0, r=0, t=55, b=0),
        paper_bgcolor="white",
        showlegend=False,
    )
    return _fig


@app.cell
def attractor_callout(mo):
    return mo.callout(
        mo.md(
            "**Key observation:** The trajectory is *bounded* — it stays on the "
            "attractor forever — but *never repeats*.  Which lobe it visits next, "
            "and exactly when it switches, cannot be predicted beyond a finite "
            "time horizon.  That horizon is what we will measure in this tutorial."
        ),
        kind="info",
    )


# ===========================================================================
# SECTION 2 — Sensitive Dependence on Initial Conditions
# ===========================================================================
@app.cell
def section2(mo):
    return mo.md(r"""
    ---
    ## 2 · Sensitive Dependence on Initial Conditions

    The defining property of chaos is **sensitive dependence on initial
    conditions (SDIC)**: two trajectories that start arbitrarily close
    together diverge exponentially fast.  If the initial separation is
    $\delta_0$, it grows (on average) as

    $$\delta(t) \approx \delta_0\,e^{\,\lambda\, t}$$

    where $\lambda > 0$ is the **Lyapunov exponent**.  For the Lorenz system,
    $\lambda \approx 0.9\,\text{MTU}^{-1}$, so errors roughly *double* every
    $\ln 2 / \lambda \approx 0.8$ MTU — about 4 days in the real atmosphere.

    No matter how small $\delta_0$ is, $\delta(t)$ eventually reaches the
    diameter of the attractor, after which the two forecasts are completely
    uncorrelated.  **Improving observations can delay, but never eliminate,
    this limit.**

    ---

    ### ▶ Activity: watch two forecasts diverge

    Both trajectories start at the same point on the attractor — one is the
    "truth", the other has a tiny initial error $\delta_0$.

    1. Set **lead time = 5 MTU**.  Are the two paths still close?
    2. Slowly drag lead time to **20 MTU**.  When do they part ways?
    3. Now reduce $\delta_0$ by two decades (from $10^{-4}$ to $10^{-6}$).
       How many extra MTU of predictability do you gain?
    """)


@app.cell
def sdic_controls(mo):
    sep_exp = mo.ui.slider(
        start=-8, stop=-1, step=0.5, value=-4,
        label="Log₁₀ initial separation  δ₀",
        show_value=True,
    )
    sdic_lead = mo.ui.slider(
        start=1, stop=30, step=1, value=10,
        label="Lead time (MTU)",
        show_value=True,
    )
    return sep_exp, sdic_lead


@app.cell
def display_sdic_controls(mo, sep_exp, sdic_lead):
    return mo.vstack([
        mo.md("### ⚙️ Controls — Sensitive Dependence"),
        mo.hstack([sep_exp, sdic_lead], gap="4rem"),
    ], gap="0.4rem")


@app.cell
def compute_sdic(lorenz, np, sep_exp, sdic_lead, solve_ivp):
    _x0 = np.array([8.5, 8.5, 27.0])
    _delta = 10.0 ** sep_exp.value
    _T = sdic_lead.value
    _t_eval = np.linspace(0, _T, 800)

    _sol_a = solve_ivp(lorenz, (0, _T), _x0,
                       t_eval=_t_eval, method="RK45", rtol=1e-10, atol=1e-13)
    _sol_b = solve_ivp(lorenz, (0, _T), _x0 + np.array([_delta, 0.0, 0.0]),
                       t_eval=_t_eval, method="RK45", rtol=1e-10, atol=1e-13)

    traj_a = _sol_a.y
    traj_b = _sol_b.y
    t_sdic = _t_eval
    sep_distance = np.sqrt(np.sum((_sol_a.y - _sol_b.y) ** 2, axis=0))
    return sep_distance, t_sdic, traj_a, traj_b


@app.cell
def fig_sdic_phase(attractor_ref, go, sdic_lead, traj_a, traj_b):
    _T = sdic_lead.value
    _fig = go.Figure()

    _fig.add_trace(go.Scatter3d(
        x=attractor_ref[0], y=attractor_ref[1], z=attractor_ref[2],
        mode="lines",
        line=dict(color="rgba(180,180,180,0.18)", width=1),
        showlegend=False, hoverinfo="skip",
    ))
    _fig.add_trace(go.Scatter3d(
        x=traj_a[0], y=traj_a[1], z=traj_a[2],
        mode="lines",
        line=dict(color="royalblue", width=2.5),
        name="Truth (A)",
    ))
    _fig.add_trace(go.Scatter3d(
        x=traj_b[0], y=traj_b[1], z=traj_b[2],
        mode="lines",
        line=dict(color="crimson", width=2.5),
        name="Perturbed forecast (B)",
    ))
    _fig.add_trace(go.Scatter3d(
        x=[traj_a[0, 0]], y=[traj_a[1, 0]], z=[traj_a[2, 0]],
        mode="markers",
        marker=dict(size=7, color="limegreen"),
        name="Shared start (t = 0)",
    ))
    _fig.add_trace(go.Scatter3d(
        x=[traj_a[0, -1]], y=[traj_a[1, -1]], z=[traj_a[2, -1]],
        mode="markers",
        marker=dict(size=7, color="royalblue", symbol="square"),
        name=f"A at t = {_T} MTU",
    ))
    _fig.add_trace(go.Scatter3d(
        x=[traj_b[0, -1]], y=[traj_b[1, -1]], z=[traj_b[2, -1]],
        mode="markers",
        marker=dict(size=7, color="crimson", symbol="square"),
        name=f"B at t = {_T} MTU",
    ))
    _fig.update_layout(
        height=480,
        title=dict(text="Two Nearly Identical Forecasts on the Attractor",
                   x=0.5, font_size=13),
        scene=dict(
            xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
            bgcolor="rgba(245,248,255,0.6)",
            camera=dict(eye=dict(x=1.5, y=1.0, z=0.8)),
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor="white",
        legend=dict(x=0.01, y=0.99, font_size=11,
                    bgcolor="rgba(255,255,255,0.85)"),
    )
    return _fig


@app.cell
def fig_sdic_spread(go, sep_distance, t_sdic):
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(
        x=t_sdic, y=sep_distance,
        mode="lines",
        line=dict(color="darkorchid", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(148,0,211,0.08)",
        name="|A − B|",
    ))
    _fig.update_layout(
        height=480,
        title=dict(text="Separation |A − B| Over Time  (log scale)",
                   x=0.5, font_size=13),
        xaxis=dict(title="Lead time (MTU)", gridcolor="#ebebeb"),
        yaxis=dict(title="Euclidean distance", type="log",
                   gridcolor="#ebebeb"),
        margin=dict(l=60, r=20, t=50, b=50),
        paper_bgcolor="white",
    )
    return _fig


@app.cell
def display_sdic(fig_sdic_phase, fig_sdic_spread, mo):
    return mo.hstack([fig_sdic_phase, fig_sdic_spread], widths=[3, 2])


@app.cell
def sdic_callout(mo, sep_distance, sep_exp, t_sdic, attractor_size):
    import numpy as _np
    _delta0 = 10.0 ** sep_exp.value
    _final_sep = float(sep_distance[-1])
    _ratio = _final_sep / attractor_size
    _growth = _final_sep / max(_delta0, 1e-15)

    return mo.callout(
        mo.md(
            f"Initial separation: **δ₀ = 10^{sep_exp.value:.1f}** · "
            f"Final separation: **{_final_sep:.3g}** · "
            f"Growth factor: **{_growth:.2g}×** · "
            f"Fraction of attractor size: **{_ratio:.2f}**  \n"
            f"{'🔴 Forecasts are uncorrelated — fully unpredictable.' if _ratio > 0.8 else '🟠 Diverging rapidly.' if _ratio > 0.3 else '🟢 Forecasts still agree.'}"
        ),
        kind="danger" if _ratio > 0.8 else "warn" if _ratio > 0.3 else "success",
    )


# ===========================================================================
# SECTION 3 — Ensemble Forecasting
# ===========================================================================
@app.cell
def section3(mo):
    return mo.md(r"""
    ---
    ## 3 · Ensemble Forecasting

    A single deterministic forecast says nothing about *how confident* we
    should be.  The operational answer is the **ensemble**: instead of
    integrating one trajectory from the best-guess initial state, we integrate
    $N$ trajectories from slightly perturbed initial states sampled from the
    analysis uncertainty.

    The **ensemble spread** — the root-mean-square standard deviation across
    members — measures how fast uncertainty grows.  When spread is small, the
    forecast is trustworthy; when it saturates at the size of the attractor,
    the forecast is climatology.

    The **right panel** below shows three regimes:
    - 🟢 **Predictable** — spread < 10 % of attractor size
    - 🟠 **Semi-predictable** — spread growing rapidly, 10–90 %
    - 🔴 **Unpredictable** — spread saturated, forecast no better than chance

    ---

    ### ▶ Activity: build your own ensemble

    Start with the default settings.  Then:

    1. Drag **lead time** slowly from 1 → 30.  Note when the green cloud (t = 0)
       turns into a red cloud (t = T) that fills the whole attractor.
    2. Change **starting location** to *Near saddle point*.  Does predictability
       increase or decrease?  Why might some regions of the attractor be more
       predictable than others?
    3. Reduce **perturbation size** by two decades.  How much extra predictable
       time do you gain?  Is the gain proportional?
    """)


@app.cell
def ens_controls(mo):
    ic_choice = mo.ui.dropdown(
        options={
            "Predictable region (near lobe center)": "predictable",
            "Near saddle point (unstable equilibrium)": "saddle",
            "Chaotic lobe transition": "chaotic",
        },
        value="Predictable region (near lobe center)",
        label="Starting location on attractor",
    )
    perturb_exp = mo.ui.slider(
        start=-6, stop=-1, step=0.5, value=-4,
        label="Log₁₀ perturbation size",
        show_value=True,
    )
    n_members = mo.ui.slider(
        start=5, stop=50, step=5, value=20,
        label="Ensemble size  N",
        show_value=True,
    )
    lead_time = mo.ui.slider(
        start=1, stop=30, step=1, value=10,
        label="Lead time (MTU)",
        show_value=True,
    )
    return ic_choice, lead_time, n_members, perturb_exp


@app.cell
def display_ens_controls(mo, ic_choice, perturb_exp, n_members, lead_time):
    return mo.vstack([
        mo.md("### ⚙️ Controls — Ensemble Forecast"),
        mo.hstack([ic_choice, n_members], gap="3rem"),
        mo.hstack([perturb_exp, lead_time], gap="3rem"),
    ], gap="0.4rem")


@app.cell
def compute_ensemble(
    attractor_ref, attractor_size, ic_choice, lead_time,
    lorenz, n_members, np, perturb_exp, solve_ivp,
):
    _ic_map = {
        "predictable": np.array([8.5,  8.5, 27.0]),
        "saddle":      np.array([0.1,  0.1,  0.1]),
        "chaotic":     np.array([-5.0, -7.0, 22.0]),
    }
    _x0 = _ic_map[ic_choice.value]
    _N = n_members.value
    _T = lead_time.value
    _pert = 10.0 ** perturb_exp.value
    _t_eval = np.linspace(0, _T, 600)

    np.random.seed(42)
    _perturbs = np.random.randn(_N, 3) * _pert
    trajs = np.zeros((_N, 3, len(_t_eval)))
    for _i in range(_N):
        _sol = solve_ivp(
            lorenz, (0, _T), _x0 + _perturbs[_i],
            t_eval=_t_eval, method="RK45", rtol=1e-9, atol=1e-12,
        )
        trajs[_i] = _sol.y

    _std = np.std(trajs, axis=0)
    rms_spread = np.sqrt(np.mean(_std ** 2, axis=0))
    t_eval = _t_eval
    return rms_spread, t_eval, trajs


@app.cell
def fig_ens_phase(attractor_ref, go, lead_time, n_members, trajs):
    _N = n_members.value
    _T = lead_time.value
    _fig = go.Figure()

    _fig.add_trace(go.Scatter3d(
        x=attractor_ref[0], y=attractor_ref[1], z=attractor_ref[2],
        mode="lines",
        line=dict(color="rgba(160,160,160,0.2)", width=1),
        showlegend=False, hoverinfo="skip",
    ))
    for _i in range(_N):
        _hue = int(200 + 130 * _i / max(_N - 1, 1))
        _show = _i < 5
        _fig.add_trace(go.Scatter3d(
            x=trajs[_i, 0], y=trajs[_i, 1], z=trajs[_i, 2],
            mode="lines",
            line=dict(color=f"hsla({_hue},65%,50%,0.7)", width=1.8),
            name=f"Member {_i+1}" if _show else "",
            showlegend=_show, hoverinfo="skip",
        ))
    _fig.add_trace(go.Scatter3d(
        x=trajs[:, 0, 0], y=trajs[:, 1, 0], z=trajs[:, 2, 0],
        mode="markers",
        marker=dict(size=5, color="limegreen", opacity=0.9),
        name="t = 0  (green)",
    ))
    _fig.add_trace(go.Scatter3d(
        x=trajs[:, 0, -1], y=trajs[:, 1, -1], z=trajs[:, 2, -1],
        mode="markers",
        marker=dict(size=5, color="crimson", opacity=0.9),
        name=f"t = {_T} MTU  (red)",
    ))
    _fig.update_layout(
        height=520,
        title=dict(text="Ensemble in Phase Space", x=0.5, font_size=13),
        scene=dict(
            xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
            camera=dict(eye=dict(x=1.5, y=1.2, z=0.9)),
            bgcolor="rgba(245,248,255,0.6)",
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(x=0.01, y=0.99, font_size=10,
                    bgcolor="rgba(255,255,255,0.8)"),
        paper_bgcolor="white",
    )
    return _fig


@app.cell
def fig_ens_spread(attractor_size, go, lead_time, n_members, np,
                   perturb_exp, rms_spread, t_eval):
    _N = n_members.value
    _T = lead_time.value
    _exp = perturb_exp.value
    _t_max = float(t_eval[-1])

    _idx_10 = np.where(rms_spread >= 0.1 * attractor_size)[0]
    _idx_90 = np.where(rms_spread >= 0.9 * attractor_size)[0]
    _t10 = float(t_eval[_idx_10[0]]) if len(_idx_10) else _t_max
    _t90 = float(t_eval[_idx_90[0]]) if len(_idx_90) else _t_max

    _fig = go.Figure()
    _fig.add_trace(go.Scatter(
        x=t_eval, y=rms_spread,
        mode="lines",
        line=dict(color="#1a3a6e", width=2.5),
        name="RMS spread",
        fill="tozeroy",
        fillcolor="rgba(26,58,110,0.08)",
    ))
    _fig.add_hline(
        y=attractor_size,
        line=dict(color="firebrick", dash="dash", width=1.5),
        annotation_text="Attractor size — fully unpredictable",
        annotation_position="top left",
        annotation_font_size=11,
    )
    _fig.add_hline(
        y=0.1 * attractor_size,
        line=dict(color="darkorange", dash="dot", width=1.5),
        annotation_text="10 % saturation",
        annotation_position="bottom right",
        annotation_font_size=11,
    )
    for _shade in [
        dict(x0=0,    x1=_t10,  color="rgba(0,180,0,0.07)",   label="🟢 Predictable"),
        dict(x0=_t10, x1=_t90,  color="rgba(255,165,0,0.07)", label="🟠 Semi-predictable"),
        dict(x0=_t90, x1=_t_max, color="rgba(220,0,0,0.07)",  label="🔴 Unpredictable"),
    ]:
        if _shade["x0"] < _shade["x1"]:
            _fig.add_vrect(
                x0=_shade["x0"], x1=_shade["x1"],
                fillcolor=_shade["color"], line_width=0,
                annotation_text=_shade["label"],
                annotation_position="top left",
                annotation_font_size=10,
            )
    _fig.update_layout(
        height=520,
        title=dict(
            text=(
                f"Ensemble spread  |  <b>N = {_N}</b>  ·  "
                f"δ₀ = 10<sup>{_exp:.1f}</sup>  ·  "
                f"T = <b>{_T}</b> MTU"
            ),
            font_size=13, x=0.5, xanchor="center",
        ),
        margin=dict(l=5, r=5, t=50, b=5),
        paper_bgcolor="white",
    )
    _fig.update_xaxes(title_text="Lead time (MTU)", gridcolor="#e8e8e8")
    _fig.update_yaxes(title_text="RMS ensemble spread", type="log",
                      gridcolor="#e8e8e8")
    return _fig


@app.cell
def display_ens(fig_ens_phase, fig_ens_spread, mo):
    return mo.hstack([fig_ens_phase, fig_ens_spread], widths=[1, 1])


@app.cell
def ens_callout(attractor_size, mo, np, rms_spread, t_eval):
    _idx = np.where(rms_spread >= 0.1 * attractor_size)[0]
    _horizon = float(t_eval[_idx[0]]) if len(_idx) else float(t_eval[-1])
    _sat = float(rms_spread[-1] / attractor_size)
    if _sat < 0.3:
        _msg = "🟢 Ensemble well-clustered — forecast still trustworthy."
        _kind = "success"
    elif _sat < 0.8:
        _msg = "🟠 Spread growing rapidly — forecast becoming uncertain."
        _kind = "warn"
    else:
        _msg = "🔴 Spread saturated — forecast is climatology."
        _kind = "danger"
    return mo.callout(
        mo.md(
            f"**Predictability horizon** (spread > 10 % of attractor size): "
            f"**t ≈ {_horizon:.1f} MTU**  ·  "
            f"Final saturation ratio: **{_sat:.2f}**  ·  {_msg}"
        ),
        kind=_kind,
    )


# ===========================================================================
# SECTION 4 — Connection to the Real Atmosphere
# ===========================================================================
@app.cell
def section4(mo):
    return mo.md(r"""
    ---
    ## 4 · Connection to the Real Atmosphere

    The Lorenz system is a toy model, but its key numbers map surprisingly
    well onto the real atmosphere:

    | Quantity | Lorenz 63 | Real atmosphere |
    |---|---|---|
    | Leading Lyapunov exponent $\lambda$ | ≈ 0.9 MTU⁻¹ | ≈ 0.35 day⁻¹ |
    | Error doubling time $\ln 2 / \lambda$ | ≈ 0.8 MTU | ≈ 2 days |
    | Saturation time (forecast → climatology) | ≈ 5–8 MTU | ≈ 2–3 weeks |

    Recalling that **1 MTU ≈ 5 days**, ECMWF's useful deterministic skill to
    ~10 days corresponds to about 2 MTU — less than 3 Lorenz times.
    The boundary between the "predictable" and "unpredictable" regimes you
    saw in the spread plot corresponds directly to the 10–15 day deterministic
    forecast ceiling.

    **Improving models or observations** can push that limit slightly by
    reducing $\delta_0$, but the exponential growth means each decade of
    improvement in initial-condition accuracy buys only $\ln(10)/\lambda
    \approx 2.6$ extra days.  The hard ceiling set by chaos is real.

    ---

    ### Predictability of the second kind

    Everything above is **predictability of the first kind**: initial-value
    prediction of a specific trajectory.  But there is a second kind:
    predicting the *response of the climate system to a sustained forcing*
    (e.g., increasing CO₂).

    In the Lorenz system, individual trajectories become unpredictable after
    ~5–8 MTU, but the *time-mean* of $X$ is determined by the shape of the
    attractor, which responds systematically to parameter changes ($\rho$,
    $\sigma$, $\beta$).  Predicting how that mean shifts is possible even
    when individual realizations are not — exactly the distinction between
    climate projection and weather forecasting.
    """)


@app.cell
def atmosphere_callout(mo):
    return mo.callout(
        mo.md(
            "**Take-away:** The ~10-day deterministic forecast ceiling is not a "
            "failure of models or observations — it is a mathematical consequence "
            "of the positive Lyapunov exponent of the atmosphere.  Ensemble "
            "forecasting and probabilistic output are the correct response: they "
            "communicate the *distribution* of possible futures, not a single "
            "misleading deterministic trajectory."
        ),
        kind="info",
    )


# ===========================================================================
# SECTION 5 — Guided Questions
# ===========================================================================
@app.cell
def guided_questions(mo):
    return mo.md(r"""
    ---
    ## 📝 Guided Questions

    Work through these with a neighbor (~15 min total).
    We will discuss as a group afterward.

    ---

    **Q1 — Predictability horizon**

    Set perturbation = 10⁻⁴, N = 20, starting location = *Predictable region*.
    Drag lead time slowly from 1 → 30.

    - At what lead time does the green start-cloud scatter across the full
      attractor?  Which colour zone does the spread plot enter at that point?
    - Switch to *Chaotic lobe transition*.  Is the horizon earlier or later?
      Why might the position on the attractor matter?

    ---

    **Q2 — Sensitivity to perturbation size**

    Fix lead time = 15.  Slide the perturbation from 10⁻⁶ → 10⁻¹.

    - Does reducing $\delta_0$ by **one decade** give you a proportionally
      longer predictable window?  Does the spread curve simply shift right,
      or does its slope change too?
    - What does this imply about the practical return on investment from
      improving observational networks by an order of magnitude?

    ---

    **Q3 — Ensemble size and sampling uncertainty**

    Fix lead time = 15 and perturbation = 10⁻⁴.  Compare N = 5 vs N = 50.

    - How stable (reproducible) is the spread estimate with N = 5?  Could
      you trust it for an operational probabilistic forecast?
    - At what N does the spread curve look reliably smooth to you?
    - ECMWF's operational ensemble uses 51 members.  Does that number seem
      justified based on what you see here?

    ---

    **Q4 — Connecting to the real atmosphere**

    The error e-folding time in L63 is ≈ 0.8 MTU ≈ 4 days.
    Useful ECMWF skill extends to ≈ 10 days.

    - How many e-folding times is a 10-day forecast?
    - What is the **fundamental upper limit** on useful deterministic
      forecasting, regardless of model resolution or data density?
    - If perfect observations could reduce analysis error by a factor of 100,
      how many extra days of predictability would that buy?
      (Hint: $\ln(100) / \lambda$ with $\lambda = 0.35\,\text{day}^{-1}$.)

    ---

    **Q5 — Predictability of the second kind** *(bonus)*

    Set starting location = *Near saddle point*, perturbation = 10⁻⁶.
    Watch the ensemble saturate — individual trajectories are completely
    unpredictable.

    - Now suppose you care not about a specific trajectory but about the
      *long-run time-average* of $X$.  Would that remain predictable even
      after the Lorenz time?  Why?
    - How does this connect to the distinction between **predictability of
      the 1st kind** (initial-value problem) and **predictability of the
      2nd kind** (forced response / climate projection)?

    ---

    *System: Lorenz (1963), σ = 10, ρ = 28, β = 8/3.  Integrated with
    RK45 (scipy), rtol = 10⁻⁹.  Ensemble members: iid Gaussian
    perturbations, seed = 42.  One MTU ≈ 5 days in the real atmosphere.*
    """)


if __name__ == "__main__":
    app.run()
