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
Lorenz 63 Ensemble Forecast Explorer
FERS Summer School 2026 — Weather & Climate Predictability

A marimo notebook for exploring chaotic error growth and ensemble forecasting.

To run:
    pip install marimo numpy scipy plotly
    marimo run lorenz63_ensemble_explorer.py

To edit interactively:
    marimo edit lorenz63_ensemble_explorer.py
"""

import marimo

__generated_with = "0.19.10"
app = marimo.App(width="full", app_title="Lorenz 63 Ensemble Explorer")


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
@app.cell
def imports():
    import marimo as mo
    import numpy as np
    from scipy.integrate import solve_ivp
    import plotly.graph_objects as go
    return go, mo, np, solve_ivp


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
@app.cell
def header(mo):
    return mo.md(
        r"""
        # 🌀 Lorenz 63 Ensemble Forecast Explorer

        **FERS Summer School 2026 — Weather & Climate Predictability**

        In this activity you will explore how small errors in initial conditions grow in a
        chaotic dynamical system — the fundamental reason weather forecasts have a finite
        predictability horizon.

        **How to use:** Adjust the controls and watch the ensemble evolve in real time.
        Work through the guided questions at the bottom with your neighbor.
        """
    )


# ---------------------------------------------------------------------------
# UI controls (exported individually for downstream reactive cells)
# ---------------------------------------------------------------------------
@app.cell
def define_controls(mo):
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
        label="Ensemble size (N members)",
        show_value=True,
    )

    lead_time = mo.ui.slider(
        start=1, stop=30, step=1, value=10,
        label="Forecast lead time (MTU)",
        show_value=True,
    )

    return ic_choice, lead_time, n_members, perturb_exp


@app.cell
def display_controls(mo, ic_choice, perturb_exp, n_members, lead_time):
    return mo.vstack(
        [
            mo.md("### ⚙️ Controls"),
            mo.hstack(
                [ic_choice, n_members],
                justify="start",
                gap="3rem",
            ),
            mo.hstack(
                [perturb_exp, lead_time],
                justify="start",
                gap="3rem",
            ),
        ],
        gap="0.6rem",
    )


# ---------------------------------------------------------------------------
# Lorenz 63 integration + ensemble spread computation
# ---------------------------------------------------------------------------
@app.cell
def compute_ensemble(ic_choice, lead_time, n_members, np, perturb_exp, solve_ivp):
    # Classic Lorenz (1963) parameters
    _sigma, _rho, _beta = 10.0, 28.0, 8.0 / 3.0

    def _lorenz(t, state):
        x, y, z = state
        return [
            _sigma * (y - x),
            x * (_rho - z) - y,
            x * y - _beta * z,
        ]

    # Three representative starting locations on the attractor
    _ic_map = {
        "predictable": np.array([8.5,  8.5, 27.0]),   # near fixed point C+
        "saddle":      np.array([0.1,  0.1,  0.1]),   # near origin (unstable)
        "chaotic":     np.array([-5.0, -7.0, 22.0]),  # lobe-transition zone
    }
    x0_base = _ic_map[ic_choice.value]

    N          = n_members.value
    T          = lead_time.value
    perturbation = 10.0 ** perturb_exp.value
    t_eval     = np.linspace(0, T, 600)

    # Integrate each ensemble member forward
    np.random.seed(42)
    _perturbs = np.random.randn(N, 3) * perturbation
    trajs = np.zeros((N, 3, len(t_eval)))
    for _i in range(N):
        _sol = solve_ivp(
            _lorenz,
            (0, T),
            x0_base + _perturbs[_i],
            t_eval=t_eval,
            method="RK45",
            rtol=1e-9,
            atol=1e-12,
        )
        trajs[_i] = _sol.y

    # Long reference run for attractor background (skip transient)
    _ref = solve_ivp(
        _lorenz,
        (0, 70),
        [1.0, 1.0, 1.0],
        t_eval=np.linspace(10, 70, 7000),
        method="RK45",
        rtol=1e-9,
        atol=1e-12,
    )
    attractor_ref = _ref.y  # shape (3, n_ref)

    # RMS ensemble spread: std across members, mean across x/y/z
    _std = np.std(trajs, axis=0)          # (3, n_times)
    rms_spread = np.sqrt(np.mean(_std**2, axis=0))  # (n_times,)

    # "Saturated" spread = typical std of the attractor itself
    attractor_size = float(np.mean(np.std(attractor_ref, axis=1)))

    return attractor_ref, attractor_size, rms_spread, t_eval, trajs


# ---------------------------------------------------------------------------
# Phase-space figure (3D)
# ---------------------------------------------------------------------------
@app.cell
def make_phase_plot(attractor_ref, go, lead_time, n_members, trajs):
    _N = n_members.value
    _T = lead_time.value

    fig3d = go.Figure()

    fig3d.add_trace(go.Scatter3d(
        x=attractor_ref[0], y=attractor_ref[1], z=attractor_ref[2],
        mode="lines",
        line=dict(color="rgba(160,160,160,0.25)", width=1),
        name="Attractor", showlegend=False, hoverinfo="skip",
    ))

    for _i in range(_N):
        _hue = int(200 + 130 * _i / max(_N - 1, 1))
        _show = _i < 5
        fig3d.add_trace(go.Scatter3d(
            x=trajs[_i, 0], y=trajs[_i, 1], z=trajs[_i, 2],
            mode="lines",
            line=dict(color=f"hsla({_hue},65%,50%,0.75)", width=1.8),
            name=f"Member {_i+1}" if _show else "",
            showlegend=_show, hoverinfo="skip",
        ))

    fig3d.add_trace(go.Scatter3d(
        x=trajs[:, 0, 0], y=trajs[:, 1, 0], z=trajs[:, 2, 0],
        mode="markers",
        marker=dict(size=5, color="limegreen", opacity=0.9),
        name="t = 0",
    ))
    fig3d.add_trace(go.Scatter3d(
        x=trajs[:, 0, -1], y=trajs[:, 1, -1], z=trajs[:, 2, -1],
        mode="markers",
        marker=dict(size=5, color="crimson", opacity=0.9),
        name=f"t = {_T} MTU",
    ))

    fig3d.update_layout(
        height=520,
        title=dict(text="Phase Space (Lorenz Attractor)", font_size=13, x=0.5, xanchor="center"),
        scene=dict(
            xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
            camera=dict(eye=dict(x=1.5, y=1.2, z=0.9)),
            bgcolor="rgba(245,248,255,0.6)",
        ),
        margin=dict(l=5, r=5, t=50, b=5),
        legend=dict(x=0.01, y=0.99, font_size=10, bgcolor="rgba(255,255,255,0.8)"),
        paper_bgcolor="white",
    )
    return fig3d


# ---------------------------------------------------------------------------
# Spread time-series figure (2D)
# ---------------------------------------------------------------------------
@app.cell
def make_spread_plot(attractor_size, go, lead_time, n_members, np, perturb_exp, rms_spread, t_eval):
    _N   = n_members.value
    _T   = lead_time.value
    _exp = perturb_exp.value

    fig2d = go.Figure()

    fig2d.add_trace(go.Scatter(
        x=t_eval, y=rms_spread,
        mode="lines",
        line=dict(color="#1a3a6e", width=2.5),
        name="RMS spread",
        fill="tozeroy",
        fillcolor="rgba(26,58,110,0.08)",
    ))

    fig2d.add_hline(
        y=attractor_size,
        line=dict(color="firebrick", dash="dash", width=1.5),
        annotation_text="Attractor size — fully unpredictable",
        annotation_position="top left",
        annotation_font_size=11,
    )
    fig2d.add_hline(
        y=0.1 * attractor_size,
        line=dict(color="darkorange", dash="dot", width=1.5),
        annotation_text="10% saturation",
        annotation_position="bottom right",
        annotation_font_size=11,
    )

    _t_max = float(t_eval[-1])
    _idx_10 = np.where(rms_spread >= 0.1 * attractor_size)[0]
    _idx_90 = np.where(rms_spread >= 0.9 * attractor_size)[0]
    _t10 = float(t_eval[_idx_10[0]]) if len(_idx_10) else _t_max
    _t90 = float(t_eval[_idx_90[0]]) if len(_idx_90) else _t_max

    for _shade in [
        dict(x0=0,    x1=_t10,  color="rgba(0,180,0,0.07)",   label="Predictable"),
        dict(x0=_t10, x1=_t90,  color="rgba(255,165,0,0.07)", label="Semi-predictable"),
        dict(x0=_t90, x1=_t_max, color="rgba(220,0,0,0.07)",  label="Unpredictable"),
    ]:
        if _shade["x0"] < _shade["x1"]:
            fig2d.add_vrect(
                x0=_shade["x0"], x1=_shade["x1"],
                fillcolor=_shade["color"], line_width=0,
                annotation_text=_shade["label"],
                annotation_position="top left",
                annotation_font_size=10,
            )

    fig2d.update_layout(
        height=520,
        title=dict(
            text=(
                f"Ensemble of <b>{_N}</b> members &nbsp;|&nbsp; "
                f"perturbation = 10<sup>{_exp:.1f}</sup> &nbsp;|&nbsp; "
                f"lead time = <b>{_T}</b> MTU"
            ),
            font_size=13, x=0.5, xanchor="center",
        ),
        margin=dict(l=5, r=5, t=50, b=5),
        paper_bgcolor="white",
    )
    fig2d.update_xaxes(title_text="Lead time (MTU)", gridcolor="#e8e8e8")
    fig2d.update_yaxes(title_text="RMS ensemble spread", type="log", gridcolor="#e8e8e8")

    return fig2d


# ---------------------------------------------------------------------------
# Display both panels side by side
# ---------------------------------------------------------------------------
@app.cell
def display_plots(mo, fig3d, fig2d):
    return mo.hstack([fig3d, fig2d], widths=[1, 1])


# ---------------------------------------------------------------------------
# Live stats callout (reactive: updates whenever computation changes)
# ---------------------------------------------------------------------------
@app.cell
def show_stats(attractor_size, mo, np, rms_spread, t_eval):
    _idx_horizon = np.where(rms_spread >= 0.1 * attractor_size)[0]
    _horizon = (
        float(t_eval[_idx_horizon[0]])
        if len(_idx_horizon) > 0
        else float(t_eval[-1])
    )
    _saturation = float(rms_spread[-1] / attractor_size)

    if _saturation < 0.3:
        _regime = "🟢 Still coherent — ensemble well-clustered"
        _kind = "success"
    elif _saturation < 0.7:
        _regime = "🟠 Semi-predictable — spread growing rapidly"
        _kind = "warn"
    else:
        _regime = "🔴 Unpredictable — spread saturated at attractor size"
        _kind = "danger"

    return mo.callout(
        mo.md(
            f"**Predictability horizon** (spread reaches 10% of attractor size): "
            f"**t ≈ {_horizon:.1f} MTU** &nbsp;|&nbsp; "
            f"**Final saturation ratio**: {_saturation:.2f} &nbsp;|&nbsp; "
            f"{_regime}"
        ),
        kind=_kind,
    )


# ---------------------------------------------------------------------------
# Guided questions
# ---------------------------------------------------------------------------
@app.cell
def guided_questions(mo):
    return mo.md(
        r"""
        ---

        ## 📝 Guided Questions

        Work through these with a neighbor and write down your answers.
        We will discuss as a group afterward (~10 min).

        ---

        **Question 1 — Predictability horizon**

        Set perturbation = 10⁻⁴ and N = 20. Choose *Predictable region* and slowly drag
        the lead-time slider from 1 → 30.

        - At what lead time does the green cluster begin to scatter across the full attractor?
          What colour zone does the spread plot enter at that point?
        - Switch to *Chaotic lobe transition*. Is the horizon earlier or later?
          Why might your starting location on the attractor matter?

        ---

        **Question 2 — Sensitivity to perturbation size**

        Fix lead time = 15. Slide the perturbation from 10⁻⁶ → 10⁻¹.

        - Does reducing the perturbation by **one decade** buy you a proportionally longer
          predictable window? Watch the spread curve — does it simply shift right, or does
          its shape change?
        - **Implication**: What does this tell us about the practical benefit of improving
          observational accuracy by an order of magnitude?

        ---

        **Question 3 — Ensemble size**

        Fix lead time = 15 and perturbation = 10⁻⁴. Compare N = 5 vs N = 50.

        - How stable is the spread estimate with small N? Could you trust it for a
          probabilistic forecast?
        - At what N does the curve look "reliable" to you?
        - ECMWF's operational ensemble uses 51 members. Does that seem justified?

        ---

        **Question 4 — Connecting to the real atmosphere**

        The Lorenz time (error e-folding time) in L63 is ≈ 1–2 MTU.
        In the real atmosphere it is approximately **1.5–2.5 days** (Lyapunov exponent ≈ 0.35 day⁻¹).

        - If ECMWF achieves useful skill to ~10 days, how many Lorenz times is that?
        - What does this imply about the **fundamental upper limit** on deterministic weather
          forecasting, regardless of model improvements or observational density?

        ---

        **Question 5 — Predictability of the second kind** *(bonus)*

        Start at *Near saddle point* with perturbation = 10⁻⁶. Notice the ensemble eventually
        saturates — individual trajectories become completely unpredictable.

        Now imagine you do **not** want to predict a specific trajectory, but instead want to
        predict the *long-run time-mean* of X.

        - Would that remain possible even after the Lorenz time? Why or why not?
        - How does this connect to the distinction between **predictability of the 1st kind**
          (initial-value forecasting) and **predictability of the 2nd kind** (forced response)
          from today's lecture?

        ---

        *System: Lorenz (1963), σ = 10, ρ = 28, β = 8/3. Integrated with RK45 (scipy),
        rtol = 10⁻⁹. Ensemble members initialized with iid Gaussian perturbations (seed = 42
        for reproducibility). MTU (model time unit) ≈ 5 days in the real atmosphere.*
        """
    )


if __name__ == "__main__":
    app.run()
