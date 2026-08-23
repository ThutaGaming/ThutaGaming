import os

SKILLS = [
    ("Unity", 90, "#DC143C"),
    ("C#", 88, "#FF4500"),
    ("Debugging", 95, "#1E5AA8"),
    ("Git", 75, "#FF6B1A"),
    ("Patience", 40, "#DC143C"),
    ("Coffee Dependency", 100, "#FF4500"),
]

MARGIN_X = 24
MARGIN_Y = 22
LABEL_W = 160
BAR_W = 300
BAR_H = 14
ROW_GAP = 30

width = MARGIN_X * 2 + LABEL_W + BAR_W + 50
height = MARGIN_Y * 2 + ROW_GAP * len(SKILLS)


def make_svg(bg, track_color, text_color):
    parts = [f'<rect width="{width}" height="{height}" fill="{bg}" rx="10"/>']
    y = MARGIN_Y
    for i, (label, pct, color) in enumerate(SKILLS):
        bar_x = MARGIN_X + LABEL_W
        bar_y = y + 6
        begin = f"{i * 0.15:.2f}s"
        target_w = BAR_W * pct / 100

        parts.append(
            f'<text x="{MARGIN_X}" y="{bar_y + BAR_H - 3}" '
            f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
            f'font-size="13" font-weight="700" fill="{text_color}">{label}</text>'
        )
        parts.append(
            f'<rect x="{bar_x}" y="{bar_y}" width="{BAR_W}" height="{BAR_H}" rx="{BAR_H / 2}" '
            f'fill="{track_color}"/>'
        )
        parts.append(
            f'<rect x="{bar_x}" y="{bar_y}" width="0" height="{BAR_H}" rx="{BAR_H / 2}" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{target_w:.1f}" dur="1.1s" '
            f'begin="{begin}" fill="freeze" calcMode="spline" keySplines="0.2 0.6 0.3 1"/>'
            f'</rect>'
        )
        parts.append(
            f'<text x="{bar_x + BAR_W + 12}" y="{bar_y + BAR_H - 3}" '
            f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
            f'font-size="12" font-weight="700" fill="{color}">{pct}%</text>'
        )
        y += ROW_GAP

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">{"".join(parts)}</svg>'
    )


out_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "skills-dark.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(bg="#0B0B0C", track_color="#1c1c1e", text_color="#ffffff"))

with open(os.path.join(out_dir, "skills-light.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(bg="#ffffff", track_color="#e9e9ea", text_color="#0B0B0C"))

print("skill bar svgs generated")
