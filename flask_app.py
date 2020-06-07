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
    certificate = make_certificate("30DaysOfCode.png", **request.args)
    return redirect(certificate)


def delete_file(img_title):
    os.unlink(os.path.join(GENERATED_PATH, img_title))


def make_certificate(filename, first_name, last_name, track, level, constant):
    # set certificate style
    font = "Cinzel-Bold.otf"
    track_font = "Montserrat-Bold.ttf"
    level_font = "Montserrat-Bold.ttf"

    # name style
    color = "#c9a04b"
    size = 70
    y = 640

    # track style
    track_color = "#ffffff"
    track_size = 40

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

    # draw track and level
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, track_font), track_size)
    x, y = 750, 840
    draw.text((x, y), "{} {} {}".format(track, level, constant), fill=track_color, font=PIL_font)

    # save certificate
    img_title = "{}-{}-{}-{}-{}.png".format(first_name, last_name, track, level, constant)
    img.save(os.path.join(GENERATED_PATH, img_title))
    task = Timer(30, delete_file, (img_title,))
    task.start()
    base_64 =  urljoin(request.host_url, url_for("static", filename="generated/" + img_title))

    return base_64

@app.route("/mentor/")
def mentor():
    certificate = make_certificate_mentor("MentorCertificate.png", **request.args)
    return redirect(certificate)

def make_certificate_mentor(filename, first_name, last_name, track, level):
    # set certificate style
    font = "Cinzel-Bold.otf"
    track_font = "Montserrat-Bold.ttf"
    level_font = "Montserrat-Bold.ttf"

    # name style
    color = "#fff"
    size = 80
    x = 830

    # track style
    track_color = "#fff"
    track_size = 30

    # name text
    text = "{} {}".format(first_name, last_name).upper()
    raw_img = Image.open(os.path.join(CERTIFICATE_PATH, filename))
    img = raw_img.copy()
    draw = ImageDraw.Draw(img)

    # draw name
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, font), size)
    w, h = draw.textsize(text, font=PIL_font)
    W, H = img.size
    y = 535
    draw.text((x, y), text.split()[0], fill=color, font=PIL_font)
    
    y = 675
    draw.text((x, y), text.split()[1], fill=color, font=PIL_font)
    # draw track and level
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, track_font), track_size)
    
    #draw.text((x, y), "{} {}".format(track, level), fill=track_color, font=PIL_font)

    # save certificate
    img_title = "mentor-{}-{}-{}-{}.png".format(first_name, last_name, track, level)
    img.save(os.path.join(GENERATED_PATH, img_title))
    task = Timer(30, delete_file, (img_title,))
    task.start()
    base_64 =  urljoin(request.host_url, url_for("static", filename="generated/" + img_title))

    return base_64

if __name__ == "__main__":
    app.run(debug=True)
