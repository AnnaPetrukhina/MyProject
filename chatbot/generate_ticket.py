
import os
from io import BytesIO
from pathlib import Path
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageDraw, ImageFont, ImageColor

PATH = Path.cwd() / "images" / "ticket_template.png"


def make_ticket(fio, from_, to, date, person):
    im = Image.open(PATH)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "ofont_ru_PetersburgITT.ttf"), size=20)
    data = {}
    x = 45

    y = im.size[1] // 3 - 10
    data[fio] = (x, y)

    y = im.size[1] // 3 + (10 + font.size) * 2
    data[from_] = (x, y)

    y = im.size[1] // 2 + (10 + font.size) * 2
    data[to] = (x, y)

    x = im.size[0] // 2.4
    data[date] = (x, y)

    for key, value in data.items():
        draw.text(value, key, font=font, fill=ImageColor.colormap['black'])

    url = f"https://joeschmoe.io/api/v1/{person}"
    response = requests.get(url, stream=True).content
    avatar_file_like = BytesIO(response)
    drawing = svg2rlg(avatar_file_like)
    avatar = renderPM.drawToPIL(drawing)

    im.paste(avatar, (400, 70))
    path_out = Path.cwd() / "images" / f"ticket_filled_{fio}_{date}.png"
    im.save(path_out)
    return path_out


if __name__ == '__main__':
    make_ticket(fio="Петрухина А.Д.", from_="Москва", to="Калининград", date="23-05-2021", person="jenni")
