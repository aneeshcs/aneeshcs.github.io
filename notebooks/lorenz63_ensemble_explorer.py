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

This tutorial accompanies the lecture on chaos and predictability in the atmosphere.
Scroll from top to bottom and interact with each panel before
reading the explanation beneath it — building intuition by *doing*
is more effective than reading first.

---

### Learning objectives

By the end of this notebook you will be able to:

1. **Describe** the Lorenz (1963) system and explain what each variable represents physically
2. **Demonstrate** sensitive dependence on initial conditions (SDIC) by running your own experiments
3. **Measure** the leading Lyapunov exponent from the slope of the error-growth curve
4. **Explain** why ensemble forecasting is the correct operational response to SDIC
5. **Calculate** the gain in predictable time from a given improvement in observational accuracy
6. **Distinguish** predictability of the first kind (initial-value) from the second kind (forced response)

---

### How to read this notebook

| Symbol | Meaning |
|--------|---------|
| ⚙️ **Controls** | Sliders and dropdowns you manipulate |
| 📐 **Theory** | Background equations and concepts |
| 🔬 **Experiment** | Step-by-step activity |
| 💡 **Observation** | Live readout that updates as you explore |

---

### Tutorial structure

| Section | Topic | Key concept introduced |
|---------|-------|----------------------|
| **1** | The Lorenz (1963) system | Strange attractor, deterministic chaos |
| **2** | Sensitive dependence on initial conditions | Lyapunov exponent, butterfly effect |
| **3** | Ensemble forecasting | Predictability horizon, ensemble spread |
| **4** | Connection to the real atmosphere | Error doubling time, 2nd-kind predictability |
| **📝** | Guided questions | Synthesis and quantitative reasoning |

> **Unit convention:** One *model time unit* (MTU) corresponds to
> approximately **5 days** in the real atmosphere.  All time axes
> in this notebook use MTU.
"""),
    ])


# ===========================================================================
# MARKDOWN CELL — Historical context: Lorenz's accidental discovery
# ===========================================================================
@app.cell
def cell_lorenz_story(mo):
    return mo.md(r"""
---
### 🕰️ Historical context: how chaos was discovered by accident

In the winter of 1961, Edward Lorenz was running a primitive numerical weather model on the
Royal McBee LGP-30 computer at MIT.  He wanted to re-examine a particular simulation from the
middle, so instead of restarting from the beginning he typed in the intermediate values
from a printout — but he entered them rounded to three decimal places (0.506) instead of
the full six-digit precision (0.506127) stored in the computer's memory.

He expected the two runs to agree.  Instead, after a few simulated weeks, the two
solutions had **diverged completely** — not just a small discrepancy, but an entirely
different weather pattern.  At first he suspected a hardware fault.  Then the insight
hit: the tiny rounding error — about one part in a thousand — had grown exponentially
until it erased all predictive information.

> *"At this point I became rather excited.  It no longer seemed that predicting
> the weather for two weeks or a month would merely be a question of developing
> better equations."*
> — Edward Lorenz, *The Essence of Chaos* (1993)

This accidental discovery led directly to the 1963 paper that founded the mathematical
study of chaos.  The three-equation model in that paper was a deliberate simplification
of the full convection equations — a toy designed to be analytically tractable — but
it captured the essential unpredictability of the real atmosphere.

**The "butterfly effect" name** came a decade later.  At the December 1972 meeting of
the American Meteorological Society, Lorenz delivered a talk titled:

> *"Does the flap of a butterfly's wings in Brazil set off a tornado in Texas?"*

