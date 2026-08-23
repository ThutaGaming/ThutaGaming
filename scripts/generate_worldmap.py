import os
import re

# Source: https://github.com/flekschas/simple-world-map (CC BY-SA 3.0)
SRC = os.path.join(os.path.dirname(__file__), "mapdata", "world-map-source.svg")
HIGHLIGHT_ID = "mm"


def build(bg, land_color, border_color, highlight_color, glow_color):
    with open(SRC, "r", encoding="utf-8") as f:
        svg = f.read()

    m = re.search(r"<svg[^>]*viewBox=\"([^\"]+)\"[^>]*>(.*)</svg>", svg, re.S)
    view_box, body = m.group(1), m.group(2)

    # strip any inline style/fill on paths, we control color via CSS below
    body = re.sub(r'\sstyle="[^"]*"', "", body)
    body = re.sub(r'\sfill="[^"]*"', "", body)

    vb_parts = [float(v) for v in view_box.split()]
    vb_w, vb_h = vb_parts[2], vb_parts[3]

    highlight_block = (
        f'<style>'
        f'#world-countries path {{ fill: {land_color}; stroke: {border_color}; stroke-width: 0.6; }}'
        f'#{HIGHLIGHT_ID} {{ fill: {highlight_color} !important; }}'
        f'</style>'
    )

    # wrap country paths in a group with a fixed id for the CSS selector above
    body = re.sub(r"(<path\b)", r"\1", body)  # no-op, kept for clarity

    glow = (
        f'<g>'
        f'<use xlink:href="#{HIGHLIGHT_ID}" fill="none" stroke="{glow_color}" '
        f'stroke-width="6" opacity="0.55">'
        f'<animate attributeName="opacity" values="0.25;0.75;0.25" dur="2.4s" repeatCount="indefinite"/>'
        f'</use>'
        f'</g>'
    )

    svg_out = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="{view_box}" width="720" height="{720 * vb_h / vb_w:.1f}">'
        f'<rect x="{vb_parts[0]}" y="{vb_parts[1]}" width="{vb_w}" height="{vb_h}" fill="{bg}"/>'
        f'{highlight_block}'
        f'<g id="world-countries">{body}</g>'
        f'{glow}'
        f'</svg>'
    )
    return svg_out


out_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(out_dir, exist_ok=True)

dark = build(
    bg="#0B0B0C",
    land_color="#1c1c1e",
    border_color="#0B0B0C",
    highlight_color="#FFD24C",
    glow_color="#FF4500",
)
light = build(
    bg="#ffffff",
    land_color="#dcdcdc",
    border_color="#ffffff",
    highlight_color="#DC143C",
    glow_color="#FF4500",
)

with open(os.path.join(out_dir, "worldmap-dark.svg"), "w", encoding="utf-8") as f:
    f.write(dark)
with open(os.path.join(out_dir, "worldmap-light.svg"), "w", encoding="utf-8") as f:
    f.write(light)

print("world map svgs generated")
