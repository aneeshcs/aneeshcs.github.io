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

To edit:
    uvx marimo edit lorenz63_ensemble_explorer.py
"""

import marimo

__generated_with = "0.19.10"
app = marimo.App(width="full", app_title="Lorenz 63: Chaos & Predictability")


# ---------------------------------------------------------------------------
# Imports + shared Lorenz function
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
# Attractor reference trajectory — computed once, reused in all sections
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# UI controls — defined in dedicated cells so their .value can be read
# reactively by the display cells below
# ---------------------------------------------------------------------------
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
        label="Log₁₀ perturbation size  δ₀",
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


# ===========================================================================
# DISPLAY CELL 0 — Title and overview
# ===========================================================================
@app.cell
def display_title(mo):
    return mo.vstack([
        mo.md(r"""
# 🦋 Chaos, Predictability, and Ensemble Forecasting

**FERS Summer School 2026 — Weather & Climate Predictability**

This tutorial accompanies the lecture on chaos and predictability.
Scroll from top to bottom and interact with each panel before
reading the explanation beneath it — building intuition by *doing*
is more effective than reading first.

---

### How to read this notebook

| Symbol | Meaning |
|--------|---------|
| ⚙️ **Controls** | Sliders and dropdowns you manipulate |
| 📐 **Theory** | Background equations and concepts |
| 🔬 **Experiment** | Step-by-step activity |
| 💡 **Observation** | Live readout that updates as you explore |

> **Unit convention:** One *model time unit* (MTU) corresponds to
> approximately **5 days** in the real atmosphere.  All time axes
> in this notebook use MTU.
"""),
    ])


# ===========================================================================
# DISPLAY CELL 1 — The Lorenz (1963) System
# ===========================================================================
@app.cell
def display_section1(attractor_ref, go, mo):

    # ---- build the attractor figure ----
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
        height=520,
        title=dict(
            text="The Lorenz Strange Attractor  (σ = 10, ρ = 28, β = 8/3) — colour = Z",
            x=0.5, font_size=13,
        ),
        scene=dict(
            xaxis_title="X  (convective intensity)",
            yaxis_title="Y  (temperature contrast)",
            zaxis_title="Z  (vertical distortion)",
            bgcolor="rgba(245,248,255,0.9)",
            camera=dict(eye=dict(x=1.6, y=1.0, z=0.8)),
        ),
        margin=dict(l=0, r=0, t=55, b=0),
        paper_bgcolor="white",
        showlegend=False,
    )

    return mo.vstack([

        mo.md(r"""
---
## 1 · The Lorenz (1963) System

In 1963 Edward Lorenz published a three-variable model of **Rayleigh–Bénard convection** —
the buoyancy-driven overturning of a fluid heated from below.
Despite its simplicity, it became the founding example of *deterministic chaos*.

### The governing equations

$$\frac{dX}{dt} = \sigma\,(Y - X)$$
$$\frac{dY}{dt} = X\,(\rho - Z) - Y$$
$$\frac{dZ}{dt} = X\,Y - \beta\,Z$$

**What the variables represent:**

| Variable | Physical meaning |
|----------|-----------------|
| $X$ | Intensity of the convective overturning circulation |
| $Y$ | Temperature difference between ascending and descending fluid |
| $Z$ | Deviation of the vertical temperature profile from linearity |

**Classic parameter values** that produce chaotic behaviour:

| Parameter | Value | Physical role |
|-----------|-------|--------------|
| $\sigma = 10$ | Prandtl number (momentum vs. thermal diffusivity) |
| $\rho = 28$ | Normalised Rayleigh number (strength of forcing) |
| $\beta = 8/3$ | Geometric factor (aspect ratio of convection cells) |

### The strange attractor

For these parameters the system is *chaotic*: trajectories are **bounded** (they
stay on the attractor forever) but **never periodic** (they never exactly repeat).
The geometric object they trace out is called a **strange attractor**.

The visualisation below shows 70 MTU of trajectory after transients have decayed.
The colour encodes the height variable $Z$ — notice how the trajectory alternates
between the two lobes (the "butterfly wings"), each corresponding to one
sense of convective overturning.