The title was chosen half-jokingly by the session organiser Philip Merilees, not by
Lorenz himself.  Lorenz used it to sharpen a point he had been making since 1963:
in a chaotic system, an *arbitrarily small* perturbation anywhere — even one too small
to measure — can, in principle, alter the large-scale evolution weeks later.
This is **not** a statement that butterflies literally cause tornadoes.
It is a statement about the *structure of deterministic predictability limits*.
""")


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

| Variable | Physical meaning | Units (non-dimensional) |
|----------|-----------------|------------------------|
| $X$ | Intensity of the convective overturning circulation | Proportional to fluid velocity |
| $Y$ | Temperature difference between ascending and descending fluid | Proportional to horizontal temperature gradient |
| $Z$ | Deviation of the vertical temperature profile from linearity | Proportional to departure from conductive equilibrium |

**Classic parameter values** that produce chaotic behaviour:

| Parameter | Value | Physical role |
|-----------|-------|--------------|
| $\sigma = 10$ | Prandtl number — ratio of momentum diffusivity to thermal diffusivity | Controls how quickly velocity adjusts to temperature |
| $\rho = 28$ | Normalised Rayleigh number — strength of thermal forcing relative to dissipation | Controls how vigorously convection is driven |
| $\beta = 8/3$ | Geometric factor — aspect ratio of convection cells | Controls how quickly vertical distortion decays |

### Fixed points and the route to chaos

The system has **three fixed points** (where all derivatives are zero):

- **Origin** $(0, 0, 0)$: the purely conductive state (no convection).
  Always exists; unstable for $\rho > 1$.

- **Two symmetric points** $C^\pm = (\pm\sqrt{\beta(\rho-1)},\; \pm\sqrt{\beta(\rho-1)},\; \rho-1)$:
  the steady convective rolls.  For $\sigma = 10$, $\beta = 8/3$, these points become
  **unstable** (Hopf bifurcation) when $\rho > \rho_H \approx 24.74$.

At $\rho = 28 > 24.74$, *none* of the three fixed points is stable.
Trajectories cannot settle anywhere — they must wander forever, tracing out the
**strange attractor** shown below.

### The strange attractor

For these parameters the system is *chaotic*: trajectories are **bounded** (they
stay on the attractor forever) but **never periodic** (they never exactly repeat).
The geometric object they trace out is called a **strange attractor**.

The visualisation below shows 70 MTU of trajectory after transients have decayed.
The colour encodes the height variable $Z$ — notice how the trajectory alternates
between the two lobes (the "butterfly wings"), each corresponding to one
sense of convective overturning.  The number of loops on each lobe before switching
to the other is *unpredictable* — that is the chaotic signature.

> 💡 **Tip:** Click and drag on the plot to rotate it in 3-D.
> Zoom in to see the fine fractal structure of the attractor.
"""),

        _fig,

        mo.callout(
            mo.md(r"""
**What makes this attractor "strange"?**

A periodic orbit would be a closed loop.  A fixed point would be a dot.
This attractor is *neither* — it is a **fractal set** with a non-integer
(Hausdorff) dimension of approximately **2.06**.

Trajectories wind around the two lobes in an order that looks random but is
in fact *completely determined* by the initial condition.  The catch is that
two trajectories starting from almost identical initial conditions will
eventually end up on opposite lobes with no correlation between them.
That is the content of *sensitive dependence on initial conditions* (SDIC),
which the next section demonstrates directly.

The fractal structure also means the attractor has **zero volume** in 3-D space —
the trajectory is confined to a set of measure zero, even though it fills a
two-dimensional surface.  This is why chaos is sometimes described as having
"more structure than a surface but less than a volume."
"""),
            kind="info",
        ),
    ])


