import os

BADGES = [
    ("Unity", 74, "#3f0a0a"),
    ("C#", 54, "#6e0000"),
    (".NET", 68, "#8b0000"),
    ("Git", 54, "#a30000"),
    ("GitHub", 86, "#8b0000"),
    ("VS Code", 96, "#6e0000"),
    ("Windows", 96, "#3f0a0a"),
]

GAP = 16
MARGIN_X = 20
MARGIN_Y = 30
HEIGHT_BADGE = 40
BOUNCE = 10

width = MARGIN_X * 2 + sum(w for _, w, _ in BADGES) + GAP * (len(BADGES) - 1)
height = MARGIN_Y * 2 + HEIGHT_BADGE + BOUNCE


def make_svg(bg):
    parts = []
    x = MARGIN_X
    for i, (label, w, color) in enumerate(BADGES):
        y = MARGIN_Y
        begin = f"{i * 0.18:.2f}s"
        dur = "1.6s"
        parts.append(
            f'<g transform="translate({x},{y})">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'additive="sum" values="0,0; 0,-{BOUNCE}; 0,0" dur="{dur}" '
            f'begin="{begin}" repeatCount="indefinite" calcMode="spline" '
            f'keySplines="0.4 0 0.6 1; 0.4 0 0.6 1" keyTimes="0;0.5;1"/>'
            f'<rect x="0" y="0" width="{w}" height="{HEIGHT_BADGE}" rx="{HEIGHT_BADGE / 2}" '
            f'fill="{color}" stroke="#ff0000" stroke-width="1.2"/>'
            f'<text x="{w / 2}" y="{HEIGHT_BADGE / 2 + 5}" text-anchor="middle" '
            f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
            f'font-size="14" font-weight="700" fill="#ffffff">{label}</text>'
            f'</g>'
        )
        x += w + GAP

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="{width}" height="{height}" fill="{bg}" rx="8"/>'
        f'{"".join(parts)}'
        f'</svg>'
    )


os.makedirs("assets", exist_ok=True)
with open("assets/tech-stack-dark.svg", "w", encoding="utf-8") as f:
    f.write(make_svg("#0D0000"))
with open("assets/tech-stack-light.svg", "w", encoding="utf-8") as f:
    f.write(make_svg("#ffffff"))

print("tech stack svgs generated")
