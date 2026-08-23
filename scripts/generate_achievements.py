import os

ACHIEVEMENTS = [
    ("\U0001F41B", "Bug Squasher", "#DC143C"),
    ("\U0001F525", "Streak Master", "#FF4500"),
    ("\U0001F989", "Night Owl", "#1E5AA8"),
    ("\U0001F680", "Shipped It", "#FF6B1A"),
    ("⭐", "Level Up", "#0B0B0C"),
]

BADGE_H = 44
PAD_X = 16
GAP = 16
MARGIN_X = 24
MARGIN_Y = 26
CHAR_W = 8.2
EMOJI_W = 22

widths = [EMOJI_W + 8 + len(label) * CHAR_W + PAD_X * 2 for _, label, _ in ACHIEVEMENTS]
width = MARGIN_X * 2 + sum(widths) + GAP * (len(ACHIEVEMENTS) - 1)
height = MARGIN_Y * 2 + BADGE_H


def make_svg(bg, border, text_color):
    parts = [f'<rect width="{width}" height="{height}" fill="{bg}" rx="10"/>']
    x = MARGIN_X
    for i, (emoji, label, color) in enumerate(ACHIEVEMENTS):
        w = widths[i]
        y = MARGIN_Y
        begin = f"{i * 0.3:.2f}s"
        glow_id = f"glow{i}"
        parts.append(
            f'<defs><filter id="{glow_id}" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="5"/></filter></defs>'
        )
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{BADGE_H}" rx="{BADGE_H / 2}" '
            f'fill="{color}" filter="url(#{glow_id})" opacity="0.55">'
            f'<animate attributeName="opacity" values="0.35;0.75;0.35" dur="2.2s" '
            f'begin="{begin}" repeatCount="indefinite"/>'
            f'</rect>'
        )
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{BADGE_H}" rx="{BADGE_H / 2}" '
            f'fill="{color}" stroke="{border}" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{x + PAD_X + 11}" y="{y + BADGE_H / 2 + 7}" text-anchor="middle" '
            f'font-size="18">{emoji}</text>'
        )
        parts.append(
            f'<text x="{x + PAD_X + EMOJI_W + 6}" y="{y + BADGE_H / 2 + 5}" '
            f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
            f'font-size="14" font-weight="700" fill="{text_color}">{label}</text>'
        )
        x += w + GAP

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">{"".join(parts)}</svg>'
    )


out_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "achievements-dark.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(bg="#0B0B0C", border="#FF6B1A", text_color="#ffffff"))

with open(os.path.join(out_dir, "achievements-light.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(bg="#ffffff", border="#1E5AA8", text_color="#ffffff"))

print("achievement svgs generated")