# ===========================================================================
# MARKDOWN CELL — What is the Lyapunov exponent? (intuition before the math)
# ===========================================================================
@app.cell
def cell_sdic_intuition(mo):
    return mo.md(r"""
---
### 📐 Background: quantifying chaos with the Lyapunov exponent

Before diving into the interactive demonstration, let's build intuition about
how we *measure* chaos quantitatively.

**The key question:** If I start two trajectories with initial separation $\delta_0$,
how fast does that separation grow?

In a chaotic system, the answer (on average, over the attractor) is **exponentially**:

$$\delta(t) \approx \delta_0 \, e^{\lambda t}$$

where $\lambda$ is the **leading Lyapunov exponent**.  Its sign determines the system's nature:

| Sign of $\lambda$ | System type | Example |
|-------------------|-------------|---------|
| $\lambda < 0$ | Stable fixed point or limit cycle | Damped pendulum |
| $\lambda = 0$ | Marginally stable (bifurcation point) | Integrable Hamiltonian system |
| $\lambda > 0$ | **Chaotic** — nearby trajectories diverge exponentially | Lorenz 63, real atmosphere |

**The Lorenz 63 Lyapunov spectrum** consists of three exponents $(\lambda_1, \lambda_2, \lambda_3)$:

| Exponent | Value (MTU⁻¹) | Meaning |
|----------|--------------|---------|
| $\lambda_1$ | ≈ +0.906 | Exponential stretching along the most unstable direction |
| $\lambda_2$ | ≈ 0.000 | Neutral — along the flow direction (neither stretching nor contracting) |
| $\lambda_3$ | ≈ −14.57 | Strong contraction — the attractor has zero volume |

The sum $\lambda_1 + \lambda_2 + \lambda_3 = \sigma(-1) + (-1) + (-\beta) \approx -13.67$
is the **divergence** of the vector field, confirming that the system is dissipative (volume-shrinking).

**The Lyapunov time** $\tau_\lambda = 1/\lambda_1 \approx 1.1$ MTU is the characteristic
e-folding time for error growth.  Beyond about $5\,\tau_\lambda \approx 5.5$ MTU, initial
errors have amplified by $e^5 \approx 150\times$ — effectively destroying all predictive skill.

In the next section you will estimate $\lambda_1$ directly from the slope of the
log-separation curve.
""")


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

Taking the logarithm of both sides:

$$\ln\delta(t) \approx \ln\delta_0 + \lambda\,t$$

This is a straight line on a **log-scale plot of separation vs time** — with slope $\lambda$.
That is exactly what the right-hand panel below shows.

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
| Grey cloud = full attractor (for reference) | Dashed red line = attractor diameter (no skill beyond this) |

### How to read the log-separation plot

- **Flat or slowly rising**: the two trajectories are still following each other.
  Forecast error is growing, but slowly (sub-exponential phase near the start).
- **Straight line (exponential phase)**: error doubling every $\ln 2/\lambda \approx 0.8$ MTU.
  This is the classic chaotic regime.
- **Levelling off at the red dashed line**: the error has saturated.
  The two trajectories have become statistically independent — completely uncorrelated.
  The forecast is no better than a random draw from the attractor (climatology).
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
5. Try δ₀ = **10⁻¹** (a large perturbation — 10 % of attractor size).
   Does the trajectory immediately diverge, or is there still a brief coherent phase?
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

**The practical predictability ceiling** in the real atmosphere is approximately
**2–3 weeks** — beyond which even a perfect initial state cannot yield a useful
deterministic forecast.  This is not a pessimistic statement about the current
state of NWP; it is a mathematical consequence of the Lorenz time of the atmosphere.
"""),
    ])


# ===========================================================================
# MARKDOWN CELL — Deeper theory: Lyapunov spectrum and Kaplan-Yorke dimension
# ===========================================================================
@app.cell
def cell_lyapunov_deeper(mo):
    return mo.md(r"""
---
### 📐 Going deeper: the Lyapunov spectrum and attractor geometry

The three Lyapunov exponents of the Lorenz system tell us how a small
three-dimensional ball of initial conditions evolves:

$$(\lambda_1,\; \lambda_2,\; \lambda_3) \approx (+0.906,\; 0,\; -14.57) \quad \text{MTU}^{-1}$$

Think of the initial ball as having three independent axes.  Over time:
- The **first axis** (aligned with the most unstable direction) is **stretched** —
  at rate $e^{\lambda_1 t}$.  This is the source of chaos.
- The **second axis** is **neutral** (neither stretched nor contracted) —
  it lies along the direction of the flow itself.
- The **third axis** is **strongly contracted** — at rate $e^{\lambda_3 t} \approx e^{-14.57 t}$.
  This rapid collapse is why the attractor is thin and sheet-like.

