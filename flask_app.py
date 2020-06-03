from threading import Timer
import os
from urllib.parse import urljoin
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, url_for, redirect


app = Flask(__name__)
BASE_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(BASE_PATH, "static")
FONT_PATH = os.path.join(STATIC_PATH, "fonts")
CERTIFICATE_PATH = os.path.join(STATIC_PATH, "certificates")
GENERATED_PATH = os.path.join(STATIC_PATH, "generated")


@app.route("/")
def index():
    return "Hello World"


@app.route("/generate/")
def generate():
    certificate = make_certificate(**request.args)
    return redirect(certificate)


def delete_file(img_title):
    os.unlink(os.path.join(GENERATED_PATH, img_title))


def make_certificate(first_name, last_name, track):
    # set certificate style
    filename = "30DaysOfCode.png"
    font = "Cinzel-Bold.otf"
    track_font = "Montserrat-Regular.tff"
    level_font = "Montserrat-Regular.tff"

    # name style
    color = "#c9a04b"
    size = 46.7
    y = 1450

    # track style
    track_color = "#ffffff"
    track_size = 13.6

    # level style
    level_color = "#ffffff"
    level_size = 13.6

    # name text
    text = "{} {}".format(first_name, last_name).upper()
    raw_img = Image.open(os.path.join(CERTIFICATE_PATH, filename))
    img = raw_img.copy()
    draw = ImageDraw.Draw(img)

    # draw name
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, font), size)
    w, h = draw.textsize(text, font=PIL_font)
    W, H = img.size
    x = (W - w) / 2
    draw.text((x, y), text, fill=color, font=PIL_font)

    # draw track
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, track_font), track_size)
    w, h = draw.textsize(track, font=PIL_font)
    x, y = 2170, 2110
    draw.text((x, y), track, fill=track_color, font=PIL_font)

    # draw level
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, level_font), level_size)
    w, h = draw.textsize(level, font=PIL_font)
    x, y = 2170, 2110
    draw.text((x, y), level, fill=level, font=PIL_font)

    # save certificate
    img_title = "{}-{}-{}.png".format(first_name, last_name, track)
    img.save(os.path.join(GENERATED_PATH, img_title))
    task = Timer(30, delete_file, (img_title,))
    task.start()
    base_64 =  urljoin(request.host_url, url_for("static", filename="generated/" + img_title))

    return base_64


if __name__ == "__main__":
    app.run(debug=True)
