import os
import re

ICON_DIR = os.path.join(os.path.dirname(__file__), "icons")

# (slug, label, file, github-needs-recolor)
ICONS = [
    ("unity", "Unity", "unity.svg"),
    ("csharp", "C#", "csharp.svg"),
    ("dotnetcore", ".NET", "dotnetcore.svg"),
    ("git", "Git", "git.svg"),
    ("github", "GitHub", "github.svg"),
    ("vscode", "VS Code", "vscode.svg"),
    ("windows8", "Windows", "windows8.svg"),
]

ICON_SIZE = 56
GAP = 22
MARGIN_X = 24
MARGIN_Y = 34
BOUNCE = 12

width = MARGIN_X * 2 + len(ICONS) * ICON_SIZE + GAP * (len(ICONS) - 1)
height = MARGIN_Y * 2 + ICON_SIZE + BOUNCE

ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')
ID_REF_RE = re.compile(r'url\(#([^)]+)\)')
HREF_REF_RE = re.compile(r'(xlink:href|href)="#([^"]+)"')


def load_icon(slug, filename):
    with open(os.path.join(ICON_DIR, filename), "r", encoding="utf-8") as f:
        raw = f.read()
    m = re.search(r"<svg[^>]*viewBox=\"([^\"]+)\"[^>]*>(.*)</svg>", raw, re.S)
    view_box, inner = m.group(1), m.group(2)

    def rename_id(match):
        return f'id="{slug}-{match.group(1)}"'

    def rename_ref(match):
        return f'url(#{slug}-{match.group(1)})'

    def rename_href(match):
        return f'{match.group(1)}="#{slug}-{match.group(2)}"'

    inner = ID_ATTR_RE.sub(rename_id, inner)
    inner = ID_REF_RE.sub(rename_ref, inner)
    inner = HREF_REF_RE.sub(rename_href, inner)
    return view_box, inner


def make_svg(github_fill=None):
    parts = []
    x = MARGIN_X
    for i, (slug, label, filename) in enumerate(ICONS):
        view_box, inner = load_icon(slug, filename)
        if slug == "github" and github_fill:
            inner = inner.replace("#181616", github_fill)
        y = MARGIN_Y
        begin = f"{i * 0.15:.2f}s"
        parts.append(
            f'<g transform="translate({x},{y})">'
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0,0; 0,-{BOUNCE}; 0,0" dur="1.7s" begin="{begin}" repeatCount="indefinite" '
            f'calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" keyTimes="0;0.5;1"/>'
            f'<title>{label}</title>'
            f'<svg width="{ICON_SIZE}" height="{ICON_SIZE}" viewBox="{view_box}">{inner}</svg>'
            f'</g>'
        )
        x += ICON_SIZE + GAP

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'{"".join(parts)}'
        f'</svg>'
    )


out_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "tech-stack-dark.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(github_fill="#f0f0f0"))

with open(os.path.join(out_dir, "tech-stack-light.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(github_fill=None))

print("tech stack icon svgs generated")