The overall **volume** of the ball changes as $e^{(\lambda_1+\lambda_2+\lambda_3)t} \approx e^{-13.67 t}$,
shrinking to zero.  The attractor therefore has **zero volume in 3-D space** — it is a
set of measure zero, even though it has a complex fractal structure.

**The Kaplan–Yorke (Lyapunov) dimension** estimates the fractal dimension of the attractor
from the Lyapunov spectrum:

$$D_{KY} = j + \frac{\lambda_1 + \cdots + \lambda_j}{|\lambda_{j+1}|}$$

where $j$ is the largest index such that the cumulative sum is still positive.
Here $j = 2$ and:

$$D_{KY} = 2 + \frac{0.906 + 0}{14.57} \approx 2.062$$

This non-integer dimension (between 2 and 3) is the hallmark of a **fractal strange attractor**.
The attractor fills more than a surface but less than a volume.

**Finite-time Lyapunov exponents (FTLEs)** measure the local stretching rate over a
finite time interval rather than the infinite-time average.  On any given initial condition
the FTLE can be much larger or smaller than $\lambda_1 \approx 0.906$.  This local variability
is why the predictability horizon depends on *where* on the attractor you start —
something you can explore in Section 3 by changing the starting location.
""")


# ===========================================================================
# MARKDOWN CELL — Brief history of ensemble NWP
# ===========================================================================
@app.cell
def cell_ensemble_history(mo):
    return mo.md(r"""
---
### 🕰️ The operational history of ensemble forecasting

The mathematical case for ensemble NWP was made long before it was computationally
feasible.  Here is the key timeline:

| Year | Development |
|------|------------|
| **1963** | Lorenz shows deterministic chaos implies finite predictability |
| **1965** | Lorenz introduces the concept of a "predictability limit" for the real atmosphere |
| **1969** | **Epstein** proposes stochastic-dynamic forecasting — the first ensemble concept |
| **1974** | **Leith** demonstrates Monte Carlo ensemble forecasting in a simple model |
| **1992** | ECMWF launches the **Ensemble Prediction System (EPS)** operationally (December 1992) |
| **1992** | NCEP launches the **Global Ensemble Forecast System (GEFS)** (December 1992) |
| **2002** | Ensemble Kalman filter (EnKF) applied to NWP by Hamill & Snyder; later by Houtekamer |
| **2010s** | Hybrid ensemble-variational (En-Var) data assimilation adopted by major centres |
| **2020s** | Machine-learning ensemble post-processing and diffusion-model ensemble generation |

**How are operational perturbations chosen?**

Simply adding random noise to the initial state (as we do in Section 3) is not
optimal — it wastes ensemble members on directions that do not grow.  Real NWP centres
use more sophisticated methods:

| Method | Idea | Used by |
|--------|------|---------|
| **Bred vectors** | Evolve a perturbation through the model for a short time, rescale it, repeat — breeds the fast-growing modes | NCEP (1992–) |
| **Singular vectors** | Linear algebra: find the perturbation that grows the most over a chosen optimisation period | ECMWF (1992–) |
| **Ensemble Kalman filter (EnKF)** | Use the ensemble itself as the background-error covariance in data assimilation | Many regional centres |
| **Stochastic physics** | Add random noise to the model tendencies to represent model uncertainty | ECMWF (2009–), most major centres |

**ECMWF EPS at a glance (2024):**
- **51 members** (1 control + 50 perturbed)
- **18 km horizontal resolution**, 137 vertical levels
- **15-day** deterministic-quality medium-range, **46-day** (weekly) extended range
- Monthly and seasonal long-range ensemble products
- Serves as the backbone of probabilistic weather warnings worldwide