> 💡 **Tip:** Click and drag on the plot to rotate it in 3-D.
> Zoom in to see the fine fractal structure of the attractor.
"""),

        _fig,

        mo.callout(
            mo.md(r"""
**What makes this attractor "strange"?**  A periodic orbit would be a closed loop.
A fixed point would be a dot.  This attractor is *neither* — it is a fractal set with
non-integer dimension (~2.06).  Trajectories wind around the two lobes in an order that
looks random but is in fact *completely determined* by the initial condition.
The catch: two trajectories starting from almost identical initial conditions will
eventually end up on opposite lobes with no correlation between them.
That is precisely what the next section demonstrates.
"""),
            kind="info",
        ),
    ])


# ===========================================================================
# DISPLAY CELL 2 — Sensitive Dependence on Initial Conditions
# ===========================================================================
@app.cell
def display_section2(
    attractor_ref, attractor_size, go, lorenz, mo, np, sep_exp, sdic_lead, solve_ivp,
):
    # ---- compute two nearby trajectories ----
    _x0 = np.array([8.5, 8.5, 27.0])          # near centre of right lobe
    _delta0 = 10.0 ** sep_exp.value
    _T = sdic_lead.value
    _t_eval = np.linspace(0, _T, 800)

    _sol_a = solve_ivp(lorenz, (0, _T), _x0,
                       t_eval=_t_eval, method="RK45", rtol=1e-10, atol=1e-13)
    _sol_b = solve_ivp(lorenz, (0, _T), _x0 + np.array([_delta0, 0.0, 0.0]),
                       t_eval=_t_eval, method="RK45", rtol=1e-10, atol=1e-13)
    _traj_a = _sol_a.y
    _traj_b = _sol_b.y
    _sep = np.sqrt(np.sum((_traj_a - _traj_b) ** 2, axis=0))

    # ---- estimate Lyapunov exponent from early exponential growth ----
    _early = (_t_eval < _T / 3) & (_sep > 0)
    if _early.sum() > 5 and _sep[_early][0] > 0:
        _log_sep = np.log(_sep[_early] + 1e-20)
        _slope, _ = np.polyfit(_t_eval[_early], _log_sep, 1)
        _lambda_est = max(0.0, float(_slope))
        _lambda_str = f"{_lambda_est:.2f} MTU⁻¹ (≈ {_lambda_est / 5:.2f} day⁻¹)"
    else:
        _lambda_est = None
        _lambda_str = "— (extend lead time to see exponential growth)"

    # ---- live stats ----
    _final_sep = float(_sep[-1])
    _frac = _final_sep / attractor_size
    if _frac > 0.8:
        _regime = "🔴 Forecasts completely uncorrelated — beyond predictability horizon"
        _ck = "danger"
    elif _frac > 0.3:
        _regime = "🟠 Diverging rapidly — entering semi-predictable regime"
        _ck = "warn"
    else:
        _regime = "🟢 Forecasts still agree — within predictable window"
        _ck = "success"

    # ---- phase-space figure ----
    _fig3d = go.Figure()
    _fig3d.add_trace(go.Scatter3d(
        x=attractor_ref[0], y=attractor_ref[1], z=attractor_ref[2],
        mode="lines",
        line=dict(color="rgba(180,180,180,0.15)", width=1),
        showlegend=False, hoverinfo="skip",
    ))
    _fig3d.add_trace(go.Scatter3d(
        x=_traj_a[0], y=_traj_a[1], z=_traj_a[2],
        mode="lines", line=dict(color="royalblue", width=2.5),
        name="Truth (A)",
    ))
    _fig3d.add_trace(go.Scatter3d(
        x=_traj_b[0], y=_traj_b[1], z=_traj_b[2],
        mode="lines", line=dict(color="crimson", width=2.5),
        name="Perturbed forecast (B)",
    ))
    _fig3d.add_trace(go.Scatter3d(
        x=[_traj_a[0, 0]], y=[_traj_a[1, 0]], z=[_traj_a[2, 0]],
        mode="markers", marker=dict(size=8, color="limegreen"),
        name=f"Shared start  (δ₀ = 10^{sep_exp.value:.1f})",
    ))
    _fig3d.add_trace(go.Scatter3d(
        x=[_traj_a[0, -1]], y=[_traj_a[1, -1]], z=[_traj_a[2, -1]],
        mode="markers", marker=dict(size=7, color="royalblue", symbol="square"),
        name=f"A at t = {_T} MTU",
    ))
    _fig3d.add_trace(go.Scatter3d(
        x=[_traj_b[0, -1]], y=[_traj_b[1, -1]], z=[_traj_b[2, -1]],
        mode="markers", marker=dict(size=7, color="crimson", symbol="square"),
        name=f"B at t = {_T} MTU",
    ))
    _fig3d.update_layout(
        height=480,
        title=dict(
            text="Phase-space view — two trajectories from (almost) the same start",
            x=0.5, font_size=13,
        ),
        scene=dict(
            xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
            bgcolor="rgba(245,248,255,0.6)",
            camera=dict(eye=dict(x=1.5, y=1.0, z=0.8)),
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor="white",
        legend=dict(x=0.01, y=0.99, font_size=11,
                    bgcolor="rgba(255,255,255,0.88)"),
    )

    # ---- separation time-series figure ----
    _fig2d = go.Figure()
    _fig2d.add_trace(go.Scatter(
        x=_t_eval, y=_sep,
        mode="lines",
        line=dict(color="darkorchid", width=2.5),
        fill="tozeroy", fillcolor="rgba(148,0,211,0.07)",
        name="|A − B|",
    ))
    # theoretical exponential growth line
    if _lambda_est and _lambda_est > 0:
        _t_ref = _t_eval[_early]
        _sep_ref_start = float(_sep[_early][0])
        _fig2d.add_trace(go.Scatter(
            x=_t_ref,
            y=_sep_ref_start * np.exp(_lambda_est * (_t_ref - _t_ref[0])),
            mode="lines",
            line=dict(color="orange", width=1.5, dash="dot"),
            name=f"e^(λt),  λ ≈ {_lambda_est:.2f} MTU⁻¹",
        ))
    _fig2d.add_hline(
        y=attractor_size,
        line=dict(color="firebrick", dash="dash", width=1.5),
        annotation_text="Attractor diameter — fully random",
        annotation_position="top left",
        annotation_font_size=11,
    )
    _fig2d.update_layout(
        height=480,
        title=dict(
            text="Separation |A − B| over time  (log-scale y-axis)",
            x=0.5, font_size=13,
        ),
        xaxis=dict(title="Lead time (MTU)", gridcolor="#ebebeb"),
        yaxis=dict(title="Euclidean distance |A − B|", type="log",
                   gridcolor="#ebebeb"),
        margin=dict(l=60, r=20, t=50, b=50),
        paper_bgcolor="white",
        legend=dict(x=0.01, y=0.01, font_size=11,
                    bgcolor="rgba(255,255,255,0.88)"),
    )

    return mo.vstack([

        mo.md(r"""
