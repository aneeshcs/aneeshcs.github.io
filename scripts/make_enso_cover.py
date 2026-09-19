#!/usr/bin/env python3
"""Generate the ensō cover image for the ENSO / barrier layer news post.

An ensō (円相) is the circle a calligrapher draws in a single breath with a
sumi brush. This script builds one procedurally rather than reusing an
existing artwork: a bundle of bristles is swept once around a hand-wobbled
circle, losing ink as it travels, and the resulting coverage field is
composited onto a paper ground.

The brush model has three ingredients, each with a physical reading:

* **pressure** — the brush is planted at the start and lifts through the
  sweep, so stroke width decays monotonically with arclength;
* **ink depletion** — the load carried by the bristles falls as the stroke
  advances. Below a load threshold individual bristles stop wetting the
  paper, which is what produces the dry-brush striation (kasure, 掠れ) that
  opens up over the second half of the stroke. Outer bristles, carrying less
  ink than the core, run dry first;
* **capillary bleed** — ink wicks a short distance into the paper fibres
  (nijimi, 滲み), a faint halo around the wet core.

The stroke begins east-southeast and sweeps clockwise, so the gap where it
fails to close falls on the east — the direction the Pacific warm pool
migrates during El Niño.

Everything is vectorised over the (sample, bristle) grid and seeded, so the
output is reproducible from SEED alone. Only the encoded WebP is committed to
the repository; regenerate the master with this script.

Usage:
    python3 scripts/make_enso_cover.py [output.webp]
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, gaussian_filter1d

# ----------------------------------------------------------------- constants

SEED: int = 20260918

WIDTH: int = 1600  # 16:9 — matches the theme's 800x450 card fill exactly,
HEIGHT: int = 900  # so the listing thumbnail is a downscale, not a crop.
SS: int = 3        # supersampling factor for the coverage field

N_SAMPLES: int = 24_000    # samples along the stroke centreline
N_BRISTLES: int = 800      # bristles across the brush
CHUNK: int = 3_000         # centreline samples splatted per pass

PAPER_RGB: tuple[int, int, int] = (0xF2, 0xEF, 0xE8)
INK_DENSE_RGB: tuple[int, int, int] = (0x17, 0x18, 0x1A)
INK_THIN_RGB: tuple[int, int, int] = (0x4A, 0x43, 0x3A)

DEFAULT_OUT = Path("content/post/lin-2026-barrier-layer-published/featured.webp")


# ----------------------------------------------------------------- utilities


def _unit_noise_1d(rng: np.random.Generator, n: int, sigma: float) -> np.ndarray:
    """Smooth zero-mean noise of unit standard deviation."""
    z = gaussian_filter1d(rng.standard_normal(n), sigma=sigma, mode="nearest")
    return z / z.std()


def _smoothstep(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    t = np.clip((x - lo) / (hi - lo), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ------------------------------------------------------------------ geometry


def centreline(
    rng: np.random.Generator,
) -> tuple[np.ndarray, ...]:
    """Path, width, per-sample arclength and dryness of the single stroke.

    Returns ``(x, y, nx, ny, width, ds, dryness)`` in supersampled pixels,
    where ``(nx, ny)`` is the unit normal to the path.
    """
    t = np.linspace(0.0, 1.0, N_SAMPLES)

    # Clockwise from east-southeast; 340° leaves a 20° opening on the east.
    theta = np.deg2rad(-25.0) + np.deg2rad(-344.0) * t

    radius = 0.36 * HEIGHT * SS
    # Low-order radial wobble — a circle drawn by hand is never round.
    wobble = (
        0.022 * np.sin(2.0 * theta + 0.7)
        + 0.014 * np.sin(3.0 * theta + 2.1)
        + 0.008 * np.sin(5.0 * theta + 4.3)
    )
    # A slow inward spiral so the tail passes inside the head instead of
    # meeting it: the cycle does not close on itself.
    r = radius * (1.0 + wobble - 0.035 * t)

    cx, cy = 0.5 * WIDTH * SS, 0.475 * HEIGHT * SS
    x = cx + 1.03 * r * np.cos(theta)  # slight ellipticity
    y = cy - r * np.sin(theta)

    # Tangent and normal from finite differences of the path.
    tx, ty = np.gradient(x), np.gradient(y)
    norm = np.hypot(tx, ty)
    nx, ny = -ty / norm, tx / norm
    ds = norm  # arclength carried by one centreline sample

    # Pressure: the brush is planted with a blunt head, swells and eases as the
    # arm sweeps, lifts steadily, and leaves the paper over the last few percent.
    w0 = 0.30 * radius
    head = 1.0 + 0.28 * np.exp(-((t / 0.07) ** 2))
    taper = 1.0 - 0.30 * t**1.1
    lift = 1.0 - 0.50 * np.clip((t - 0.94) / 0.06, 0.0, 1.0) ** 1.4
    swell = 1.0 + 0.16 * _unit_noise_1d(rng, N_SAMPLES, N_SAMPLES / 5.0)
    width = w0 * head * taper * lift * swell

    # Ink depletes roughly linearly with distance travelled.
    dryness = np.clip(t**0.75 + 0.07 * _unit_noise_1d(rng, N_SAMPLES, N_SAMPLES / 30), 0.0, 1.0)

    return x, y, nx, ny, width, ds, dryness


# ------------------------------------------------------------------ coverage


def _splat(
    canvases: list[np.ndarray],
    px: np.ndarray,
    py: np.ndarray,
    weights: list[np.ndarray],
) -> None:
    """Bilinear scatter of several weight fields sharing one set of points."""
    w_px, h_px = WIDTH * SS, HEIGHT * SS
    keep = weights[0] > 0.0
    px, py = px[keep], py[keep]
    weights = [w[keep] for w in weights]
    if px.size == 0:
        return

    x0 = np.floor(px).astype(np.int64)
    y0 = np.floor(py).astype(np.int64)
    fx, fy = px - x0, py - y0

    idx_parts: list[np.ndarray] = []
    frac_parts: list[np.ndarray] = []
    for dx, dy, frac in (
        (0, 0, (1.0 - fx) * (1.0 - fy)),
        (1, 0, fx * (1.0 - fy)),
        (0, 1, (1.0 - fx) * fy),
        (1, 1, fx * fy),
    ):
        ix, iy = x0 + dx, y0 + dy
        inside = (ix >= 0) & (ix < w_px) & (iy >= 0) & (iy < h_px)
        idx_parts.append(iy[inside] * w_px + ix[inside])
        frac_parts.append((frac, inside))

    index = np.concatenate(idx_parts)
    for canvas, wt in zip(canvases, weights):
        canvas += np.bincount(
            index,
            weights=np.concatenate([(wt * frac)[inside] for frac, inside in frac_parts]),
            minlength=w_px * h_px,
        ).astype(np.float32)


def ink_coverage(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Supersampled ink coverage and ink tone.

    Coverage is ~1 where the brush laid a full wet load. Tone is the
    coverage-weighted mean of the ink carried by the bristles that passed
    through each pixel: 1 for a saturated black load, falling towards 0 as the
    brush dries and the stroke browns.
    """
    x, y, nx, ny, width, ds, dryness = centreline(rng)
    xi = np.linspace(-1.0, 1.0, N_BRISTLES)  # position across the brush

    # Kasure. A noise field smoothed hard along the stroke and lightly across
    # the bristles, so where it lifts bristles it does so for a long run —
    # streaks parallel to the stroke rather than speckle.
    # Two scales: tufts of bristles that dry out together and open broad gaps,
    # plus a finer component that draws the hairline streaks through ink that
    # is otherwise still wet.
    noise = rng.standard_normal((N_SAMPLES, N_BRISTLES)).astype(np.float32)
    tufts = gaussian_filter(noise, sigma=(N_SAMPLES / 60.0, N_BRISTLES / 26.0), mode="nearest")
    hairs = gaussian_filter(noise, sigma=(N_SAMPLES / 160.0, N_BRISTLES / 95.0), mode="nearest")
    del noise
    load = 0.78 * tufts / tufts.std() + 0.55 * hairs / hairs.std()
    load /= load.std()
    del tufts, hairs
    # Threshold falls as the brush dries; outer bristles, carrying less ink,
    # cross it well before the core does.
    threshold = (2.4 - 3.8 * dryness[:, None]) + 1.15 * (1.0 - np.abs(xi))[None, :] ** 0.8
    wetting = load < threshold

    # Per-bristle wander, in units of the brush half-width: this is what makes
    # the stroke edge fibrous instead of geometric.
    wander = gaussian_filter1d(
        rng.standard_normal((N_SAMPLES, N_BRISTLES)).astype(np.float32),
        sigma=N_SAMPLES / 900.0,
        axis=0,
        mode="nearest",
    )
    wander *= 0.070 / wander.std()
    # Dither the bristle axis so the discrete bundle does not print as a weave.
    wander += rng.uniform(-1.0, 1.0, wander.shape).astype(np.float32) / N_BRISTLES

    # Ink carried by the brush: saturated at the outset, thinning as it runs
    # out, with a slow variation from the unevenness of the original load.
    tone = np.clip(
        1.0 - 0.45 * dryness + 0.08 * _unit_noise_1d(rng, N_SAMPLES, N_SAMPLES / 9.0),
        0.0,
        1.0,
    )

    canvas = np.zeros(WIDTH * SS * HEIGHT * SS, dtype=np.float32)
    canvas_tone = np.zeros_like(canvas)
    for lo in range(0, N_SAMPLES, CHUNK):
        sl = slice(lo, min(lo + CHUNK, N_SAMPLES))
        offset = (xi[None, :] + wander[sl]) * (0.5 * width[sl, None])
        px = x[sl, None] + nx[sl, None] * offset
        py = y[sl, None] + ny[sl, None] * offset
        # Weight so that a fully wetted stroke deposits unit coverage per unit
        # area regardless of how wide or how fast the brush is moving.
        wt = np.broadcast_to(
            (width[sl] * ds[sl] / N_BRISTLES)[:, None], offset.shape
        ) * wetting[sl]
        flat = wt.ravel()
        _splat(
            [canvas, canvas_tone],
            px.ravel(),
            py.ravel(),
            [flat, flat * np.broadcast_to(tone[sl, None], offset.shape).ravel()],
        )

    shape = (HEIGHT * SS, WIDTH * SS)
    return canvas.reshape(shape), canvas_tone.reshape(shape)


