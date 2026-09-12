#!/usr/bin/env python3
"""Generate live, accessible SVG widgets for the profile README.

The generator uses only the Python standard library. GitHub Actions supplies
the contribution calendar JSON, while profile copy stays in data/profile.json.
"""

from __future__ import annotations

import argparse
import html
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
PROFILE_PATH = ROOT / "data" / "profile.json"
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
    "heat_0": "#111b2b",
    "heat_1": "#143c45",
    "heat_2": "#0d665b",
    "heat_3": "#1b8f6e",
    "heat_4": "#55d68c",
    "heat_5": "#b5f6a2",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def color(name: str, fallback: str = "muted") -> str:
    return COLORS.get(name, COLORS[fallback])


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
    class_name: str | None = None,
) -> str:
    class_attribute = f' class="{class_name}"' if class_name else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'fill="{fill}" stroke="{stroke}" rx="{radius}" '
        f'stroke-width="{stroke_width}" opacity="{opacity}"{class_attribute} />'
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
    class_name: str | None = None,
) -> str:
    class_attribute = f' class="{class_name}"' if class_name else ""
    return (
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"{class_attribute} />'
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
  <style>
    @keyframes pulse {{ 0%, 100% {{ opacity: 0.45; }} 50% {{ opacity: 1; }} }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{ .pulse {{ animation: none; }} }}
  </style>
  <rect width="{width}" height="{height}" fill="url(#background-gradient)" />
  <rect width="{width}" height="{height}" fill="url(#grid)" />
  {content}
</svg>
'''


def load_profile(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_contributions(path: Path | None) -> dict[str, Any]:
    empty = {
        "available": False,
        "total": 0,
        "active_days": 0,
        "peak_count": 0,
        "peak_date": "-",
        "start_date": "-",
        "end_date": "-",
        "weeks": [],
    }
    if path is None or not path.exists():
        return empty

    payload = json.loads(path.read_text(encoding="utf-8"))
    calendar = (
        payload.get("data", {})
        .get("user", {})
        .get("contributionsCollection", {})
        .get("contributionCalendar", {})
    )
    raw_weeks = calendar.get("weeks", [])
    weeks: list[list[dict[str, Any]]] = []
    days: list[dict[str, Any]] = []
    for week in raw_weeks:
        week_days: list[dict[str, Any]] = []
        for raw_day in week.get("contributionDays", []):
            raw_date = str(raw_day.get("date", ""))[:10]
            try:
                parsed_date = date.fromisoformat(raw_date)
            except ValueError:
                continue
            day = {
                "date": raw_date,
                "parsed_date": parsed_date,
                "count": int(raw_day.get("contributionCount", 0)),
            }
            week_days.append(day)
            days.append(day)
        weeks.append(week_days)

    if not days:
        return empty

    peak_day = max(days, key=lambda item: item["count"])
    return {
        "available": True,
        "total": int(calendar.get("totalContributions", sum(day["count"] for day in days))),
        "active_days": sum(day["count"] > 0 for day in days),
        "peak_count": peak_day["count"],
        "peak_date": peak_day["date"],
        "start_date": days[0]["date"],
        "end_date": days[-1]["date"],
        "weeks": weeks,
    }


def profile_dashboard(profile: dict[str, Any], stats: dict[str, Any]) -> str:
    body: list[str] = []
    body.append(rect(24, 24, 1152, 712, fill="none", stroke=COLORS["border"], radius=22, stroke_width=1.5))
    body.append(rect(24, 24, 1152, 56, fill="#0b1424", stroke=COLORS["border"], radius=22))
    body.append(rect(24, 58, 1152, 22, fill="#0b1424"))
    body.extend(
        [
            circle(52, 52, 6, fill=COLORS["pink"]),
            circle(73, 52, 6, fill=COLORS["orange"]),
            circle(94, 52, 6, fill=COLORS["green"]),
            text(120, 57, f'{profile["username"]}@github:~$ ./profile --initialize', size=12, fill=COLORS["muted"]),
            circle(1021, 52, 4, fill=COLORS["green"], class_name="pulse"),
            text(1148, 57, "SYSTEM ONLINE", size=11, fill=COLORS["green"], weight="700", anchor="end", spacing=1.2),
        ]
    )
    body.extend(
        [
            text(58, 133, profile["name"].upper(), size=34, fill=COLORS["text"], weight="700", spacing=1),
            text(60, 163, profile["headline"], size=13, fill=COLORS["cyan"], weight="700", spacing=1.2),
            text(60, 192, profile["tagline"], size=15, fill=COLORS["muted"]),
            line(58, 218, 1142, 218, stroke=COLORS["border_soft"]),
        ]
    )
    x = 60
    for item in profile["focus"]:
        width = int(item["width"])
        body.extend(pill(x, 230, width, item["label"], color(item["color"])))
        x += width + 14
        if x > 1000:
            break
    contribution_label = f'CONTRIBUTIONS: {stats["total"]:,}' if stats["available"] else "CONTRIBUTIONS: PENDING"
    body.extend(pill(936, 230, 206, contribution_label, COLORS["green"]))

    body.extend(card(44, 270, 330, 430, "IDENTITY NODE", COLORS["cyan"]))
    body.extend(
        [
            circle(209, 409, 74, fill="none", stroke=COLORS["cyan"], width=1.5, opacity=0.25),
            circle(209, 409, 55, fill="none", stroke=COLORS["violet"], width=1.2, opacity=0.4),
            line(120, 409, 298, 409, stroke=COLORS["cyan"], opacity=0.18, dash="4 8"),
            line(209, 320, 209, 498, stroke=COLORS["violet"], opacity=0.18, dash="4 8"),
            text(209, 419, profile["name"][0].upper(), size=54, fill=COLORS["text"], weight="700", anchor="middle", spacing=2),
            text(209, 453, "NEURAL SYSTEMS", size=10, fill=COLORS["cyan"], weight="700", anchor="middle", spacing=2),
        ]
    )
    orbit_nodes = [(209, 335, COLORS["green"]), (282, 378, COLORS["orange"]), (263, 468, COLORS["violet"]), (145, 474, COLORS["pink"]), (136, 365, COLORS["cyan"])]
    for node_x, node_y, node_color in orbit_nodes:
        body.append(line(209, 409, node_x, node_y, stroke=node_color, opacity=0.42, dash="2 5"))
        body.append(circle(node_x, node_y, 5, fill=node_color, stroke=COLORS["background"], width=2, opacity=0.95))
    body.extend(
        [
            line(66, 522, 352, 522, stroke=COLORS["border_soft"]),
            text(66, 552, "BASE", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            text(352, 552, profile["base"], size=11, fill=COLORS["text"], weight="700", anchor="end"),
            text(66, 581, "EDU", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            text(352, 581, profile["education"], size=10, fill=COLORS["text"], weight="700", anchor="end"),
            text(66, 610, "GRAD", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            text(352, 610, profile["graduation"], size=11, fill=COLORS["green"], weight="700", anchor="end"),
            text(66, 655, "STATUS", size=10, fill=COLORS["muted"], weight="700", spacing=1.4),
            circle(79, 677, 4, fill=COLORS["green"], opacity=0.95, class_name="pulse"),
            text(92, 681, profile["status"], size=10, fill=COLORS["green"], weight="700"),
        ]
    )

    body.extend(card(398, 270, 758, 200, "SYSTEM PROFILE", COLORS["violet"]))
    for index, row in enumerate(profile["system_profile"]):
        y = 344 + index * 30
        body.append(text(426, y, row["label"], size=10, fill=color(row["color"]), weight="700", spacing=1.2))
        body.append(text(554, y, row["value"], size=12, fill=COLORS["text"]))

    body.extend(card(398, 492, 758, 208, "FEATURED MODULES", COLORS["orange"]))
    project_x = [426, 672, 918]
    for x, project in zip(project_x, profile["projects"][:3]):
        project_color = color(project["color"])
        body.append(rect(x, 545, 220, 124, fill="#0a1322", stroke=COLORS["border_soft"], radius=11))
        body.append(circle(x + 20, 570, 4, fill=project_color, opacity=0.95))
        body.append(text(x + 34, 574, project["title"], size=11, fill=COLORS["text"], weight="700"))
        body.append(text(x + 18, 606, project["subtitle"], size=10, fill=project_color, weight="700", spacing=0.6))
        body.append(text(x + 18, 632, project["stack"], size=10, fill=COLORS["muted"]))
        body.append(text(x + 18, 654, "LIVE PROFILE MODULE", size=9, fill=COLORS["muted"], spacing=0.8))

    body.extend(
        [
            line(44, 718, 1156, 718, stroke=COLORS["border_soft"]),
            text(44, 729, "BUILD / LEARN / CREATE / REPEAT", size=9, fill=COLORS["muted"], spacing=1.2),
            text(1156, 729, "AUTO-GENERATED // LIVE DATA", size=9, fill=COLORS["muted"], anchor="end", spacing=1.2),
        ]
    )
    return document(
        f'{profile["name"]} - AI developer profile',
        "A live profile dashboard showing identity, technical focus, contribution totals, and featured machine learning projects.",
        1200,
        760,
        body,
    )


def heat_level(count: int, maximum: int) -> int:
    if count <= 0 or maximum <= 0:
        return 0
    return min(5, max(1, int((count / maximum) * 4) + 1))


def activity_telemetry(stats: dict[str, Any]) -> str:
    body: list[str] = []
    body.append(rect(24, 24, 1152, 346, fill="none", stroke=COLORS["border"], radius=22, stroke_width=1.5))
    body.append(rect(24, 24, 1152, 54, fill="#0b1424", stroke=COLORS["border"], radius=22))
    body.append(rect(24, 57, 1152, 21, fill="#0b1424"))
    body.extend(
        [
            circle(52, 51, 6, fill=COLORS["pink"]),
            circle(73, 51, 6, fill=COLORS["orange"]),
            circle(94, 51, 6, fill=COLORS["green"]),
            text(120, 56, "naresh@github:~$ telemetry --contributions", size=12, fill=COLORS["muted"]),
            circle(1017, 51, 4, fill=COLORS["green"], class_name="pulse"),
            text(1148, 56, "LIVE GITHUB DATA", size=11, fill=COLORS["cyan"], weight="700", anchor="end", spacing=1.2),
        ]
    )

    total = f'{stats["total"]:,}' if stats["available"] else "PENDING"
    active_days = str(stats["active_days"]) if stats["available"] else "-"
    peak = f'{stats["peak_count"]} / {stats["peak_date"]}' if stats["available"] else "-"
    window = f'{stats["start_date"]} -> {stats["end_date"]}' if stats["available"] else "WAITING FOR FIRST SYNC"
    metrics = [
        (44, 248, "TOTAL CONTRIBUTIONS", total, COLORS["cyan"]),
        (310, 248, "ACTIVE DAYS", active_days, COLORS["green"]),
        (576, 248, "PEAK DAY", peak, COLORS["orange"]),
        (842, 314, "WINDOW", window, COLORS["violet"]),
    ]
    for x, width, label, value, metric_color in metrics:
        body.append(rect(x, 101, width, 58, fill="url(#panel-gradient)", stroke=COLORS["border_soft"], radius=11))
        body.append(text(x + 16, 122, label, size=9, fill=metric_color, weight="700", spacing=1.1))
        body.append(text(x + 16, 145, value, size=11, fill=COLORS["text"], weight="700"))

    body.append(text(44, 185, "CONTRIBUTION CALENDAR", size=10, fill=COLORS["muted"], weight="700", spacing=1.3))
    body.append(text(1148, 185, "SOURCE: GITHUB CONTRIBUTIONS API", size=9, fill=COLORS["muted"], anchor="end", spacing=0.8))
    weeks = stats["weeks"]
    week_count = max(53, len(weeks))
    padded_weeks = weeks + ([[]] * (week_count - len(weeks)))
    start_x = 126
    start_y = 204
    cell = 12
    gap = 4
    maximum = max((day["count"] for week in weeks for day in week), default=0)
    month_seen: set[str] = set()
    for column, week in enumerate(padded_weeks):
        x = start_x + column * (cell + gap)
        for day in week:
            weekday = (day["parsed_date"].weekday() + 1) % 7
            y = start_y + weekday * (cell + gap)
            body.append(rect(x, y, cell, cell, fill=color(f"heat_{heat_level(day['count'], maximum)}"), radius=3, opacity=0.95))
            month_key = day["date"][:7]
            if month_key not in month_seen and day["parsed_date"].day <= 7:
                body.append(text(x, 197, day["parsed_date"].strftime("%b").upper(), size=9, fill=COLORS["muted"], weight="700"))
                month_seen.add(month_key)

    for row, label in enumerate(("SUN", "MON", "WED", "FRI")):
        y = start_y + (row * 2) * (cell + gap) + 10
        body.append(text(44, y, label, size=8, fill=COLORS["muted"], weight="700"))
    body.extend(
        [
            text(126, 348, "LAST 52 WEEKS", size=9, fill=COLORS["muted"], weight="700", spacing=1),
            text(1148, 348, "LIVE SVG / AUTO-REFRESHED BY GITHUB ACTIONS", size=9, fill=COLORS["muted"], anchor="end", spacing=0.8),
        ]
    )
    return document(
        "Naresh Kumar V - live contribution telemetry",
        "A contribution calendar generated from the GitHub contribution API with live totals, active days, and peak activity.",
        1200,
        390,
        body,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=PROFILE_PATH)
    parser.add_argument("--contributions-json", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ASSET_DIR)
    args = parser.parse_args()

    profile = load_profile(args.profile)
    stats = load_contributions(args.contributions_json)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "profile-dashboard.svg").write_text(profile_dashboard(profile, stats), encoding="utf-8")
    (args.output_dir / "activity-telemetry.svg").write_text(activity_telemetry(stats), encoding="utf-8")
    status = f'{stats["total"]:,} contributions' if stats["available"] else "live data pending"
    print(f"Generated profile assets ({status}) in {args.output_dir}")


if __name__ == "__main__":
    main()