---
## 2 · Sensitive Dependence on Initial Conditions

The defining signature of chaos is that two trajectories starting from
**arbitrarily close** initial conditions diverge exponentially fast.
This is called *sensitive dependence on initial conditions* (SDIC) —
colloquially, the **butterfly effect**.

### The mathematics of error growth

If $\delta_0 = |A(0) - B(0)|$ is the initial separation, it grows (on average) as

$$\delta(t) \approx \delta_0 \, e^{\,\lambda \, t}$$

where $\lambda > 0$ is the **leading Lyapunov exponent** — the characteristic rate
of exponential error growth.  For the Lorenz system, $\lambda \approx 0.9\;\text{MTU}^{-1}$.

**Key consequence:** Even if $\delta_0$ is made *infinitesimally* small,
$\delta(t)$ eventually becomes comparable to the size of the attractor itself.
At that point the two forecasts share no useful information — knowing trajectory
A tells you nothing about trajectory B.

### What the two panels show

| Left panel | Right panel |
|------------|-------------|
| Both trajectories in 3-D phase space | Separation $|A - B|$ vs time on a **log scale** |
| Green dot = shared start; coloured squares = positions at lead time $T$ | A straight line on the log-scale = pure exponential growth |
| When paths overlap they are predictable; when they separate they are not | The orange dotted line shows the fitted $e^{\lambda t}$ slope |
"""),

        mo.callout(
            mo.md(r"""
