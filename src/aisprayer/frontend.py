from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.route("/")
@app.route("/index")
def show_index():
    return render_template("index.html")


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
