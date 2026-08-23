import datetime

MMT = datetime.timezone(datetime.timedelta(hours=6, minutes=30))

WIDTH = 420
HEIGHT = 110


def make_svg(bg, accent, text_color, sub_color):
    now = datetime.datetime.now(MMT)
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M %p")

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{bg}" rx="12"/>'
        f'<text x="24" y="42" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="13" font-weight="700" fill="{sub_color}">\U0001F4CD Yangon, Myanmar</text>'
        f'<text x="24" y="78" font-family="Consolas,Menlo,monospace" '
        f'font-size="30" font-weight="700" fill="{accent}">{time_str} MMT'
        f'<animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/>'
        f'</text>'
        f'<text x="24" y="98" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="12" fill="{text_color}">{date_str}</text>'
        f'</svg>'
    )


import os

out_dir = os.path.join(os.path.dirname(__file__), "..", "dist")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "clock-dark.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(bg="#0B0B0C", accent="#FF4500", text_color="#bbbbbb", sub_color="#1E5AA8"))

with open(os.path.join(out_dir, "clock-light.svg"), "w", encoding="utf-8") as f:
    f.write(make_svg(bg="#ffffff", accent="#DC143C", text_color="#333333", sub_color="#1E5AA8"))

print("clock svgs generated")