**🔬 Experiment — measure the Lyapunov exponent:**

1. Set lead time = **5 MTU** and δ₀ = **10⁻⁴**.
   Are the blue and red paths still together?
2. Drag lead time slowly to **20 MTU**.
   At what time do they part ways on the 3-D plot?
   Does the right panel enter "exponential growth" (straight line)?
3. Now reduce δ₀ to **10⁻⁶** (two decades smaller).
   How many extra MTU of predictability does that buy?
   Is the gain proportional to the change in δ₀?
4. The slope of the log-separation curve ≈ λ.
   Read off λ from the orange dotted line.
   Compare it to the theoretical value of ≈ 0.9 MTU⁻¹.
"""),
            kind="neutral",
        ),

        mo.md("### ⚙️ Controls"),
        mo.hstack([sep_exp, sdic_lead], gap="4rem"),
        mo.hstack([_fig3d, _fig2d], widths=[3, 2]),

        mo.callout(
            mo.md(
                f"**💡 Live readout** &nbsp;|&nbsp; "
                f"δ₀ = 10^{sep_exp.value:.1f} &nbsp;·&nbsp; "
                f"Lead time = {_T} MTU &nbsp;·&nbsp; "
                f"Final separation = **{_final_sep:.3g}** "
                f"({_frac:.0%} of attractor size)  \n"
                f"Estimated λ from early growth: **{_lambda_str}**  \n"
                f"{_regime}"
            ),
            kind=_ck,
        ),

        mo.md(r"""
### Why this matters for weather forecasting

In the real atmosphere the leading Lyapunov exponent is $\lambda \approx 0.35\;\text{day}^{-1}$,
giving an error **doubling time** of

$$\tau_{2} = \frac{\ln 2}{\lambda} \approx \frac{0.69}{0.35\;\text{day}^{-1}} \approx 2\;\text{days}$$

