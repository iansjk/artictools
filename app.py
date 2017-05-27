from flask import Flask, render_template, json, request, url_for, abort, redirect
from flask_jsglue import JSGlue

from pictograms.arasaac import find_pictograms
from targets.minimal_pairs import find_minimal_pairs

STATIC_FOLDER = "static"
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config["PICTOGRAM_S3_BUCKET"] = "artictools-pictograms"
JSGlue(app)


@app.context_processor
def inject_constants():
    return {
        "project_name": "ArticTools",
        "active_page": "Home",
        "navigation": (
            ("Home", "/"),
            ("Pictograms", url_for("pictograms")),
            ("Minimal Pairs", url_for("minimal_pairs")),
            ("Grid Builder", url_for("grid_builder")),
            ("About", url_for("about")),
        )}


@app.after_request
def add_cache_header(response):
    response.cache_control.max_age = 300
    response.cache_control.public = True
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pictograms/")
def pictograms():
    return render_template("pictograms.html")


@app.route("/pictograms/search", methods=["GET"])
def pictogram_search():
    try:
        query = request.args["query"]
        return json.jsonify({
            "data": find_pictograms(query),
        })
    except ValueError:
        return abort(400)


@app.route("/minimal-pairs/")
def minimal_pairs():
    return render_template("minimal-pairs.html")


@app.route("/minimal-pairs/search", methods=["GET"])
def minimal_pair_search():
    target1 = request.args["target1"]
    target2 = request.args["target2"]
    position = request.args["position"]
    return json.jsonify({
        "data": find_minimal_pairs(target1, target2, position)
    })


@app.route("/grid-builder")
def grid_builder():
    return render_template("grid-builder.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/%s/pictograms/<int:pictogram_id>" % STATIC_FOLDER)
def static_pictogram(pictogram_id):
    return redirect("https://s3.amazonaws.com/%s/%d.png" % (app.config["PICTOGRAM_S3_BUCKET"], pictogram_id))


if __name__ == "__main__":
    app.run()