# --------------------------------------------------------------- compositing


def paper_ground(rng: np.random.Generator) -> np.ndarray:
    """Warm off-white ground with faint fibre grain, mottle and vignette."""
    grain = gaussian_filter(rng.standard_normal((HEIGHT, WIDTH)).astype(np.float32), 1.1)
    grain /= grain.std()
    mottle = gaussian_filter(rng.standard_normal((HEIGHT, WIDTH)).astype(np.float32), 55.0)
    mottle /= mottle.std()

    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    radial = np.hypot((xx - WIDTH / 2) / (WIDTH / 2), (yy - HEIGHT / 2) / (HEIGHT / 2))
    vignette = 1.0 - 0.022 * np.clip(radial, 0.0, 1.4) ** 2

    shade = (1.0 + 0.010 * grain + 0.012 * mottle) * vignette
    base = np.array(PAPER_RGB, dtype=np.float32) / 255.0
    return np.clip(base[None, None, :] * shade[..., None], 0.0, 1.0)


def render(seed: int = SEED) -> Image.Image:
    rng = np.random.default_rng(seed)

    cov_ss, tone_ss = ink_coverage(rng)
    cov_ss = gaussian_filter(cov_ss, sigma=1.5)  # knit the scattered points
    tone_ss = gaussian_filter(tone_ss, sigma=1.5)
    cov = cov_ss.reshape(HEIGHT, SS, WIDTH, SS).mean(axis=(1, 3))
    tone = tone_ss.reshape(HEIGHT, SS, WIDTH, SS).mean(axis=(1, 3))
    del cov_ss, tone_ss

    alpha = _smoothstep(cov, 0.26, 0.58)
    bleed = gaussian_filter(alpha, 10.0) * 0.06  # nijimi
    alpha = np.clip(alpha + bleed * (1.0 - alpha), 0.0, 1.0)

    # Thin ink is warm grey, dense ink near-black — as sumi behaves on paper.
    # Divide out the coverage to recover the mean tone carried into each pixel.
    density = np.clip(tone / np.maximum(cov, 1e-3), 0.0, 1.0)
    density = np.clip(density * _smoothstep(cov, 0.10, 0.75), 0.0, 1.0)[..., None]
    dense = np.array(INK_DENSE_RGB, dtype=np.float32) / 255.0
    thin = np.array(INK_THIN_RGB, dtype=np.float32) / 255.0
    ink = thin + (dense - thin) * density

    rgb = paper_ground(rng) * (1.0 - alpha[..., None]) + ink * alpha[..., None]
    return Image.fromarray(np.round(np.clip(rgb, 0.0, 1.0) * 255.0).astype(np.uint8), "RGB")


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUT
    image = render()

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
        master = Path(handle.name)
    image.save(master)

    subprocess.run(
        ["cwebp", "-q", "86", "-m", "6", "-quiet", str(master), "-o", str(out)],
        check=True,
    )
    print(f"{out}  {image.width}x{image.height}  {out.stat().st_size / 1024:.0f} KB")
    print(f"master (uncommitted): {master}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