This means that even a perfect 1-hour analysis error doubles in two days.
A 10-day forecast must survive five doublings — an amplification factor of $2^5 = 32$.
No conceivable improvement in observations or models can eliminate this growth,
because it is a property of the underlying flow, not of our instruments.
"""),
    ])


# ===========================================================================
# DISPLAY CELL 3 — Ensemble Forecasting
# ===========================================================================
@app.cell
def display_section3(
    attractor_ref, attractor_size, go, ic_choice, lead_time,
    lorenz, mo, n_members, np, perturb_exp, solve_ivp,
):
    # ---- ensemble integration ----
    _ic_map = {
        "predictable": np.array([8.5,  8.5, 27.0]),
        "saddle":      np.array([0.1,  0.1,  0.1]),
        "chaotic":     np.array([-5.0, -7.0, 22.0]),
    }
    _ic_labels = {
        "predictable": "near lobe centre — relatively stable region",
        "saddle":      "near origin — highly unstable saddle point",
        "chaotic":     "lobe-transition zone — rapid lobe switching",
    }
    _x0 = _ic_map[ic_choice.value]
    _N = n_members.value
    _T = lead_time.value
    _pert = 10.0 ** perturb_exp.value
    _t_eval = np.linspace(0, _T, 600)

    np.random.seed(42)
    _perturbs = np.random.randn(_N, 3) * _pert
    _trajs = np.zeros((_N, 3, len(_t_eval)))
    for _i in range(_N):
        _sol = solve_ivp(
            lorenz, (0, _T), _x0 + _perturbs[_i],
            t_eval=_t_eval, method="RK45", rtol=1e-9, atol=1e-12,
        )
        _trajs[_i] = _sol.y

    _std = np.std(_trajs, axis=0)
    _rms_spread = np.sqrt(np.mean(_std ** 2, axis=0))
    _t_max = float(_t_eval[-1])

    # predictability horizon indices
    _idx_10 = np.where(_rms_spread >= 0.1 * attractor_size)[0]
    _idx_90 = np.where(_rms_spread >= 0.9 * attractor_size)[0]
    _t10 = float(_t_eval[_idx_10[0]]) if len(_idx_10) else _t_max
    _t90 = float(_t_eval[_idx_90[0]]) if len(_idx_90) else _t_max

    _final_sat = float(_rms_spread[-1] / attractor_size)
    if _final_sat < 0.3:
        _regime = "🟢 Ensemble well-clustered — forecast trustworthy"
        _ck = "success"
    elif _final_sat < 0.8:
        _regime = "🟠 Spread growing rapidly — probabilistic guidance only"
        _ck = "warn"
    else:
        _regime = "🔴 Spread saturated — forecast is climatology"
        _ck = "danger"

    # ---- phase-space figure ----
    _fig3d = go.Figure()
    _fig3d.add_trace(go.Scatter3d(
        x=attractor_ref[0], y=attractor_ref[1], z=attractor_ref[2],
        mode="lines",
        line=dict(color="rgba(160,160,160,0.18)", width=1),
        showlegend=False, hoverinfo="skip",
    ))
    for _i in range(_N):
        _hue = int(200 + 130 * _i / max(_N - 1, 1))
        _show = _i < 5
        _fig3d.add_trace(go.Scatter3d(
            x=_trajs[_i, 0], y=_trajs[_i, 1], z=_trajs[_i, 2],
            mode="lines",
            line=dict(color=f"hsla({_hue},65%,50%,0.65)", width=1.8),
            name=f"Member {_i+1}" if _show else "",
            showlegend=_show, hoverinfo="skip",
        ))
    _fig3d.add_trace(go.Scatter3d(
        x=_trajs[:, 0, 0], y=_trajs[:, 1, 0], z=_trajs[:, 2, 0],
        mode="markers",
        marker=dict(size=5, color="limegreen", opacity=0.9),
        name="t = 0  (initial cloud, green)",
    ))
    _fig3d.add_trace(go.Scatter3d(
        x=_trajs[:, 0, -1], y=_trajs[:, 1, -1], z=_trajs[:, 2, -1],
        mode="markers",
        marker=dict(size=5, color="crimson", opacity=0.9),
        name=f"t = {_T} MTU  (final cloud, red)",
    ))
    _fig3d.update_layout(
        height=520,
        title=dict(
            text=f"Ensemble in phase space  |  IC: {_ic_labels[ic_choice.value]}",
            x=0.5, font_size=12,
        ),
        scene=dict(
            xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
            camera=dict(eye=dict(x=1.5, y=1.2, z=0.9)),
            bgcolor="rgba(245,248,255,0.6)",
        ),
        margin=dict(l=0, r=0, t=55, b=0),
        legend=dict(x=0.01, y=0.99, font_size=10,
                    bgcolor="rgba(255,255,255,0.85)"),
        paper_bgcolor="white",
    )

    # ---- spread time-series figure ----
    _fig2d = go.Figure()
    _fig2d.add_trace(go.Scatter(
        x=_t_eval, y=_rms_spread,
        mode="lines",
        line=dict(color="#1a3a6e", width=2.5),
        name="RMS spread",
        fill="tozeroy",
        fillcolor="rgba(26,58,110,0.08)",
    ))
    _fig2d.add_hline(
        y=attractor_size,
        line=dict(color="firebrick", dash="dash", width=1.5),
        annotation_text="Attractor size — fully unpredictable",
        annotation_position="top left",
        annotation_font_size=11,
    )
    _fig2d.add_hline(
        y=0.1 * attractor_size,
        line=dict(color="darkorange", dash="dot", width=1.5),
        annotation_text="10 % saturation threshold",
        annotation_position="bottom right",
        annotation_font_size=11,
    )
    for _shade in [
        dict(x0=0,    x1=_t10,  color="rgba(0,180,0,0.08)",   label="🟢 Predictable"),
        dict(x0=_t10, x1=_t90,  color="rgba(255,165,0,0.08)", label="🟠 Semi-predictable"),
        dict(x0=_t90, x1=_t_max, color="rgba(220,0,0,0.08)",  label="🔴 Unpredictable"),
    ]:
        if _shade["x0"] < _shade["x1"]:
            _fig2d.add_vrect(
                x0=_shade["x0"], x1=_shade["x1"],
                fillcolor=_shade["color"], line_width=0,
                annotation_text=_shade["label"],
                annotation_position="top left",
                annotation_font_size=10,
            )
    _fig2d.update_layout(
        height=520,
        title=dict(
            text=(
                f"Ensemble spread  |  N = {_N}  ·  "
                f"δ₀ = 10^{perturb_exp.value:.1f}  ·  T = {_T} MTU"
            ),
            font_size=12, x=0.5, xanchor="center",
        ),
        margin=dict(l=5, r=5, t=55, b=5),
        paper_bgcolor="white",
    )
    _fig2d.update_xaxes(title_text="Lead time (MTU)", gridcolor="#e8e8e8")
    _fig2d.update_yaxes(title_text="RMS ensemble spread", type="log",
                        gridcolor="#e8e8e8")

    return mo.vstack([

        mo.md(r"""
