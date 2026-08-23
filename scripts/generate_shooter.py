import os
import requests

TOKEN = os.environ["GH_TOKEN"]
USERNAME = os.environ.get("GH_USERNAME", "ThutaGaming")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

resp = requests.post(
    "https://api.github.com/graphql",
    json={"query": QUERY, "variables": {"login": USERNAME}},
    headers={"Authorization": f"bearer {TOKEN}"},
    timeout=30,
)
resp.raise_for_status()
weeks = resp.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

CELL = 10
GAP = 3
STEP = CELL + GAP
MARGIN_X = 20
MARGIN_Y = 20
SHIP_GAP = 22
TOTAL_DURATION = 30.0

num_cols = len(weeks)
width = MARGIN_X * 2 + num_cols * STEP - GAP
grid_height = 7 * STEP - GAP
ship_y = MARGIN_Y + grid_height + SHIP_GAP
height = ship_y + MARGIN_Y


def make_svg(bg, empty_color, levels, ship_fill, laser_color):
    counts = [d["contributionCount"] for w in weeks for d in w["contributionDays"]]
    max_count = max(counts) if counts else 0

    def level_color(count):
        if count == 0 or max_count == 0:
            return empty_color
        ratio = count / max_count
        if ratio > 0.75:
            return levels[3]
        if ratio > 0.5:
            return levels[2]
        if ratio > 0.25:
            return levels[1]
        return levels[0]

    parts = []

    for col, week in enumerate(weeks):
        cx = MARGIN_X + col * STEP
        col_time = (col + 0.5) / num_cols * TOTAL_DURATION
        stagger = 0
        for row, day in enumerate(week["contributionDays"]):
            cy = MARGIN_Y + row * STEP
            count = day["contributionCount"]
            color = level_color(count)
            if count > 0:
                shot_time = min(col_time + stagger * 0.05, TOTAL_DURATION - 0.05)
                stagger += 1
                f = shot_time / TOTAL_DURATION
                eps = max(0.0005, min(0.004, f / 2, (1 - f) / 2))
                f0 = max(0.0, f - eps)
                f1 = min(1.0, f + eps)
                parts.append(
                    f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="{color}">'
                    f'<animate attributeName="fill" dur="{TOTAL_DURATION}s" repeatCount="indefinite" '
                    f'keyTimes="0;{f0:.4f};{f1:.4f};1" values="{color};{color};{empty_color};{empty_color}"/>'
                    f'</rect>'
                )
                lf0 = max(0.0, f - 0.012)
                lf1 = min(1.0, f + 0.012)
                parts.append(
                    f'<line x1="{cx + CELL / 2}" y1="{ship_y}" x2="{cx + CELL / 2}" y2="{cy + CELL}" '
                    f'stroke="{laser_color}" stroke-width="1.5" opacity="0">'
                    f'<animate attributeName="opacity" dur="{TOTAL_DURATION}s" repeatCount="indefinite" '
                    f'keyTimes="0;{lf0:.4f};{f:.4f};{lf1:.4f};1" values="0;0;1;0;0"/>'
                    f'</line>'
                )
                parts.append(
                    f'<circle cx="{cx + CELL / 2}" cy="{cy + CELL / 2}" r="0" fill="#ffffff" opacity="0">'
                    f'<animate attributeName="r" dur="{TOTAL_DURATION}s" repeatCount="indefinite" '
                    f'keyTimes="0;{f0:.4f};{f:.4f};{lf1:.4f};1" values="0;0;7;0;0"/>'
                    f'<animate attributeName="opacity" dur="{TOTAL_DURATION}s" repeatCount="indefinite" '
                    f'keyTimes="0;{f0:.4f};{f:.4f};{lf1:.4f};1" values="0;0;0.9;0;0"/>'
                    f'</circle>'
                )
            else:
                parts.append(
                    f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>'
                )

    ship_path = f"M {MARGIN_X},{ship_y} L {width - MARGIN_X},{ship_y}"
    parts.append(
        f'<polygon points="0,-6 6,7 -6,7" fill="{ship_fill}">'
        f'<animateMotion dur="{TOTAL_DURATION}s" repeatCount="indefinite" path="{ship_path}"/>'
        f'</polygon>'
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="{width}" height="{height}" fill="{bg}" rx="6"/>'
        f'{"".join(parts)}'
        f'</svg>'
    )


dark_svg = make_svg(
    bg="#0D0000",
    empty_color="#1a0000",
    levels=["#3f0a0a", "#6e0000", "#a30000", "#ff0000"],
    ship_fill="#ff3b3b",
    laser_color="#ff5555",
)

light_svg = make_svg(
    bg="#ffffff",
    empty_color="#f2dede",
    levels=["#f4a3a3", "#e05656", "#b30000", "#7a0000"],
    ship_fill="#8b0000",
    laser_color="#c40000",
)

os.makedirs("dist", exist_ok=True)
with open("dist/shooter-dark.svg", "w", encoding="utf-8") as f:
    f.write(dark_svg)
with open("dist/shooter-light.svg", "w", encoding="utf-8") as f:
    f.write(light_svg)

print("shooter svgs generated")
