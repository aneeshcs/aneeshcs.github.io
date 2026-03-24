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
    # Internal Waves in a Stratified Fluid
    ## An Interactive GFD Tutorial

    The ocean and atmosphere are **stratified** — density decreases with height
    (or increases with depth in the ocean). This stratification supports a rich
    family of oscillations called **internal gravity waves**, which transport energy
    and momentum over vast distances and play a crucial role in mixing.

    This notebook builds up the physics from scratch:

    1. **Two-layer system** — the simplest model of a stratified fluid
    2. **Continuously stratified fluid** — the Brunt-Väisälä frequency $N$
    3. **Internal wave dispersion** — how frequency depends on wavenumber and angle
    4. **Wave beams** — internal waves propagate along characteristics, not radially
    5. **Vertical modes** — how internal waves fit into a bounded ocean/atmosphere
    6. **2-D wave packet simulation** — watch wave beams propagate in real time

    > **How to use:** Read the theory sections, adjust sliders, and press
    > **▶ Run Simulation** buttons to generate animations.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 1 · The Two-Layer System

    The simplest stratified fluid consists of **two layers** of different densities
    stacked on top of each other:

    - Upper layer: density $\rho_1$, thickness $h_1$
    - Lower layer: density $\rho_2 > \rho_1$, thickness $h_2$

    At the **interface** between the layers, small vertical displacements $\eta$
    are restored by buoyancy.  The reduced gravity is:

    $$g' = g\,\frac{\rho_2 - \rho_1}{\rho_1}$$

    For interface waves with horizontal wavenumber $k$, the dispersion relation is:

    $$\omega^2 = g' k \tanh(kh_2)$$

    In the **shallow-water limit** ($k h_2 \ll 1$): $\omega = k\sqrt{g' h_2}$

    In the **deep-water limit** ($k h_2 \gg 1$): $\omega = \sqrt{g' k}$

    Compare with **surface** gravity waves ($\rho_2 \to \infty$, $g' \to g$):
    the interface waves travel much more slowly because $g' \ll g$
    (typical oceanic $g'/g \sim 10^{-3}$).
    """)
    return


@app.cell
def _(mo):
    # Two-layer dispersion controls
    tl_rho1 = mo.ui.slider(990, 1025, value=1000, step=1,
                           label="Upper density ρ₁ (kg/m³)")
    tl_rho2 = mo.ui.slider(1000, 1030, value=1025, step=1,
                           label="Lower density ρ₂ (kg/m³)")
    tl_h2   = mo.ui.slider(10, 5000, value=500, step=10,
                           label="Lower layer depth h₂ (m)")
    mo.vstack([
        mo.md("**Two-layer dispersion relation — adjust parameters:**"),
        tl_rho1, tl_rho2, tl_h2,
    ])
    return tl_h2, tl_rho1, tl_rho2


@app.cell
def _(mo, tl_h2, tl_rho1, tl_rho2):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import io, base64

    g = 9.81
    rho1 = tl_rho1.value
    rho2 = tl_rho2.value
    h2   = tl_h2.value

    if rho2 <= rho1:
        mo.md("⚠️ ρ₂ must be greater than ρ₁ for stable stratification.")
    else:
        gprime = g * (rho2 - rho1) / rho1
        c_iw   = np.sqrt(gprime * h2)          # shallow interface wave speed
        Ld     = np.sqrt(gprime * h2) / 1e-4   # deformation radius (f~1e-4 s^-1)

        k_arr = np.logspace(-5, 0, 300)        # wavenumber (rad/m)
        omega_iw     = np.sqrt(gprime * k_arr * np.tanh(k_arr * h2))
        omega_sw     = np.sqrt(g       * k_arr)  # surface gravity wave

        phase_iw = omega_iw / k_arr
        phase_sw = omega_sw / k_arr

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        ax = axes[0]
        ax.loglog(k_arr, omega_iw / (2*np.pi), label="Interface wave", color="#2196F3", lw=2)
        ax.loglog(k_arr, omega_sw / (2*np.pi), label="Surface wave",   color="#FF9800", lw=2, ls="--")
        ax.set_xlabel("Wavenumber k (rad/m)")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_title("Dispersion relation")
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)

        ax = axes[1]
        ax.semilogx(k_arr, phase_iw, label="Interface wave", color="#2196F3", lw=2)
        ax.semilogx(k_arr, phase_sw, label="Surface wave",   color="#FF9800", lw=2, ls="--")
        ax.set_xlabel("Wavenumber k (rad/m)")
        ax.set_ylabel("Phase speed c = ω/k (m/s)")
        ax.set_title("Phase speed")
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)

        fig.suptitle(
            f"g′ = {gprime:.4f} m/s²,   "
            f"c_interface = {c_iw:.2f} m/s  (vs {np.sqrt(g*h2):.0f} m/s surface),   "
            f"L_d ≈ {Ld/1e3:.0f} km",
            fontsize=10,
        )
        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=110)
        plt.close(fig)
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode()
        mo.Html(f'<img src="data:image/png;base64,{img_b64}" style="max-width:100%">')
    return (
        base64,
        buf,
        c_iw,
        fig,
        g,
        gprime,
        img_b64,
        io,
        k_arr,
        matplotlib,
        np,
        omega_iw,
        omega_sw,
        phase_iw,
        phase_sw,
        plt,
        rho1,
        rho2,
        h2,
        Ld,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Continuously Stratified Fluid: The Brunt-Väisälä Frequency

    In a real ocean or atmosphere, density varies **continuously** with height $z$.
    The key quantity is the **Brunt-Väisälä (buoyancy) frequency** $N$:

    $$N^2(z) = -\frac{g}{\rho_0}\frac{d\rho}{dz}$$

    $N$ is the frequency at which a fluid parcel oscillates vertically when
    displaced from equilibrium — the "restoring spring constant" of stratification.

    | Location | Typical $N$ |
    |----------|------------|
    | Ocean thermocline | $5-20$ cph ($\sim 10^{-3}$ rad/s) |
    | Ocean deep water | $0.5-2$ cph |
    | Lower troposphere | $\sim 10^{-2}$ rad/s |
    | Stratosphere | $\sim 2\times10^{-2}$ rad/s |

    ### Common stratification profiles

    **Exponential** (typical ocean):
    $$\rho(z) = \rho_0 e^{-z/H_\rho}, \quad N^2 = g/H_\rho = \text{const}$$

    **Tanh** (sharp thermocline at depth $z_0$, width $\delta$):
    $$N^2(z) = N_0^2 \left[1 + \tanh\!\left(\frac{z - z_0}{\delta}\right)\right]/2$$

    **Two-layer limit**: $N(z) = N_0\,\delta(z - z_0)$ (concentrated at the interface)
    """)
    return


@app.cell
def _(mo):
    strat_type = mo.ui.dropdown(
        ["Constant N", "Tanh (thermocline)", "Exponential"],
        value="Tanh (thermocline)",
        label="Stratification profile",
    )
    N0_slider = mo.ui.slider(1, 20, value=10, step=1,
                             label="Peak N₀ (cycles/hour)")
    thermo_depth = mo.ui.slider(0, 1000, value=200, step=10,
                                label="Thermocline depth (m)")
    thermo_width = mo.ui.slider(10, 300, value=80, step=10,
                                label="Thermocline width δ (m)")
    mo.vstack([strat_type, N0_slider, thermo_depth, thermo_width])
    return N0_slider, strat_type, thermo_depth, thermo_width


@app.cell
def _(N0_slider, mo, np, plt, strat_type, thermo_depth, thermo_width, base64, io):
    _z = np.linspace(-2000, 0, 500)   # depth in metres (negative upward)
    _N0 = N0_slider.value * 2*np.pi / 3600   # convert cph → rad/s

    _stype = strat_type.value
    if _stype == "Constant N":
        _N2 = np.full_like(_z, _N0**2)
    elif _stype == "Tanh (thermocline)":
        _z0 = -thermo_depth.value
        _dz = thermo_width.value
        _N2 = _N0**2 * (1 + np.tanh((_z - _z0)/_dz)) / 2
    else:   # Exponential
        _Hr = 500.0  # scale depth
        _N2 = (_N0**2) * np.exp(_z/_Hr) / np.exp(-2000/_Hr)

    _N  = np.sqrt(np.maximum(_N2, 0))

    _fig, _axes = plt.subplots(1, 2, figsize=(8, 5), sharey=True)

    _axes[0].plot(_N * 3600 / (2*np.pi), _z, color="#2196F3", lw=2)
    _axes[0].set_xlabel("N (cycles per hour)")
    _axes[0].set_ylabel("Depth (m)")
    _axes[0].set_title("Buoyancy frequency N(z)")
    _axes[0].grid(True, alpha=0.3)

    _axes[1].plot(_N2, _z, color="#E91E63", lw=2)
    _axes[1].set_xlabel("N² (rad²/s²)")
    _axes[1].set_title("N²(z)")
    _axes[1].grid(True, alpha=0.3)

    _fig.tight_layout()
    _buf = io.BytesIO()
    _fig.savefig(_buf, format="png", dpi=110)
    plt.close(_fig)
    _buf.seek(0)
    _img = base64.b64encode(_buf.read()).decode()
    mo.Html(f'<img src="data:image/png;base64,{_img}" style="max-width:100%">')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Internal Wave Dispersion Relation

    For a **plane internal wave** with horizontal wavenumber $k$ and vertical
    wavenumber $m$ in a uniformly stratified fluid (constant $N$), the dispersion
    relation is:

    $$\boxed{\omega^2 = \frac{N^2 k^2 + f^2 m^2}{k^2 + m^2}}$$

    where $f = 2\Omega\sin\phi$ is the Coriolis parameter.  This can be written as:

    $$\omega^2 = N^2 \cos^2\!\theta + f^2 \sin^2\!\theta$$

    where $\theta$ is the angle of the wavenumber vector from the **vertical**
    (equivalently, the angle of the wave beam from the **horizontal**).

    ### Key properties

    - Frequency depends only on **propagation angle** $\theta$, not on the
      magnitude of the wavenumber → **scale invariance**
    - Internal waves exist only for $f \le |\omega| \le N$
    - Energy propagates along **wave beams** at angle $\theta$ to the horizontal
    - Group velocity is **perpendicular** to phase velocity!

    ### Group velocity

    $$c_{gx} = \frac{\partial\omega}{\partial k} = \frac{(N^2-f^2) k m^2}{\omega(k^2+m^2)^2}$$
    $$c_{gz} = \frac{\partial\omega}{\partial m} = -\frac{(N^2-f^2) k^2 m}{\omega(k^2+m^2)^2}$$

    Note: $c_{gz}$ has **opposite sign** to $m$ — if phase propagates upward,
    energy propagates downward (and vice versa).
    """)
    return


@app.cell
def _(mo):
    disp_N_slider = mo.ui.slider(1, 30, value=10, step=1,
                                 label="N (cycles/hour)")
    disp_f_slider = mo.ui.slider(0, 5, value=1, step=0.1,
                                 label="f (cycles/hour) — set 0 for non-rotating")
    mo.vstack([
        mo.md("**Explore the dispersion relation:**"),
        disp_N_slider, disp_f_slider,
    ])
    return disp_N_slider, disp_f_slider


@app.cell
def _(base64, disp_N_slider, disp_f_slider, io, mo, np, plt):
    _N  = disp_N_slider.value * 2*np.pi / 3600
    _f  = disp_f_slider.value * 2*np.pi / 3600

    if _N <= _f:
        mo.md("⚠️ N must exceed f for internal waves to exist.")
    else:
        _theta = np.linspace(0, np.pi/2, 300)   # angle from vertical
        _omega = np.sqrt(_N**2 * np.cos(_theta)**2 + _f**2 * np.sin(_theta)**2)

        # 2-D dispersion surface: omega(k,m)
        _kgrid = np.linspace(-0.02, 0.02, 200)
        _mgrid = np.linspace(-0.02, 0.02, 200)
        _KK, _MM = np.meshgrid(_kgrid, _mgrid)
        _Kmag2   = _KK**2 + _MM**2
        _Kmag2   = np.where(_Kmag2 == 0, 1e-30, _Kmag2)
        _OM      = np.sqrt((_N**2 * _KK**2 + _f**2 * _MM**2) / _Kmag2)

        _fig, _axes = plt.subplots(1, 3, figsize=(13, 4))

        # (a) omega vs theta
        _ax = _axes[0]
        _ax.plot(np.degrees(_theta), _omega * 3600/(2*np.pi), color="#2196F3", lw=2)
        _ax.axhline(_N * 3600/(2*np.pi), color="red",   ls="--", lw=1, label="N")
        _ax.axhline(_f * 3600/(2*np.pi), color="green", ls="--", lw=1, label="f")
        _ax.set_xlabel("Propagation angle θ from vertical (°)")
        _ax.set_ylabel("Frequency ω (cph)")
        _ax.set_title("ω vs. angle")
        _ax.legend()
        _ax.grid(True, alpha=0.3)

        # (b) dispersion surface
        _ax = _axes[1]
        _pc = _ax.contourf(_kgrid*1e3, _mgrid*1e3, _OM * 3600/(2*np.pi),
                           levels=20, cmap="viridis")
        plt.colorbar(_pc, ax=_ax, label="ω (cph)")
        _ax.set_xlabel("k (rad/km)")
        _ax.set_ylabel("m (rad/km)")
        _ax.set_title("Dispersion surface ω(k,m)")
        _ax.set_aspect("equal")

        # (c) group velocity angle vs omega
        _om_range = np.linspace(_f*1.01, _N*0.99, 300)
        _cos_th   = np.sqrt((_om_range**2 - _f**2) / (_N**2 - _f**2))
        _beam_ang = np.degrees(np.arccos(_cos_th))   # beam angle from horizontal
        _ax = _axes[2]
        _ax.plot(_om_range * 3600/(2*np.pi), _beam_ang, color="#E91E63", lw=2)
        _ax.set_xlabel("Frequency ω (cph)")
        _ax.set_ylabel("Wave beam angle from horizontal (°)")
        _ax.set_title("Beam angle vs. frequency")
        _ax.grid(True, alpha=0.3)

        _fig.tight_layout()
        _buf = io.BytesIO()
        _fig.savefig(_buf, format="png", dpi=110)
        plt.close(_fig)
        _buf.seek(0)
        _img = base64.b64encode(_buf.read()).decode()
        mo.Html(f'<img src="data:image/png;base64,{_img}" style="max-width:100%">')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 4 · Wave Beams and Ray Tracing

    Because internal wave frequency depends only on **angle** (not wavenumber
    magnitude), energy from a localised source concentrates into narrow
    **wave beams** emanating at angle $\theta$ to the horizontal, where:

    $$\cos\theta = \sqrt{\frac{\omega^2 - f^2}{N^2 - f^2}}$$

    In a uniformly stratified fluid, beams travel in **straight lines**.
    When $N$ varies with depth, beams follow curved rays according to
    **Snell's law for internal waves**:

    $$k_h = \text{const}, \qquad
    m(z) = k_h \sqrt{\frac{N^2(z) - \omega^2}{\omega^2 - f^2}}$$

    A beam is **reflected** where $\omega = N(z)$ (turning level) or at solid
    boundaries.  It is **trapped** if $\omega < N$ everywhere between two
    turning levels.

    ### The "St. Andrew's Cross"

    A classic experiment: oscillate a sphere at frequency $\omega$ in a
    uniformly stratified tank. Energy radiates along four beams forming
    an "X" shape at angles $\pm\theta$ above and below the horizontal.
    """)
    return


@app.cell
def _(mo):
    ray_omega = mo.ui.slider(1, 20, value=7, step=0.5,
                             label="Wave frequency ω (cph)")
    ray_N0_sl = mo.ui.slider(2, 30, value=15, step=1,
                             label="Peak N₀ (cph)")
    ray_f_sl  = mo.ui.slider(0, 3, value=0.5, step=0.1,
                             label="f (cph)")
    ray_nsrc  = mo.ui.slider(1, 5, value=3, step=1,
                             label="Number of source beams")
    mo.vstack([
        mo.md("**Ray tracing in a variable-N ocean:**"),
        ray_omega, ray_N0_sl, ray_f_sl, ray_nsrc,
    ])
    return ray_N0_sl, ray_f_sl, ray_nsrc, ray_omega


@app.cell
def _(base64, io, mo, np, plt, ray_N0_sl, ray_f_sl, ray_nsrc, ray_omega):
    _omega = ray_omega.value * 2*np.pi/3600
    _N0    = ray_N0_sl.value * 2*np.pi/3600
    _f     = ray_f_sl.value  * 2*np.pi/3600
    _nsrc  = ray_nsrc.value

    if _omega >= _N0 or _omega <= _f:
        mo.md("⚠️ Need f < ω < N₀ for internal waves.")
    else:
        # Tanh N(z) profile
        _z_arr = np.linspace(-2000, 0, 1000)
        _z0_th = -200.0
        _N2_arr = _N0**2 * (1 + np.tanh((_z_arr - _z0_th)/80)) / 2
        _N_arr  = np.sqrt(np.maximum(_N2_arr, 0))

        def _N_of_z(z):
            return np.sqrt(max(0, _N0**2 * (1 + np.tanh((z - _z0_th)/80)) / 2))

        # Ray tracing: dz/dx = ±tan(θ(z)), θ = arccos(sqrt((ω²-f²)/(N²-f²)))
        def _trace_ray(z_start, up=True, x_max=4e5, ds=100.0):
            """Trace a single ray starting at x=0, z=z_start."""
            xs, zs = [0.0], [z_start]
            x, z = 0.0, z_start
            sign = 1 if up else -1
            for _ in range(200000):
                N_z = _N_of_z(z)
                if N_z <= _omega:
                    break   # turning level
                arg = (_omega**2 - _f**2) / (N_z**2 - _f**2)
                cos_th = np.sqrt(np.clip(arg, 0, 1))
                sin_th = np.sqrt(1 - cos_th**2)
                if sin_th < 1e-9:
                    break
                dz_ds = sign * cos_th
                dx_ds = sin_th
                x += dx_ds * ds
                z += dz_ds * ds
                if z >= 0:
                    z = 0.0
                    sign = -1     # reflect off surface
                elif z <= -2000:
                    z = -2000.0
                    sign = 1      # reflect off bottom
                if x > x_max:
                    break
                xs.append(x)
                zs.append(z)
            return np.array(xs), np.array(zs)

        _fig, _axes = plt.subplots(1, 2, figsize=(12, 5))

        # Left: N(z) profile
        _ax = _axes[0]
        _ax.plot(_N_arr * 3600/(2*np.pi), _z_arr, color="#2196F3", lw=2)
        _ax.axvline(_omega * 3600/(2*np.pi), color="red", ls="--", lw=1.5,
                    label=f"ω = {ray_omega.value} cph")
        _ax.set_xlabel("N (cph)")
        _ax.set_ylabel("Depth (m)")
        _ax.set_title("Stratification profile")
        _ax.legend()
        _ax.grid(True, alpha=0.3)

        # Right: ray paths
        _ax = _axes[1]
        _colors = plt.cm.plasma(np.linspace(0.2, 0.9, _nsrc))
        _z_srcs = np.linspace(-100, -1500, _nsrc)
        for _i, (_zs_src, _col) in enumerate(zip(_z_srcs, _colors)):
            _xr, _zr = _trace_ray(_zs_src, up=True,  x_max=3e5, ds=200)
            _ax.plot(_xr/1e3, _zr, color=_col, lw=1.2)
            _xr2, _zr2 = _trace_ray(_zs_src, up=False, x_max=3e5, ds=200)
            _ax.plot(_xr2/1e3, _zr2, color=_col, lw=1.2,
                     label=f"src z={_zs_src:.0f} m")

        _ax.set_xlabel("Horizontal distance (km)")
        _ax.set_ylabel("Depth (m)")
        _ax.set_title(f"Ray paths  (ω = {ray_omega.value} cph)")
        _ax.set_xlim(0, 300)
        _ax.set_ylim(-2000, 50)
        _ax.legend(fontsize=8, loc="lower right")
        _ax.grid(True, alpha=0.3)
        _ax.fill_between([0, 300], [-2000, -2000], [-2050, -2050],
                         color="#8D6E63", alpha=0.5)

        _fig.tight_layout()
        _buf = io.BytesIO()
        _fig.savefig(_buf, format="png", dpi=110)
        plt.close(_fig)
        _buf.seek(0)
        _img = base64.b64encode(_buf.read()).decode()
        mo.Html(f'<img src="data:image/png;base64,{_img}" style="max-width:100%">')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Vertical Modes in a Bounded Ocean

    In an ocean of depth $H$ with rigid-lid boundary conditions ($w=0$ at
    $z=0$ and $z=-H$), the vertical structure of internal waves is described
    by the **eigenvalue problem**:

    $$\frac{d^2 F_n}{dz^2} + \frac{N^2(z)}{c_n^2} F_n = 0,
    \qquad F_n(0) = F_n(-H) = 0$$

    where $c_n = \omega/k$ is the **mode speed** (equivalent phase speed) and
    $F_n(z)$ is the vertical structure of horizontal velocity.
    Mode $n$ has $n$ zero-crossings and characteristic horizontal scale:

    $$L_n = c_n / f \qquad \text{(deformation radius of mode } n \text{)}$$

    The pressure/density structure is given by $p \propto F_n$, while
    vertical velocity scales as $dF_n/dz$.

    For constant $N$, the solutions are simply:

    $$F_n(z) = \sin\!\left(\frac{n\pi(z+H)}{H}\right), \quad
    c_n = \frac{NH}{n\pi}$$
    """)
    return


@app.cell
def _(mo):
    vm_N_sl   = mo.ui.slider(1, 30, value=10, step=1,
                              label="N (cph)")
    vm_H_sl   = mo.ui.slider(200, 5000, value=2000, step=100,
                              label="Ocean depth H (m)")
    vm_nmodes = mo.ui.slider(1, 8, value=4, step=1,
                              label="Number of modes to show")
    vm_strat  = mo.ui.dropdown(
        ["Constant N", "Tanh (thermocline)"],
        value="Tanh (thermocline)",
        label="Stratification",
    )
    mo.vstack([vm_strat, vm_N_sl, vm_H_sl, vm_nmodes])
    return vm_H_sl, vm_N_sl, vm_nmodes, vm_strat


@app.cell
def _(base64, io, mo, np, plt, vm_H_sl, vm_N_sl, vm_nmodes, vm_strat):
    _N0  = vm_N_sl.value * 2*np.pi/3600
    _H   = vm_H_sl.value
    _nmo = vm_nmodes.value

    _nz = 500
    _z  = np.linspace(-_H, 0, _nz)
    _dz = _z[1] - _z[0]

    if vm_strat.value == "Constant N":
        _N2 = np.full(_nz, _N0**2)
    else:
        _N2 = _N0**2 * (1 + np.tanh((_z + _H/4) / (_H/10))) / 2

    # Build tridiagonal eigenvalue matrix for d²F/dz² + (N²/c²)F = 0
    # Discretise: F'' ≈ (F_{j+1} - 2F_j + F_{j-1})/dz²
    # Interior points only (Dirichlet BCs)
    _ni = _nz - 2
    _diag  = -2.0 * np.ones(_ni) / _dz**2
    _off   =  1.0 * np.ones(_ni - 1) / _dz**2
    _N2int = _N2[1:-1]

    from scipy.linalg import eigh_tridiagonal
    # Eigenvalues of d²/dz² (Dirichlet BCs) are all negative:
    # μ_n ≈ -(nπ/H)².  Mode 1 has the LARGEST (least-negative) eigenvalue.
    # Select the top _nmo eigenvalues (indices _ni-_nmo to _ni-1).
    _eigvals, _eigvecs = eigh_tridiagonal(_diag, _off,
                                          select="i",
                                          select_range=(_ni - _nmo, _ni - 1))
    # Reverse so mode 1 comes first
    _eigvals = _eigvals[::-1]
    _eigvecs = _eigvecs[:, ::-1]

    # c_n = N_mean / sqrt(|μ_n|)  (exact for constant N; approx for variable N)
    _N2mean = np.mean(_N2int)
    _c_n    = np.sqrt(-_N2mean / _eigvals)   # modal speeds (all positive)

    _fig, _axes = plt.subplots(1, 2, figsize=(10, 5))

    _ax = _axes[0]
    _ax.plot(_N2**0.5 * 3600/(2*np.pi), _z, color="#2196F3", lw=2)
    _ax.set_xlabel("N (cph)")
    _ax.set_ylabel("Depth (m)")
    _ax.set_title("N(z) profile")
    _ax.grid(True, alpha=0.3)

    _ax = _axes[1]
    _cols = plt.cm.tab10(np.linspace(0, 0.9, _nmo))
    for _n in range(_nmo):
        _F = np.zeros(_nz)
        _F[1:-1] = _eigvecs[:, _n]
        _F /= np.max(np.abs(_F) + 1e-30)
        _ax.plot(_F, _z, color=_cols[_n], lw=2,
                 label=f"Mode {_n+1}  c={_c_n[_n]:.1f} m/s")

    _ax.axvline(0, color="k", ls="--", lw=0.8)
    _ax.set_xlabel("Normalised horizontal velocity F_n(z)")
    _ax.set_ylabel("Depth (m)")
    _ax.set_title("Vertical mode structures")
    _ax.legend(fontsize=8)
    _ax.grid(True, alpha=0.3)

    _fig.tight_layout()
    _buf = io.BytesIO()
    _fig.savefig(_buf, format="png", dpi=110)
    plt.close(_fig)
    _buf.seek(0)
    _img = base64.b64encode(_buf.read()).decode()
    mo.Html(f'<img src="data:image/png;base64,{_img}" style="max-width:100%">')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 6 · 2-D Internal Wave Beam Simulation

    We now simulate an internal wave beam in a **2-D ($x$-$z$) domain** with
    uniform stratification $N$ and rotation $f$.

    The governing equations for the perturbation velocity and buoyancy are:

    $$\frac{\partial u}{\partial t} - f v = -\frac{1}{\rho_0}\frac{\partial p'}{\partial x}$$
    $$\frac{\partial v}{\partial t} + f u = 0$$
    $$\frac{\partial w}{\partial t} = -\frac{1}{\rho_0}\frac{\partial p'}{\partial z} + b$$
    $$\frac{\partial b}{\partial t} + N^2 w = 0$$
    $$\frac{\partial u}{\partial x} + \frac{\partial w}{\partial z} = 0$$

    where $b = -g\rho'/\rho_0$ is the buoyancy perturbation.

    Eliminating pressure using incompressibility, we track the **velocity
    potential** $\psi$ ($u = \partial\psi/\partial z$, $w = -\partial\psi/\partial x$).
    The single evolution equation for the stream function is:

    $$\frac{\partial^2}{\partial t^2}\nabla^2\psi + N^2 \frac{\partial^2\psi}{\partial x^2}
    + f^2 \frac{\partial^2\psi}{\partial z^2} = S(x,z,t)$$

    where $S$ is an oscillating source at frequency $\omega$.

    **Simulation**: We force the fluid at a point source oscillating at $\omega$,
    and watch the cross-shaped beam pattern develop (St. Andrew's Cross).
    """)
    return


@app.cell
def _(mo):
    sim_N_sl    = mo.ui.slider(1, 20, value=10, step=1,
                               label="N (cph)")
    sim_f_sl    = mo.ui.slider(0, 5, value=1, step=0.5,
                               label="f (cph)")
    sim_omega_sl= mo.ui.slider(1, 18, value=6, step=1,
                               label="Source frequency ω (cph)")
    sim_T_sl    = mo.ui.slider(1, 20, value=8, step=1,
                               label="Simulation duration (wave periods)")
    sim_run     = mo.ui.run_button(label="▶ Run Wave Beam Simulation")
    mo.vstack([
        mo.md("**Configure and run the 2-D internal wave simulation:**"),
        sim_N_sl, sim_f_sl, sim_omega_sl, sim_T_sl,
        sim_run,
        mo.callout(
            mo.md("Larger grids or longer durations will take more time. "
                  "Start with defaults for a quick preview."),
            kind="info",
        ),
    ])
    return sim_N_sl, sim_T_sl, sim_f_sl, sim_omega_sl, sim_run


@app.cell
def _(mo, sim_run):
    mo.stop(not sim_run.value, mo.md("Press **▶ Run Wave Beam Simulation** above."))
    return


@app.cell
def _(base64, io, mo, np, plt, sim_N_sl, sim_T_sl, sim_f_sl, sim_omega_sl):
    from PIL import Image as _PIL_Image

    _N     = sim_N_sl.value    * 2*np.pi/3600
    _f     = sim_f_sl.value    * 2*np.pi/3600
    _omega = sim_omega_sl.value * 2*np.pi/3600
    _nT    = sim_T_sl.value

    if _omega >= _N or (_f > 0 and _omega <= _f):
        mo.md("⚠️ Need f < ω < N for internal waves to exist.")
    else:
        # Grid
        _Lx, _Lz = 200e3, 100e3          # domain size (m)
        _Nx, _Nz = 128, 64
        _dx = _Lx / _Nx
        _dz = _Lz / _Nz
        _x  = np.linspace(0, _Lx, _Nx, endpoint=False)
        _z  = np.linspace(0, _Lz, _Nz, endpoint=False)

        # Spectral operators
        _kx = 2*np.pi * np.fft.fftfreq(_Nx, d=_dx)
        _kz = 2*np.pi * np.fft.fftfreq(_Nz, d=_dz)
        _KX, _KZ = np.meshgrid(_kx, _kz, indexing="ij")
        _K2 = _KX**2 + _KZ**2
        _K2[0, 0] = 1.0            # avoid div/0 at DC

        # Invert Laplacian: ψ = L⁻¹ RHS
        def _inv_laplacian(rhs_hat):
            return -rhs_hat / _K2

        # Source: Gaussian blob at domain centre, oscillating at ω
        _xc, _zc = _Lx/2, _Lz/2
        _sigma_s  = 5e3    # source width (m)
        _XX, _ZZ  = np.meshgrid(_x, _z, indexing="ij")
        _source_env = np.exp(-(((_XX-_xc)**2 + (_ZZ-_zc)**2) / (2*_sigma_s**2)))

        # Time integration of  ∂²/∂t² ∇²ψ + N² ∂²ψ/∂x² + f² ∂²ψ/∂z² = S
        # Use second-order leapfrog on ∇²ψ ≡ q
        # ∂²q/∂t² = -(N²kx² + f²kz²)/K² * q + Ŝ/K²  →  simple harmonic oscillator per mode

        _T_wave  = 2*np.pi / _omega
        _T_sim   = _nT * _T_wave
        _dt      = _T_wave / 40           # 40 steps per period
        _nsteps  = int(_T_sim / _dt)
        _nframes = min(60, _nsteps)
        _frame_interval = max(1, _nsteps // _nframes)

        # Characteristic frequency per spectral mode
        _omega_hat2 = (_N**2 * _KX**2 + _f**2 * _KZ**2) / _K2   # ω²(k,m)

        # Initialise
        _psi_hat  = np.zeros((_Nx, _Nz), dtype=complex)
        _dpsi_hat = np.zeros((_Nx, _Nz), dtype=complex)  # ∂/∂t ψ_hat

        # We integrate ∂²/∂t² ψ̂_k + ω_k² ψ̂_k = Ŝ_k(t)
        # using Störmer-Verlet (leapfrog):
        #   ψ̂^{n+1} = 2ψ̂^n - ψ̂^{n-1} - dt² ω_k² ψ̂^n + dt² Ŝ_k^n

        _source_hat_env = np.fft.fft2(_source_env) / _K2  # ∇⁻²(source_env)

        _frames_psi = []
        _psi_prev = _psi_hat.copy()
        _t = 0.0

        for _step in range(_nsteps + 1):
            _S_now = _source_env * np.sin(_omega * _t)
            _S_hat = np.fft.fft2(_S_now) / _K2

            _psi_new = 2*_psi_hat - _psi_prev - _dt**2 * (_omega_hat2 * _psi_hat - _S_hat)

            if _step % _frame_interval == 0:
                _psi_phys = np.real(np.fft.ifft2(_psi_hat))
                # vertical velocity w = -∂ψ/∂x (spectral)
                _w_hat  = -1j * _KX * _psi_hat
                _w_phys = np.real(np.fft.ifft2(_w_hat))
                _frames_psi.append(_w_phys.copy())

            _psi_prev = _psi_hat
            _psi_hat  = _psi_new
            _t += _dt

        # Compute expected beam angle
        _cos_th  = np.sqrt((_omega**2 - _f**2) / (_N**2 - _f**2))
        _beam_deg = np.degrees(np.arccos(_cos_th))

        # Build GIF
        _half = _frames_psi[len(_frames_psi)//2:]
        _vmax = max(np.abs(_fr).max() for _fr in _half) if _half else 1e-10
        _vmax = max(_vmax, 1e-10)

        _gif_frames = []
        for _i, _w in enumerate(_frames_psi):
            _fig2, _ax2 = plt.subplots(figsize=(7, 4))
            _im = _ax2.pcolormesh(
                _x/1e3, _z/1e3, _w.T,
                cmap="RdBu_r", vmin=-_vmax, vmax=_vmax, shading="auto",
            )
            plt.colorbar(_im, ax=_ax2, label="w (m/s)")
            _ax2.set_xlabel("x (km)")
            _ax2.set_ylabel("z (km)")
            _ax2.set_title(
                f"Internal wave beam  (N={sim_N_sl.value} cph, "
                f"ω={sim_omega_sl.value} cph, beam angle={_beam_deg:.1f}°)\n"
                f"t = {_i * _frame_interval * _dt / _T_wave:.1f} wave periods"
            )
            _ax2.plot(_xc/1e3, _zc/1e3, "k*", ms=8, label="Source")
            _ax2.legend(fontsize=8)
            _fig2.tight_layout()

            _fb = io.BytesIO()
            _fig2.savefig(_fb, format="png", dpi=80)
            plt.close(_fig2)
            _fb.seek(0)
            _gif_frames.append(_PIL_Image.open(_fb).convert("P"))

        _gif_buf = io.BytesIO()
        _gif_frames[0].save(
            _gif_buf, format="GIF", save_all=True,
            append_images=_gif_frames[1:], loop=0, duration=80,
        )
        _gif_buf.seek(0)
        _gif_b64 = base64.b64encode(_gif_buf.read()).decode()

        mo.vstack([
            mo.md(f"**Beam angle from horizontal:** {_beam_deg:.1f}°  "
                  f"(set by cos θ = √[(ω²−f²)/(N²−f²)])"),
            mo.Html(f'<img src="data:image/gif;base64,{_gif_b64}" '
                    f'style="max-width:100%; border:1px solid #ccc">'),
        ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 7 · Garrett-Munk Spectrum

    The ocean is filled with a broad-band background of internal waves.
    **Munk (1981)** and **Garrett & Munk (1972)** described this background
    as a universal spectrum known as the **Garrett-Munk (GM) spectrum**.

    The GM energy density in frequency-wavenumber space takes the form:

    $$E(\omega, j) \propto \frac{f}{\omega\sqrt{\omega^2 - f^2}} \cdot
    \frac{1}{(j^2 + j_*^2)}$$

    where $j$ is the vertical mode number and $j_* \approx 3$ is a reference
    mode number (GM76 value).

    Key features:
    - Energy falls off as $\omega^{-2}$ at high frequency (between $f$ and $N$)
    - Most energy is at **near-inertial frequencies** (just above $f$)
    - Low vertical modes ($j = 1, 2, 3$) carry most of the energy
    - Total energy density: $E \approx 3 \times 10^{-3}$ m² s⁻²
    """)
    return


@app.cell
def _(base64, io, mo, np, plt):
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 4))

    # Frequency spectrum S(ω) ∝ f / (ω√(ω²-f²))
    _f_gm  = 1.0 * 2*np.pi/3600   # 1 cph (mid-latitude)
    _N_gm  = 10.0 * 2*np.pi/3600  # 10 cph
    _om    = np.linspace(_f_gm*1.02, _N_gm*0.98, 500)
    _S_om  = _f_gm / (_om * np.sqrt(_om**2 - _f_gm**2))
    _S_om /= np.trapz(_S_om, _om)   # normalise

    _ax = _axes[0]
    _ax.semilogy((_om/(2*np.pi))*3600, _S_om * 3600/(2*np.pi),
                 color="#2196F3", lw=2)
    _ax.axvline(_f_gm * 3600/(2*np.pi), color="red",   ls="--",
                lw=1.5, label="f (near-inertial)")
    _ax.axvline(_N_gm * 3600/(2*np.pi), color="green", ls="--",
                lw=1.5, label="N")
    _ax.set_xlabel("Frequency (cph)")
    _ax.set_ylabel("Normalised energy density")
    _ax.set_title("GM frequency spectrum")
    _ax.legend()
    _ax.grid(True, which="both", alpha=0.3)

    # Mode spectrum S(j) ∝ 1/(j² + j*²)
    _j    = np.arange(1, 21)
    _jstr = 3
    _S_j  = 1.0 / (_j**2 + _jstr**2)
    _S_j /= _S_j.sum()

    _ax = _axes[1]
    _ax.bar(_j, _S_j, color="#E91E63", alpha=0.8)
    _ax.set_xlabel("Vertical mode number j")
    _ax.set_ylabel("Relative energy")
    _ax.set_title(f"GM mode spectrum (j* = {_jstr})")
    _ax.grid(True, axis="y", alpha=0.3)

    _fig.tight_layout()
    _buf = io.BytesIO()
    _fig.savefig(_buf, format="png", dpi=110)
    plt.close(_fig)
    _buf.seek(0)
    _img = base64.b64encode(_buf.read()).decode()
    mo.Html(f'<img src="data:image/png;base64,{_img}" style="max-width:100%">')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## 8 · Physical Interpretation & Oceanic Role

    ### Why internal waves matter

    | Process | Role of internal waves |
    |---------|----------------------|
    | **Diapycnal mixing** | Breaking internal waves provide ~90% of the energy for deep-ocean mixing |
    | **Tidal energy dissipation** | Barotropic tides excite internal tides at topography; these radiate away as low-mode internal waves |
    | **Near-inertial waves** | Wind-forced; carry ~30% of the total internal wave energy; important for upper-ocean mixing |
    | **Lee waves** | Stratified flow over topography generates internal waves that dissipate downstream |
    | **Momentum transport** | Internal waves flux horizontal momentum upward/downward, driving the QBO and other stratospheric oscillations |

    ### Key dimensionless numbers

    | Parameter | Definition | Meaning |
    |-----------|-----------|---------|
    | Froude number | $Fr = U/NH$ | Ratio of inertial to buoyancy forces |
    | Richardson number | $Ri = N^2 / (dU/dz)^2$ | Stability against shear instability; $Ri < 1/4$ → unstable |
    | Rossby number | $Ro = U/fL$ | Ratio of inertial to Coriolis forces |

    ### Connection to the two-layer model

    The two-layer model introduced in Section 1 is the $n=1$ vertical mode
    of the full continuously stratified problem. Each baroclinic mode has a
    corresponding "reduced gravity" and deformation radius:

    $$g_n' = (c_n)^2 / H, \qquad L_{R,n} = c_n / f$$

    Mode 1 dominates large-scale ocean variability (mesoscale eddies, El Niño),
    while higher modes are important for internal wave dynamics and tidal mixing.

    ### Summary of wave properties

    | Property | Internal gravity wave |
    |---------|-----------------------|
    | Restoring force | Buoyancy |
    | Frequency range | $f \le \omega \le N$ |
    | Propagation | Along wave beams at angle $\theta$ to horizontal |
    | Group velocity | ⊥ to phase velocity |
    | Vertical propagation | Phase down ↔ energy up |
    | Breaking | When wave amplitude → background stratification |
    """)
    return


if __name__ == "__main__":
    app.run()