---
## 3 · Ensemble Forecasting

A single deterministic forecast is an *answer without an error bar*.
The operational response to SDIC is the **ensemble forecast**: instead of
integrating one trajectory from the best-guess initial state, integrate
$N$ slightly different trajectories from initial states that sample the
analysis uncertainty.

### What the ensemble tells us

The **ensemble mean** is a better point forecast than any single member.
The **ensemble spread** — the RMS standard deviation across members — is a
direct measure of forecast uncertainty.

$$\sigma_\text{spread}(t) = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left|X_i(t) - \bar X(t)\right|^2}$$

Three regimes are marked on the spread plot:

| Regime | Spread / attractor size | Interpretation |
|--------|------------------------|---------------|
| 🟢 **Predictable** | < 10 % | Members closely clustered; deterministic forecast reliable |
| 🟠 **Semi-predictable** | 10 – 90 % | Spread growing fast; probabilistic guidance still useful |
| 🔴 **Unpredictable** | > 90 % | Spread saturated; forecast no better than climatology |

### What the two panels show

**Left (phase space):** The green cloud is the ensemble at $t = 0$ — all members start
near the same point.  The red cloud is the ensemble at $t = T$.  A compact red cloud
means the forecast is still reliable.  A red cloud spanning the whole attractor means
the forecast has no skill.

**Right (spread plot):** The blue curve is $\sigma_\text{spread}(t)$ on a log scale.
The dashed red line marks the attractor diameter.  The coloured shading shows the
three predictability regimes.  The x-position of the 🟢→🟠 transition is the
**predictability horizon**.
"""),

        mo.callout(
            mo.md(r"""
**🔬 Experiment — find the predictability horizon:**

1. Start with defaults (predictable region, δ₀ = 10⁻⁴, N = 20).
   Drag **lead time** slowly from 1 → 30 MTU.
   Note the time when the green cloud (left) turns into a red cloud
   that fills the whole attractor.  Does the spread plot enter the 🔴 zone
   at the same time?

2. Change **starting location** to *Near saddle point*.
   Is the predictability horizon earlier or later?
   Why might the position on the attractor matter?

