#!/usr/bin/env python3
"""Render the explainer video for the Zhu et al. (2026, GRL) news post.

Zhu, Han, Wang, Zheng, Suhas, Subramanian, Leung, Garuba & Balaguru (2026),
"Decadal Sea Level Variability Along the U.S. East Coast: Roles of
Extratropical Versus Tropical Climate Modes Over the North Atlantic Ocean",
Geophysical Research Letters 53, e2026GL125873 (CC BY 4.0).

The video tells the paper's argument in six beats, each tied to a figure:

1. **The signal** -- decadal sea level anomalies (SLAs) at USEC tide gauges,
   north and south of Cape Hatteras (Fig. 1a-c, observed curve eta^O).
2. **Local versus remote** -- a barotropic coastal model gives the locally
   forced part eta^L; the residual eta^R = eta^O - eta^L is remote and explains
   81.2 % (north) and 88.8 % (south) of the variance (Fig. 1b-c).
3. **Rossby waves** -- first-mode baroclinic Rossby waves, forced by wind
   curl and by buoyancy (heat and freshwater) fluxes, carry the open-ocean
   signal westward to the boundary, where coastally trapped waves pass it
   along the shelf (Section 3.1, Fig. 2). Roughly half the decadal variance
   travels this way.
4. **Which modes** -- Rossby waves forced by the tropical modes (AMM +
   Atlantic Nino) explain 34.6 % / 27.7 % of the remote variance in the
   north / south, against 25.9 % / 40.9 % for the extratropical NAO + AMO
   (Fig. 3c-d).
5. **The AMM "double whammy"** -- during positive AMM phases a cyclonic
   anomaly sits over the North Atlantic. In region R2 (northwest, >~40 N) its
   wind and buoyancy forcing both lower sea level; in R1 (southwest) they
   oppose and cancel (Fig. 4a).
6. **Takeaway** and citation.

Curves in beats 1-2 are digitized from Fig. 1b-c; the gauge positions and the
R1/R2 boxes are read off Figs. 1a and 4a (see scripts/data/zhu2026/paper.json).
Waves, arrows and mode footprints are schematic and labelled as such. Text is
set with manim's Pango `Text` only, so no LaTeX installation is needed.

Usage:
    uvx --with manim manim -qh scripts/make_usec_sea_level_video.py UsecSeaLevel   # 1080p60
    uvx --with manim manim -ql scripts/make_usec_sea_level_video.py UsecSeaLevel   # quick preview
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from manim import (
    BOLD, DOWN, LEFT, RIGHT, UP, Arc, Arrow, Circle, Create, Dot, DashedLine, FadeIn,
    FadeOut, GrowArrow, GrowFromCenter, GrowFromEdge, LaggedStart, Line,
    MoveAlongPath, Polygon, Rectangle, RoundedRectangle, Scene, Text,
    Transform, VGroup, VMobject, config, linear, smooth, there_and_back,
)

DATA = Path(__file__).with_name("data") / "zhu2026"
PAPER = json.loads((DATA / "paper.json").read_text())
LAND = json.loads((DATA / "land.json").read_text())["polygons"]

# Palette: the slate / amber / violet of the barrier-layer post, on a dark ground.
FONT = "Avenir Next"
BG, OCEAN, LAND_FILL, LAND_EDGE = "#0f172a", "#10233f", "#334155", "#475569"
INK, MUTED = "#e2e8f0", "#94a3b8"
HIGH, LOW = "#f59e0b", "#38bdf8"      # sea level above / below normal
TROPICAL, EXTRATROPICAL = "#f59e0b", "#38bdf8"
BUOYANCY, GAUGE, BOX = "#a78bfa", "#4ade80", "#4ade80"

config.background_color = BG

# Plate carree map, as in the paper's figures: 98W-2W, 6S-64N.
SCALE, LON0, LAT0, X0, Y0 = 0.085, -98.0, -6.0, -6.85, -3.05


def ll(lat: float, lon: float) -> np.ndarray:
    """Scene coordinates of a (lat, lon) point."""
    return np.array([X0 + (lon - LON0) * SCALE, Y0 + (lat - LAT0) * SCALE, 0.0])


def txt(s: str, size: float = 24, color: str = INK, bold: bool = False) -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=BOLD if bold else "NORMAL")


class MiniChart(VGroup):
    """A small time-series panel built from lines and Pango text (no LaTeX)."""

    def __init__(self, title: str, center: np.ndarray, width: float = 4.9,
                 height: float = 1.75, vmax: float = 60.0,
                 t0: float = 1950.0, t1: float = 2023.0) -> None:
        super().__init__()
        self.c, self.w, self.h, self.vmax, self.t0, self.t1 = center, width, height, vmax, t0, t1
        frame = Rectangle(width=width, height=height, stroke_color=LAND_EDGE, stroke_width=1.5).move_to(center)
        zero = Line(self.p(t0, 0), self.p(t1, 0), stroke_color=MUTED, stroke_width=1, stroke_opacity=0.6)
        self.add(frame, zero, txt(title, 20, INK, bold=True).next_to(frame, UP, buff=0.08).align_to(frame, LEFT))
        for v in (-50, 50):
            self.add(txt(f"{v:+d} mm", 13, MUTED).next_to(self.p(t0, v), LEFT, buff=0.08))
        for yr in (1960, 1980, 2000, 2020):
            self.add(Line(self.p(yr, -vmax), self.p(yr, -vmax) + 0.06 * UP, stroke_color=MUTED, stroke_width=1),
                     txt(str(yr), 13, MUTED).next_to(self.p(yr, -vmax), DOWN, buff=0.06))

    def p(self, t: float, v: float) -> np.ndarray:
        x = (t - self.t0) / (self.t1 - self.t0) - 0.5
        return self.c + np.array([x * self.w, 0.5 * self.h * v / self.vmax, 0.0])

    def curve(self, values: list[float], color: str, width: float = 3.0) -> VMobject:
        pts = [self.p(t, v) for t, v in zip(PAPER["t"], values)]
        return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def sla_blob(color: str, radius: float = 0.6) -> VGroup:
    """A sea-surface height anomaly: concentric rings fading outward."""
    return VGroup(*[
        Circle(radius=radius * k / 4, stroke_width=0,
            fill_color=color, fill_opacity=0.3)
        for k in (4, 3, 2, 1)
    ])


def box(region: dict, label: str) -> VGroup:
    (lo0, lo1), (la0, la1) = region["lon"], region["lat"]
    rect = Polygon(ll(la0, lo0), ll(la0, lo1), ll(la1, lo1), ll(la1, lo0),
                   stroke_color=BOX, stroke_width=3, fill_opacity=0)
    return VGroup(rect, txt(label, 20, BOX, bold=True).next_to(rect.get_corner(UP + LEFT), DOWN + RIGHT, buff=0.06))


class UsecSeaLevel(Scene):
    def construct(self) -> None:
        self.title = txt(" ", 30).to_edge(UP)
        self.caption = txt(" ", 18).to_edge(DOWN)
        self.add(self.title, self.caption)

        self.map = self.build_map()
        self.gauges = VGroup(*[Dot(ll(la, lo), radius=0.045, color=GAUGE) for la, lo in PAPER["gauges_latlon"]])
        hat = PAPER["cape_hatteras_lat"]
        self.north_gauges = VGroup(*[d for d, (la, _) in zip(self.gauges, PAPER["gauges_latlon"]) if la > hat])

        self.beat_signal()
        self.beat_local_remote()
        self.beat_rossby()
        self.beat_modes()
        self.beat_amm()
        self.beat_takeaway()

    # ------------------------------------------------------------------ helpers
    def build_map(self) -> VGroup:
        ocean = Polygon(ll(LAT0, LON0), ll(LAT0, -2), ll(64, -2), ll(64, LON0),
                        stroke_width=0, fill_color=OCEAN, fill_opacity=1)
        land = VGroup(*[
            Polygon(*[ll(la, lo) for lo, la in poly[:-1]], stroke_color=LAND_EDGE,
                    stroke_width=1, fill_color=LAND_FILL, fill_opacity=1)
            for poly in LAND
        ])
        return VGroup(ocean, land)

    def set_title(self, s: str, caption: str = "") -> None:
        new_t = txt(s, 30, INK, bold=True).to_edge(UP, buff=0.3)
        new_c = txt(caption, 17, MUTED).to_edge(DOWN, buff=0.2)
        self.play(Transform(self.title, new_t), Transform(self.caption, new_c), run_time=0.8)

    def set_caption(self, caption: str) -> None:
        self.play(Transform(self.caption, txt(caption, 17, MUTED).to_edge(DOWN, buff=0.2)), run_time=0.6)

    # ------------------------------------------------------------------- beats
    def beat_signal(self) -> None:
        self.set_title("East Coast sea level swings up and down over decades",
                       "Tide-gauge records, 1950-2023, with the long-term trend and global mean removed")
        self.play(FadeIn(self.map), run_time=1.2)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in self.gauges], lag_ratio=0.06), run_time=1.4)

        hat = PAPER["cape_hatteras_lat"]
        self.hatteras = VGroup(
            DashedLine(ll(hat, -75.5), ll(hat, -58), dash_length=0.08, color=INK, stroke_width=2),
            txt("Cape Hatteras", 15, MUTED).next_to(ll(hat, -58), RIGHT, buff=0.08),
            txt("North", 20, INK, bold=True).move_to(ll(40.5, -55)),
            txt("South", 20, INK, bold=True).move_to(ll(30.0, -62)),
        )
        self.play(Create(self.hatteras[0]), FadeIn(self.hatteras[1:]), run_time=1.0)

        self.north = MiniChart("North of Cape Hatteras", np.array([4.3, 1.45, 0]))
        self.south = MiniChart("South of Cape Hatteras", np.array([4.3, -1.55, 0]))
        self.play(FadeIn(self.north), FadeIn(self.south), run_time=0.8)
        self.obs = VGroup(self.north.curve(PAPER["north_O"], INK), self.south.curve(PAPER["south_O"], INK))
        self.play(Create(self.obs), run_time=3.5, rate_func=linear)
        self.set_caption("Decades of higher sea level bring far more frequent nuisance flooding")
        self.wait(1.5)

    def beat_local_remote(self) -> None:
        self.set_title("Most of the swing starts far offshore",
                       "Local: coastal winds and air pressure.   Remote: everything arriving from the open ocean")
        coast_wind = VGroup(*[
            Arrow(ll(la, lo), ll(la - 1.6, lo - 1.4), buff=0, color=INK, stroke_width=3,
                  max_tip_length_to_length_ratio=0.35)
            for la, lo in [(43, -66.5), (40.5, -70.5), (37.5, -73.5)]
        ])
        local = txt("local", 18, INK, bold=True).next_to(coast_wind[1], LEFT, buff=0.15)
        remote_glow = Circle(radius=1.35, stroke_width=0, fill_color=HIGH,
                          fill_opacity=0.12).move_to(ll(28, -40))
        remote = txt("remote", 18, HIGH, bold=True).move_to(ll(28, -40))
        self.play(LaggedStart(*[GrowArrow(a) for a in coast_wind], lag_ratio=0.2), FadeIn(local), run_time=1.2)
        self.play(FadeIn(remote_glow), FadeIn(remote), run_time=1.0)

        rem = VGroup(self.north.curve(PAPER["north_R"], HIGH), self.south.curve(PAPER["south_R"], HIGH))
        self.play(Create(rem), run_time=3.0, rate_func=linear)
        v = PAPER["variance_pct"]["remote"]
        stats = VGroup(
            txt(f"remote: {v['north']:.0f}% of variance", 17, HIGH, bold=True)
            .next_to(self.north.p(2023, -60), UP + LEFT, buff=0.08),
            txt(f"remote: {v['south']:.0f}% of variance", 17, HIGH, bold=True)
            .next_to(self.south.p(2023, -60), UP + LEFT, buff=0.08),
        )
        self.play(FadeIn(stats, shift=0.1 * UP), run_time=0.8)
        self.set_caption("Local winds and pressure explain 41% in the north and nothing in the south (Fig. 1)")
        self.wait(2.0)
        self.play(FadeOut(VGroup(coast_wind, local, remote_glow, remote, self.north, self.south,
                                 self.obs, rem, stats)), run_time=0.8)

    def beat_rossby(self) -> None:
        self.set_title("Signals ride slow Rossby waves west to the coast",
                       "Schematic, not to scale: wind and buoyancy forcing raise or lower the sea surface far offshore")
        notes = VGroup(
            txt("Wind and buoyancy", 22, INK, bold=True),
            txt("(heat and freshwater) forcing", 20, INK),
            txt("launch the waves.", 20, INK),
            txt("They creep west over", 20, INK),
            txt("several years.", 20, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(np.array([4.4, 1.2, 0]))
        self.play(FadeIn(notes[:3]), run_time=0.8)

        # Two zonal sections, as in the Hovmoller diagrams of Fig. 2c-d.
        paths = [(33.5, -40, -76.5, HIGH), (47.5, -30, -52.5, LOW)]
        forcing, blobs = VGroup(), VGroup()
        for lat, lon_start, _, color in paths:
            wind = Arc(radius=0.45, start_angle=0, angle=1.6 * np.pi, color=INK, stroke_width=3,
                       arc_center=ll(lat, lon_start)).add_tip(tip_length=0.14)
            heat = VGroup(*[Arrow(ll(lat - 2.5, lon_start + d), ll(lat + 3.5, lon_start + d), buff=0,
                                  color=BUOYANCY, stroke_width=3, max_tip_length_to_length_ratio=0.3)
                            for d in (-6, 6)])
            forcing.add(VGroup(wind, heat))
            blobs.add(sla_blob(color).move_to(ll(lat, lon_start)))
        self.play(Create(forcing[0][0]), Create(forcing[1][0]), *[GrowArrow(a) for f in forcing for a in f[1]],
                  run_time=1.2)
        self.play(FadeIn(blobs, scale=0.3), FadeOut(forcing), run_time=1.0)

        tracks = VGroup(*[DashedLine(ll(lat, lon0), ll(lat, lon1), dash_length=0.06, color=MUTED, stroke_width=1.5)
                          for lat, lon0, lon1, _ in paths])
        self.play(FadeIn(tracks), FadeIn(notes[3:]), run_time=0.6)
        self.play(*[b.animate.move_to(ll(lat, lon1)) for b, (lat, _, lon1, _) in zip(blobs, paths)],
                  run_time=5.0, rate_func=linear)

        # At the western boundary the signal is passed along the shelf by coastally trapped waves.
        shelf = VMobject(stroke_color=LOW, stroke_width=4).set_points_smoothly(
            [ll(47.0, -53.5), ll(45.0, -60.5), ll(43.3, -66.0), ll(41.8, -69.5), ll(40.6, -72.5)])
        trapped = txt("coastally trapped waves", 15, LOW).next_to(ll(45.5, -60), UP + LEFT, buff=0.05)
        self.play(Create(shelf), FadeIn(trapped), run_time=1.5)
        self.play(self.gauges.animate.scale(1.6), rate_func=there_and_back, run_time=1.0)

        half = txt("About half of the decadal\nsignal arrives this way", 22, HIGH, bold=True)
        half.next_to(notes, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(FadeIn(half, shift=0.1 * UP), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(VGroup(notes, blobs, tracks, shelf, trapped, half)), run_time=0.8)

    def beat_modes(self) -> None:
        self.set_title("Which climate patterns set the waves going?",
                       "Share of the remotely forced decadal variance each group explains (Fig. 3). Footprints schematic")
        extra = VGroup(
            Circle(radius=1.0, stroke_color=EXTRATROPICAL, stroke_width=2,
                fill_color=EXTRATROPICAL, fill_opacity=0.15).stretch(1.9, 0).move_to(ll(53, -32)),
            txt("NAO + AMO", 20, EXTRATROPICAL, bold=True).move_to(ll(55, -32)),
            txt("extratropical", 15, EXTRATROPICAL).move_to(ll(50.5, -32)),
        )
        tropic = VGroup(
            Circle(radius=0.8, stroke_color=TROPICAL, stroke_width=2,
                fill_color=TROPICAL, fill_opacity=0.15).stretch(2.1, 0).move_to(ll(15, -40)),
            txt("AMM", 20, TROPICAL, bold=True).move_to(ll(16.5, -40)),
            txt("tropical", 15, TROPICAL).move_to(ll(12.5, -40)),
            Polygon(ll(-3, -20), ll(-3, -2), ll(3, -2), ll(3, -20), stroke_color=TROPICAL, stroke_width=2,
                    fill_color=TROPICAL, fill_opacity=0.15),
            txt("Atlantic Niño", 15, TROPICAL, bold=True).next_to(ll(3, -11), UP, buff=0.05),
        )
        self.play(FadeIn(extra), run_time=0.8)
        self.play(FadeIn(tropic), run_time=0.8)

        pct = PAPER["variance_pct"]
        rows, unit = VGroup(), 3.4 / 50.0     # bar length per percentage point
        for i, region in enumerate(("north", "south")):
            head = txt(f"{region.capitalize()} of Cape Hatteras", 20, INK, bold=True)
            bars = VGroup()
            for key, color, name in (("tropical_AMM_ATL3", TROPICAL, "tropical"),
                                     ("extratropical_NAO_AMO", EXTRATROPICAL, "extratropical")):
                val = pct[key][region]
                bar = Rectangle(width=val * unit, height=0.34, stroke_width=0, fill_color=color, fill_opacity=0.9)
                label = txt(name, 15, MUTED)
                value = txt(f"{val:.1f}%", 18, color, bold=True)
                bars.add(VGroup(label, bar, value))
            row = VGroup(head, bars)
            y = 1.5 - i * 2.4
            head.move_to(np.array([1.75, y, 0]), aligned_edge=LEFT)
            for j, (label, bar, value) in enumerate(bars):
                yy = y - 0.55 - j * 0.6
                label.move_to(np.array([1.75, yy, 0]), aligned_edge=LEFT)
                bar.move_to(np.array([3.05, yy, 0]), aligned_edge=LEFT)
                value.next_to(bar, RIGHT, buff=0.1)
            rows.add(row)
        for row in rows:
            head, bars = row
            self.play(FadeIn(head), *[FadeIn(b[0]) for b in bars], run_time=0.5)
            self.play(*[GrowFromEdge(b[1], LEFT) for b in bars], run_time=1.2)
            self.play(*[FadeIn(b[2]) for b in bars], run_time=0.4)
        self.set_caption("The tropics rival the extratropics, and in the north they explain more")
        self.wait(2.2)
        self.play(FadeOut(VGroup(extra, tropic, rows)), run_time=0.8)

    def beat_amm(self) -> None:
        self.set_title("Why the AMM matters most in the north",
                       "Positive AMM phase, after Fig. 4a. Arrows schematic")
        centre = ll(36, -36)
        low = txt("L", 34, LOW, bold=True).move_to(centre)
        cyclone = VGroup(*[
            Arc(radius=1.15, start_angle=a, angle=0.55 * np.pi, color=INK, stroke_width=3,
                arc_center=centre).add_tip(tip_length=0.16)          # counter-clockwise: cyclonic
            for a in (0.1 * np.pi, 0.77 * np.pi, 1.43 * np.pi)
        ])
        self.play(FadeOut(self.hatteras[1:]), FadeIn(low), Create(cyclone), run_time=1.4)
        r1, r2 = box(PAPER["R1"], "R1"), box(PAPER["R2"], "R2")
        self.play(Create(r2[0]), Create(r1[0]), FadeIn(r2[1]), FadeIn(r1[1]), run_time=1.0)

        def pair(lat: float, lon: float, buoy_up: bool) -> VGroup:
            wind = Arrow(ll(lat + 3, lon - 4), ll(lat - 4, lon - 4), buff=0, color=INK, stroke_width=5,
                         max_tip_length_to_length_ratio=0.3)
            b0, b1 = (lat - 4, lat + 3) if buoy_up else (lat + 3, lat - 4)
            buoy = Arrow(ll(b0, lon + 4), ll(b1, lon + 4), buff=0, color=BUOYANCY, stroke_width=5,
                         max_tip_length_to_length_ratio=0.3)
            return VGroup(wind, buoy)

        notes = VGroup(
            txt("wind", 18, INK, bold=True), txt("buoyancy", 18, BUOYANCY, bold=True),
        ).arrange(RIGHT, buff=0.35).move_to(np.array([4.4, 2.6, 0]))
        r2_pair, r1_pair = pair(52, -52, buoy_up=False), pair(28, -66, buoy_up=True)
        self.play(FadeIn(notes), GrowArrow(r2_pair[0]), GrowArrow(r2_pair[1]), run_time=1.0)
        r2_text = VGroup(txt("R2: both lower sea level", 20, LOW, bold=True),
                         txt("the effects add up", 18, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        r2_text.move_to(np.array([4.4, 1.5, 0]))
        big = Arrow(ll(56, -54), ll(45, -54), buff=0, color=LOW, stroke_width=10, max_tip_length_to_length_ratio=0.3)
        self.play(Transform(r2_pair, big), FadeIn(r2_text), run_time=1.2)

        self.play(GrowArrow(r1_pair[0]), GrowArrow(r1_pair[1]), run_time=1.0)
        r1_text = VGroup(txt("R1: they push opposite ways", 20, INK, bold=True),
                         txt("and largely cancel", 18, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        r1_text.move_to(np.array([4.4, 0.2, 0]))
        cancel = txt("≈ 0", 26, MUTED, bold=True).move_to(ll(28, -66))
        self.play(Transform(r1_pair, cancel), FadeIn(r1_text), run_time=1.2)

        pulse = sla_blob(LOW, radius=0.35).move_to(ll(48, -50))
        route = VMobject().set_points_smoothly([ll(48, -50), ll(46, -58), ll(44, -64), ll(42, -69)])
        self.play(FadeIn(pulse), run_time=0.3)
        self.play(MoveAlongPath(pulse, route), run_time=2.0, rate_func=smooth)
        north_text = txt("Amplified signal reaches\nthe north coast", 20, LOW, bold=True)
        north_text.move_to(np.array([4.4, -1.2, 0]), aligned_edge=LEFT).align_to(r1_text, LEFT)
        self.play(self.north_gauges.animate.set_color(LOW).scale(1.5), FadeIn(north_text), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(VGroup(low, cyclone, r1, r2, notes, r2_pair, r1_pair, r2_text, r1_text,
                                 pulse, north_text, self.map, self.gauges, self.hatteras[0])), run_time=1.0)

    def beat_takeaway(self) -> None:
        self.play(FadeOut(self.title), FadeOut(self.caption), run_time=0.4)
        msg = VGroup(
            txt("The tropical Atlantic is an important, yet previously", 30, INK, bold=True),
            txt("underappreciated, driver of East Coast sea level.", 30, INK, bold=True),
        ).arrange(DOWN, buff=0.15).move_to(1.6 * UP)
        sub = txt("Watching it could sharpen decadal sea level predictions and flood risk assessments.",
                  21, HIGH).next_to(msg, DOWN, buff=0.45)
        card = RoundedRectangle(corner_radius=0.15, width=12.4, height=1.9, stroke_color=LAND_EDGE,
                                stroke_width=1.5).move_to(1.65 * DOWN)
        cite = VGroup(
            txt("Zhu, Han, Wang, Zheng, Suhas, Subramanian, Leung, Garuba & Balaguru (2026)", 19, INK),
            txt("Decadal Sea Level Variability Along the U.S. East Coast: Roles of Extratropical", 17, MUTED),
            txt("Versus Tropical Climate Modes Over the North Atlantic Ocean", 17, MUTED),
            txt("Geophysical Research Letters 53, e2026GL125873  ·  doi.org/10.1029/2026GL125873", 18, INK),
        ).arrange(DOWN, buff=0.1).move_to(card)
        credit = txt("Animation: CHAOS group, CU Boulder  ·  curves digitized from Fig. 1 (CC BY 4.0)",
                     14, MUTED).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.2)
        self.play(FadeIn(sub), run_time=0.8)
        self.play(Create(card), FadeIn(cite), FadeIn(credit), run_time=1.0)
        self.wait(4.0)
