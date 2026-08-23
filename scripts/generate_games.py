import os

GAMES = [
    ("\U0001F9DF", "Resident Evil", "#0B0B0C"),
    ("⚔️", "God of War", "#DC143C"),
    ("\U0001F48D", "Elden Ring", "#FF4500"),
    ("\U0001F525", "Dark Souls", "#0B0B0C"),
    ("\U0001F30D", "The Last of Us", "#1E5AA8"),
    ("\U0001F916", "Cyberpunk 2077", "#FF6B1A"),
    ("\U0001F920", "Red Dead 2", "#DC143C"),
]

CARD_W = 108
CARD_H = 100
GAP = 14
MARGIN_X = 22
MARGIN_Y = 22

width = MARGIN_X * 2 + len(GAMES) * CARD_W + GAP * (len(GAMES) - 1)
height = MARGIN_Y * 2 + CARD_H + 10


def make_svg(text_color):
    parts = []
    x = MARGIN_X
    for i, (emoji, label, color) in enumerate(GAMES):
        y = MARGIN_Y
        begin = f"{i * 0.15:.2f}s"
        cx = CARD_W / 2
        cy = CARD_H / 2
        parts.append(
            f'<g transform="translate({x},{y})">'
            f'<animateTransform attributeName="transform" type="rotate" additive="sum" '
            f'values="-6 {cx} {cy}; 6 {cx} {cy}; -6 {cx} {cy}" dur="2.2s" begin="{begin}" '
            f'repeatCount="indefinite" calcMode="spline" '
            f'keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" keyTimes="0;0.5;1"/>'
            f'<rect width="{CARD_W}" height="{CARD_H}" rx="14" fill="{color}" stroke="#FF6B1A" stroke-width="1.2"/>'
            f'<text x="{CARD_W / 2}" y="44" text-anchor="middle" font-size="34">{emoji}</text>'
            f'<text x="{CARD_W / 2}" y="76" text-anchor="middle" '
            f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" font-size="11" '
            f'font-weight="700" fill="{text_color}">{label}</text>'
            f'</g>'
        )
        x += CARD_W + GAP

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">{"".join(parts)}</svg>'
    )


out_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "games-dark.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(text_color="#ffffff"))

with open(os.path.join(out_dir, "games-light.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(text_color="#ffffff"))

print("favorite games svgs generated")