3. Fix lead time = 15.  Slide **perturbation size** from 10⁻⁶ → 10⁻¹.
   Does reducing δ₀ by one decade give you a proportionally longer horizon?
   (It shouldn't — why not?)

4. Fix lead time = 15 and δ₀ = 10⁻⁴.  Compare **N = 5** vs **N = 50**.
   Which gives a smoother, more reliable spread estimate?
   ECMWF uses 51 members — does that seem justified?
"""),
            kind="neutral",
        ),

        mo.md("### ⚙️ Controls"),
        mo.hstack([ic_choice, n_members], gap="3rem"),
        mo.hstack([perturb_exp, lead_time], gap="3rem"),

        mo.hstack([_fig3d, _fig2d], widths=[1, 1]),

        mo.callout(
            mo.md(
                f"**💡 Live readout** &nbsp;|&nbsp; "
                f"N = {_N} members &nbsp;·&nbsp; "
                f"δ₀ = 10^{perturb_exp.value:.1f} &nbsp;·&nbsp; "
                f"T = {_T} MTU  \n"
                f"Predictability horizon (spread > 10 %): **t ≈ {_t10:.1f} MTU**  \n"
                f"Final saturation: **{_final_sat:.0%}** of attractor size  \n"
                f"{_regime}"
            ),
            kind=_ck,
        ),
    ])


# ===========================================================================
# DISPLAY CELL 4 — Connection to the Real Atmosphere
# ===========================================================================
@app.cell
def display_section4(mo):
    return mo.vstack([

        mo.md(r"""
---
## 4 · Connection to the Real Atmosphere

The Lorenz model is a toy, but its key numbers map onto the real atmosphere
with surprising fidelity.

### Lyapunov numbers: model vs. atmosphere

| Quantity | Lorenz 63 | Real atmosphere |
|----------|-----------|----------------|
| Leading Lyapunov exponent $\lambda$ | ≈ 0.9 MTU⁻¹ | ≈ 0.35 day⁻¹ |
| Error doubling time $\ln 2 / \lambda$ | ≈ 0.8 MTU | ≈ 2 days |
| Predictability horizon (spread > 10 %) | ≈ 3–5 MTU | ≈ 1–2 weeks |
| Full saturation | ≈ 6–9 MTU | ≈ 3–4 weeks |

With 1 MTU ≈ 5 days, ECMWF achieves useful deterministic skill to about 10 days —
roughly 2 MTU, or about 2.5 e-folding times.

### The diminishing return of better observations

Suppose you improve your analysis error from $\delta_0$ to $\delta_0 / 10$.
The extra predictable time gained is

$$\Delta t = \frac{\ln 10}{\lambda} \approx \frac{2.3}{0.35\;\text{day}^{-1}} \approx 6.5\;\text{days}$$

A factor-of-10 improvement in observational accuracy buys only about 6 extra days.
A factor of 100 improvement (two decades) buys only 13 extra days.
This logarithmic ceiling means that the atmospheric predictability limit of
≈ 2–3 weeks is fundamental, **not** a consequence of inadequate technology.

### Predictability of the second kind

Everything above is **predictability of the first kind**: initial-value prediction
of a specific trajectory.  There is also a **second kind**: predicting the *response
of the attractor to a sustained external forcing* (in the atmosphere, a change in
greenhouse-gas concentration or sea-surface temperature).

In the Lorenz system, individual trajectories become unpredictable after ≈ 5–8 MTU,
but if you change $\rho$ (the forcing parameter), the *time-mean* of $X$ shifts
systematically — and that shift can be predicted even when individual trajectories
cannot.  This is the mathematical analogue of the climate-vs-weather distinction:

| Predictability type | Question asked | Chaotic limit applies? |
|---------------------|----------------|----------------------|
| **1st kind** | Where will this air mass be in 10 days? | Yes — hard ceiling |
| **2nd kind** | How will the *average* temperature change if CO₂ doubles? | No — signal persists |

Climate projections are a predictability-of-the-second-kind problem.
Their uncertainty comes from *model structural error* and *scenario uncertainty*,
not from the butterfly effect.
"""),

        mo.callout(
            mo.md(r"""
**Key take-aways from this tutorial**

1. **Chaos is irreducible:** SDIC means that no finite improvement in initial
   conditions can extend deterministic forecast skill indefinitely.
   The atmosphere has a hard predictability ceiling near 2–3 weeks.

2. **Ensembles are the correct response:** A probabilistic forecast communicates
   the *distribution* of possible futures honestly.  A deterministic forecast
   beyond the predictability horizon is overconfident by construction.

3. **The two kinds of predictability are different problems:**
   Weather forecasting (1st kind) is limited by chaos.
   Climate projection (2nd kind) is not — but it faces other sources of uncertainty.

4. **Improving observations has diminishing returns:**
   Each decade of improvement in $\delta_0$ buys only $\ln(10)/\lambda$ extra days.
   For the atmosphere that is ≈ 6.5 days per decade of observational improvement.
"""),
            kind="info",
        ),
    ])


# ===========================================================================
# DISPLAY CELL 5 — Guided Questions
# ===========================================================================
@app.cell
def display_questions(mo):
    return mo.vstack([

        mo.md(r"""
---
## 📝 Guided Questions

Work through these with a neighbour (~15 min).  We will discuss as a group.

---

**Q1 — Predictability horizon** *(Section 3)*

Set δ₀ = 10⁻⁴, N = 20, starting location = *Predictable region*.
Drag lead time slowly from 1 → 30 MTU.

- At what lead time does the green start-cloud scatter across the entire attractor?
- Which colour zone does the spread plot enter at that point?
- Switch to *Chaotic lobe transition*.  Is the horizon earlier or later?
  Why might some regions of the attractor be more predictable than others?

---

**Q2 — Sensitivity to perturbation size** *(Section 3)*

Fix lead time = 15 MTU.  Slide δ₀ from 10⁻⁶ → 10⁻¹.

- Does reducing δ₀ by **one decade** give you a proportionally longer horizon?
- Using $\lambda \approx 0.9\;\text{MTU}^{-1}$, calculate how much extra
  predictable time one decade of improvement should give:
  $\Delta t = \ln(10)/\lambda = ?$
  Does your experiment agree?
- What does this imply about the practical benefit of improving atmospheric
  observations by an order of magnitude?

---

**Q3 — Ensemble size** *(Section 3)*

Fix lead time = 15 MTU and δ₀ = 10⁻⁴.  Compare N = 5 vs N = 50.

- How *noisy* is the spread estimate with N = 5?
  Could you reliably identify the predictability horizon from it?
- At what N does the spread curve look smooth enough to trust?
- ECMWF's operational ensemble uses 51 members.
  Based on your experiments, does that number seem justified?

---

**Q4 — Quantitative connection to the real atmosphere** *(Section 2 & 4)*

The error e-folding time in L63 is ≈ 0.8 MTU ≈ 4 days.
ECMWF achieves useful skill to ≈ 10 days.

- How many e-folding times is a 10-day forecast?
- If ECMWF could reduce analysis error by a factor of 100
  (two decades of observational improvement), how many extra days of
  deterministic predictability would that buy?
  Use $\Delta t = \ln(100) / 0.35\;\text{day}^{-1}$.
- Is this gain worth the cost of a factor-100 improvement in observations?

---

**Q5 — Predictability of the second kind** *(Section 4, bonus)*

Set starting location = *Near saddle point*, δ₀ = 10⁻⁶, N = 20.
Watch the ensemble saturate — individual trajectories become completely uncorrelated.

- Suppose you care not about any specific trajectory but about the
  **long-run time-average** of $X$.  Would that remain predictable
  even after the Lorenz time?  Why?
- Suppose someone changed the forcing parameter $\rho$ from 28 to 30.
  The attractor would shift.  Could you predict the *new* time-mean of $X$
  even though individual trajectories are still chaotic?
- How does this connect to the distinction between weather forecasting
  (**predictability of the 1st kind**) and climate projection
  (**predictability of the 2nd kind**)?

---

*System: Lorenz (1963), σ = 10, ρ = 28, β = 8/3.*
*Integration: RK45 (scipy), rtol = 10⁻⁹.*
*Ensemble perturbations: iid Gaussian with seed = 42.*
*1 MTU ≈ 5 days in the real atmosphere.*
"""),

    ])


if __name__ == "__main__":
    app.run()