The next section lets you explore the same core principles with an idealised
Lorenz-system ensemble.
""")


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

The **ensemble mean** $\bar X(t) = \frac{1}{N}\sum_{i=1}^N X_i(t)$ is a better
point forecast than any single member, because it averages out the component of
uncertainty that is purely random across members.

The **ensemble spread** — the RMS standard deviation across members — is a
direct measure of forecast uncertainty:

$$\sigma_\text{spread}(t) = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left|X_i(t) - \bar X(t)\right|^2}$$

When the ensemble spread equals the error of the ensemble mean against the truth,
the ensemble is said to be **reliable** (well-calibrated).

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

### Why starting location matters

The Lorenz attractor is not uniformly chaotic.  Near the **lobe centres**, trajectories
make several loops on the same lobe before switching — a relatively coherent phase.
Near the **saddle point** at the origin, the unstable manifold has very large curvature
and small perturbations grow much faster.  Near **lobe transitions**, trajectories
are about to switch lobes — which one they go to becomes sensitive to tiny perturbations.

This **flow-dependent predictability** is why modern NWP systems compute a fresh
ensemble every 6 hours: the predictability horizon changes with the weather pattern.
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
   (It shouldn't — why not?  Hint: finite-time vs infinite-time Lyapunov exponents.)

4. Fix lead time = 15 and δ₀ = 10⁻⁴.  Compare **N = 5** vs **N = 50**.
   Which gives a smoother, more reliable spread estimate?
   At what N does the curve look "trustworthy"?

5. *Bonus:* Set N = 50, δ₀ = 10⁻⁴, location = *Chaotic lobe transition*.
   Is the predictability horizon shorter or longer than the predictable region?
   Can you explain this in terms of the local Lyapunov exponent?
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
                f"Full saturation (spread > 90 %): **t ≈ {_t90:.1f} MTU**  \n"
                f"Final saturation: **{_final_sat:.0%}** of attractor size  \n"
                f"{_regime}"
            ),
            kind=_ck,
        ),

        mo.md(r"""
### Ensemble spread vs. ensemble mean error

A fundamental result from ensemble theory is that a **perfectly calibrated** ensemble
satisfies:

$$\langle \sigma^2_\text{spread} \rangle = \langle \epsilon^2_\text{mean} \rangle$$

where $\epsilon_\text{mean} = |\bar X - X_\text{truth}|$ is the error of the ensemble mean
and angle brackets denote averages over many forecasts.

In practice, most NWP ensembles are **underdispersive** — spread is smaller than error —
because:

1. The initial perturbations do not fully sample the true analysis error
2. Model error is not fully represented
3. Ensemble size $N$ is finite

Underdispersion means the ensemble is **overconfident**: it claims more certainty than
it actually has.  Calibration techniques (inflation, rank histogram adjustment) correct
for this in post-processing.
"""),
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

A factor-of-10 improvement in observational accuracy buys only about **6.5 extra days**.
A factor of 100 improvement (two decades) buys only **13 extra days**.
This logarithmic ceiling means that the atmospheric predictability limit of
≈ 2–3 weeks is **fundamental, not a consequence of inadequate technology**.

This has major implications for how we invest in observational infrastructure.
Each successive decade of improvement in $\delta_0$ yields the same fixed bonus $\Delta t$,
so the return (in days of skill) on a factor-of-10 investment decreases as skill improves.

### Historical skill improvement at ECMWF

ECMWF has tracked forecast skill continuously since 1980.  The 500 hPa geopotential
anomaly correlation (AC) score measures how well the forecast pattern matches the verifying
analysis.  A score of 0.6 is a conventional threshold for "useful" forecasting.

| Era | 500 hPa AC = 0.6 reached at... |
|-----|-------------------------------|
| 1980 | ≈ 5 days (Northern Hemisphere) |
| 1990 | ≈ 7 days |
| 2000 | ≈ 8 days |
| 2010 | ≈ 9 days |
| 2020 | ≈ 9–10 days |

The slowing rate of improvement is consistent with the **logarithmic limit** imposed
by SDIC: each decade of forecast improvement costs an exponentially greater effort.

### Predictability of the second kind

Everything above is **predictability of the first kind**: initial-value prediction
of a specific trajectory.  There is also a **second kind**: predicting the *response
of the attractor to a sustained external forcing* (in the atmosphere, a change in
greenhouse-gas concentration or sea-surface temperature).

In the Lorenz system, individual trajectories become unpredictable after ≈ 5–8 MTU,
but if you change $\rho$ (the forcing parameter), the *time-mean* of $X$ shifts
systematically — and that shift can be predicted even when individual trajectories
cannot.  This is the mathematical analogue of the climate-vs-weather distinction.

**Examples of second-kind predictability in the real atmosphere:**

| Phenomenon | Typical lead time | Mechanism |
|------------|------------------|-----------|
| El Niño / La Niña (ENSO) | 6–18 months | Slow ocean-atmosphere coupling |
| Monsoon onset | 2–4 weeks | Land–sea thermal contrast |
| Stratospheric sudden warmings | 2–3 weeks | Wave-mean-flow interaction |
| Arctic Oscillation | 10–20 days | Stratosphere-troposphere coupling |
| Long-term climate change | Decades–centuries | Radiative forcing from GHGs |

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

5. **Flow-dependent predictability matters:**
   Not all weather patterns are equally predictable.  Some synoptic situations
   (strong blocking, active MJO) are more predictable than others (rapidly developing
   extratropical cyclones, post-frontal convection).  Ensemble spread is the
   operational estimate of this situation-dependent uncertainty.
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

**Q4 — Quantitative connection to the real atmosphere** *(Sections 2 & 4)*

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


# ===========================================================================
# MARKDOWN CELL — Further reading and references
# ===========================================================================
@app.cell
def cell_further_reading(mo):
    return mo.md(r"""
