"""Public-facing schematic for Suhas et al. (2026, J. Climate).

"Marine Heatwaves in the Arabian Sea: Drivers and Impacts on Atmospheric
Circulation and Extreme Precipitation", doi:10.1175/JCLI-D-25-0458.1.

Draws a three-panel storyboard of the paper's two-way coupling for short
(<= 20 day) summer marine heatwaves (MHWs):

  1. Atmosphere -> ocean: the suppressed-convection phase of the boreal summer
     intraseasonal oscillation (BSISO) brings clear skies (more shortwave) and
     slack monsoon winds (less latent heat loss), so the sea warms.
  2. Ocean -> atmosphere: the warm anomaly spins up a low-level cyclone, with
     cloud and rain over the sea; cloud and stronger winds then cool the sea.
  3. The cyclone steers moisture onshore: southwest India (Kerala) for eastern
     Arabian Sea MHWs, Pakistan and northwest India for northern ones.

Geography is real (Natural Earth 1:50m land, equirectangular projection with a
cos(18 N) aspect correction); every arrow, patch and cloud is schematic. The
hotspot boxes are the paper's EAS (8-18 N, 62-77 E) and NAS (18-25 N, 59-73 E).

Writes two layouts to the news post folder: a wide one for desktop and a
stacked one that the post serves to narrow screens through <picture>.

    uvx python scripts/make_arabian_sea_mhw_schematic.py
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAND = json.loads((ROOT / "scripts/data/suhas2026/land.json").read_text())["polygons"]
OUT = ROOT / "content/post/suhas-2026-arabian-sea-mhw-published"

# Map extent (degrees) shared by every panel.
LON0, LON1, LAT0, LAT1 = 56.0, 80.0, 6.0, 30.0
ASPECT = math.cos(math.radians(18.0))  # x-stretch so shapes are not squashed

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

# Palette: light card that sits on either site theme, like the other post SVGs.
C = {
    "card": "#fcfcfb", "edge": "#e2e8f0", "ink": "#0f172a", "body": "#334155",
    "muted": "#64748b", "ocean": "#d8ecf4", "land": "#f2e8d5", "coast": "#bfae8e",
    "warm": "#e4572e", "sun": "#f5a800", "sw": "#ef7d00", "wind": "#475569",
    "cyc": "#1e3a8a", "cloud": "#8b98ab", "rain": "#2563eb", "risk": "#6d28d9",
    "dry": "#a16207", "atm": "#0e7490",
}


@dataclass(frozen=True)
class Panel:
    """A map panel placed at (x, y) with width w; height follows the extent."""

    x: float
    y: float
    w: float

    @property
    def k(self) -> float:  # pixels per degree latitude
        return self.w / ((LON1 - LON0) * ASPECT)

    @property
    def h(self) -> float:
        return (LAT1 - LAT0) * self.k

    def p(self, lon: float, lat: float) -> tuple[float, float]:
        return (self.x + (lon - LON0) * ASPECT * self.k, self.y + (LAT1 - lat) * self.k)

    def d(self, deg: float) -> float:
        """Convert a latitude-degree length to pixels (for radii, offsets)."""
        return deg * self.k


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def text(x: float, y: float, s: str, size: float = 13, weight: int = 500,
         fill: str = C["body"], anchor: str = "start", halo: bool = False,
         italic: bool = False) -> str:
    halo_attr = ' stroke="#fcfcfb" stroke-width="3.5" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    style = ' font-style="italic"' if italic else ""
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{style}{halo_attr}>{s}</text>')


def lines(x: float, y: float, rows: list[str], size: float = 13, lh: float = 1.35, **kw) -> str:
    return "".join(text(x, y + i * size * lh, r, size=size, **kw) for i, r in enumerate(rows))


def arrow(pts: list[tuple[float, float]], color: str, width: float, marker: str,
          dash: str | None = None, opacity: float = 1.0) -> str:
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}"{da} marker-end="url(#{marker})"/>')


def curve(p0, c, p1, color: str, width: float, marker: str, opacity: float = 1.0) -> str:
    return (f'<path d="M{f(p0[0])} {f(p0[1])} Q{f(c[0])} {f(c[1])} {f(p1[0])} {f(p1[1])}" fill="none" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" opacity="{opacity}" '
            f'marker-end="url(#{marker})"/>')


def cyclone(cx: float, cy: float, rx: float, ry: float, width: float, opacity: float = 1.0) -> str:
    """Counter-clockwise (Northern Hemisphere cyclonic) loop in two arrowed arcs."""
    def arc(t0: float, t1: float) -> list[tuple[float, float]]:
        n = 28
        return [(cx + rx * math.cos(t0 + (t1 - t0) * i / n), cy - ry * math.sin(t0 + (t1 - t0) * i / n))
                for i in range(n + 1)]
    r = math.radians
    return (arrow(arc(r(-70), r(95)), C["cyc"], width, "mCyc", opacity=opacity)
            + arrow(arc(r(118), r(272)), C["cyc"], width, "mCyc", opacity=opacity))


def cloud(x: float, y: float, s: float, rain: int = 0, fill: str = C["cloud"]) -> str:
    """Cumulus glyph centred on (x, y) with scale s; optional rain streaks."""
    out = [f'<g fill="{fill}">',
           f'<circle cx="{f(x - 0.55*s)}" cy="{f(y + 0.05*s)}" r="{f(0.42*s)}"/>',
           f'<circle cx="{f(x)}" cy="{f(y - 0.25*s)}" r="{f(0.55*s)}"/>',
           f'<circle cx="{f(x + 0.55*s)}" cy="{f(y + 0.02*s)}" r="{f(0.40*s)}"/>',
           f'<rect x="{f(x - 0.95*s)}" y="{f(y)}" width="{f(1.9*s)}" height="{f(0.45*s)}" rx="{f(0.22*s)}"/>',
           "</g>"]
    if rain:
        out.append(f'<g stroke="{C["rain"]}" stroke-width="{f(max(1.6, 0.11*s))}" stroke-linecap="round">')
        for i in range(rain):
            rx = x - 0.7 * s + i * (1.4 * s / max(rain - 1, 1))
            out.append(f'<line x1="{f(rx)}" y1="{f(y + 0.62*s)}" x2="{f(rx - 0.18*s)}" y2="{f(y + 1.05*s)}"/>')
        out.append("</g>")
    return "".join(out)


def sun(x: float, y: float, r: float) -> str:
    rays = "".join(
        f'<line x1="{f(x + 1.35*r*math.cos(a))}" y1="{f(y + 1.35*r*math.sin(a))}" '
        f'x2="{f(x + 1.85*r*math.cos(a))}" y2="{f(y + 1.85*r*math.sin(a))}"/>'
        for a in (math.radians(i * 45) for i in range(8)))
    return (f'<g stroke="{C["sun"]}" stroke-width="2.4" stroke-linecap="round">{rays}</g>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{C["sun"]}"/>')


def warm_patch(P: Panel, lon: float, lat: float, rx: float, ry: float, opacity: float = 1.0) -> str:
    x, y = P.p(lon, lat)
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(P.d(rx) * ASPECT)}" ry="{f(P.d(ry))}" '
            f'fill="url(#gWarm)" opacity="{opacity}"/>')


def base_map(P: Panel, cid: str) -> str:
    """Clip path and ocean background for a panel."""
    return (f'<clipPath id="{cid}"><rect x="{f(P.x)}" y="{f(P.y)}" width="{f(P.w)}" height="{f(P.h)}" rx="8"/></clipPath>'
            f'<rect x="{f(P.x)}" y="{f(P.y)}" width="{f(P.w)}" height="{f(P.h)}" rx="8" fill="{C["ocean"]}"/>')


def land_layer(P: Panel, cid: str) -> str:
    land = "".join(
        '<path d="M' + " L".join(f"{f(a)} {f(b)}" for a, b in (P.p(lon, lat) for lon, lat in poly)) + 'Z"/>'
        for poly in LAND)
    return (f'<g clip-path="url(#{cid})" fill="{C["land"]}" stroke="{C["coast"]}" stroke-width="1" '
            f'stroke-linejoin="round">{land}</g>')


def frame(P: Panel) -> str:
    return (f'<rect x="{f(P.x)}" y="{f(P.y)}" width="{f(P.w)}" height="{f(P.h)}" rx="8" fill="none" '
            f'stroke="#94a3b8" stroke-width="1"/>')


def hotspot_boxes(P: Panel, labels: bool) -> str:
    out = []
    for name, (lo0, lo1, la0, la1), (llon, llat) in (
        ("Eastern", (62, 77, 8, 18), (62.4, 17.0)),
        ("Northern", (59, 73, 18, 25), (59.4, 24.2)),
    ):
        x0, y0 = P.p(lo0, la1)
        x1, y1 = P.p(lo1, la0)
        out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1-x0)}" height="{f(y1-y0)}" fill="none" '
                   f'stroke="{C["muted"]}" stroke-width="1.1" stroke-dasharray="4 3" opacity="0.8"/>')
        if labels:
            lx, ly = P.p(llon, llat)
            out.append(text(lx, ly, name, size=10.5, weight=600, fill=C["muted"], halo=True))
    return "".join(out)


# --------------------------------------------------------------------------- panels

def panel_build(P: Panel, s: float) -> str:
    """Step 1: clear skies and slack monsoon winds warm the sea (days -10 to 0)."""
    o = [warm_patch(P, 69.0, 13.2, 6.2, 3.4), warm_patch(P, 65.5, 21.6, 4.8, 2.4), land_layer(P, P_ID[id(P)])]
    o.append(hotspot_boxes(P, labels=True))
    # Weakened southwest monsoon flow: thin, dashed, faded.
    for a, b in (((57.0, 11.0), (61.5, 14.0)), ((62.0, 6.8), (66.6, 9.6)), ((58.5, 16.2), (62.0, 18.6))):
        o.append(arrow([P.p(*a), P.p(*b)], C["wind"], 2.0, "mWind", dash="5 4", opacity=0.75))
    # Sun over the sea with shortwave beams into both warm patches.
    sx, sy = P.p(60.3, 27.6)
    o.append(sun(sx, sy, P.d(1.0)))
    for a, b in (((64.8, 26.4), (65.0, 23.0)), ((68.0, 26.4), (67.6, 23.0)),
                 ((67.4, 18.9), (67.6, 15.4)), ((71.2, 18.9), (70.8, 15.4))):
        o.append(arrow([P.p(*a), P.p(*b)], C["sw"], 4.4 * s, "mSw"))
    # Labels.
    o.append(lines(*P.p(66.6, 28.2), ["Clear skies:", "more sunshine"], size=12.5 * s, weight=600, fill=C["ink"], halo=True))
    o.append(lines(*P.p(66.8, 9.0), ["Slack winds:", "less evaporation"], size=12 * s, weight=600,
                   fill=C["ink"], halo=True, lh=1.25))
    x, y = P.p(68.9, 13.6)
    o.append(text(x, y, "Sea warms", size=13 * s, weight=700, fill="#7f1d1d", anchor="middle", halo=True))
    x, y = P.p(65.5, 21.9)
    o.append(text(x, y, "Sea warms", size=11.5 * s, weight=700, fill="#7f1d1d", anchor="middle", halo=True))
    return "".join(o)


def panel_spin(P: Panel, s: float) -> str:
    """Step 2: the warm patch spins up a low-level cyclone (days 0 to +3)."""
    o = [warm_patch(P, 69.0, 13.2, 6.2, 3.4, 0.6), warm_patch(P, 65.5, 21.6, 4.8, 2.4, 0.6),
         land_layer(P, P_ID[id(P)]), hotspot_boxes(P, labels=False)]
    for (lon, lat, rx, ry) in ((68.6, 13.0, 4.6, 3.6), (65.3, 21.7, 3.9, 2.6)):
        cx, cy = P.p(lon, lat)
        o.append(cyclone(cx, cy, P.d(rx) * ASPECT, P.d(ry), 3.2 * s))
    # Rising air: clouds and rain over the sea.
    o.append(cloud(*P.p(68.6, 13.9), P.d(1.35), rain=4))
    o.append(cloud(*P.p(65.3, 22.4), P.d(1.05), rain=3))
    # Labels.
    x, y = P.p(68.6, 8.0)
    o.append(text(x, y, "Low-level cyclone", size=12.5 * s, weight=700, fill=C["cyc"], anchor="middle", halo=True))
    x, y = P.p(71.0, 28.2)
    o.append(lines(x, y, ["Warm sea heats and", "moistens the air above"], size=11.5 * s, weight=600,
                   fill=C["ink"], anchor="middle", halo=True))
    return "".join(o)


def panel_rain(P: Panel, s: float) -> str:
    """Step 3: moisture is steered onshore; extreme-rain risk rises (days +1 to +10)."""
    o = [land_layer(P, P_ID[id(P)]), hotspot_boxes(P, labels=False)]
    for (lon, lat, rx, ry) in ((68.6, 13.0, 4.6, 3.6), (65.3, 21.7, 3.9, 2.6)):
        cx, cy = P.p(lon, lat)
        o.append(cyclone(cx, cy, P.d(rx) * ASPECT, P.d(ry), 2.0 * s, opacity=0.45))
    # Eastern hotspot: westerlies on the cyclone's southern flank feed Kerala.
    o.append(curve(P.p(64.5, 9.0), P.p(70.0, 8.4), P.p(75.0, 10.4), C["atm"], 6.0 * s, "mMoist"))
    o.append(cloud(*P.p(77.2, 11.6), P.d(1.3), rain=4))
    # ... and offshore flow on its northern flank leaves the north drier.
    o.append(arrow([P.p(74.6, 17.4), P.p(71.4, 17.0)], C["dry"], 2.6 * s, "mDry", dash="5 4"))
    # Northern hotspot: onshore flow on the eastern flank reaches Pakistan / NW India.
    o.append(curve(P.p(68.6, 19.6), P.p(70.6, 22.4), P.p(69.2, 25.2), C["atm"], 6.0 * s, "mMoist"))
    o.append(cloud(*P.p(69.4, 27.4), P.d(1.3), rain=4))
    # Risk callouts.
    right = P.x + P.w - 7
    o.append(lines(right, P.p(0, 8.9)[1], ["SW India:", "2–3× risk"], size=12 * s, weight=700, fill=C["risk"],
                   anchor="end", halo=True, lh=1.2))
    o.append(lines(P.p(67.9, 0)[0], P.p(0, 28.7)[1], ["Pakistan &amp;", "NW India:", "2–3× risk"], size=12 * s,
                   weight=700, fill=C["risk"], anchor="end", halo=True, lh=1.2))
    o.append(lines(right, P.p(0, 20.0)[1], ["drier", "farther north"], size=10.5 * s, weight=600, fill=C["dry"],
                   anchor="end", halo=True, lh=1.2))
    return "".join(o)


P_ID: dict[int, str] = {}

STEPS = [
    ("1", "The sky heats the sea", "the days before the peak",
     ["A dry, clear spell of the monsoon", "brings extra sunshine and slack", "winds: the sea warms past its", "usual summer range."],
     panel_build),
    ("2", "The warm sea stirs the air", "peak to 3 days after",
     ["The heatwave warms and moistens", "the air above it. A low-level", "cyclone forms, its clouds and", "winds then cool the sea again."],
     panel_spin),
    ("3", "The rain comes ashore", "1 to 10 days after the peak",
     ["The swirl pushes moist ocean air", "onshore. Extreme rain becomes", "2–3 times as likely in SW India", "or in Pakistan and NW India."],
     panel_rain),
]


def defs() -> str:
    def mk(i: str, color: str, size: float = 5.0) -> str:
        return (f'<marker id="{i}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="{size}" '
                f'markerHeight="{size}" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{color}"/></marker>')
    return ("<defs>"
            '<radialGradient id="gWarm"><stop offset="0" stop-color="#d62f1c" stop-opacity="0.95"/>'
            '<stop offset="0.6" stop-color="#ef6f3c" stop-opacity="0.75"/>'
            '<stop offset="1" stop-color="#f6a37a" stop-opacity="0"/></radialGradient>'
            + mk("mSw", C["sw"], 3.2) + mk("mWind", C["wind"], 4.4) + mk("mCyc", C["cyc"], 3.6)
            + mk("mMoist", C["atm"], 3.0) + mk("mDry", C["dry"], 4.0) + "</defs>")


def header(cx: float, y: float, n: str, title: str, when: str, s: float) -> str:
    return (f'<circle cx="{f(cx)}" cy="{f(y)}" r="{f(13*s)}" fill="{C["ink"]}"/>'
            + text(cx, y + 4.6 * s, n, size=14 * s, weight=700, fill="#ffffff", anchor="middle")
            + text(cx + 22 * s, y + 1 * s, title, size=16 * s, weight=700, fill=C["ink"])
            + text(cx + 22 * s, y + 18 * s, when, size=12 * s, weight=500, fill=C["muted"], italic=True))


def coupling_bar(x0: float, x1: float, y: float, label: str, color: str, s: float) -> str:
    return (arrow([(x0, y), (x1, y)], color, 3.0 * s, "mBar" + color[1:], opacity=0.9)
            + f'<marker id="mBar{color[1:]}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" '
              f'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{color}"/></marker>'
            + text((x0 + x1) / 2, y - 9 * s, label, size=12 * s, weight=700, fill=color, anchor="middle"))


def build(layout: str) -> str:
    title = "How an Arabian Sea marine heatwave can fuel extreme monsoon rain"
    desc = ("Three map panels of the Arabian Sea, India and Pakistan. Panel 1: during a dry, clear spell of the "
            "summer monsoon, extra sunshine and slack winds warm two hotspot regions, the eastern and northern "
            "Arabian Sea, into a marine heatwave. Panel 2: the warm water heats and moistens the air above it and a "
            "counter-clockwise low-level cyclone forms over each warm patch, with clouds and rain over the sea that "
            "then cool the water. Panel 3: the cyclone pushes moist ocean air onshore, onto southwest India near "
            "Kerala for eastern heatwaves and onto Pakistan and northwest India for northern ones, where extreme "
            "rain becomes two to three times as likely; offshore winds leave the coast farther north drier. "
            "A bar beneath reads: the atmosphere drives the ocean, then the ocean drives the atmosphere.")

    if layout == "wide":
        W, s, mapw, gap, x0 = 960, 1.0, 296, 16, 24
        panels = [Panel(x0 + i * (mapw + gap), 132, mapw) for i in range(3)]
        H = 0
    else:
        W, s, mapw, x0 = 480, 1.15, 432, 24
        panels = []
        y = 112
        for _ in range(3):
            panels.append(Panel(x0, y + 52, mapw))
            y += 52 + Panel(0, 0, mapw).h + 132
        H = 0

    for i, P in enumerate(panels):
        P_ID[id(P)] = f"clip{layout}{i}"

    body: list[str] = [f'<rect x="0.5" y="0.5" width="{W-1}" height="__H__" rx="14" fill="{C["card"]}" stroke="{C["edge"]}"/>']
    if layout == "wide":
        body.append(text(24, 40, title, size=21, weight=700, fill=C["ink"]))
        body.append(text(24, 64, "Suhas et al. (2026), Journal of Climate · summer (June–September) heatwaves lasting 20 days or less: "
                         "50 of the 61 events from 1982–2023", size=13, fill=C["muted"]))
    else:
        body.append(lines(24, 40, ["How an Arabian Sea marine heatwave", "can fuel extreme monsoon rain"],
                          size=22, weight=700, fill=C["ink"], lh=1.25))
        body.append(text(24, 96, "Suhas et al. (2026), Journal of Climate", size=14, fill=C["muted"]))

    for P, (n, head, when, cap, fn) in zip(panels, STEPS):
        hy = P.y - 36 * (1 if layout == "wide" else s) - 2
        body.append(header(P.x + 13 * s, hy, n, head, when, s))
        if layout != "wide":
            tag, col = ("ATMOSPHERE → OCEAN", C["sw"]) if n == "1" else ("OCEAN → ATMOSPHERE", C["atm"])
            body.append(text(P.x + P.w, hy + 18 * s, tag, size=11 * s, weight=700, fill=col, anchor="end"))
        body.append(base_map(P, P_ID[id(P)]))
        body.append(f'<g clip-path="url(#{P_ID[id(P)]})">{fn(P, s)}</g>')
        body.append(frame(P))
        body.append(lines(P.x, P.y + P.h + 24 * s, cap, size=13.5 * s, lh=1.4, fill=C["body"]))

    if layout == "wide":
        yb = panels[0].y + panels[0].h + 24 + 4 * 13.5 * 1.4 + 26
        p0, p1, p2 = panels
        body.append(coupling_bar(p0.x + 8, p0.x + p0.w - 8, yb, "ATMOSPHERE DRIVES THE OCEAN", C["sw"], 1.0))
        body.append(coupling_bar(p1.x + 8, p2.x + p2.w - 8, yb, "THE OCEAN DRIVES THE ATMOSPHERE", C["atm"], 1.0))
        foot = yb + 30
    else:
        foot = panels[-1].y + panels[-1].h + 24 * s + 4 * 13.5 * s * 1.4 + 10
    body.append(text(24, foot, "Conceptual schematic, not to scale. Coastlines: Natural Earth. "
                     "Dashed boxes: the paper’s eastern and northern Arabian Sea hotspots.",
                     size=11 if layout == "wide" else 11.5, fill=C["muted"]) if layout == "wide" else
                lines(24, foot, ["Conceptual schematic, not to scale. Coastlines: Natural Earth.",
                                 "Dashed boxes: the paper’s eastern and northern hotspots."],
                      size=12, fill=C["muted"]))
    H = int(foot + (16 if layout == "wide" else 34))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-labelledby="mhwTitle{layout} mhwDesc{layout}" font-family="{FONT}">'
           f'<title id="mhwTitle{layout}">{title}</title><desc id="mhwDesc{layout}">{desc}</desc>'
           + defs() + "".join(body).replace("__H__", str(H - 1)) + "</svg>\n")
    return svg


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for layout, name in (("wide", "mhw-two-way-loop.svg"), ("stacked", "mhw-two-way-loop-stacked.svg")):
        (OUT / name).write_text(build(layout))
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
