import base64
import io
from flask import Flask, render_template, request
from PIL import Image
import os

from .config_handler import ConfigHandler

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

CONFIG = ConfigHandler()


def _update_image(image):
    buffer = io.BytesIO()
    image.save(buffer, "JPEG")
    buffer.seek(0)

    global CURRENT_IMAGE
    CURRENT_IMAGE = base64.b64encode(buffer.read()).decode("utf-8")


img = Image.open(os.path.join(os.path.dirname(__file__), "static", "initial_image.jpg"))
_update_image(img)


@app.route("/update_image", methods=["POST"])
def update_image():
    img = request.files["image"]
    _update_image(img)


@app.route("/")
@app.route("/index")
def show_index():
    return render_template("index.html", img_data=CURRENT_IMAGE)


@app.route("/config")
def show_config():
    return render_template("config.html")


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        motion_threshold = request.form["motion_threshold"]
        print(motion_threshold)
    return render_template("config.html")


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers[
        "Cache-Control"
    ] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


def run_frontend():
    app.run(host="0.0.0.0", debug=False)
