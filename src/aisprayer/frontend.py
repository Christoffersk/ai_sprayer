import base64
import io
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os

from .config_handler import ConfigHandler
from .sprayer import Sprayer

# Init Flask
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024

# Init config
CONFIG = ConfigHandler()

# Set initial images
img = Image.open(os.path.join(os.path.dirname(__file__), "static", "initial_image.jpg"))
buffer = io.BytesIO()
img.save(buffer, "JPEG")
buffer.seek(0)
CURRENT_IMAGE = base64.b64encode(buffer.read()).decode("utf-8")
CURRENT_DETECT_IMAGE = CURRENT_IMAGE

# init sprayer
sprayer = Sprayer()

@app.route("/update_image", methods=["POST"])
def update_image():
    try:
        img = request.files["image"]
        img.seek(0)
        global CURRENT_IMAGE
        CURRENT_IMAGE = base64.b64encode(img.read()).decode("utf-8")
    except Exception:
        img = request.files["detect_image"]
        img.seek(0)
        global CURRENT_DETECT_IMAGE
        CURRENT_DETECT_IMAGE = base64.b64encode(img.read()).decode("utf-8")

    return "OK"


@app.route("/")
@app.route("/index")
def show_index():
    return render_template("index.html", img_data=CURRENT_IMAGE)


@app.route("/detections")
def show_detections():
    return render_template("detections.html", img_data=CURRENT_DETECT_IMAGE)


@app.route("/config")
def show_config():

    remove_settings = ["API_ENDPOINT", "PUMPPIN", "TARGETS"]
    settings = {
        key: value
        for (key, value) in CONFIG.config.items()
        if not key in remove_settings
    }

    return render_template("config.html", config_dict=settings)


@app.route("/send", methods=["POST"])
def send():

    new_config = request.form.to_dict()
    print(new_config)
    CONFIG.update_config(new_config)

    return redirect(url_for("show_config"))

@app.route("/spray", methods=["POST"])
def manual_spray():

    sprayer.spray()

    return render_template("index.html", img_data=CURRENT_IMAGE)

@app.route("/test", methods=["POST"])
def test():

    print(request.form)

    return redirect(url_for("show_config"))


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