---
## 📚 Further Reading

### Original papers

- **Lorenz, E. N. (1963)**. *Deterministic nonperiodic flow.*
  Journal of the Atmospheric Sciences, 20(2), 130–141.
  The founding paper.  Remarkably readable for a mathematical landmark.

- **Lorenz, E. N. (1965)**. *A study of the predictability of a 28-variable atmospheric model.*
  Tellus, 17(3), 321–333.
  First estimate of the atmospheric predictability limit.

- **Lorenz, E. N. (1975)**. *Climatic predictability.*
  In: *The Physical Basis of Climate and Climate Modelling*, GARP Publication Series No. 16, 132–136.
  Introduces the distinction between predictability of the first and second kinds.

- **Epstein, E. S. (1969)**. *Stochastic dynamic prediction.*
  Tellus, 21(6), 739–759.
  The first formal ensemble forecasting proposal.

- **Palmer, T. N. (2000)**. *Predicting uncertainty in forecasts of weather and climate.*
  Reports on Progress in Physics, 63(2), 71.
  Excellent review connecting chaos theory to operational NWP.

### Books

- **Lorenz, E. N. (1993)**. *The Essence of Chaos.*
  University of Washington Press.
  Lorenz's own account, written for a general audience.  Highly recommended.

- **Gleick, J. (1987)**. *Chaos: Making a New Science.*
  Viking Penguin.
  Popular science account of the chaos revolution; contains the Lorenz story.

- **Palmer, T. N. & Hagedorn, R. (Eds.) (2006)**. *Predictability of Weather and Climate.*
  Cambridge University Press.
  Comprehensive graduate-level treatment of ensemble methods and predictability theory.

- **Kalnay, E. (2003)**. *Atmospheric Modelling, Data Assimilation and Predictability.*
  Cambridge University Press.
  Standard NWP textbook; Chapter 6 covers ensemble forecasting in depth.

### Online resources

- [ECMWF Ensemble Prediction System documentation](https://www.ecmwf.int/en/forecasts/documentation-and-support/changes-ecmwf-model/ensemble-forecasts)
- [The Lorenz attractor — interactive 3-D (Paul Bourke)](http://paulbourke.net/fractals/lorenz/)
- [Chaos and Dynamical Systems (Santa Fe Institute, free course)](https://complexity.santa-fe.edu)

---
*Notebook by Aneesh C. Subramanian — FERS Summer School 2026.*
*Built with [marimo](https://marimo.io), [NumPy](https://numpy.org), [SciPy](https://scipy.org), [Plotly](https://plotly.com).*
""")


if __name__ == "__main__":
    app.run()
