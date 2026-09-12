#!/usr/bin/env python3
"""Generate the visual assets used by the profile README.

The generator intentionally uses only the Python standard library so the
profile can be rebuilt without a frontend toolchain or external package.
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
FONT = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace"

COLORS = {
    "background": "#070b14",
    "panel": "#0c1525",
    "panel_alt": "#101b2e",
    "border": "#294b7c",
    "border_soft": "#1c3154",
    "text": "#d9e7ff",
    "muted": "#7890b2",
    "cyan": "#50e3ff",
    "violet": "#a78bfa",
    "green": "#7ee787",
    "lime": "#b5f6a2",
    "orange": "#ffb86b",
    "pink": "#ff7a9b",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(
    x: int | float,
    y: int | float,
    value: str,
    *,
    size: int = 14,
    fill: str = COLORS["text"],
    weight: str = "400",
    anchor: str = "start",
    opacity: float = 1,
    spacing: int | float | None = None,
) -> str:
    attributes = [
        f'x="{x}"',
        f'y="{y}"',
        f'fill="{fill}"',
        f'font-family="{FONT}"',
        f'font-size="{size}px"',
        f'font-weight="{weight}"',
        f'text-anchor="{anchor}"',
        f'opacity="{opacity}"',
    ]
    if spacing is not None:
        attributes.append(f'letter-spacing="{spacing}px"')
    return f'<text {" ".join(attributes)}>{esc(value)}</text>'


def rect(
    x: int | float,
    y: int | float,
    width: int | float,
    height: int | float,
    *,
    fill: str = "none",
    stroke: str = "none",
    radius: int = 0,
    stroke_width: int | float = 1,
    opacity: float = 1,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'fill="{fill}" stroke="{stroke}" rx="{radius}" '
        f'stroke-width="{stroke_width}" opacity="{opacity}" />'
    )


def line(
    x1: int | float,
    y1: int | float,
    x2: int | float,
    y2: int | float,
    *,
    stroke: str = COLORS["border_soft"],
    width: int | float = 1,
    opacity: float = 1,
    dash: str | None = None,
) -> str:
    dash_attribute = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"{dash_attribute} />'
    )


def circle(
    x: int | float,
    y: int | float,
    radius: int | float,
    *,
    fill: str,
    stroke: str = "none",
    width: int | float = 1,
    opacity: float = 1,
) -> str:
    return (
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" />'
    )


def card(x: int, y: int, width: int, height: int, label: str, accent: str) -> list[str]:
    return [
        rect(x, y, width, height, fill="url(#panel-gradient)", stroke=COLORS["border_soft"], radius=16),
        rect(x, y, 4, height, fill=accent, radius=2),
        text(x + 22, y + 30, label, size=12, fill=accent, weight="700", spacing=1.5),
        line(x + 22, y + 46, x + width - 22, y + 46, stroke=COLORS["border_soft"]),
    ]


def pill(x: int, y: int, width: int, label: str, accent: str) -> list[str]:
    return [
        rect(x, y, width, 28, fill=accent, stroke=accent, radius=14, opacity=0.14),
        text(x + width / 2, y + 19, label, size=11, fill=accent, weight="700", anchor="middle", spacing=0.8),
    ]


def document(title: str, description: str, width: int, height: int, body: list[str]) -> str:
    content = "\n".join(body)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
  <title id="title">{esc(title)}</title>
  <desc id="description">{esc(description)}</desc>
  <defs>
    <linearGradient id="background-gradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{COLORS['background']}" />
      <stop offset="100%" stop-color="#0b1323" />
    </linearGradient>
    <linearGradient id="panel-gradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{COLORS['panel_alt']}" />
      <stop offset="100%" stop-color="{COLORS['panel']}" />
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#294b7c" stroke-width="1" opacity="0.12" />
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#background-gradient)" />
  <rect width="{width}" height="{height}" fill="url(#grid)" />
  {content}
</svg>
'''


def profile_dashboard() -> str:
    body: list[str] = []
    body.append(rect(24, 24, 1152, 712, fill="none", stroke=COLORS["border"], radius=22, stroke_width=1.5))
    body.append(rect(24, 24, 1152, 56, fill="#0b1424", stroke=COLORS["border"], radius=22))
    body.append(rect(24, 58, 1152, 22, fill="#0b1424"))
    body.extend(
        [
            circle(52, 52, 6, fill=COLORS["pink"]),
            circle(73, 52, 6, fill=COLORS["orange"]),
            circle(94, 52, 6, fill=COLORS["green"]),
            text(120, 57, "naresh@github:~$ ./profile --initialize", size=12, fill=COLORS["muted"]),
            text(1148, 57, "SYSTEM ONLINE", size=11, fill=COLORS["green"], weight="700", anchor="end", spacing=1.2),
        ]
    )
    body.extend(
        [
            text(58, 133, "NARESH KUMAR V", size=34, fill=COLORS["text"], weight="700", spacing=1),
            text(60, 163, "AI DEVELOPER  /  ML RESEARCHER  /  SYSTEM BUILDER", size=13, fill=COLORS["cyan"], weight="700", spacing=1.2),
            text(60, 192, "Turning research ideas into useful, explainable software.", size=15, fill=COLORS["muted"]),
            line(58, 218, 1142, 218, stroke=COLORS["border_soft"]),
        ]
    )
    body.extend(pill(60, 230, 126, "AI / ML", COLORS["cyan"]))
    body.extend(pill(196, 230, 112, "GENAI", COLORS["violet"]))
    body.extend(pill(318, 230, 154, "COMPUTER VISION", COLORS["orange"]))
    body.extend(pill(482, 230, 134, "FULL STACK", COLORS["green"]))
    body.extend(pill(626, 230, 174, "NEXT: NEXUS-LAB", COLORS["pink"]))

    body.extend(card(44, 270, 330, 430, "IDENTITY NODE", COLORS["cyan"]))
    body.extend(
        [
            circle(209, 409, 74, fill="none", stroke=COLORS["cyan"], width=1.5, opacity=0.25),
            circle(209, 409, 55, fill="none", stroke=COLORS["violet"], width=1.2, opacity=0.4),
            line(120, 409, 298, 409, stroke=COLORS["cyan"], opacity=0.18, dash="4 8"),
            line(209, 320, 209, 498, stroke=COLORS["violet"], opacity=0.18, dash="4 8"),
            text(209, 419, "N", size=54, fill=COLORS["text"], weight="700", anchor="middle", spacing=2),
            text(209, 453, "NEURAL SYSTEMS", size=10, fill=COLORS["cyan"], weight="700", anchor="middle", spacing=2),
        ]
    )
    orbit_nodes = [(209, 335, COLORS["green"]), (282, 378, COLORS["orange"]), (263, 468, COLORS["violet"]), (145, 474, COLORS["pink"]), (136, 365, COLORS["cyan"])]
    for node_x, node_y, color in orbit_nodes:
        body.append(line(209, 409, node_x, node_y, stroke=color, opacity=0.42, dash="2 5"))
        body.append(circle(node_x, node_y, 5, fill=color, stroke=COLORS["background"], width=2, opacity=0.95))
    body.extend(
        [
            line(66, 522, 352, 522, stroke=COLORS["border_soft"]),
            text(66, 552, "BASE", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            text(352, 552, "COIMBATORE / INDIA", size=11, fill=COLORS["text"], weight="700", anchor="end"),
            text(66, 581, "EDU", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            text(352, 581, "AMRITA VISHWA VIDYAPEETHAM", size=10, fill=COLORS["text"], weight="700", anchor="end"),
            text(66, 610, "GRAD", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            text(352, 610, "2027", size=11, fill=COLORS["green"], weight="700", anchor="end"),
            text(66, 655, "STATUS", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            circle(79, 677, 4, fill=COLORS["green"], opacity=0.95),
            text(92, 681, "BUILDING / RESEARCHING / LEARNING", size=10, fill=COLORS["green"], weight="700"),
        ]
    )

    body.extend(card(398, 270, 758, 200, "SYSTEM PROFILE", COLORS["violet"]))
    profile_rows = [
        ("ROLE", "AI Developer / ML Researcher", COLORS["cyan"]),
        ("FOCUS", "AI / ML   +   GenAI   +   Computer Vision", COLORS["violet"]),
        ("RESEARCH", "EEG signals   +   intelligent interfaces", COLORS["orange"]),
        ("MISSION", "Build reliable systems with visible reasoning", COLORS["green"]),
    ]
    for index, (label, value, color) in enumerate(profile_rows):
        y = 344 + index * 30
        body.append(text(426, y, label, size=10, fill=color, weight="700", spacing=1.2))
        body.append(text(554, y, value, size=12, fill=COLORS["text"]))

    body.extend(card(398, 492, 758, 208, "FEATURED MODULES", COLORS["orange"]))
    projects = [
        (426, "[01] EEG MDD", "WAVELET + ML", "Python / MNE", COLORS["cyan"]),
        (672, "[02] FABRICQA", "VISION QA", "OpenCV / Streamlit", COLORS["orange"]),
        (918, "[03] BOOK RAG", "SEMANTIC SEARCH", "LangChain / HF", COLORS["violet"]),
    ]
    for x, title, subtitle, stack, color in projects:
        body.append(rect(x, 545, 220, 124, fill="#0a1322", stroke=COLORS["border_soft"], radius=11))
        body.append(circle(x + 20, 570, 4, fill=color, opacity=0.95))
        body.append(text(x + 34, 574, title, size=11, fill=COLORS["text"], weight="700"))
        body.append(text(x + 18, 606, subtitle, size=10, fill=color, weight="700", spacing=0.6))
        body.append(text(x + 18, 632, stack, size=10, fill=COLORS["muted"]))
        body.append(text(x + 18, 654, "OPEN SOURCE MODULE", size=9, fill=COLORS["muted"], spacing=0.8))

    body.extend(
        [
            line(44, 718, 1156, 718, stroke=COLORS["border_soft"]),
            text(44, 729, "BUILD / LEARN / CREATE / REPEAT", size=9, fill=COLORS["muted"], spacing=1.2),
            text(1156, 729, "v1.0 // PROFILE SIGNAL", size=9, fill=COLORS["muted"], anchor="end", spacing=1.2),
        ]
    )
    return document(
        "Naresh Kumar V - AI developer profile",
        "A futuristic profile dashboard showing identity, technical focus, and featured machine learning projects.",
        1200,
        760,
        body,
    )


def activity_telemetry() -> str:
    body: list[str] = []
    body.append(rect(24, 24, 1152, 302, fill="none", stroke=COLORS["border"], radius=22, stroke_width=1.5))
    body.append(rect(24, 24, 1152, 54, fill="#0b1424", stroke=COLORS["border"], radius=22))
    body.append(rect(24, 57, 1152, 21, fill="#0b1424"))
    body.extend(
        [
            circle(52, 51, 6, fill=COLORS["pink"]),
            circle(73, 51, 6, fill=COLORS["orange"]),
            circle(94, 51, 6, fill=COLORS["green"]),
            text(120, 56, "naresh@github:~$ telemetry --focus-map", size=12, fill=COLORS["muted"]),
            text(1148, 56, "LIVE DIRECTION", size=11, fill=COLORS["cyan"], weight="700", anchor="end", spacing=1.2),
        ]
    )

    metrics = [
        (44, "PRIMARY VECTOR", "AI / ML + GENAI", COLORS["cyan"]),
        (332, "RESEARCH SIGNAL", "CV + EEG SYSTEMS", COLORS["orange"]),
        (620, "ENGINEERING MODE", "BUILDING IN PUBLIC", COLORS["green"]),
        (908, "NEXT SYSTEM", "NEXUS-LAB", COLORS["violet"]),
    ]
    for x, label, value, color in metrics:
        body.append(rect(x, 101, 248, 58, fill="url(#panel-gradient)", stroke=COLORS["border_soft"], radius=11))
        body.append(text(x + 16, 122, label, size=9, fill=color, weight="700", spacing=1.1))
        body.append(text(x + 16, 145, value, size=11, fill=COLORS["text"], weight="700"))

    body.append(text(44, 185, "BUILD SIGNAL", size=10, fill=COLORS["muted"], weight="700", spacing=1.3))
    body.append(text(1148, 185, "VISUAL FOCUS MAP / NOT A NUMERIC SCORE", size=9, fill=COLORS["muted"], anchor="end", spacing=0.8))
    levels = ["#111b2b", "#143c45", "#0d665b", "#1b8f6e", "#55d68c", "#b5f6a2"]
    start_x = 124
    start_y = 201
    cell = 13
    gap = 4
    for column in range(52):
        for row in range(5):
            signal = (column * 7 + row * 11 + (column // 4) * 3 + (column * row) % 5) % 12
            level = min(5, signal // 2)
            if (column + row * 3) % 19 == 0:
                level = 5
            x = start_x + column * (cell + gap)
            y = start_y + row * (cell + gap)
            body.append(rect(x, y, cell, cell, fill=levels[level], radius=3, opacity=0.95))

    body.extend(
        [
            text(44, 211, "AI", size=9, fill=COLORS["cyan"], weight="700"),
            text(44, 228, "CV", size=9, fill=COLORS["orange"], weight="700"),
            text(44, 245, "RAG", size=9, fill=COLORS["violet"], weight="700"),
            text(44, 262, "OPS", size=9, fill=COLORS["green"], weight="700"),
            text(44, 279, "LAB", size=9, fill=COLORS["pink"], weight="700"),
            text(124, 306, "NOW", size=9, fill=COLORS["muted"], weight="700", spacing=1),
            text(1148, 306, "RESEARCH-DRIVEN SYSTEMS, SHIPPED AS WORKING SOFTWARE", size=9, fill=COLORS["muted"], anchor="end", spacing=0.8),
        ]
    )
    return document(
        "Naresh Kumar V - build telemetry",
        "A visual focus map for current AI, research, and engineering directions.",
        1200,
        350,
        body,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ASSET_DIR)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "profile-dashboard.svg").write_text(profile_dashboard(), encoding="utf-8")
    (args.output_dir / "activity-telemetry.svg").write_text(activity_telemetry(), encoding="utf-8")
    print(f"Generated profile assets in {args.output_dir}")


if __name__ == "__main__":
    main()
